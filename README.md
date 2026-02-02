# Dharma Game Engine

基于唯识学"种子-熏习-现行"理论的游戏心理系统引擎。

## 核心概念

### 三层状态模型

```
┌─────────────────────────────────────┐
│         现行层 (Manifest)            │
│   当前激活的心所状态 (buff/debuff)    │
├─────────────────────────────────────┤
│         熏习层 (Update)              │
│   行为→种子权重的更新规则             │
├─────────────────────────────────────┤
│         种子层 (Seed Bank)           │
│   长期潜在倾向 (权重向量)             │
└─────────────────────────────────────┘
```

### 核心公式

现行概率计算：

```
P(现行_i) = sigmoid(a × Seed_i + b × Condition_i - c × Counterforce_i)
```

其中：
- `Seed_i`: 种子权重 ∈ [0, 1]
- `Condition_i`: 场景/缘的影响系数
- `Counterforce_i`: 对治力量

### 五十一心所分类

| 类别 | 数量 | 系统角色 |
|-----|------|---------|
| 遍行 | 5 | 内核进程（必有） |
| 别境 | 5 | 核心应用（常驻） |
| 善 | 11 | 正向buff |
| 根本烦恼 | 6 | 核心debuff |
| 随烦恼 | 20 | 衍生debuff |
| 不定 | 4 | 双向可用 |

## 使用

```python
from dharma_engine import DharmaEngine, Scene

# 创建引擎
engine = DharmaEngine()

# 创建场景（带缘矩阵）
scene = Scene("诱惑之境", {
    "贪": 0.8,
    "痴": 0.3,
    "念": -0.2  # 此场景让正念更难升起
})

# 计算当前心所现行
manifest = engine.calculate_manifest(scene)

# 执行行为并熏习
engine.perform_action("布施", intensity=0.7)

# 应用对治
engine.apply_counterforce("无贪", target="贪")
```

## 佛学依据

- 《成唯识论》：八识、种子六义、熏习四义
- 《瑜伽师地论》：五十一心所、修行次第
- 《俱舍论》：七十五法体系

## License

MIT
