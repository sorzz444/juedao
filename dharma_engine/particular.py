"""
别境五 (Particular Five) - 中性能力条

别境五是"中性能力"，不是天然正向buff：
- 欲 ≠ 善（可能是贪欲）
- 胜解 ≠ 善（可能是执见）
- 念 ≠ 善（可能是邪念）
- 定 ≠ 善（可能是邪定）
- 慧 ≠ 善（可能是邪慧）

方向由"伴随心所"决定。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class CapabilityDirection(Enum):
    """能力的方向/染净"""
    WHOLESOME = "善"      # 与善心所伴随
    UNWHOLESOME = "不善"   # 与烦恼伴随
    NEUTRAL = "无记"       # 方向不定


@dataclass
class ParticularCapability:
    """
    别境能力
    
    每个别境有：
    - 强度：能力的高低
    - 方向：由伴随心所决定
    - 稳定性：是否容易被打断
    """
    id: str
    name_zh: str
    name_en: str
    
    strength: float = 0.5           # 能力强度 [0, 1]
    direction: CapabilityDirection = CapabilityDirection.NEUTRAL
    stability: float = 0.5          # 稳定性 [0, 1]
    
    # 什么会打断这个能力
    disruptors: List[str] = field(default_factory=list)
    
    # 当前是否被打断
    disrupted: bool = False
    disruption_source: Optional[str] = None
    
    def effective_strength(self) -> float:
        """有效强度（考虑打断）"""
        if self.disrupted:
            return self.strength * 0.2  # 被打断时大幅削弱
        return self.strength
    
    def get_valence(self) -> float:
        """获取方向的数值表示（用于计算）"""
        if self.direction == CapabilityDirection.WHOLESOME:
            return 1.0
        elif self.direction == CapabilityDirection.UNWHOLESOME:
            return -1.0
        return 0.0


class ParticularSystem:
    """
    别境五系统
    
    管理五个中性能力条：
    1. 欲 (chanda) - 动机/趋向
    2. 胜解 (adhimoksa) - 承诺/决断
    3. 念 (smrti) - 记忆/持续
    4. 定 (samadhi) - 稳定/一境
    5. 慧 (prajna) - 辨析/简择
    """
    
    def __init__(self, initial_values: Optional[Dict[str, float]] = None):
        self.capabilities: Dict[str, ParticularCapability] = {}
        self._init_capabilities(initial_values or {})
    
    def _init_capabilities(self, initial: Dict[str, float]):
        """初始化五个别境"""
        
        self.capabilities["chanda"] = ParticularCapability(
            id="chanda",
            name_zh="欲",
            name_en="desire-to-act",
            strength=initial.get("chanda", 0.5),
            disruptors=["kausidya", "styana"],  # 懈怠、惛沉会打断
        )
        
        self.capabilities["adhimoksa"] = ParticularCapability(
            id="adhimoksa",
            name_zh="胜解",
            name_en="resolve",
            strength=initial.get("adhimoksa", 0.5),
            disruptors=["vicikitsa"],  # 疑会打断
        )
        
        self.capabilities["smrti"] = ParticularCapability(
            id="smrti",
            name_zh="念",
            name_en="mindfulness",
            strength=initial.get("smrti", 0.5),
            disruptors=["musitasmritita", "viksepa"],  # 失念、散乱会打断
        )
        
        self.capabilities["samadhi"] = ParticularCapability(
            id="samadhi",
            name_zh="定",
            name_en="concentration",
            strength=initial.get("samadhi", 0.5),
            disruptors=["viksepa", "auddhatya", "styana"],  # 散乱、掉举、惛沉
        )
        
        self.capabilities["prajna"] = ParticularCapability(
            id="prajna",
            name_zh="慧",
            name_en="wisdom",
            strength=initial.get("prajna", 0.5),
            disruptors=["styana", "moha"],  # 惛沉、痴会打断
        )
    
    def get(self, cap_id: str) -> Optional[ParticularCapability]:
        """获取能力"""
        return self.capabilities.get(cap_id)
    
    def get_strength(self, cap_id: str) -> float:
        """获取能力强度"""
        cap = self.capabilities.get(cap_id)
        return cap.effective_strength() if cap else 0.5
    
    def get_all_strengths(self) -> Dict[str, float]:
        """获取所有能力的有效强度"""
        return {k: v.effective_strength() for k, v in self.capabilities.items()}
    
    def update_strength(self, cap_id: str, delta: float, intensity: float = 1.0):
        """更新能力强度（熏习）"""
        if cap_id not in self.capabilities:
            return
        
        cap = self.capabilities[cap_id]
        cap.strength = max(0.0, min(1.0, cap.strength + delta * intensity * 0.1))
    
    def update_direction(self, cap_id: str, accompanying: Dict[str, float]):
        """
        根据伴随心所更新方向
        
        Args:
            cap_id: 能力ID
            accompanying: 当前激活的心所及其强度
        """
        if cap_id not in self.capabilities:
            return
        
        cap = self.capabilities[cap_id]
        
        # 计算善/不善的总权重
        wholesome_weight = 0.0
        unwholesome_weight = 0.0
        
        # 善心所
        wholesome_factors = [
            "sraddha", "hri", "apatrapya", "alobha", "advesa", "amoha",
            "virya", "prasrabdhi", "apramada", "upeksa", "ahimsa"
        ]
        
        # 根本烦恼
        unwholesome_factors = [
            "raga", "pratigha", "moha", "mana", "vicikitsa", "drsti"
        ]
        
        for factor_id, strength in accompanying.items():
            if factor_id in wholesome_factors:
                wholesome_weight += strength
            elif factor_id in unwholesome_factors:
                unwholesome_weight += strength
        
        # 决定方向
        if wholesome_weight > unwholesome_weight + 0.2:
            cap.direction = CapabilityDirection.WHOLESOME
        elif unwholesome_weight > wholesome_weight + 0.2:
            cap.direction = CapabilityDirection.UNWHOLESOME
        else:
            cap.direction = CapabilityDirection.NEUTRAL
    
    def check_disruption(self, active_afflictions: Dict[str, float]):
        """
        检查打断状态
        
        Args:
            active_afflictions: 当前激活的烦恼及其强度
        """
        for cap_id, cap in self.capabilities.items():
            cap.disrupted = False
            cap.disruption_source = None
            
            for disruptor in cap.disruptors:
                if disruptor in active_afflictions:
                    disruptor_strength = active_afflictions[disruptor]
                    # 如果打断者强度超过能力稳定性，则打断
                    if disruptor_strength > cap.stability:
                        cap.disrupted = True
                        cap.disruption_source = disruptor
                        break
    
    def get_combined_effect(self, cap_id: str) -> Tuple[float, str]:
        """
        获取能力的综合效果（强度 × 方向）
        
        Returns:
            (效果值, 描述)
            效果值：正数=善用，负数=恶用，0=中性
        """
        cap = self.capabilities.get(cap_id)
        if not cap:
            return 0.0, "无"
        
        strength = cap.effective_strength()
        valence = cap.get_valence()
        
        effect = strength * valence
        
        if cap.disrupted:
            desc = f"{cap.name_zh}被{cap.disruption_source}打断"
        elif valence > 0:
            desc = f"{cap.name_zh}善用（{strength:.2f}）"
        elif valence < 0:
            desc = f"{cap.name_zh}恶用（{strength:.2f}）"
        else:
            desc = f"{cap.name_zh}中性（{strength:.2f}）"
        
        return effect, desc
    
    def get_status(self) -> Dict:
        """获取状态摘要"""
        status = {}
        for cap_id, cap in self.capabilities.items():
            effect, desc = self.get_combined_effect(cap_id)
            status[cap_id] = {
                "name": cap.name_zh,
                "strength": cap.strength,
                "effective": cap.effective_strength(),
                "direction": cap.direction.value,
                "disrupted": cap.disrupted,
                "disruption_source": cap.disruption_source,
                "effect": effect,
                "description": desc
            }
        return status
    
    def __repr__(self) -> str:
        parts = []
        for cap_id, cap in self.capabilities.items():
            effect, _ = self.get_combined_effect(cap_id)
            sign = "+" if effect > 0 else ("−" if effect < 0 else "○")
            disrupted = "!" if cap.disrupted else ""
            parts.append(f"{cap.name_zh}{sign}{disrupted}:{cap.effective_strength():.2f}")
        return f"Particular({', '.join(parts)})"


# 预定义的能力组合模式
CAPABILITY_PATTERNS = {
    "正慧": {
        "required": {"prajna": 0.6, "amoha": 0.5},
        "forbidden": {"drsti": 0.5},
        "effect": "洞察、破执、对治增强"
    },
    "邪慧": {
        "required": {"prajna": 0.6, "drsti": 0.5},
        "effect": "自圆其说、越聪明越难救"
    },
    "清明定": {
        "required": {"samadhi": 0.6, "prasrabdhi": 0.5},
        "forbidden": {"styana": 0.5},
        "effect": "稳定清明的专注"
    },
    "昏沉定": {
        "required": {"samadhi": 0.6, "styana": 0.5},
        "effect": "沉没式假定，看似稳实则黑"
    },
    "正念": {
        "required": {"smrti": 0.6, "apramada": 0.5},
        "effect": "明记不忘，不放逸"
    },
    "执念": {
        "required": {"smrti": 0.6, "raga": 0.5},
        "effect": "记住但执著，难以放下"
    },
    "正勤": {
        "required": {"chanda": 0.6, "virya": 0.5},
        "forbidden": {"raga": 0.5},
        "effect": "正向动力，精进修行"
    },
    "贪欲": {
        "required": {"chanda": 0.6, "raga": 0.5},
        "effect": "强烈渴求，难以满足"
    },
    "正信": {
        "required": {"adhimoksa": 0.6, "sraddha": 0.5},
        "effect": "坚定信念，不被动摇"
    },
    "固执": {
        "required": {"adhimoksa": 0.6, "mana": 0.5},
        "effect": "刚愎自用，不听劝告"
    },
}


def detect_pattern(
    particular: ParticularSystem, 
    active_factors: Dict[str, float]
) -> List[str]:
    """
    检测当前符合哪些能力模式
    
    Args:
        particular: 别境系统
        active_factors: 当前激活的所有心所
    
    Returns:
        匹配的模式名列表
    """
    matched = []
    
    for pattern_name, pattern_def in CAPABILITY_PATTERNS.items():
        # 检查必要条件
        required_met = True
        for factor_id, min_strength in pattern_def["required"].items():
            if factor_id in ["prajna", "samadhi", "smrti", "chanda", "adhimoksa"]:
                # 别境
                if particular.get_strength(factor_id) < min_strength:
                    required_met = False
                    break
            else:
                # 其他心所
                if active_factors.get(factor_id, 0) < min_strength:
                    required_met = False
                    break
        
        if not required_met:
            continue
        
        # 检查禁止条件
        forbidden = pattern_def.get("forbidden", {})
        forbidden_present = False
        for factor_id, max_strength in forbidden.items():
            if active_factors.get(factor_id, 0) >= max_strength:
                forbidden_present = True
                break
        
        if forbidden_present:
            continue
        
        matched.append(pattern_name)
    
    return matched
