"""
场景 (Scene) - 缘矩阵

场景定义了当前环境对各种心所现行的影响
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Scene:
    """
    场景定义
    
    每个场景有一个"缘矩阵"，决定哪些种子更容易现行
    """
    name: str                           # 场景名称
    conditions: Dict[str, float]        # 缘矩阵：心所ID → 影响系数
    description: str = ""               # 场景描述
    triggers: List[str] = field(default_factory=list)  # 场景会触发的事件
    duration: int = -1                  # 持续时间（-1表示无限）
    
    def get_condition(self, factor_id: str) -> float:
        """获取场景对某心所的影响系数"""
        return self.conditions.get(factor_id, 0.0)
    
    def __repr__(self) -> str:
        cond_str = ", ".join([f"{k}:{v:+.1f}" for k, v in self.conditions.items()])
        return f"Scene({self.name}, [{cond_str}])"


# 预定义场景
PREDEFINED_SCENES: Dict[str, Scene] = {}


def _init_scenes():
    """初始化预定义场景"""
    global PREDEFINED_SCENES
    
    PREDEFINED_SCENES["market"] = Scene(
        name="繁华市集",
        description="商品琳琅满目，人声鼎沸，各种欲望的诱惑",
        conditions={
            "raga": 0.6,       # 贪：强烈触发
            "chanda": 0.4,     # 欲：增强
            "viksepa": 0.3,    # 散乱：增加
            "samadhi": -0.3,   # 定：难以维持
            "alobha": -0.2,    # 无贪：更难升起
        },
        triggers=["desirable_object", "scarcity_perceived"]
    )
    
    PREDEFINED_SCENES["battlefield"] = Scene(
        name="战场",
        description="刀光剑影，生死一线，愤怒与恐惧交织",
        conditions={
            "pratigha": 0.7,   # 嗔：强烈触发
            "krodha": 0.5,     # 忿：容易爆发
            "virya": 0.4,      # 精进：被激发
            "auddhatya": 0.4,  # 掉举：心难静
            "advesa": -0.4,    # 无嗔：很难保持
            "prasrabdhi": -0.5, # 轻安：几乎不可能
        },
        triggers=["harm_received", "obstacle_encountered"]
    )
    
    PREDEFINED_SCENES["meditation_hall"] = Scene(
        name="禅堂",
        description="清净庄严，香烟袅袅，适合收摄身心",
        conditions={
            "samadhi": 0.5,    # 定：有利
            "prasrabdhi": 0.4, # 轻安：容易升起
            "smrti": 0.3,      # 念：增强
            "viksepa": -0.4,   # 散乱：减少
            "auddhatya": -0.3, # 掉举：减少
            "raga": -0.2,      # 贪：减弱
        },
        triggers=["meditation_deepened", "focus_sustained"]
    )
    
    PREDEFINED_SCENES["deceptive_realm"] = Scene(
        name="幻惑之境",
        description="真假难辨，迷雾重重，充满欺骗与幻象",
        conditions={
            "moha": 0.7,       # 痴：强烈触发
            "drsti": 0.4,      # 不正见：容易生起
            "vicikitsa": 0.5,  # 疑：增加
            "prajna": -0.4,    # 慧：难以发挥
            "adhimoksa": -0.3, # 胜解：难以确定
        },
        triggers=["complexity_high", "deceptive_input"]
    )
    
    PREDEFINED_SCENES["competition"] = Scene(
        name="竞技场",
        description="高手如云，胜负分明，名利得失系于一念",
        conditions={
            "mana": 0.5,       # 慢：容易升起
            "irsya": 0.4,      # 嫉：看到他人成功时
            "virya": 0.4,      # 精进：被激发
            "vicikitsa": 0.2,  # 疑：压力下的犹豫
            "upeksa": -0.4,    # 行舍：难保平衡
        },
        triggers=["comparison_favorable", "comparison_unfavorable", "success_achieved"]
    )
    
    PREDEFINED_SCENES["solitude"] = Scene(
        name="独处",
        description="远离人群，只有自己面对内心",
        conditions={
            "kaukritya": 0.3,  # 恶作：容易回忆过去
            "styana": 0.2,    # 惛沉：可能无聊
            "vicara": 0.3,     # 伺：内省增加
            "viksepa": -0.4,   # 散乱：外缘减少
            "sathya": -0.5,    # 谄：无需讨好
        },
        triggers=["action_reviewed", "memory_accessed"]
    )
    
    PREDEFINED_SCENES["teaching"] = Scene(
        name="闻法道场",
        description="善知识说法，正理开显",
        conditions={
            "sraddha": 0.4,    # 信：增强
            "prajna": 0.5,     # 慧：有利于发展
            "amoha": 0.3,      # 无痴：正见熏习
            "drsti": -0.4,     # 不正见：被对治
            "moha": -0.3,      # 痴：减弱
            "asraddhya": -0.3, # 不信：减弱
        },
        triggers=["truth_encountered", "understanding_gained"]
    )
    
    PREDEFINED_SCENES["suffering"] = Scene(
        name="苦难",
        description="身心受苦，逆境现前",
        conditions={
            "pratigha": 0.4,   # 嗔：对苦的抗拒
            "vicikitsa": 0.3,  # 疑：为什么是我
            "kausidya": 0.3,   # 懈怠：想放弃
            "virya": -0.2,     # 精进：可能被消磨
            # 但也可能激发...
            "sraddha": 0.1,    # 信：求出离
            "hri": 0.2,        # 惭：反省
        },
        triggers=["obstacle_encountered", "harm_received"]
    )


_init_scenes()


def get_scene(name: str) -> Optional[Scene]:
    """获取预定义场景"""
    return PREDEFINED_SCENES.get(name)


def list_scenes() -> List[str]:
    """列出所有预定义场景"""
    return list(PREDEFINED_SCENES.keys())
