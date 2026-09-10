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

### D-016——任务侧对象采用带版本的结构化 formalism

**状态：** 已接受
**决策：** 一个 task family 规定 instance distribution、correctness semantics、
reference-solution interface、rendering family、controlled 与 nuisance variable、semantic
identity、reference dependency representation、version 和 provenance。Canonical instance
与 rendered prompt 保持为不同对象。Workflow task ID 不是 reasoning task。

### D-017——Pilot 启发的 construct 需要独立确认

**状态：** 已接受
**决策：** Exploratory model pilot 前必须存在薄的 task specification。Pilot evidence 可以
启发修订后的 task decomposition、candidate operation 或 cross-task hypothesis，但修订必须
获得新版本，并在未参与定义的证据上评估前冻结。Candidate operation 和 task-side
correspondence 是假设；model-side empirical correspondence 才是结果。

### D-018——规划与 Codex 实施采用明确的文档交接

**状态：** 已接受
**决策：** 规划对话在不修改仓库的情况下冻结有边界的需求。动作预告获批后，Codex 创建
可审核的规划产物。人类审核计划并明确批准实施后，Codex 才能修改文件。`plan.json` 是
机器可读合同，中英文 plan 与 review 是面向人类的接口。Commit、push、模型和服务器权限
继续分别声明。

### D-019——Pilot A 是模式发现与测量验证 pilot

**状态：** 已接受
**决策：** Pilot A 用于开发受控测量环境，只能支持限定于具名 model、task distribution
和 response regime 的结论。它不能确立 universal primitive、一般 reasoning role、跨领域
普遍性或因果必要性。

### D-020——Pilot A 采用 matched task-language design

**状态：** 已接受
**决策：** 一个临时 typed task language 交叉 serial/fork-join topology 与 externally
supplied/intermediate-state-computed control。Transform、merge、predicate 和 select 只
是 task-language category。必须加入 direct-read control、paired rerendering 和 untouched
semantic instance。详细协议为 `docs/PILOT_A.zh-CN.md`。

### D-021——现有 generator 不定义 Pilot A

**状态：** 已接受
**决策：** 已实现的 `function_composition` 和 `relational_path` family 是非权威工程校准
artifact。Pilot A 由科学 contrast 推导；可以复用、替换或绕过其基础设施，但不能让旧任务
假设获得优先地位。

### D-022——Pilot A 排除 Qwen，默认采用 Mistral 级模型

**状态：** 已接受
**决策：** Pilot A 排除 Qwen model。工作默认是冻结的 7B 级 instruction-tuned Mistral，
当前为 `mistralai/Mistral-7B-Instruct-v0.3`；相近规模的 Llama instruct checkpoint 是首选
替代。执行前仍必须固定 model/tokenizer 的 immutable exact revision。

### D-023——Pilot A 分阶段进行行为、对齐测量与确认

**状态：** 已接受
**决策：** 先评估 behavior，再检查 activation。第一测量是显式 trace regime 中 aligned
event 的 residual stream。Pattern definition 必须在 untouched confirmation 前冻结。
Final-answer-only measurement、head/MLP capture、intervention 和 semantic-domain
replication 需要后续有边界的独立方案。

### D-024——Functional contrast 必须匹配 structural signature

**状态：** 已接受；取代 D-020 中的粗粒度 label 细节
**决策：** Transform、merge、predicate 和 select 是 structural task-language family，
不是主要 functional label。Pilot A 只在相同 input/output signature 内比较 functional
subtype：`shift/reflect`、`add_merge/subtract_merge`、`parity/upper_half` 和
`select_if/select_unless`。核心 program 固定包含六个 answer-relevant node。R1 测量每个
state symbol 之前固定 delimiter 位置的 residual stream。Functional-subtype label 必须在
模型运行前通过针对 graph 与 position metadata 的 identifiability audit。

### D-025——科学 Pilot A 任务前必须进行 target-task grounding

**状态：** 已接受；取代 D-019 至 D-024 所隐含的“可直接实施”状态，但保留其中的 calibration
与 control 原则
**决策：** 论文的预期去处是当前主流 textual multi-step reasoning。在选择科学 Pilot A
任务前，项目必须冻结 target-task population，在独立于模型 activation 的条件下 reconstruction
具有 provenance 的 source sample，从 audit 中归纳 candidate motif，并要求每个 benchmark-
derived microtask 具有 abstraction map 与 return-to-source test。除非 Pilot A0 为其建立
grounding，`Symbol8`、拟议 function pair 与 C1–C4 降级为候选 calibration sandbox。
`pilot-a-design-v1` 实施方案在代码修改前暂停。

### D-026——Discovery 从 native inference 与 model-side pattern 开始

**状态：** 已接受；取代 D-023 至 D-025 所隐含的 annotation-first 与 controlled-task-first
方法
**决策：** 主要路线从已接受 source stratum 上成功、benchmark-faithful 的 native inference
开始。它捕获 model-side activation/transition trajectory，在不使用 task-operation label 的
情况下发现 within-task recurring pattern，冻结 pattern，并在赋予 functional interpretation
前检验 cross-task transfer。Generated reasoning 是 behavior，不是 latent ground truth。Mutual
information 是辅助 association diagnostic，不是 operation detector 或 causal test。新的 manual
annotation 与 synthetic task construction 延后为 fallback tool；只有出现具名 identification
failure、生成新的有边界方案并获得明确授权后才可使用。

### D-027——持续进行文献差异性追踪

**状态：** 已接受
**决策：** 无论何时遇到直接相关的新研究，都报告 primary source、日期、核心结果、与本项目
的重合、方法差异，以及对 novelty 或设计的影响。Recurring literature watch 补充这项持续
规则，并且只在出现实质相关新工作或方法变化时通知。

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
| O-001 | Mistral model/tokenizer exact revision 与后续 replication model | 任何真实模型 run 前 |
| O-003 | 已接受 source stratum 的准确 repository、immutable revision/checksum、license、eligible split 与 return-test reservation | 任何 source inventory 实施前 |
| O-005 | 准确 readout、discovery 与 stability method | 模型侧分析实施前 |
| O-006 | R2 final-answer-only measurement unit 与 alignment | R2 activation capture 前 |
| O-007 | uncertainty estimator 与 multiplicity policy | confirmation analysis 前 |
| O-009 | 服务器 GPU、CUDA、存储、scheduler 和环境 | 任何服务器运行前 |
| O-013 | tokenizer-compatible single-token `Symbol8` rendering 与 delimiter bank，仅当相关元素被保留 | 任何使用 v0.2 元素的真实模型 run 前 |
| O-014 | Source access mode，以及 inventory 只检查 schema 还是也检查一小批明确声明的 instance | Pilot A0 实施前 |
| O-015 | 第一个 native task/task pair、benchmark-faithful prompt、decoding 与 behavioral gate | Native behavioral pilot 方案前 |
| O-016 | Activation unit、capture scope、alignment、storage、MI/predictive、trajectory 与 transfer method | Model-side instrumentation 与 analysis 方案前 |

## 决策变更规则

当决策改变时，新增一条记录，不得静默改写原有理由。记录受影响的 run ID，并说明
现有 artifact 是否必须重新生成。实施方案只有在某个待定选择是局部、可逆且明确标注为
临时时，才可以实例化该选择。
