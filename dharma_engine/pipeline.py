"""
遍行五事件管线 (Universal Five Pipeline)

遍行五不是"条件"，而是每个心刹那的组件。
它们构成从"境"到"行为"的事件处理管线。

境 → 作意(选中) → 触(接通) → 受(体验) → 想(标签) → 思(推动)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class FeelingTone(Enum):
    """受的三种性质"""
    PLEASANT = "乐受"      # 想要更多
    UNPLEASANT = "苦受"    # 想要逃避
    NEUTRAL = "舍受"       # 不推不拒


@dataclass
class MentalEvent:
    """
    心理事件 - 一次完整的遍行五管线输出
    
    这是底层计算结果，不一定要给玩家看，
    但可以在debug/复盘时展示。
    """
    # 输入
    stimulus: str                    # 触发刺激
    stimulus_intensity: float        # 刺激强度 [0, 1]
    
    # 遍行五处理结果
    manaskara_target: str            # 作意：选中了什么
    manaskara_strength: float        # 作意强度（注意力分配）
    
    sparsa_success: bool             # 触：是否成功接通
    sparsa_clarity: float            # 触的清晰度
    
    vedana_tone: FeelingTone         # 受：苦乐舍
    vedana_intensity: float          # 受的强度
    
    samjna_label: str                # 想：贴的标签/概念
    samjna_confidence: float         # 标签的确信度
    
    cetana_direction: str            # 思：推动的方向（趋/避/住）
    cetana_force: float              # 推动力量
    
    # 元数据
    timestamp: int = 0
    triggered_factors: List[str] = field(default_factory=list)  # 触发了哪些心所
    
    def to_log(self) -> str:
        """生成日志字符串"""
        return (
            f"[{self.timestamp}] {self.stimulus} "
            f"→ 作意({self.manaskara_target}, {self.manaskara_strength:.2f}) "
            f"→ 触({'✓' if self.sparsa_success else '✗'}, {self.sparsa_clarity:.2f}) "
            f"→ 受({self.vedana_tone.value}, {self.vedana_intensity:.2f}) "
            f"→ 想({self.samjna_label}, {self.samjna_confidence:.2f}) "
            f"→ 思({self.cetana_direction}, {self.cetana_force:.2f})"
        )


class UniversalPipeline:
    """
    遍行五事件管线
    
    处理从外境输入到心理事件的转换。
    这是系统底层，每个"心刹那"都要经过这个管线。
    """
    
    def __init__(self):
        self.event_log: List[MentalEvent] = []
        self.current_time: int = 0
    
    def process(
        self,
        stimulus: str,
        stimulus_intensity: float,
        context: Dict[str, Any]
    ) -> MentalEvent:
        """
        处理一次输入，生成心理事件
        
        Args:
            stimulus: 刺激描述
            stimulus_intensity: 刺激强度
            context: 上下文（包含别境五状态、种子权重等）
        
        Returns:
            完整的心理事件
        """
        # 1. 作意 (Manaskāra) - 注意力选择
        # 受别境"欲"和种子倾向影响
        manaskara_target = stimulus
        manaskara_strength = self._calculate_attention(
            stimulus, stimulus_intensity, context
        )
        
        # 2. 触 (Sparśa) - 根境识和合
        # 受别境"定"和当前散乱程度影响
        sparsa_success, sparsa_clarity = self._calculate_contact(
            manaskara_strength, context
        )
        
        if not sparsa_success:
            # 触不成功，后续都弱化
            sparsa_clarity = 0.1
        
        # 3. 受 (Vedanā) - 苦乐舍体验
        # 受种子倾向和当前场景影响
        vedana_tone, vedana_intensity = self._calculate_feeling(
            stimulus, sparsa_clarity, context
        )
        
        # 4. 想 (Saṃjñā) - 概念化/贴标签
        # 受别境"慧"和记忆影响
        samjna_label, samjna_confidence = self._calculate_perception(
            stimulus, vedana_tone, context
        )
        
        # 5. 思 (Cetanā) - 意志推动
        # 综合以上，决定行为方向
        cetana_direction, cetana_force = self._calculate_volition(
            vedana_tone, vedana_intensity, samjna_label, context
        )
        
        # 创建事件
        event = MentalEvent(
            stimulus=stimulus,
            stimulus_intensity=stimulus_intensity,
            manaskara_target=manaskara_target,
            manaskara_strength=manaskara_strength,
            sparsa_success=sparsa_success,
            sparsa_clarity=sparsa_clarity,
            vedana_tone=vedana_tone,
            vedana_intensity=vedana_intensity,
            samjna_label=samjna_label,
            samjna_confidence=samjna_confidence,
            cetana_direction=cetana_direction,
            cetana_force=cetana_force,
            timestamp=self.current_time
        )
        
        # 记录日志
        self.event_log.append(event)
        if len(self.event_log) > 1000:
            self.event_log = self.event_log[-500:]
        
        return event
    
    def _calculate_attention(
        self, 
        stimulus: str, 
        intensity: float, 
        context: Dict
    ) -> float:
        """计算作意强度"""
        base = intensity
        
        # 别境"欲"影响：有欲求则更容易注意
        chanda = context.get("particular", {}).get("chanda", 0.5)
        
        # 种子倾向影响：对某类刺激的习惯性注意
        seed_bias = context.get("seed_bias", {}).get(stimulus, 0.0)
        
        # 散乱影响：散乱高则注意力分散
        distraction = context.get("afflictions", {}).get("viksepa", 0.0)
        
        attention = base * (0.5 + chanda * 0.3 + seed_bias * 0.2) * (1 - distraction * 0.5)
        return max(0.0, min(1.0, attention))
    
    def _calculate_contact(
        self, 
        attention: float, 
        context: Dict
    ) -> tuple:
        """计算触的成功与清晰度"""
        # 别境"定"影响
        samadhi = context.get("particular", {}).get("samadhi", 0.5)
        
        # 惛沉影响
        torpor = context.get("afflictions", {}).get("styana", 0.0)
        
        clarity = attention * (0.5 + samadhi * 0.5) * (1 - torpor * 0.7)
        success = clarity > 0.2
        
        return success, max(0.0, min(1.0, clarity))
    
    def _calculate_feeling(
        self, 
        stimulus: str, 
        clarity: float, 
        context: Dict
    ) -> tuple:
        """计算受"""
        # 从种子库获取对此类刺激的倾向
        seed_valence = context.get("seed_valence", {}).get(stimulus, 0.0)
        
        # 场景影响
        scene_valence = context.get("scene_valence", 0.0)
        
        combined = seed_valence + scene_valence
        
        if combined > 0.2:
            tone = FeelingTone.PLEASANT
        elif combined < -0.2:
            tone = FeelingTone.UNPLEASANT
        else:
            tone = FeelingTone.NEUTRAL
        
        intensity = abs(combined) * clarity
        return tone, max(0.0, min(1.0, intensity))
    
    def _calculate_perception(
        self, 
        stimulus: str, 
        feeling: FeelingTone, 
        context: Dict
    ) -> tuple:
        """计算想（概念化）"""
        # 别境"慧"影响标签的精确度
        prajna = context.get("particular", {}).get("prajna", 0.5)
        
        # 别境"念"影响能否调取正确记忆
        smrti = context.get("particular", {}).get("smrti", 0.5)
        
        # 不正见影响：可能贴错标签
        wrong_view = context.get("afflictions", {}).get("drsti", 0.0)
        
        # 简化：使用刺激名作为标签
        label = stimulus
        
        # 确信度受慧和念影响，但可能被不正见歪曲
        confidence = (prajna * 0.5 + smrti * 0.5) * (1 - wrong_view * 0.5)
        
        return label, max(0.0, min(1.0, confidence))
    
    def _calculate_volition(
        self, 
        feeling: FeelingTone, 
        intensity: float, 
        label: str, 
        context: Dict
    ) -> tuple:
        """计算思（意志推动）"""
        # 基于受决定方向
        if feeling == FeelingTone.PLEASANT:
            direction = "趋"  # 想要接近/获得
        elif feeling == FeelingTone.UNPLEASANT:
            direction = "避"  # 想要远离/消除
        else:
            direction = "住"  # 保持现状
        
        # 推动力量受别境"欲"和"胜解"影响
        chanda = context.get("particular", {}).get("chanda", 0.5)
        adhimoksa = context.get("particular", {}).get("adhimoksa", 0.5)
        
        # 也受懈怠影响
        laziness = context.get("afflictions", {}).get("kausidya", 0.0)
        
        force = intensity * (chanda * 0.5 + adhimoksa * 0.5) * (1 - laziness * 0.5)
        
        return direction, max(0.0, min(1.0, force))
    
    def tick(self):
        """时间前进"""
        self.current_time += 1
    
    def get_recent_events(self, n: int = 10) -> List[MentalEvent]:
        """获取最近的事件"""
        return self.event_log[-n:]
    
    def get_event_summary(self) -> Dict:
        """获取事件统计摘要"""
        if not self.event_log:
            return {}
        
        recent = self.event_log[-100:]
        
        pleasant = sum(1 for e in recent if e.vedana_tone == FeelingTone.PLEASANT)
        unpleasant = sum(1 for e in recent if e.vedana_tone == FeelingTone.UNPLEASANT)
        neutral = sum(1 for e in recent if e.vedana_tone == FeelingTone.NEUTRAL)
        
        avg_attention = sum(e.manaskara_strength for e in recent) / len(recent)
        avg_clarity = sum(e.sparsa_clarity for e in recent) / len(recent)
        
        return {
            "total_events": len(self.event_log),
            "recent_pleasant": pleasant,
            "recent_unpleasant": unpleasant,
            "recent_neutral": neutral,
            "avg_attention": avg_attention,
            "avg_clarity": avg_clarity
        }
