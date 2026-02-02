"""
Dharma Game Engine V2 - 五层架构

唯识风格的心理系统：

1. 遍行五 (Pipeline)     → 事件管线（永远在）
2. 别境五 (Particular)   → 中性能力条（可被打断、方向由伴随决定）
3. 种子库 (SeedBank)     → 潜伏层（长期倾向，不一定表现）
4. 现行层 (Manifest)     → 当前激活的善/烦恼（buff/debuff）
5. 不定四 (Indeterminate) → 工具（受染净决定正邪）
"""

import math
import random
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field

from .pipeline import UniversalPipeline, MentalEvent, FeelingTone
from .particular import ParticularSystem, detect_pattern, CapabilityDirection
from .seed_bank import SeedBank
from .mental_factors import MENTAL_FACTORS, MentalFactor, MentalFactorType
from .scene import Scene


@dataclass
class ManifestLayer:
    """
    第四层：现行层
    
    当前激活的善心所和烦恼
    """
    active_wholesome: Dict[str, float] = field(default_factory=dict)   # 善心所
    active_afflictions: Dict[str, float] = field(default_factory=dict)  # 烦恼
    active_patterns: List[str] = field(default_factory=list)  # 当前能力模式
    timestamp: int = 0
    
    def get_all_active(self) -> Dict[str, float]:
        """获取所有激活的心所"""
        return {**self.active_wholesome, **self.active_afflictions}
    
    def is_active(self, factor_id: str) -> bool:
        return factor_id in self.active_wholesome or factor_id in self.active_afflictions
    
    def get_strength(self, factor_id: str) -> float:
        if factor_id in self.active_wholesome:
            return self.active_wholesome[factor_id]
        if factor_id in self.active_afflictions:
            return self.active_afflictions[factor_id]
        return 0.0
    
    def net_valence(self) -> float:
        """计算净善恶倾向"""
        wholesome_sum = sum(self.active_wholesome.values())
        affliction_sum = sum(self.active_afflictions.values())
        return wholesome_sum - affliction_sum


@dataclass 
class IndeterminateState:
    """
    第五层：不定四状态
    
    睡眠、恶作、寻、伺 - 可正可邪
    """
    sleep: float = 0.0      # 睡眠
    regret: float = 0.0     # 恶作/悔
    vitarka: float = 0.0    # 寻（粗）
    vicara: float = 0.0     # 伺（细）
    
    # 方向由伴随决定
    sleep_quality: str = "中性"   # 正常休息 / 懈怠逃避
    regret_quality: str = "中性"  # 正向反省 / 负面内耗
    vitarka_quality: str = "中性" # 正向探索 / 散乱妄想
    vicara_quality: str = "中性"  # 正向深入 / 执着纠缠


class DharmaEngineV2:
    """
    Dharma游戏引擎 V2
    
    五层架构的完整实现
    """
    
    # 核心公式参数
    SEED_WEIGHT = 2.0       # 种子权重
    CONDITION_WEIGHT = 1.5  # 场景条件
    COUNTER_WEIGHT = 1.0    # 对治系数
    PARTICULAR_WEIGHT = 0.8 # 别境影响
    
    MANIFEST_THRESHOLD = 0.4
    
    def __init__(
        self, 
        initial_seeds: Optional[Dict[str, float]] = None,
        initial_particular: Optional[Dict[str, float]] = None
    ):
        # 第一层：遍行五事件管线
        self.pipeline = UniversalPipeline()
        
        # 第二层：别境五能力系统
        self.particular = ParticularSystem(initial_particular)
        
        # 第三层：种子库
        self.seed_bank = SeedBank(initial_seeds)
        
        # 第四层：现行层
        self.manifest = ManifestLayer()
        
        # 第五层：不定四
        self.indeterminate = IndeterminateState()
        
        # 当前场景
        self.current_scene: Optional[Scene] = None
        
        # 主动对治力
        self.active_counterforces: Dict[str, float] = {}
        
        # 历史记录
        self.manifest_history: List[ManifestLayer] = []
    
    @staticmethod
    def sigmoid(x: float) -> float:
        return 1.0 / (1.0 + math.exp(-x))
    
    def process_stimulus(self, stimulus: str, intensity: float = 1.0) -> MentalEvent:
        """
        处理一个刺激，通过遍行五管线
        
        这是第一层的入口
        """
        context = self._build_pipeline_context()
        event = self.pipeline.process(stimulus, intensity, context)
        return event
    
    def _build_pipeline_context(self) -> Dict:
        """构建管线上下文"""
        return {
            "particular": self.particular.get_all_strengths(),
            "afflictions": self.manifest.active_afflictions,
            "seed_bias": {},  # TODO: 从种子库提取倾向
            "scene_valence": 0.0 if not self.current_scene else 0.0,
        }
    
    def calculate_manifest_probability(self, factor_id: str) -> float:
        """
        计算心所现行概率
        
        P = sigmoid(a*Seed + b*Condition + d*Particular - c*Counter)
        """
        factor = MENTAL_FACTORS.get(factor_id)
        if not factor:
            return 0.0
        
        # 种子权重
        seed_weight = self.seed_bank.get_weight(factor_id)
        
        # 场景条件
        condition = 0.0
        if self.current_scene:
            condition = self.current_scene.get_condition(factor_id)
        
        # 别境影响（某些心所受别境能力调制）
        particular_mod = self._get_particular_modifier(factor_id)
        
        # 对治力
        counterforce = self.active_counterforces.get(factor_id, 0.0)
        
        x = (self.SEED_WEIGHT * (seed_weight - 0.5) +
             self.CONDITION_WEIGHT * condition +
             self.PARTICULAR_WEIGHT * particular_mod -
             self.COUNTER_WEIGHT * counterforce)
        
        return self.sigmoid(x)
    
    def _get_particular_modifier(self, factor_id: str) -> float:
        """获取别境对特定心所的调制"""
        factor = MENTAL_FACTORS.get(factor_id)
        if not factor:
            return 0.0
        
        # 烦恼受定/念的抑制
        if factor.type in [MentalFactorType.PRIMARY_AFFLICTION, 
                           MentalFactorType.SECONDARY_AFFLICTION]:
            samadhi = self.particular.get_strength("samadhi")
            smrti = self.particular.get_strength("smrti")
            return -(samadhi + smrti) * 0.3  # 定和念高时，烦恼更难现行
        
        # 善心所受慧的增强
        if factor.type == MentalFactorType.WHOLESOME:
            prajna = self.particular.get_strength("prajna")
            return prajna * 0.2
        
        return 0.0
    
    def update_manifest(self, scene: Optional[Scene] = None) -> ManifestLayer:
        """
        更新现行层
        
        根据种子、场景、别境计算当前激活的心所
        """
        if scene:
            self.current_scene = scene
        
        # 先检查别境的打断状态
        self.particular.check_disruption(self.manifest.active_afflictions)
        
        new_manifest = ManifestLayer(timestamp=self.seed_bank.current_time)
        
        # 遍历所有心所（除遍行和别境）
        for factor_id, factor in MENTAL_FACTORS.items():
            if factor.type in [MentalFactorType.UNIVERSAL, 
                               MentalFactorType.PARTICULAR]:
                continue
            
            prob = self.calculate_manifest_probability(factor_id)
            
            if prob > self.MANIFEST_THRESHOLD and random.random() < prob:
                if factor.type == MentalFactorType.WHOLESOME:
                    new_manifest.active_wholesome[factor_id] = prob
                elif factor.type in [MentalFactorType.PRIMARY_AFFLICTION,
                                     MentalFactorType.SECONDARY_AFFLICTION]:
                    new_manifest.active_afflictions[factor_id] = prob
                
                # 记录现行
                self.seed_bank.manifest(factor_id)
        
        # 更新别境方向
        all_active = new_manifest.get_all_active()
        for cap_id in ["chanda", "adhimoksa", "smrti", "samadhi", "prajna"]:
            self.particular.update_direction(cap_id, all_active)
        
        # 检测能力模式
        new_manifest.active_patterns = detect_pattern(self.particular, all_active)
        
        # 保存
        self.manifest = new_manifest
        self.manifest_history.append(new_manifest)
        if len(self.manifest_history) > 100:
            self.manifest_history = self.manifest_history[-50:]
        
        return new_manifest
    
    def perform_action(self, action_name: str, intensity: float = 1.0) -> Dict:
        """
        执行行为，产生熏习
        
        更新种子库和别境能力
        """
        from .engine import PREDEFINED_ACTIONS
        
        action = PREDEFINED_ACTIONS.get(action_name)
        if not action:
            return {"error": f"未知行为: {action_name}"}
        
        changes = {"seeds": {}, "particular": {}}
        
        # 更新种子
        for factor_id, effect in action.effects.items():
            self.seed_bank.update(factor_id, effect, intensity)
            changes["seeds"][factor_id] = effect * intensity
        
        # 特定行为更新别境能力
        particular_effects = self._get_action_particular_effects(action_name)
        for cap_id, effect in particular_effects.items():
            self.particular.update_strength(cap_id, effect, intensity)
            changes["particular"][cap_id] = effect * intensity
        
        # 应用对治
        for target_id in action.counterforce_targets:
            factor = MENTAL_FACTORS.get(target_id)
            if factor and factor.counterforce:
                self.seed_bank.apply_counterforce(
                    factor.counterforce, target_id, intensity
                )
        
        return changes
    
    def _get_action_particular_effects(self, action_name: str) -> Dict[str, float]:
        """获取行为对别境的影响"""
        effects = {
            "布施": {"chanda": 0.1},           # 布施增强正向动力
            "持戒": {"adhimoksa": 0.1},        # 持戒增强承诺
            "忍辱": {"adhimoksa": 0.1, "samadhi": 0.05},
            "精进": {"chanda": 0.15, "smrti": 0.05},
            "禅定": {"samadhi": 0.2, "smrti": 0.1},
            "观察": {"prajna": 0.15},
            "正念": {"smrti": 0.2, "samadhi": 0.1},
            "慈心": {"samadhi": 0.05},
        }
        return effects.get(action_name, {})
    
    def apply_counterforce(self, counterforce_id: str, target_id: str, strength: float = 1.0):
        """应用对治"""
        self.active_counterforces[target_id] = strength
        self.seed_bank.apply_counterforce(counterforce_id, target_id, strength)
    
    def tick(self):
        """时间前进"""
        self.seed_bank.tick()
        self.pipeline.tick()
        
        # 对治力衰减
        for k in list(self.active_counterforces.keys()):
            self.active_counterforces[k] *= 0.8
            if self.active_counterforces[k] < 0.1:
                del self.active_counterforces[k]
        
        # 不定四衰减
        self.indeterminate.sleep *= 0.9
        self.indeterminate.regret *= 0.95
        self.indeterminate.vitarka *= 0.9
        self.indeterminate.vicara *= 0.9
    
    def get_full_status(self) -> Dict:
        """获取完整状态"""
        return {
            "time": self.seed_bank.current_time,
            "scene": self.current_scene.name if self.current_scene else None,
            
            # 第二层：别境
            "particular": self.particular.get_status(),
            "active_patterns": self.manifest.active_patterns,
            
            # 第三层：种子（摘要）
            "dominant_affliction_seeds": self.seed_bank.get_dominant_afflictions(3),
            "dominant_wholesome_seeds": self.seed_bank.get_dominant_virtues(3),
            
            # 第四层：现行
            "manifest_wholesome": self.manifest.active_wholesome,
            "manifest_afflictions": self.manifest.active_afflictions,
            "net_valence": self.manifest.net_valence(),
            
            # 第五层：不定
            "indeterminate": {
                "sleep": self.indeterminate.sleep,
                "regret": self.indeterminate.regret,
                "vitarka": self.indeterminate.vitarka,
                "vicara": self.indeterminate.vicara,
            },
            
            # 管线统计
            "pipeline_summary": self.pipeline.get_event_summary(),
        }
    
    def get_review(self) -> str:
        """
        获取可复盘的状态描述
        
        用于失败/成功后分析原因
        """
        lines = []
        lines.append("=== 心理状态复盘 ===\n")
        
        # 别境状态
        lines.append("【别境五（能力条）】")
        for cap_id, cap in self.particular.capabilities.items():
            effect, desc = self.particular.get_combined_effect(cap_id)
            lines.append(f"  {desc}")
        
        # 能力模式
        if self.manifest.active_patterns:
            lines.append(f"\n【当前模式】{', '.join(self.manifest.active_patterns)}")
        
        # 现行层
        if self.manifest.active_wholesome:
            wholesome_str = ", ".join([
                f"{MENTAL_FACTORS[k].name_zh}({v:.2f})" 
                for k, v in self.manifest.active_wholesome.items()
            ])
            lines.append(f"\n【善心所现行】{wholesome_str}")
        
        if self.manifest.active_afflictions:
            affliction_str = ", ".join([
                f"{MENTAL_FACTORS[k].name_zh}({v:.2f})" 
                for k, v in self.manifest.active_afflictions.items()
            ])
            lines.append(f"\n【烦恼现行】{affliction_str}")
        
        # 净善恶
        valence = self.manifest.net_valence()
        if valence > 0.5:
            lines.append(f"\n【总体】善力较强 (+{valence:.2f})")
        elif valence < -0.5:
            lines.append(f"\n【总体】烦恼较重 ({valence:.2f})")
        else:
            lines.append(f"\n【总体】善恶相当 ({valence:.2f})")
        
        # 关键种子
        top_afflictions = self.seed_bank.get_dominant_afflictions(2)
        if top_afflictions:
            lines.append(f"\n【潜伏烦恼种子】" + 
                        ", ".join([f"{MENTAL_FACTORS[k].name_zh}({v:.2f})" 
                                   for k, v in top_afflictions]))
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        return (f"DharmaEngineV2(t={self.seed_bank.current_time}, "
                f"particular={self.particular}, "
                f"valence={self.manifest.net_valence():.2f})")


def create_character_v2(archetype: str = "neutral") -> DharmaEngineV2:
    """创建角色（V2）"""
    seeds = {}
    particular = {}
    
    if archetype == "修行者":
        seeds = {
            "sraddha": 0.7, "virya": 0.6, "alobha": 0.6,
            "raga": 0.3, "moha": 0.4
        }
        particular = {
            "samadhi": 0.6, "prajna": 0.6, "smrti": 0.6
        }
    
    elif archetype == "凡夫":
        seeds = {
            "raga": 0.6, "moha": 0.6, "mana": 0.5,
            "alobha": 0.3, "amoha": 0.3
        }
        particular = {
            "chanda": 0.6, "prajna": 0.4
        }
    
    elif archetype == "智者":
        seeds = {
            "amoha": 0.8, "prajna": 0.7,
            "moha": 0.2, "drsti": 0.2
        }
        particular = {
            "prajna": 0.8, "smrti": 0.6, "samadhi": 0.5
        }
    
    elif archetype == "贪者":
        seeds = {
            "raga": 0.8, "matsarya": 0.6,
            "alobha": 0.2
        }
        particular = {
            "chanda": 0.7
        }
    
    elif archetype == "嗔者":
        seeds = {
            "pratigha": 0.8, "krodha": 0.7,
            "advesa": 0.2
        }
        particular = {
            "adhimoksa": 0.6  # 固执
        }
    
    return DharmaEngineV2(initial_seeds=seeds, initial_particular=particular)
