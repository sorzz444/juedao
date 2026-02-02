#!/usr/bin/env python3
"""
Dharma Game Engine V2 演示

五层架构：
1. 遍行五 - 事件管线
2. 别境五 - 中性能力条
3. 种子库 - 潜伏层
4. 现行层 - 当前buff/debuff
5. 不定四 - 可正可邪工具
"""

import sys
sys.path.insert(0, '..')

from dharma_engine import (
    DharmaEngineV2, create_character_v2,
    Scene, MentalFactors, MentalFactorType,
    detect_pattern
)
from dharma_engine.scene import get_scene, list_scenes
from dharma_engine.particular import CAPABILITY_PATTERNS


def print_separator(title: str = ""):
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)


def demo_five_layers():
    """五层架构演示"""
    print_separator("五层架构演示")
    
    # 创建修行者角色
    engine = create_character_v2("修行者")
    print(f"创建角色: {engine}")
    
    # 进入禅堂场景
    meditation_hall = get_scene("meditation_hall")
    print(f"\n进入场景: {meditation_hall}")
    
    # 更新现行层
    manifest = engine.update_manifest(meditation_hall)
    
    # 显示完整状态
    print("\n【第一层：遍行五管线】")
    print("  (底层事件处理，不直接显示)")
    
    print("\n【第二层：别境五能力条】")
    for cap_id, info in engine.particular.get_status().items():
        print(f"  {info['name']}: {info['effective']:.2f} ({info['direction']}) {info['description']}")
    
    print("\n【第三层：种子库（潜伏层）】")
    print(f"  主要烦恼种子: {engine.seed_bank.get_dominant_afflictions(3)}")
    print(f"  主要善种子: {engine.seed_bank.get_dominant_virtues(3)}")
    
    print("\n【第四层：现行层】")
    print(f"  善心所: {list(manifest.active_wholesome.keys())}")
    print(f"  烦恼: {list(manifest.active_afflictions.keys())}")
    print(f"  净善恶: {manifest.net_valence():.2f}")
    
    print("\n【第五层：不定四】")
    print(f"  睡眠={engine.indeterminate.sleep:.2f}, "
          f"悔={engine.indeterminate.regret:.2f}, "
          f"寻={engine.indeterminate.vitarka:.2f}, "
          f"伺={engine.indeterminate.vicara:.2f}")
    
    return engine


def demo_neutral_capability():
    """别境五中性能力演示"""
    print_separator("别境五中性能力演示：慧可正可邪")
    
    print("\n场景A：智者（慧高 + 无痴高）")
    wise = create_character_v2("智者")
    # 模拟正见环境
    wise.manifest.active_wholesome = {"amoha": 0.7, "sraddha": 0.6}
    wise.particular.update_direction("prajna", wise.manifest.get_all_active())
    effect, desc = wise.particular.get_combined_effect("prajna")
    print(f"  慧的状态: {desc}")
    print(f"  -> 效果: 洞察、破执、对治增强")
    
    print("\n场景B：邪智者（慧高 + 不正见高）")
    # 模拟不正见
    wise.manifest.active_afflictions = {"drsti": 0.7, "mana": 0.5}
    wise.manifest.active_wholesome = {}
    wise.particular.update_direction("prajna", wise.manifest.get_all_active())
    effect, desc = wise.particular.get_combined_effect("prajna")
    print(f"  慧的状态: {desc}")
    print(f"  -> 效果: 自圆其说，越聪明越难救")
    
    print("\n场景C：定也是中性（定高 + 惛沉）")
    engine = create_character_v2("修行者")
    engine.manifest.active_afflictions = {"styana": 0.7}
    engine.particular.check_disruption(engine.manifest.active_afflictions)
    effect, desc = engine.particular.get_combined_effect("samadhi")
    print(f"  定的状态: {desc}")
    print(f"  -> 这就是'昏沉定'：看似稳定，实则昏暗")


def demo_disruption():
    """能力打断演示"""
    print_separator("能力打断演示：烦恼如何破坏别境")
    
    engine = create_character_v2("修行者")
    print(f"初始状态: {engine.particular}")
    
    # 模拟进入高散乱场景
    print("\n进入高刺激场景，散乱和掉举升起...")
    engine.manifest.active_afflictions = {
        "viksepa": 0.8,    # 散乱
        "auddhatya": 0.7,  # 掉举
    }
    
    # 检查打断
    engine.particular.check_disruption(engine.manifest.active_afflictions)
    
    print("\n打断情况:")
    for cap_id, cap in engine.particular.capabilities.items():
        if cap.disrupted:
            print(f"  ❌ {cap.name_zh} 被 {cap.disruption_source} 打断!")
        else:
            print(f"  ✓ {cap.name_zh} 正常")
    
    print(f"\n打断后状态: {engine.particular}")


def demo_patterns():
    """能力模式检测演示"""
    print_separator("能力模式检测")
    
    print("\n预定义的能力模式:")
    for name, pattern in CAPABILITY_PATTERNS.items():
        print(f"\n  【{name}】")
        print(f"    条件: {pattern['required']}")
        if "forbidden" in pattern:
            print(f"    禁止: {pattern['forbidden']}")
        print(f"    效果: {pattern['effect']}")
    
    print("\n" + "-" * 40)
    print("实际检测:")
    
    # 创建不同角色检测
    for archetype in ["修行者", "凡夫", "智者", "贪者"]:
        engine = create_character_v2(archetype)
        engine.update_manifest()
        patterns = engine.manifest.active_patterns
        print(f"\n  {archetype}: {patterns if patterns else '无特殊模式'}")


def demo_training_session():
    """禅修训练演示"""
    print_separator("禅修训练：从散乱到定")
    
    engine = create_character_v2("凡夫")
    print(f"凡夫开始修行: {engine}")
    
    meditation_hall = get_scene("meditation_hall")
    
    print("\n初始别境状态:")
    print(f"  定: {engine.particular.get_strength('samadhi'):.3f}")
    print(f"  念: {engine.particular.get_strength('smrti'):.3f}")
    print(f"  慧: {engine.particular.get_strength('prajna'):.3f}")
    
    print("\n开始30天禅修...")
    for day in range(30):
        # 每天的修行
        engine.update_manifest(meditation_hall)
        
        # 检查是否有散乱/掉举，需要对治
        if engine.manifest.is_active("viksepa") or engine.manifest.is_active("auddhatya"):
            engine.perform_action("正念", intensity=0.6)
        
        # 主修禅定
        engine.perform_action("禅定", intensity=0.7)
        
        # 观察修
        if (day + 1) % 3 == 0:
            engine.perform_action("观察", intensity=0.5)
        
        engine.tick()
        
        if (day + 1) % 10 == 0:
            patterns = detect_pattern(engine.particular, engine.manifest.get_all_active())
            print(f"\n  第{day+1}天:")
            print(f"    定: {engine.particular.get_strength('samadhi'):.3f}")
            print(f"    念: {engine.particular.get_strength('smrti'):.3f}")
            print(f"    净善恶: {engine.manifest.net_valence():.2f}")
            if patterns:
                print(f"    达成模式: {patterns}")
    
    print("\n" + "-" * 40)
    print("【复盘】")
    print(engine.get_review())


def demo_affliction_battle():
    """烦恼对治战斗演示"""
    print_separator("战场考验：嗔者能否保持无嗔")
    
    engine = create_character_v2("嗔者")
    print(f"嗔者角色: {engine}")
    print(f"初始嗔种子: {engine.seed_bank.get_weight('pratigha'):.3f}")
    print(f"初始无嗔种子: {engine.seed_bank.get_weight('advesa'):.3f}")
    
    battlefield = get_scene("battlefield")
    print(f"\n进入战场: {battlefield}")
    
    print("\n战斗开始...")
    anger_outbursts = 0
    successful_counters = 0
    
    for round in range(15):
        engine.update_manifest(battlefield)
        
        # 检查嗔是否现行
        anger_strength = engine.manifest.get_strength("pratigha")
        fury_strength = engine.manifest.get_strength("krodha")
        
        total_anger = anger_strength + fury_strength
        
        if total_anger > 0.3:
            anger_outbursts += 1
            print(f"\n  第{round+1}回合: 嗔心爆发! (强度={total_anger:.2f})")
            
            # 尝试对治
            if engine.particular.get_strength("smrti") > 0.4:
                print(f"    -> 正念觉察，修慈心对治")
                engine.perform_action("慈心", intensity=0.8)
                successful_counters += 1
            else:
                print(f"    -> 失念，无法对治")
        else:
            print(f"  第{round+1}回合: 平静 (嗔={total_anger:.2f})")
        
        engine.tick()
    
    print("\n" + "-" * 40)
    print(f"战斗结束:")
    print(f"  嗔心爆发次数: {anger_outbursts}")
    print(f"  成功对治次数: {successful_counters}")
    print(f"  最终嗔种子: {engine.seed_bank.get_weight('pratigha'):.3f}")
    print(f"  最终无嗔种子: {engine.seed_bank.get_weight('advesa'):.3f}")
    
    print("\n【复盘】")
    print(engine.get_review())


def main():
    print("=" * 60)
    print("  Dharma Game Engine V2 演示")
    print("  唯识五层架构")
    print("=" * 60)
    
    demo_five_layers()
    demo_neutral_capability()
    demo_disruption()
    demo_patterns()
    demo_training_session()
    demo_affliction_battle()
    
    print_separator("演示完成")


if __name__ == "__main__":
    main()
