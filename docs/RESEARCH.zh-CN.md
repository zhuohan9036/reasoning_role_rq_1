# 研究方案：多步推理中的稳定功能分化

> English: [RESEARCH.md](RESEARCH.md)

**状态：** 已审核研究规格；任务侧 formalism v1 已接受；具体实验选择仍保持开放
**研究问题：** RQ1
**最后更新：** 2026-09-08

## 1. 核心问题

当一个冻结的预训练 Transformer 执行多步推理时，其内部计算是否表现出稳定的
功能分化：是否存在能够被重复识别的计算模式，系统性地对应“正在进行什么计算”，
而不仅仅对应计算发生在“哪里”或“何时”？

本研究不得预设这种分化一定存在。研究应判断现有证据最适合由功能组织、通用网络
结构、任务特有规律，还是缺乏稳健分化来解释。

## 2. 研究范围与非目标

### 范围内

- 刻画成功执行多步推理时可重复出现的模型侧计算模式。
- 在控制 layer depth、token position、reasoning step、prompt format、任务难度和
  固定 component identity 后，检验分化是否仍然存在。
- 衡量模式在不同 instance、受控输入变化、task family，以及至少一个额外的冻结
  预训练模型或不同 architecture 上的稳定性。
- 比较独立规定的任务侧计算结构与独立测量的模型侧结构。

### 仅凭 RQ1 不能确立

- 所发现的模式是推理必需的因果机制。
- 任务侧 operation 就是模型实际使用的 primitive 或 atomic primitive。
- 某个 cluster、probe direction、attention head、MLP、layer 或 token position 本身
  就是 reasoning role。
- task-specific training 揭示了预训练模型中自然存在的组织结构。

因果 intervention 可以作为有针对性的诊断，但除非有专门的 intervention 设计支持，
强因果结论属于后续研究问题。

## 3. 结构化任务侧对象

仓库中的 **workflow task**，例如 `task-modeling-v1`，表示一个有边界的规划或实施动作，
不是 reasoning task。科学分析区分以下带版本的外部对象。

### 任务族规格

一个 task family specification 包含：

- instance space 以及生成或采样分布；
- input、query、output 和 correctness semantics；
- reference-solution interface；
- 将 canonical instance 映射为 prompt 的 rendering family；
- controlled factor 与 nuisance variable；
- semantic identity 与 split rule；
- 一种明确声明的 reference dependency structure；
- version identifier 与 provenance。

Symbolic function composition 和 relational path composition 是其中的例子。Task
family 是外部研究对象，不表示模型使用相同变量或遵循 reference solver。

### Canonical task instance

一个 canonical instance 包含 family 和 schema version、canonical problem 与 query、
由任务正确性语义定义的 target、controlled 与 nuisance variable、semantic identity、
reference dependency structure 及其 provenance，以及零个或多个临时 task-side
annotation。可以从 instance 生成一个或多个 prompt；除非任务规格另有明确规定，
rendering 不属于 canonical task identity。

### Reference dependency structure

由于一个任务可能存在多种有效算法，task family 可以使用：

1. 某一个明确 reference solver 的 graph；
2. 一组或一族有效 solution graph；或
3. 某个明确限定的有效解法类别共同满足的 partial-order constraint。

规格必须说明 node、edge、intermediate state 和 execution semantics 的含义。Reference
graph 记录 generator 或 solver provenance；在没有独立证据时，它不是模型的 computation
graph，也不是唯一必需算法。

### Candidate operation 与 correspondence

Candidate operation 是对 node 或 transition 提出的临时 task-side equivalence claim。
必须说明其 identity criterion、granularity、scope、motivation 和 version。它可以由理论、
任务语义或探索性证据启发，但不是模型侧发现。

Task-side cross-task correspondence 是一项假设：两个任务侧 operation 共享某种相关
计算性质。Model-side empirical correspondence 是另一类结果，需要独立测量的 pattern、
结构性 control、held-out evaluation、不确定性以及适当的 negative-control comparison。

### 分阶段承诺

在 exploratory pilot 前，一个任务必须具有足以确定 instance、answer、provenance、
rendering 和主要结构 covariate 的薄规格。细粒度 operation label 和 cross-task mapping
可以暂不设定。

探索性模型证据可以启发修订后的 task decomposition 或 role vocabulary。每次这类修订
都必须记录启发它的证据、获得新版本，并在 confirmatory evaluation 前冻结。用于定义
或选择 construct 的证据，不能同时作为其独立确认；确认必须使用未参与定义的 instance、
held-out structural condition、新 task pair、额外冻结模型或其他事先声明的 partition。

## 4. 相互竞争的经验解释

项目把以下解释视为真正的竞争者，而不是预先设定层级中的不同阶段。

### E0：只有结构性或时间性组织

观察到的模式可由 layer、token position、reasoning-step progression、sequence
length 或其他通用处理结构解释。对这些变量进行匹配或控制后，几乎不剩与 function
相关的信号。

### E1：任务特有的功能分化

控制结构性混淆后仍存在与 function 相关的模式，但这些模式不能在 task family 之间
有意义地泛化。

### E2：可跨任务复用的功能组织

某些模型侧模式对应在多个 task family 中重复出现的 computation；与匹配的结构性
baseline 相比，它们能更好地泛化到未见过的 surface form、instance 和 task。

### E3：功能稳定但实现可移动

功能模式可以复现，但承载这些模式的具体 head、MLP、layer 或其他物理 component
会随 example、model instance 或 architecture 改变。

允许混合结果和负结果。例如，可能只有一部分 operation 或 task 显示出分化。

## 5. 研究目标与判断标准

### G0——建立明确的任务侧计算模型

为受控多步推理任务表示 instance dependency graph、deterministic solution、candidate
local operation 和 nuisance variable。

成功意味着任务实例可复现、可审计；候选标签明确标为临时标签；任务结构可以独立于
surface form 和关键结构性混淆因素进行操纵。

### G1——确定是否存在可重复的模型侧模式

使用不完全由固定 component identity 定义的分析单位测量内部计算，并使用 held-out
instance 比较不同 condition 内部与之间的可复现性。

支持 G1 的证据必须表现出超越 shuffled-label 和 structure-only null model 的样本外
稳定性。仅有探索性 clustering 不足以支持 G1。

### G2——区分计算功能与结构性混淆

使用 matched contrast、statistical variance partitioning 或等价设计，把功能性解释
与 layer、position、reasoning step、prompt form 和 difficulty 进行比较。

最强的初始检验是 cross-classification：在一组 position/step/layer 上训练或对齐，在
held-out position/step/layer 上评估功能相关结构，同时也检验反向预测。

### G3——量化稳定性

评估模式在不同 example、paraphrase 或 symbolic renaming、problem length、random
seed、适用时的 sampling condition，以及 model instance 上的稳定性。报告置信区间
以及对分析选择的敏感性。

### G4——区分任务特有计算与可复用计算

检验独立发现的模型侧模式能否在 task family 间迁移：这些任务族具有假设共享的
computation，但 token、semantics 和 presentation 不同。同时加入结构同样匹配、但
不共享假设功能的 negative-control pair。

### G5——复现核心发现

在另一个冻结预训练模型或不同 architecture 上复现 G1–G4 中最小但具有决定性的
测试集合。优先复现：分化是否存在、function 与 step 的区分，以及最强的泛化结果。

## 6. 计划中的证据结构

### 阶段 A——模式发现与测量验证

已接受的 Pilot A 协议见 [PILOT_A.zh-CN.md](PILOT_A.zh-CN.md)。它使用新的临时 typed
task language，不把现有 `function_composition` 和 `relational_path` generator 当作科学
gold standard。

- 交叉 serial/fork-join dependency topology 与 externally supplied/intermediate-state-
  computed control。
- Transform、merge、predicate 和 select 只是临时 task-language category；加入
  direct-read negative control。
- 平衡 operation placement、answer value、active length、vocabulary、rendering 和其他
  已声明 nuisance factor。
- 分离 canonical program 与 paired rendering，并在 rendering 前按 semantic identity
  切分。
- 使用相互独立的 discovery 与 untouched confirmation instance。
- Activation analysis 前先建立 behavioral feasibility。
- 首先在显式 aligned-trace regime 中开发 alignment 与 measurement；final-answer-only
  measurement 是单独条件。
- 每个 pilot 启发的 pattern 或 decomposition 都必须在 confirmation 前冻结。

`task-modeling-v1` 继续作为工程校准 artifact。它的两个 task family 可以提供可复用
基础设施或后续 comparison condition，但其存在不约束 Pilot A 的任务设计或论文最终
task ontology。

### 阶段 B——行为与 instrumentation baseline

- 选择冻结、可进行机制访问的主模型和复现模型。
- 按 task、length、template 和 nuisance factor 确立 accuracy。
- 在查看功能性结果之前，定义哪些正确样例可以进入 mechanistic analysis。
- 实现可复现的 trace capture，明确 token alignment，并记录 model、tokenizer、prompt
  和 software version。

### 阶段 C——模型侧模式发现

- 在主要 confirmatory run 之前预注册分析单位和候选 measurement。
- 尽可能不使用 task-operation label，在训练分区上发现模式；否则必须明确区分
  supervised correspondence test 与 discovery。
- 评估样本外 cluster/pattern stability，并与 shuffled、layer-only、position-only 和
  step-only baseline 比较。

在 instrumentation pilot 确认哪些量可以被可靠测量之前，representation、
fingerprint、dimensionality reduction 和 clustering method 保持开放。

### 阶段 D——功能对应与混淆检验

- 只有在模型侧结构定义完成后，才检验其与 candidate task operation 的关联。
- 使用平衡 matched cell 和 held-out-axis cross-classification。
- 在报告不确定性并控制 multiple comparison 的前提下，比较 candidate function 相对
  structural covariate 的增量解释力。
- 在可行时加入 prompt permutation、label permutation 和 non-reasoning control。

### 阶段 E——稳定性、迁移与复现

- 衡量跨 task instance 和受控 surface change 的稳定性。
- 分开评估 within-task 和 cross-task generalization。
- 检验 physical component identity 改变后 functional similarity 是否仍然存在。
- 在第二个模型上只复现核心结构性结果、混淆控制结果和迁移结果。

## 7. Baseline 与 null model

主要分析至少应比较以下 baseline：

- 仅使用 layer/depth 的预测；
- 仅使用 token position 的预测；
- 仅使用 reasoning step/chain depth 的预测；
- task family 和 prompt template 预测；
- difficulty 和 correctness control；
- 在合适 matched strata 内随机置换 candidate-operation label；
- 与所选 metric 相适配的 randomly initialized、resampled 或 dimension-matched
  representation；
- 在一个 partition 上学习、在严格 held-out partition 上评分的模型侧模式。

具体统计模型与 metric 仍为待定决策。选择必须由科学对照关系驱动，不能因为某种方法
产生的 cluster 最清晰就选择它。

## 8. 报告规范

每一项报告结果都必须说明：

- 属于 exploratory 还是 confirmatory；
- task distribution 和 split；
- model 和 tokenizer revision；
- inclusion/exclusion rule 和 behavioral accuracy；
- measurement unit 和 alignment procedure；
- 控制或匹配了哪些 confound；
- seed、不确定性和 sensitivity analysis；
- 结果属于 within-task、cross-task 还是 cross-model；
- 证据能够支持的最弱解释。

在证据足以支持更强术语之前，应使用“computation pattern”或“candidate role”。Null
finding 和 task-specific finding 都是一等结果。

## 9. 模型实验前的主要待定决策

Pilot A 已解决初始任务设计、response-regime 顺序、第一项 residual-stream measurement、
临时 behavioral gate 和数据量。剩余决定为：

1. Mistral model/tokenizer 的 immutable exact revision；Qwen 已排除。
2. 相近规模的 Llama checkpoint 用作 alternative pilot 还是后续 replication model。
3. 与 tokenizer 兼容的 single-token `Symbol8` rendering symbol。
4. 准确 readout regularization、score、uncertainty estimator、clustering method、
   stability metric 和 multiplicity policy。
5. R2 final-answer-only 的 measurement unit 与 alignment rule。
6. 服务器 GPU、software、storage、scheduler 和 artifact path。
7. 哪一个 post-pilot semantic domain 用作第一次真正 replication。

这些决定在约束代码或主要实验前，必须在 `DECISIONS.md` 中解决。
