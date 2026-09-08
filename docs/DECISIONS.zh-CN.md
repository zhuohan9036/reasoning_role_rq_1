# 决策日志

> English: [DECISIONS.md](DECISIONS.md)

本文件区分已经确立的研究承诺、临时性的工作假设和未解决的选择。实现上的方便不等于
科学承诺。

## 已接受的决策

### D-001——RQ1 是刻画性问题

**状态：** 已接受
**决策：** 论文研究功能分化是否存在、它对应什么、稳定性如何，以及能泛化多远。
仅有 correlation、probing、clustering 或 representation similarity 时，不得描述为
因果证据。

### D-002——任务侧结构与模型侧结构必须保持区分

**状态：** 已接受
**决策：** Generator trace、dependency graph 和 candidate operation label 是外部任务
描述。在解释 correspondence 之前，必须独立测量模型侧模式。

### D-003——竞争解释始终保持有效

**状态：** 已接受
**决策：** structural-only、task-specific、cross-task reusable 和
implementation-mobile 等解释都必须接受检验。负结果与混合结果同样有效。

### D-004——主要证据来自冻结的预训练模型

**状态：** 已接受
**决策：** 主要结论依赖能够进行机制访问的冻结预训练 Transformer。训练或 adaptation
只能作为单独标记的诊断手段。

### D-005——物理 component identity 不定义 functional identity

**状态：** 已接受
**决策：** 可以测量固定的 head、MLP 或 layer index，但它们本身不能定义 reasoning
role。

### D-006——第一个实施任务是任务校准

**状态：** 已接受
**决策：** 第一个有边界的代码任务实现 canonical task-record schema、两个 pilot task
family 的 deterministic generator 和 reference solver、抗泄漏 split、manifest 与
validation test。它不加载 Transformer，也不实现模型侧分析。

### D-007——中间任务状态保留为隐藏 annotation

**状态：** 已接受
**决策：** Canonical record 可以保留任务侧中间状态，用于验证和未来 alignment 研究，
但默认 prompt 不得暴露它们。它们是 generator provenance，不是模型 chain of thought。

### D-008——Python 3.11 是项目基线

**状态：** 已接受
**决策：** 代码以 Python 3.11 为目标。在更新且兼容的 Python 版本上进行本地验证可以
作为补充，但不能替代必需的 Python 3.11 兼容性检查。

### D-009——任务侧校准 v1 已通过本地验收

**状态：** 已接受
**决策：** `task-modeling-v1` 已通过本地验收。其 smoke run 只是工程验证，不构成支持
或否定模型侧功能分化的证据。

### D-010——行为校准是下一项已提出任务

**状态：** 已接受
**决策：** 下一个有边界的任务构建仅评估模型输出的行为评估框架，包含本地假后端和
通用的冻结 Hugging Face adapter。Activation capture 与真实模型执行继续采用独立门禁。

### D-011——行为 pilot 使用 final-answer-only prompt

**状态：** 已接受
**决策：** 行为校准 v1 使用现有的 final-answer-only prompt、greedy decoding，并且
不显示 scratchpad。任何 scratchpad 对比都必须作为独立实验条件进行规划。

### D-012——行为 pilot 阈值是临时工程门禁

**状态：** 已接受
**决策：** 临时门禁为：总体 trimmed exact match 至少 80%，每个接受评估的 chain
length cell 至少 60%，invalid-format 或 inference failure 不超过 5%。通过该门禁不支持
论文结论，也不自动授权机制研究。

### D-013——面向人的文档使用中英文双语

**状态：** 已接受
**决策：** 每一份面向人的 Markdown 文档都具有英文版，以及以 `.zh-CN.md` 结尾的
同步中文对应版。代码、配置、生成产物和 `plan.json` 等机器可读契约保持单一来源，
除非后续已批准方案另有规定。

### D-014——讨论、规划和实施需要分别授权

**状态：** 已接受
**决策：** 每个候选任务都从多轮讨论开始。创建规划文件前，assistant 必须提供具体的
动作预告，说明动作、产物、审核路径、Git 行为和范围外事项。用户必须明确授权生成
计划；该授权只允许产生可审核的规划 artifact。实施需要第二次明确批准，服务器执行
还需要第三次、针对具体 run 的授权。

### D-015——服务器结果使用被忽略的本地交接包

**状态：** 已接受
**决策：** 大型服务器 artifact 保留在 Git 之外。每个服务器 run 生成小型 manifest、
summary、diagnostic 和 artifact index，可复制到
`artifacts/server-results/<run-id>/` 供本地审核。只有经过审核的小型证据和中英文报告
才能提升到 `results/<run-id>/` 并提交。

## 工作假设

这些假设用于指导实验设计，但尚未被当作事实。

### WH-001——与 function 相关的信号可能在结构控制后仍然存在

至少一部分内部计算模式，可能在 held-out layer、position 或 reasoning step 上预测
candidate operation，并优于 structure-only 和 permuted-label baseline。

### WH-002——部分模式可能在受控 task family 之间迁移

语义和 surface form 不同、但具有经过谨慎论证的共享 computation 的任务，可能表现出
cross-task correspondence。迁移也可能只存在一部分，或者完全不存在。

### WH-003——功能稳定性可能高于 component 稳定性

即使计算的物理实现会在 component、input 或 architecture 之间移动，计算层面的模式
仍可能保持稳定。

## 待定决策

| ID | 需要决定的事项 | 最晚必须解决的阶段 |
|---|---|---|
| O-001 | 主模型与复现模型及其 exact revision | instrumentation 实现前 |
| O-002 | direct-answer 与 visible-scratchpad 条件 | prompt 与 trace 设计前 |
| O-003 | 校准后的最终 pilot task family | 主数据集冻结前 |
| O-004 | 模型侧 measurement unit | trace capture 实现前 |
| O-005 | discovery 和 stability method | confirmatory 模型侧分析前 |
| O-006 | token/event alignment protocol | functional correspondence test 前 |
| O-007 | 主统计模型与 multiplicity policy | confirmatory analysis 前 |
| O-008 | accuracy threshold 与 example inclusion policy | activation collection 前 |
| O-009 | 服务器 GPU、CUDA、存储、scheduler 和环境 | 任何服务器运行前 |
| O-010 | 主实验数据集大小与存储位置 | 数据集冻结前 |
| O-013 | pilot 模型与 tokenizer 的 exact revision | 真实模型 pilot 前 |

## 决策变更规则

当决策改变时，新增一条记录，不得静默改写原有理由。记录受影响的 run ID，并说明
现有 artifact 是否必须重新生成。实施方案只有在某个待定选择是局部、可逆且明确标注为
临时时，才可以实例化该选择。
