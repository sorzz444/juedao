"""
Dharma Game Engine - 核心引擎

实现 种子-熏习-现行 的游戏循环
"""

import math
import random
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field

from .mental_factors import MENTAL_FACTORS, MentalFactor, MentalFactorType
from .seed_bank import SeedBank, Seed
from .scene import Scene


@dataclass
class ManifestState:
    """现行状态"""
    active_factors: Dict[str, float]  # 当前激活的心所及其强度
    scene: Optional[Scene]            # 当前场景
    timestamp: int                    # 时间戳
    
    def get_active_by_type(self, factor_type: MentalFactorType) -> Dict[str, float]:
        """按类型获取激活的心所"""
        result = {}
        for factor_id, strength in self.active_factors.items():
            factor = MENTAL_FACTORS.get(factor_id)
            if factor and factor.type == factor_type:
                result[factor_id] = strength
        return result
    
    def is_active(self, factor_id: str) -> bool:
        """检查心所是否激活"""
        return factor_id in self.active_factors
    
    def __repr__(self) -> str:
        active_list = [f"{MENTAL_FACTORS[k].name_zh}:{v:.2f}" 
                       for k, v in sorted(self.active_factors.items(), 
                                          key=lambda x: x[1], reverse=True)[:5]]
        return f"ManifestState([{', '.join(active_list)}])"


@dataclass
class Action:
    """行为定义"""
    name: str                          # 行为名称
    effects: Dict[str, float]          # 对心所种子的影响
    counterforce_targets: List[str] = field(default_factory=list)  # 对治目标
    triggers: List[str] = field(default_factory=list)  # 触发的事件


# 预定义行为
PREDEFINED_ACTIONS: Dict[str, Action] = {
    "布施": Action(
        name="布施",
        effects={"alobha": 0.5, "matsarya": -0.3, "raga": -0.2, "sraddha": 0.2},
        counterforce_targets=["raga", "matsarya"],
        triggers=["generosity_practiced", "letting_go"]
    ),
    "持戒": Action(
        name="持戒",
        effects={"apramada": 0.4, "hri": 0.3, "apatrapya": 0.3, "pramada": -0.3},
        counterforce_targets=["pramada"],
        triggers=["discipline_maintained"]
    ),
    "忍辱": Action(
        name="忍辱",
        effects={"advesa": 0.5, "pratigha": -0.4, "krodha": -0.3, "upeksa": 0.3},
        counterforce_targets=["pratigha", "krodha"],
        triggers=["patience_shown"]
    ),
    "精进": Action(
        name="精进",
        effects={"virya": 0.5, "kausidya": -0.4, "styana": -0.2},
        counterforce_targets=["kausidya", "styana"],
        triggers=["effort_sustained"]
    ),
    "禅定": Action(
        name="禅定",
        effects={"samadhi": 0.5, "prasrabdhi": 0.4, "viksepa": -0.4, "auddhatya": -0.3},
        counterforce_targets=["viksepa", "auddhatya"],
        triggers=["meditation_deepened", "focus_sustained"]
    ),
    "观察": Action(
        name="观察",
        effects={"prajna": 0.4, "moha": -0.3, "drsti": -0.2},
        counterforce_targets=["moha"],
        triggers=["analysis_active"]
    ),
    "正念": Action(
        name="正念",
        effects={"smrti": 0.5, "musitasmritita": -0.4, "viksepa": -0.2},
        counterforce_targets=["musitasmritita"],
        triggers=["mindfulness_practiced"]
    ),
    "慈心": Action(
        name="慈心",
        effects={"advesa": 0.5, "ahimsa": 0.4, "pratigha": -0.3, "vihimsa": -0.4},
        counterforce_targets=["pratigha", "vihimsa"],
        triggers=["compassion_practiced"]
    ),
    "随喜": Action(
        name="随喜",
        effects={"irsya": -0.5, "alobha": 0.3},
        counterforce_targets=["irsya"],
        triggers=["joy_in_others_success"]
    ),
    "忏悔": Action(
        name="忏悔",
        effects={"hri": 0.5, "apatrapya": 0.5, "mraksa": -0.5, "ahrikya": -0.4},
        counterforce_targets=["mraksa", "ahrikya"],
        triggers=["confession_made"]
    ),
}


class DharmaEngine:
    """
    Dharma游戏引擎
    
    核心循环：
    1. 场景设置缘矩阵
    2. 根据种子+缘矩阵+对治力计算现行概率
    3. 抽样决定哪些心所现行
    4. 玩家行为产生熏习，更新种子
    5. 时间前进，循环
    """
    
    # 核心公式参数
    SEED_WEIGHT = 2.0       # a: 种子权重系数
    CONDITION_WEIGHT = 1.5  # b: 场景条件系数
    COUNTER_WEIGHT = 1.0    # c: 对治系数
    
    # 现行阈值
    MANIFEST_THRESHOLD = 0.5
    
    def __init__(self, initial_weights: Optional[Dict[str, float]] = None):
        self.seed_bank = SeedBank(initial_weights)
        self.current_scene: Optional[Scene] = None
        self.current_manifest: Optional[ManifestState] = None
        self.active_counterforces: Dict[str, float] = {}  # 当前激活的对治力
        self.history: List[ManifestState] = []
    
    @staticmethod
    def sigmoid(x: float) -> float:
        """Sigmoid函数"""
        return 1.0 / (1.0 + math.exp(-x))
    
    def calculate_manifest_probability(self, factor_id: str) -> float:
        """
        计算心所现行概率
        
        P(现行) = sigmoid(a * Seed + b * Condition - c * Counterforce)
        """
        # 获取种子权重
        seed_weight = self.seed_bank.get_weight(factor_id)
        
        # 获取场景条件
        condition = 0.0
        if self.current_scene:
            condition = self.current_scene.get_condition(factor_id)
        
        # 获取对治力
        counterforce = self.active_counterforces.get(factor_id, 0.0)
        
        # 核心公式
        x = (self.SEED_WEIGHT * (seed_weight - 0.5) +  # 中心化
             self.CONDITION_WEIGHT * condition -
             self.COUNTER_WEIGHT * counterforce)
        
        return self.sigmoid(x)
    
    def calculate_manifest(self, scene: Optional[Scene] = None) -> ManifestState:
        """
        计算当前心所现行状态
        
        Args:
            scene: 场景（可选，若提供则更新当前场景）
        
        Returns:
            当前现行状态
        """
        if scene:
            self.current_scene = scene
        
        active_factors = {}
        
        # 遍行五：必定现行
        for factor_id in ["cetana", "sparsa", "manaskara", "vedana", "samjna"]:
            active_factors[factor_id] = 1.0
        
        # 别境五：高概率现行（但可受影响）
        for factor_id in ["chanda", "adhimoksa", "smrti", "samadhi", "prajna"]:
            prob = self.calculate_manifest_probability(factor_id)
            # 别境基础概率较高
            adjusted_prob = 0.5 + prob * 0.5
            if random.random() < adjusted_prob:
                active_factors[factor_id] = prob
        
        # 其他心所：按概率抽样
        for factor_id, factor in MENTAL_FACTORS.items():
            if factor_id in active_factors:
                continue
            if factor.type in [MentalFactorType.UNIVERSAL, MentalFactorType.PARTICULAR]:
                continue
            
            prob = self.calculate_manifest_probability(factor_id)
            if prob > self.MANIFEST_THRESHOLD and random.random() < prob:
                active_factors[factor_id] = prob
                # 记录现行
                self.seed_bank.manifest(factor_id)
        
        # 创建现行状态
        self.current_manifest = ManifestState(
            active_factors=active_factors,
            scene=self.current_scene,
            timestamp=self.seed_bank.current_time
        )
        
        # 记录历史
        self.history.append(self.current_manifest)
        if len(self.history) > 100:  # 限制历史长度
            self.history = self.history[-100:]
        
        return self.current_manifest
    
    def perform_action(self, action_name: str, intensity: float = 1.0) -> Dict[str, float]:
        """
        执行行为，产生熏习
        
        Args:
            action_name: 行为名称
            intensity: 行为强度 (0-1)
        
        Returns:
            种子变化量
        """
        action = PREDEFINED_ACTIONS.get(action_name)
        if not action:
            return {}
        
        changes = {}
        
        # 应用行为效果到种子
        for factor_id, effect in action.effects.items():
            self.seed_bank.update(factor_id, effect, intensity)
            changes[factor_id] = effect * intensity
        
        # 应用对治
        for target_id in action.counterforce_targets:
            factor = MENTAL_FACTORS.get(target_id)
            if factor and factor.counterforce:
                self.seed_bank.apply_counterforce(factor.counterforce, target_id, intensity)
        
        return changes
    
    def apply_counterforce(self, counterforce_id: str, target_id: str, strength: float = 1.0):
        """
        直接应用对治
        
        Args:
            counterforce_id: 对治心所ID
            target_id: 目标烦恼ID
            strength: 对治强度
        """
        # 设置临时对治力（影响现行概率）
        self.active_counterforces[target_id] = strength
        
        # 更新种子
        self.seed_bank.apply_counterforce(counterforce_id, target_id, strength)
    
    def clear_counterforces(self):
        """清除临时对治力"""
        self.active_counterforces.clear()
    
    def tick(self):
        """时间前进"""
        self.seed_bank.tick()
        # 对治力衰减
        for k in list(self.active_counterforces.keys()):
            self.active_counterforces[k] *= 0.8
            if self.active_counterforces[k] < 0.1:
                del self.active_counterforces[k]
    
    def get_status(self) -> Dict:
        """获取当前状态摘要"""
        return {
            "time": self.seed_bank.current_time,
            "scene": self.current_scene.name if self.current_scene else None,
            "dominant_afflictions": self.seed_bank.get_dominant_afflictions(3),
            "dominant_virtues": self.seed_bank.get_dominant_virtues(3),
            "active_counterforces": dict(self.active_counterforces),
            "current_manifest": str(self.current_manifest) if self.current_manifest else None
        }
    
    def save(self, filepath: str):
        """保存状态"""
        self.seed_bank.save(filepath)
    
    def load(self, filepath: str):
        """加载状态"""
        self.seed_bank = SeedBank.load(filepath)
    
    def __repr__(self) -> str:
        return f"DharmaEngine({self.seed_bank})"


# 辅助函数
def create_character(archetype: str = "neutral") -> DharmaEngine:
    """
    创建角色
    
    Args:
        archetype: 角色原型
            - "neutral": 中性
            - "virtuous": 善根深厚
            - "afflicted": 烦恼重
            - "wise": 慧根利
            - "passionate": 贪欲重
            - "angry": 嗔心重
    """
    weights = {}
    
    if archetype == "virtuous":
        for factor_id, factor in MENTAL_FACTORS.items():
            if factor.type == MentalFactorType.WHOLESOME:
                weights[factor_id] = 0.7
            elif factor.type in [MentalFactorType.PRIMARY_AFFLICTION, 
                                 MentalFactorType.SECONDARY_AFFLICTION]:
                weights[factor_id] = 0.3
    
    elif archetype == "afflicted":
        for factor_id, factor in MENTAL_FACTORS.items():
            if factor.type == MentalFactorType.WHOLESOME:
                weights[factor_id] = 0.3
            elif factor.type in [MentalFactorType.PRIMARY_AFFLICTION]:
                weights[factor_id] = 0.7
    
    elif archetype == "wise":
        weights["prajna"] = 0.8
        weights["amoha"] = 0.7
        weights["smrti"] = 0.7
        weights["samadhi"] = 0.6
        weights["moha"] = 0.2
        weights["drsti"] = 0.2
    
    elif archetype == "passionate":
        weights["raga"] = 0.8
        weights["chanda"] = 0.7
        weights["alobha"] = 0.2
    
    elif archetype == "angry":
        weights["pratigha"] = 0.8
        weights["krodha"] = 0.7
        weights["advesa"] = 0.2
    
    return DharmaEngine(initial_weights=weights if weights else None)
