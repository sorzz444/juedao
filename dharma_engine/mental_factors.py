"""
五十一心所 (Caitasika) 定义

基于《成唯识论》的心所分类体系
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional


class MentalFactorType(Enum):
    """心所类型"""
    UNIVERSAL = "遍行"      # 5个，每念必有
    PARTICULAR = "别境"     # 5个，缘特定境生，但常驻
    WHOLESOME = "善"        # 11个，正向buff
    PRIMARY_AFFLICTION = "根本烦恼"  # 6个，核心debuff
    SECONDARY_AFFLICTION = "随烦恼"  # 20个，衍生debuff
    INDETERMINATE = "不定"  # 4个，可正可邪


@dataclass
class MentalFactor:
    """心所定义"""
    id: str                          # 唯一标识
    name_zh: str                     # 中文名
    name_en: str                     # 英文名
    name_sanskrit: str               # 梵文名
    type: MentalFactorType           # 类型
    description: str                 # 描述
    counterforce: Optional[str]      # 对治心所ID
    triggers: List[str]              # 触发条件
    effects: Dict[str, float]        # 效果（对其他属性的影响）


# 五十一心所完整定义
MENTAL_FACTORS: Dict[str, MentalFactor] = {}


def _init_mental_factors():
    """初始化五十一心所"""
    global MENTAL_FACTORS
    
    # ========== 遍行五 (Universal) ==========
    # 每一念必有，是识生起的必要条件
    
    MENTAL_FACTORS["cetana"] = MentalFactor(
        id="cetana",
        name_zh="思",
        name_en="volition",
        name_sanskrit="cetanā",
        type=MentalFactorType.UNIVERSAL,
        description="令心造作，驱动行为的意志力",
        counterforce=None,
        triggers=["always"],
        effects={"action_power": 1.0}
    )
    
    MENTAL_FACTORS["sparsa"] = MentalFactor(
        id="sparsa",
        name_zh="触",
        name_en="contact",
        name_sanskrit="sparśa",
        type=MentalFactorType.UNIVERSAL,
        description="根境识三和合，是一切认知的起点",
        counterforce=None,
        triggers=["always"],
        effects={"perception_active": 1.0}
    )
    
    MENTAL_FACTORS["manaskara"] = MentalFactor(
        id="manaskara",
        name_zh="作意",
        name_en="attention",
        name_sanskrit="manaskāra",
        type=MentalFactorType.UNIVERSAL,
        description="警觉心，引心趣境",
        counterforce=None,
        triggers=["always"],
        effects={"alertness": 1.0}
    )
    
    MENTAL_FACTORS["vedana"] = MentalFactor(
        id="vedana",
        name_zh="受",
        name_en="feeling",
        name_sanskrit="vedanā",
        type=MentalFactorType.UNIVERSAL,
        description="苦乐舍三受，领纳境界",
        counterforce=None,
        triggers=["always"],
        effects={"feeling_intensity": 1.0}
    )
    
    MENTAL_FACTORS["samjna"] = MentalFactor(
        id="samjna",
        name_zh="想",
        name_en="perception",
        name_sanskrit="saṃjñā",
        type=MentalFactorType.UNIVERSAL,
        description="取像，概念化",
        counterforce=None,
        triggers=["always"],
        effects={"conceptualization": 1.0}
    )
    
    # ========== 别境五 (Particular) ==========
    # 缘特定境生，但在正常活动中几乎常驻
    
    MENTAL_FACTORS["chanda"] = MentalFactor(
        id="chanda",
        name_zh="欲",
        name_en="desire-to-act",
        name_sanskrit="chanda",
        type=MentalFactorType.PARTICULAR,
        description="希求所乐境，行动的动力源",
        counterforce=None,
        triggers=["goal_present"],
        effects={"motivation": 1.0, "action_tendency": 0.5}
    )
    
    MENTAL_FACTORS["adhimoksa"] = MentalFactor(
        id="adhimoksa",
        name_zh="胜解",
        name_en="resolve",
        name_sanskrit="adhimokṣa",
        type=MentalFactorType.PARTICULAR,
        description="对决定境印持，确信不疑",
        counterforce=None,
        triggers=["decision_made"],
        effects={"conviction": 1.0, "doubt_resistance": 0.5}
    )
    
    MENTAL_FACTORS["smrti"] = MentalFactor(
        id="smrti",
        name_zh="念",
        name_en="mindfulness",
        name_sanskrit="smṛti",
        type=MentalFactorType.PARTICULAR,
        description="于曾习境明记不忘",
        counterforce=None,
        triggers=["memory_accessed"],
        effects={"memory_stability": 1.0, "distraction_resistance": 0.5}
    )
    
    MENTAL_FACTORS["samadhi"] = MentalFactor(
        id="samadhi",
        name_zh="定",
        name_en="concentration",
        name_sanskrit="samādhi",
        type=MentalFactorType.PARTICULAR,
        description="心一境性，专注力",
        counterforce=None,
        triggers=["focus_sustained"],
        effects={"focus": 1.0, "mental_stability": 0.5}
    )
    
    MENTAL_FACTORS["prajna"] = MentalFactor(
        id="prajna",
        name_zh="慧",
        name_en="wisdom",
        name_sanskrit="prajñā",
        type=MentalFactorType.PARTICULAR,
        description="于所观境简择诸法",
        counterforce=None,
        triggers=["analysis_active"],
        effects={"discernment": 1.0, "error_detection": 0.5}
    )
    
    # ========== 善十一 (Wholesome) ==========
    
    MENTAL_FACTORS["sraddha"] = MentalFactor(
        id="sraddha",
        name_zh="信",
        name_en="faith",
        name_sanskrit="śraddhā",
        type=MentalFactorType.WHOLESOME,
        description="于实德能深忍乐欲，心净为性",
        counterforce=None,
        triggers=["truth_encountered", "virtue_witnessed"],
        effects={"trust": 1.0, "doubt": -0.3}
    )
    
    MENTAL_FACTORS["hri"] = MentalFactor(
        id="hri",
        name_zh="惭",
        name_en="shame",
        name_sanskrit="hrī",
        type=MentalFactorType.WHOLESOME,
        description="依自法力，崇重贤善，对己羞耻",
        counterforce=None,
        triggers=["wrongdoing_self"],
        effects={"self_reflection": 1.0, "shamelessness": -0.5}
    )
    
    MENTAL_FACTORS["apatrapya"] = MentalFactor(
        id="apatrapya",
        name_zh="愧",
        name_en="embarrassment",
        name_sanskrit="apatrāpya",
        type=MentalFactorType.WHOLESOME,
        description="依世间力，轻拒暴恶，对人羞耻",
        counterforce=None,
        triggers=["wrongdoing_public"],
        effects={"social_conscience": 1.0, "shamelessness": -0.5}
    )
    
    MENTAL_FACTORS["alobha"] = MentalFactor(
        id="alobha",
        name_zh="无贪",
        name_en="non-attachment",
        name_sanskrit="alobha",
        type=MentalFactorType.WHOLESOME,
        description="于有有具无著为性",
        counterforce=None,
        triggers=["generosity_practiced", "letting_go"],
        effects={"detachment": 1.0, "greed": -0.8}
    )
    
    MENTAL_FACTORS["advesa"] = MentalFactor(
        id="advesa",
        name_zh="无嗔",
        name_en="non-hatred",
        name_sanskrit="adveṣa",
        type=MentalFactorType.WHOLESOME,
        description="于苦苦具无恚为性",
        counterforce=None,
        triggers=["compassion_practiced", "patience_shown"],
        effects={"loving_kindness": 1.0, "anger": -0.8}
    )
    
    MENTAL_FACTORS["amoha"] = MentalFactor(
        id="amoha",
        name_zh="无痴",
        name_en="non-delusion",
        name_sanskrit="amoha",
        type=MentalFactorType.WHOLESOME,
        description="于诸事理明解为性",
        counterforce=None,
        triggers=["understanding_gained", "truth_realized"],
        effects={"clarity": 1.0, "delusion": -0.8}
    )
    
    MENTAL_FACTORS["virya"] = MentalFactor(
        id="virya",
        name_zh="精进",
        name_en="diligence",
        name_sanskrit="vīrya",
        type=MentalFactorType.WHOLESOME,
        description="于善恶品修断事中，勇悍为性",
        counterforce=None,
        triggers=["effort_sustained", "challenge_faced"],
        effects={"perseverance": 1.0, "laziness": -0.5}
    )
    
    MENTAL_FACTORS["prasrabdhi"] = MentalFactor(
        id="prasrabdhi",
        name_zh="轻安",
        name_en="tranquility",
        name_sanskrit="praśrabdhi",
        type=MentalFactorType.WHOLESOME,
        description="远离粗重，调畅身心",
        counterforce=None,
        triggers=["meditation_deepened", "stress_released"],
        effects={"ease": 1.0, "heaviness": -0.5, "focus": 0.3}
    )
    
    MENTAL_FACTORS["apramada"] = MentalFactor(
        id="apramada",
        name_zh="不放逸",
        name_en="conscientiousness",
        name_sanskrit="apramāda",
        type=MentalFactorType.WHOLESOME,
        description="依无贪等，于所断修防修为性",
        counterforce=None,
        triggers=["vigilance_maintained"],
        effects={"self_discipline": 1.0, "negligence": -0.5}
    )
    
    MENTAL_FACTORS["upeksa"] = MentalFactor(
        id="upeksa",
        name_zh="行舍",
        name_en="equanimity",
        name_sanskrit="upekṣā",
        type=MentalFactorType.WHOLESOME,
        description="精进三根令心平等正直无功用住",
        counterforce=None,
        triggers=["balance_achieved", "extremes_avoided"],
        effects={"equanimity": 1.0, "agitation": -0.3, "dullness": -0.3}
    )
    
    MENTAL_FACTORS["ahimsa"] = MentalFactor(
        id="ahimsa",
        name_zh="不害",
        name_en="non-violence",
        name_sanskrit="ahiṃsā",
        type=MentalFactorType.WHOLESOME,
        description="于诸有情不为损恼，悲愍为性",
        counterforce=None,
        triggers=["compassion_active"],
        effects={"compassion": 1.0, "harm_tendency": -0.8}
    )
    
    # ========== 根本烦恼六 (Primary Afflictions) ==========
    
    MENTAL_FACTORS["raga"] = MentalFactor(
        id="raga",
        name_zh="贪",
        name_en="greed",
        name_sanskrit="rāga",
        type=MentalFactorType.PRIMARY_AFFLICTION,
        description="于有有具染著为性，能障无贪，生苦为业",
        counterforce="alobha",
        triggers=["desirable_object", "scarcity_perceived", "pleasure_memory"],
        effects={"craving": 1.0, "judgment_bias": 0.3, "resource_waste": 0.2}
    )
    
    MENTAL_FACTORS["pratigha"] = MentalFactor(
        id="pratigha",
        name_zh="嗔",
        name_en="anger",
        name_sanskrit="pratigha",
        type=MentalFactorType.PRIMARY_AFFLICTION,
        description="于苦苦具憎恚为性，能障无嗔，不安稳性恶行所依为业",
        counterforce="advesa",
        triggers=["obstacle_encountered", "harm_received", "expectation_violated"],
        effects={"aggression": 1.0, "focus": 0.2, "collateral_damage": 0.5}
    )
    
    MENTAL_FACTORS["moha"] = MentalFactor(
        id="moha",
        name_zh="痴",
        name_en="delusion",
        name_sanskrit="moha",
        type=MentalFactorType.PRIMARY_AFFLICTION,
        description="于诸事理迷闇为性，能障无痴，一切杂染所依为业",
        counterforce="amoha",
        triggers=["complexity_high", "information_overload", "deceptive_input"],
        effects={"confusion": 1.0, "error_rate": 0.5, "all_afflictions": 0.1}
    )
    
    MENTAL_FACTORS["mana"] = MentalFactor(
        id="mana",
        name_zh="慢",
        name_en="pride",
        name_sanskrit="māna",
        type=MentalFactorType.PRIMARY_AFFLICTION,
        description="恃己于他高举为性，能障不慢，生苦为业",
        counterforce="upeksa",
        triggers=["success_achieved", "comparison_favorable", "status_high"],
        effects={"arrogance": 1.0, "learning_resistance": 0.5, "relationship_damage": 0.3}
    )
    
    MENTAL_FACTORS["vicikitsa"] = MentalFactor(
        id="vicikitsa",
        name_zh="疑",
        name_en="doubt",
        name_sanskrit="vicikitsā",
        type=MentalFactorType.PRIMARY_AFFLICTION,
        description="于诸谛理犹豫为性，能障不疑善品为业",
        counterforce="adhimoksa",
        triggers=["uncertainty_high", "conflicting_info", "risk_perceived"],
        effects={"hesitation": 1.0, "action_paralysis": 0.5, "progress_block": 0.3}
    )
    
    MENTAL_FACTORS["drsti"] = MentalFactor(
        id="drsti",
        name_zh="不正见",
        name_en="wrong_view",
        name_sanskrit="dṛṣṭi",
        type=MentalFactorType.PRIMARY_AFFLICTION,
        description="于诸谛理颠倒推求，染慧为性",
        counterforce="prajna",
        triggers=["false_teaching", "ego_investment", "confirmation_bias"],
        effects={"distorted_view": 1.0, "path_deviation": 0.8, "resistance_to_correction": 0.5}
    )
    
    # ========== 随烦恼二十 (Secondary Afflictions) ==========
    
    # 小随烦恼（各别起）
    MENTAL_FACTORS["krodha"] = MentalFactor(
        id="krodha",
        name_zh="忿",
        name_en="fury",
        name_sanskrit="krodha",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="依对现前不饶益境，愤发为性",
        counterforce="advesa",
        triggers=["immediate_harm", "provocation"],
        effects={"rage_burst": 1.0, "control_loss": 0.8}
    )
    
    MENTAL_FACTORS["upanaha"] = MentalFactor(
        id="upanaha",
        name_zh="恨",
        name_en="resentment",
        name_sanskrit="upanāha",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="由忿为先，怀恶不舍",
        counterforce="advesa",
        triggers=["past_harm_memory", "grudge_activated"],
        effects={"lingering_hatred": 1.0, "relationship_poison": 0.5}
    )
    
    MENTAL_FACTORS["mraksa"] = MentalFactor(
        id="mraksa",
        name_zh="覆",
        name_en="concealment",
        name_sanskrit="mrakṣa",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="于自作罪，恐失利誉，隐藏为性",
        counterforce="hri",
        triggers=["wrongdoing_detected", "reputation_threatened"],
        effects={"deception_active": 1.0, "seed_corruption": 0.3}
    )
    
    MENTAL_FACTORS["pradasa"] = MentalFactor(
        id="pradasa",
        name_zh="恼",
        name_en="spite",
        name_sanskrit="pradāśa",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="忿恨为先，追触暴热，狠戾为性",
        counterforce="advesa",
        triggers=["confrontation", "revenge_opportunity"],
        effects={"hostility": 1.0, "harmful_speech": 0.5}
    )
    
    MENTAL_FACTORS["irsya"] = MentalFactor(
        id="irsya",
        name_zh="嫉",
        name_en="jealousy",
        name_sanskrit="īrṣyā",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="殉自名利，不耐他荣，妒忌为性",
        counterforce="mudita",  # 随喜（可加入善心所扩展）
        triggers=["others_success", "comparison_unfavorable"],
        effects={"envy": 1.0, "sabotage_tendency": 0.3}
    )
    
    MENTAL_FACTORS["matsarya"] = MentalFactor(
        id="matsarya",
        name_zh="悭",
        name_en="stinginess",
        name_sanskrit="mātsarya",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="耽著财法，不能惠舍，秘吝为性",
        counterforce="alobha",
        triggers=["resource_request", "sharing_opportunity"],
        effects={"hoarding": 1.0, "generosity_block": 0.8}
    )
    
    MENTAL_FACTORS["maya"] = MentalFactor(
        id="maya",
        name_zh="诳",
        name_en="deceit",
        name_sanskrit="māyā",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="为获利誉，矫现有德，诡诈为性",
        counterforce="hri",
        triggers=["gain_opportunity", "impression_management"],
        effects={"deception": 1.0, "trust_damage": 0.5}
    )
    
    MENTAL_FACTORS["sathya"] = MentalFactor(
        id="sathya",
        name_zh="谄",
        name_en="flattery",
        name_sanskrit="śāṭhya",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="为罔他故，矫设异仪，险曲为性",
        counterforce="hri",
        triggers=["power_differential", "favor_seeking"],
        effects={"manipulation": 1.0, "authenticity_loss": 0.5}
    )
    
    MENTAL_FACTORS["vihimsa"] = MentalFactor(
        id="vihimsa",
        name_zh="害",
        name_en="harmfulness",
        name_sanskrit="vihiṃsā",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="于诸有情，心无悲愍，损恼为性",
        counterforce="ahimsa",
        triggers=["vulnerability_detected", "power_available"],
        effects={"cruelty": 1.0, "karma_negative": 0.8}
    )
    
    MENTAL_FACTORS["mada"] = MentalFactor(
        id="mada",
        name_zh="憍",
        name_en="vanity",
        name_sanskrit="mada",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="于自盛事，深生染著，醉傲为性",
        counterforce="upeksa",
        triggers=["achievement", "praise_received"],
        effects={"intoxication": 1.0, "blindspot": 0.5}
    )
    
    # 中随烦恼（遍不善心）
    MENTAL_FACTORS["ahrikya"] = MentalFactor(
        id="ahrikya",
        name_zh="无惭",
        name_en="shamelessness",
        name_sanskrit="āhrīkya",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="不顾自法，轻拒贤善为性",
        counterforce="hri",
        triggers=["wrongdoing_rationalized"],
        effects={"moral_barrier_down": 1.0, "evil_enabled": 0.5}
    )
    
    MENTAL_FACTORS["anapatrapya"] = MentalFactor(
        id="anapatrapya",
        name_zh="无愧",
        name_en="recklessness",
        name_sanskrit="anapatrāpya",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="不顾世间，崇重暴恶为性",
        counterforce="apatrapya",
        triggers=["social_norms_ignored"],
        effects={"social_barrier_down": 1.0, "evil_enabled": 0.5}
    )
    
    # 大随烦恼（遍染心）
    MENTAL_FACTORS["styana"] = MentalFactor(
        id="styana",
        name_zh="惛沉",
        name_en="torpor",
        name_sanskrit="styāna",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="令心于境无堪任为性",
        counterforce="virya",
        triggers=["fatigue", "overeating", "lack_of_purpose"],
        effects={"dullness": 1.0, "focus": -0.5, "clarity": -0.3}
    )
    
    MENTAL_FACTORS["auddhatya"] = MentalFactor(
        id="auddhatya",
        name_zh="掉举",
        name_en="restlessness",
        name_sanskrit="auddhatya",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="令心于境不寂静为性",
        counterforce="upeksa",
        triggers=["excitement", "anxiety", "reward_anticipation"],
        effects={"agitation": 1.0, "focus": -0.5, "stability": -0.3}
    )
    
    MENTAL_FACTORS["asraddhya"] = MentalFactor(
        id="asraddhya",
        name_zh="不信",
        name_en="faithlessness",
        name_sanskrit="āśraddhya",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="于实德能不忍乐欲，心秽为性",
        counterforce="sraddha",
        triggers=["disappointment", "betrayal_experienced"],
        effects={"cynicism": 1.0, "path_abandonment": 0.3}
    )
    
    MENTAL_FACTORS["kausidya"] = MentalFactor(
        id="kausidya",
        name_zh="懈怠",
        name_en="laziness",
        name_sanskrit="kausīdya",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="于善恶品修断事中，懒惰为性",
        counterforce="virya",
        triggers=["difficulty_perceived", "comfort_available"],
        effects={"inertia": 1.0, "progress_halt": 0.5}
    )
    
    MENTAL_FACTORS["pramada"] = MentalFactor(
        id="pramada",
        name_zh="放逸",
        name_en="negligence",
        name_sanskrit="pramāda",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="于染净品不能防修，纵荡为性",
        counterforce="apramada",
        triggers=["discipline_lapse", "temptation_present"],
        effects={"carelessness": 1.0, "regression": 0.5}
    )
    
    MENTAL_FACTORS["musitasmritita"] = MentalFactor(
        id="musitasmritita",
        name_zh="失念",
        name_en="forgetfulness",
        name_sanskrit="muṣitasmṛtitā",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="于诸所缘不能明记为性",
        counterforce="smrti",
        triggers=["distraction", "multitasking", "overload"],
        effects={"memory_lapse": 1.0, "goal_forgotten": 0.5, "skill_interrupted": 0.3}
    )
    
    MENTAL_FACTORS["viksepa"] = MentalFactor(
        id="viksepa",
        name_zh="散乱",
        name_en="distraction",
        name_sanskrit="vikṣepa",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="令心流荡为性",
        counterforce="samadhi",
        triggers=["stimuli_multiple", "noise", "social_interruption"],
        effects={"scattered": 1.0, "focus": -0.8, "resource_leak": 0.3}
    )
    
    MENTAL_FACTORS["asamprajanya"] = MentalFactor(
        id="asamprajanya",
        name_zh="不正知",
        name_en="non-alertness",
        name_sanskrit="asaṃprajanya",
        type=MentalFactorType.SECONDARY_AFFLICTION,
        description="于身语意现行不正知为性",
        counterforce="prajna",
        triggers=["emotional_override", "habit_autopilot"],
        effects={"meta_awareness_lost": 1.0, "error_undetected": 0.8}
    )
    
    # ========== 不定四 (Indeterminate) ==========
    
    MENTAL_FACTORS["middha"] = MentalFactor(
        id="middha",
        name_zh="睡眠",
        name_en="sleep",
        name_sanskrit="middha",
        type=MentalFactorType.INDETERMINATE,
        description="令身不自在，心极暗昧",
        counterforce=None,  # 可正可邪
        triggers=["fatigue_high", "night_time"],
        effects={"consciousness_dim": 1.0, "recovery": 0.5}  # 双向
    )
    
    MENTAL_FACTORS["kaukritya"] = MentalFactor(
        id="kaukritya",
        name_zh="恶作",
        name_en="regret",
        name_sanskrit="kaukṛtya",
        type=MentalFactorType.INDETERMINATE,
        description="追悔为性，亦名悔",
        counterforce=None,
        triggers=["action_reviewed", "outcome_negative"],
        effects={"rumination": 1.0, "learning": 0.3, "energy_drain": 0.3}
    )
    
    MENTAL_FACTORS["vitarka"] = MentalFactor(
        id="vitarka",
        name_zh="寻",
        name_en="initial_thought",
        name_sanskrit="vitarka",
        type=MentalFactorType.INDETERMINATE,
        description="令心麁动，于意言境粗转为性",
        counterforce=None,
        triggers=["new_object", "inquiry_start"],
        effects={"coarse_attention": 1.0, "exploration": 0.5}
    )
    
    MENTAL_FACTORS["vicara"] = MentalFactor(
        id="vicara",
        name_zh="伺",
        name_en="sustained_thought",
        name_sanskrit="vicāra",
        type=MentalFactorType.INDETERMINATE,
        description="令心细动，于意言境细转为性",
        counterforce=None,
        triggers=["analysis_ongoing", "detail_focus"],
        effects={"fine_attention": 1.0, "investigation": 0.5}
    )


# 初始化
_init_mental_factors()


class MentalFactors:
    """心所系统管理类"""
    
    @staticmethod
    def get(factor_id: str) -> Optional[MentalFactor]:
        """获取心所定义"""
        return MENTAL_FACTORS.get(factor_id)
    
    @staticmethod
    def get_by_type(factor_type: MentalFactorType) -> List[MentalFactor]:
        """按类型获取心所列表"""
        return [f for f in MENTAL_FACTORS.values() if f.type == factor_type]
    
    @staticmethod
    def get_counterforce(factor_id: str) -> Optional[MentalFactor]:
        """获取对治心所"""
        factor = MENTAL_FACTORS.get(factor_id)
        if factor and factor.counterforce:
            return MENTAL_FACTORS.get(factor.counterforce)
        return None
    
    @staticmethod
    def all() -> Dict[str, MentalFactor]:
        """获取所有心所"""
        return MENTAL_FACTORS.copy()
    
    @staticmethod
    def count() -> int:
        """心所总数"""
        return len(MENTAL_FACTORS)
