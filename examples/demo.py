#!/usr/bin/env python3
"""
Dharma Game Engine 示例

演示 种子-熏习-现行 的游戏循环
"""

import sys
sys.path.insert(0, '..')

from dharma_engine import DharmaEngine, Scene, MentalFactors, MentalFactorType
from dharma_engine.scene import get_scene, list_scenes
from dharma_engine.engine import create_character, PREDEFINED_ACTIONS


def print_separator(title: str = ""):
    print("\n" + "=" * 50)
    if title:
        print(f"  {title}")
        print("=" * 50)


def demo_basic():
    """基础演示"""
    print_separator("基础演示：创建角色并进入场景")
    
    # 创建一个中性角色
    engine = create_character("neutral")
    print(f"创建角色: {engine}")
    
    # 进入市集场景
    market = get_scene("market")
    print(f"\n进入场景: {market}")
    
    # 计算心所现行
    manifest = engine.calculate_manifest(market)
    print(f"\n当前心所现行: {manifest}")
    
    # 显示激活的烦恼
    afflictions = manifest.get_active_by_type(MentalFactorType.PRIMARY_AFFLICTION)
    if afflictions:
        print(f"激活的根本烦恼: {afflictions}")
    
    return engine


def demo_action_and_training():
    """行为与熏习演示"""
    print_separator("行为与熏习演示")
    
    # 创建一个贪欲重的角色
    engine = create_character("passionate")
    print(f"创建角色（贪欲重）: {engine}")
    print(f"初始贪种子权重: {engine.seed_bank.get_weight('raga'):.3f}")
    print(f"初始无贪种子权重: {engine.seed_bank.get_weight('alobha'):.3f}")
    
    # 在市集场景中
    market = get_scene("market")
    manifest = engine.calculate_manifest(market)
    print(f"\n进入市集后: {manifest}")
    
    # 执行布施（对治贪）
    print("\n执行行为: 布施")
    changes = engine.perform_action("布施", intensity=0.8)
    print(f"种子变化: {changes}")
    
    # 时间前进
    engine.tick()
    
    # 再次检查
    print(f"\n布施后贪种子权重: {engine.seed_bank.get_weight('raga'):.3f}")
    print(f"布施后无贪种子权重: {engine.seed_bank.get_weight('alobha'):.3f}")
    
    # 重复布施多次
    print("\n连续布施10次...")
    for i in range(10):
        engine.perform_action("布施", intensity=0.5)
        engine.tick()
    
    print(f"多次布施后贪种子权重: {engine.seed_bank.get_weight('raga'):.3f}")
    print(f"多次布施后无贪种子权重: {engine.seed_bank.get_weight('alobha'):.3f}")
    
    return engine


def demo_meditation():
    """禅修演示"""
    print_separator("禅修演示：从散乱到定")
    
    engine = create_character("neutral")
    
    # 初始状态
    print(f"初始定种子: {engine.seed_bank.get_weight('samadhi'):.3f}")
    print(f"初始散乱种子: {engine.seed_bank.get_weight('viksepa'):.3f}")
    print(f"初始掉举种子: {engine.seed_bank.get_weight('auddhatya'):.3f}")
    
    # 进入禅堂
    meditation_hall = get_scene("meditation_hall")
    print(f"\n进入禅堂: {meditation_hall}")
    
    # 修禅定
    print("\n开始禅修（20个时间单位）...")
    for i in range(20):
        # 每个时间单位
        manifest = engine.calculate_manifest(meditation_hall)
        
        # 检查是否有散乱/掉举现行
        if manifest.is_active("viksepa") or manifest.is_active("auddhatya"):
            # 需要对治
            engine.perform_action("正念", intensity=0.5)
        
        # 主修禅定
        engine.perform_action("禅定", intensity=0.7)
        engine.tick()
        
        if (i + 1) % 5 == 0:
            print(f"  第{i+1}轮: 定={engine.seed_bank.get_weight('samadhi'):.3f}, "
                  f"散乱={engine.seed_bank.get_weight('viksepa'):.3f}")
    
    print(f"\n禅修后定种子: {engine.seed_bank.get_weight('samadhi'):.3f}")
    print(f"禅修后散乱种子: {engine.seed_bank.get_weight('viksepa'):.3f}")
    print(f"禅修后轻安种子: {engine.seed_bank.get_weight('prasrabdhi'):.3f}")
    
    return engine


def demo_affliction_battle():
    """烦恼对治演示"""
    print_separator("烦恼对治演示：在战场中保持无嗔")
    
    # 创建一个嗔心重的角色
    engine = create_character("angry")
    print(f"创建角色（嗔心重）: {engine}")
    
    # 进入战场
    battlefield = get_scene("battlefield")
    print(f"\n进入战场: {battlefield}")
    
    # 战斗10轮
    print("\n开始战斗...")
    for i in range(10):
        manifest = engine.calculate_manifest(battlefield)
        
        # 检查嗔是否现行
        if manifest.is_active("pratigha"):
            anger_level = manifest.active_factors.get("pratigha", 0)
            print(f"  第{i+1}轮: 嗔现行! 强度={anger_level:.2f}")
            
            # 尝试用慈心对治
            if anger_level > 0.6:
                print(f"         -> 修慈心对治")
                engine.perform_action("慈心", intensity=0.8)
            else:
                engine.perform_action("忍辱", intensity=0.6)
        else:
            print(f"  第{i+1}轮: 保持平静")
        
        engine.tick()
    
    print(f"\n战斗后嗔种子: {engine.seed_bank.get_weight('pratigha'):.3f}")
    print(f"战斗后无嗔种子: {engine.seed_bank.get_weight('advesa'):.3f}")
    print(f"战斗后忿种子: {engine.seed_bank.get_weight('krodha'):.3f}")
    
    return engine


def demo_mental_factors_info():
    """心所信息演示"""
    print_separator("五十一心所概览")
    
    for factor_type in MentalFactorType:
        factors = MentalFactors.get_by_type(factor_type)
        print(f"\n{factor_type.value} ({len(factors)}个):")
        for f in factors:
            counter = ""
            if f.counterforce:
                cf = MentalFactors.get(f.counterforce)
                if cf:
                    counter = f" [对治: {cf.name_zh}]"
            print(f"  - {f.name_zh} ({f.name_en}){counter}")


def main():
    print("=" * 60)
    print("  Dharma Game Engine 演示")
    print("  基于唯识学的游戏心理系统")
    print("=" * 60)
    
    # 运行演示
    demo_mental_factors_info()
    demo_basic()
    demo_action_and_training()
    demo_meditation()
    demo_affliction_battle()
    
    print_separator("演示完成")
    print("\n可用的预定义行为:")
    for action_name in PREDEFINED_ACTIONS:
        print(f"  - {action_name}")
    
    print("\n可用的预定义场景:")
    for scene_name in list_scenes():
        print(f"  - {scene_name}")


if __name__ == "__main__":
    main()
