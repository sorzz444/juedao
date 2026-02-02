"""
种子库 (Seed Bank / Ālaya-vijñāna Storage)

基于唯识的阿赖耶识种子理论
"""

import math
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from .mental_factors import MENTAL_FACTORS, MentalFactorType


@dataclass
class Seed:
    """种子结构"""
    factor_id: str           # 对应的心所ID
    weight: float            # 权重 ∈ [0, 1]
    momentum: float = 0.0    # 动量（连续熏习的累积效应）
    last_manifest: int = 0   # 上次现行的时间戳
    manifest_count: int = 0  # 总现行次数
    
    def to_dict(self) -> dict:
        return {
            "factor_id": self.factor_id,
            "weight": self.weight,
            "momentum": self.momentum,
            "last_manifest": self.last_manifest,
            "manifest_count": self.manifest_count
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Seed':
        return cls(**data)


class SeedBank:
    """
    种子库 - 阿赖耶识的种子储藏功能
    
    实现种子六义：
    1. 刹那灭 - 种子每时刻都在变化（通过weight的持续更新）
    2. 果俱有 - 种子与现行同时（计算时同时考虑）
    3. 恒随转 - 种子持续存在（persistence）
    4. 性决定 - 善恶性质决定（通过MentalFactorType）
    5. 待众缘 - 需要条件才能现行（Condition矩阵）
    6. 引自果 - 各引各的果（factor_id对应）
    """
    
    def __init__(self, initial_weights: Optional[Dict[str, float]] = None):
        self.seeds: Dict[str, Seed] = {}
        self.current_time: int = 0
        
        # 初始化所有心所的种子
        for factor_id in MENTAL_FACTORS:
            initial_weight = 0.5  # 默认中性
            if initial_weights and factor_id in initial_weights:
                initial_weight = initial_weights[factor_id]
            
            self.seeds[factor_id] = Seed(
                factor_id=factor_id,
                weight=self._clamp(initial_weight)
            )
    
    def _clamp(self, value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """限制值在范围内"""
        return max(min_val, min(max_val, value))
    
    def get_weight(self, factor_id: str) -> float:
        """获取种子权重"""
        if factor_id in self.seeds:
            return self.seeds[factor_id].weight
        return 0.5  # 默认中性
    
    def get_seed(self, factor_id: str) -> Optional[Seed]:
        """获取种子对象"""
        return self.seeds.get(factor_id)
    
    def update(self, factor_id: str, delta: float, intensity: float = 1.0):
        """
        熏习更新种子
        
        实现熏习四义：
        1. 有生灭 - delta可正可负
        2. 有胜用 - intensity影响更新强度
        3. 有增减 - weight会增减
        4. 与所熏和合 - 直接更新对应种子
        
        Args:
            factor_id: 心所ID
            delta: 变化量 (-1 到 1)
            intensity: 熏习强度 (0 到 1)
        """
        if factor_id not in self.seeds:
            return
        
        seed = self.seeds[factor_id]
        
        # 基础更新
        base_delta = delta * intensity * 0.1  # 缩放因子
        
        # 动量效应：连续同向熏习会加速
        if (delta > 0 and seed.momentum > 0) or (delta < 0 and seed.momentum < 0):
            momentum_bonus = abs(seed.momentum) * 0.2
            base_delta *= (1 + momentum_bonus)
        
        # 更新权重
        seed.weight = self._clamp(seed.weight + base_delta)
        
        # 更新动量（衰减 + 新增）
        seed.momentum = seed.momentum * 0.9 + delta * 0.1
        seed.momentum = self._clamp(seed.momentum, -1.0, 1.0)
    
    def manifest(self, factor_id: str):
        """记录现行"""
        if factor_id in self.seeds:
            seed = self.seeds[factor_id]
            seed.last_manifest = self.current_time
            seed.manifest_count += 1
    
    def tick(self):
        """时间前进"""
        self.current_time += 1
        
        # 动量自然衰减
        for seed in self.seeds.values():
            seed.momentum *= 0.95
    
    def get_weights_by_type(self, factor_type: MentalFactorType) -> Dict[str, float]:
        """按类型获取权重"""
        result = {}
        for factor_id, seed in self.seeds.items():
            factor = MENTAL_FACTORS.get(factor_id)
            if factor and factor.type == factor_type:
                result[factor_id] = seed.weight
        return result
    
    def get_dominant_afflictions(self, top_n: int = 3) -> List[Tuple[str, float]]:
        """获取最强的烦恼"""
        afflictions = []
        for factor_id, seed in self.seeds.items():
            factor = MENTAL_FACTORS.get(factor_id)
            if factor and factor.type in [
                MentalFactorType.PRIMARY_AFFLICTION,
                MentalFactorType.SECONDARY_AFFLICTION
            ]:
                afflictions.append((factor_id, seed.weight))
        
        afflictions.sort(key=lambda x: x[1], reverse=True)
        return afflictions[:top_n]
    
    def get_dominant_virtues(self, top_n: int = 3) -> List[Tuple[str, float]]:
        """获取最强的善心所"""
        virtues = []
        for factor_id, seed in self.seeds.items():
            factor = MENTAL_FACTORS.get(factor_id)
            if factor and factor.type == MentalFactorType.WHOLESOME:
                virtues.append((factor_id, seed.weight))
        
        virtues.sort(key=lambda x: x[1], reverse=True)
        return virtues[:top_n]
    
    def apply_counterforce(self, counterforce_id: str, target_id: str, strength: float = 1.0):
        """
        应用对治
        
        对治成功时：
        - 目标烦恼种子减弱
        - 对治善法种子增强
        """
        if counterforce_id not in self.seeds or target_id not in self.seeds:
            return
        
        # 削弱目标
        self.update(target_id, -strength * 0.5, intensity=1.0)
        
        # 增强对治
        self.update(counterforce_id, strength * 0.3, intensity=1.0)
    
    def to_dict(self) -> dict:
        """序列化"""
        return {
            "current_time": self.current_time,
            "seeds": {k: v.to_dict() for k, v in self.seeds.items()}
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SeedBank':
        """反序列化"""
        bank = cls()
        bank.current_time = data.get("current_time", 0)
        for factor_id, seed_data in data.get("seeds", {}).items():
            if factor_id in bank.seeds:
                bank.seeds[factor_id] = Seed.from_dict(seed_data)
        return bank
    
    def save(self, filepath: str):
        """保存到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'SeedBank':
        """从文件加载"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def __repr__(self) -> str:
        top_afflictions = self.get_dominant_afflictions(3)
        top_virtues = self.get_dominant_virtues(3)
        
        affliction_str = ", ".join([f"{MENTAL_FACTORS[k].name_zh}:{v:.2f}" for k, v in top_afflictions])
        virtue_str = ", ".join([f"{MENTAL_FACTORS[k].name_zh}:{v:.2f}" for k, v in top_virtues])
        
        return f"SeedBank(time={self.current_time}, 主烦恼=[{affliction_str}], 主善=[{virtue_str}])"
