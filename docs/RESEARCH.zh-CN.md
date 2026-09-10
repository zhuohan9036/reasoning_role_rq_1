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

对于从现有 benchmark 抽样的任务，项目还必须记录 target-population definition、benchmark
release 与 native instance identity、task origin、sampling stratum，并显式区分任务的历史
构造方式与本项目之后做出的 analytical reconstruction。不能只因为某个 task dimension 便于
生成干净的 synthetic design 就认为它已经得到论证。

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

### G0——建立可审计任务来源与原生 semantics

记录准确 task provenance、native identity、input、answer、correctness semantics、source
自带 structural artifact 与主要 observable covariate。在 exploratory model-side discovery
前，不要求新增 operation vocabulary 或人工 solution decomposition。

成功意味着 instance、prompt、output 与 source metadata 可复现、可审计。任何后续 task-
side decomposition 继续是需要单独论证的临时对象。

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

冻结独立发现的 model-side pattern，并检验它们能否在不根据 target-task outcome 重新定义
的情况下迁移到其他 task family。与 layer、position、lexical、answer-format、difficulty
与 task-identity explanation 比较。Functional interpretation 跟随成功 transfer，而不是
成为定义它的先决条件。

### G5——复现核心发现

在另一个冻结预训练模型或不同 architecture 上复现 G1–G4 中最小但具有决定性的
测试集合。优先复现：分化是否存在、function 与 step 的区分，以及最强的泛化结果。

## 6. 计划中的证据结构

### 阶段 A0——不新增 annotation 的 native-source inventory

修订协议见 [PILOT_A0.zh-CN.md](PILOT_A0.zh-CN.md)。为 GSM8K、DROP、MuSiQue-Ans v1.0
与选定 BIG-Bench task 冻结准确 provenance、native correctness semantics、source 自带
metadata/structure、grouping risk、perturbation affordance 与 reserved split role。不得创建
operation label 或人工 reconstruction solution graph。

`Symbol8`、拟议 matched function pair、C1–C4 与新 manual annotation 都是非活动 fallback
instrument，不是先决条件。

### 阶段 A1——Native behavioral feasibility

- 选择一个冻结、可进行机制访问的模型和 benchmark-faithful free-form response regime。
- 在 activation analysis 前，按 source task 与 native covariate 确立 behavior。
- 所有 attempt 都保留在 behavioral denominator 中，并区分 correct 与 incorrect inference
  trajectory。
- 不能用所选模型能够解决哪些任务来定义 target population。

### 阶段 B——Activation-trajectory instrumentation

- 在 native inference 中可复现地捕获 token-by-layer residual state 与声明的 residual update。
- 把 generated reasoning 当作 behavior 与可能的 alignment evidence，而不是 latent-
  computation ground truth。
- 在 confirmatory use 前冻结 measurement unit、storage policy、alignment 与 quality control。

### 阶段 C——Label-free within-task pattern discovery

- 在不使用 task-operation label 的情况下发现 activation/transition pattern。
- 跨 instance 与有效 surface variation 检验 held-out within-task recurrence。
- 与 shuffled、layer-only、position-only、lexical、answer、difficulty、output-length、
  correctness 与 task-identity baseline 比较。
- MI 只作为 estimator-sensitive information diagnostic，并与 held-out prediction、trajectory、
  similarity 与 permutation analysis 共同使用。

### 阶段 D——冻结的 cross-task reuse 与 functional interpretation

- 在应用于 held-out task 前冻结 pattern definition。
- 分开报告 A-to-B 与 B-to-A transfer，不根据 target task 重新定义。
- 使用 native metadata、source-preserving/answer-changing perturbation 与 correct/incorrect
  comparison 解释成功 transfer。
- Semantic function 仍不确定时，继续使用中性的 `candidate computation pattern`。

### 阶段 E——复现与因果边界

- 在第二个冻结模型上复现最小但决定性的 within-task 与 cross-task finding。
- 只有出现具名 identification failure 并获得单独方案后，才引入 targeted annotation 或
  synthetic calibration。
- 将 patching、ablation 与更强 causal claim 视为超出 observational pattern recurrence 的
  单独设计证据。

## 7. Baseline 与 null model

主要分析至少应比较以下 baseline：

- 仅使用 layer/depth 的预测；
- 仅使用 token position 的预测；
- 仅使用 reasoning step/chain depth 的预测；
- task family 和 prompt template 预测；
- difficulty 和 correctness control；
- 在合适 matched strata 内随机置换 discovered-pattern assignment 或 evaluation variable；
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

Pilot A0 必须先冻结 source provenance 与 access。剩余决定为：

1. 已接受 source stratum 的准确 repository、immutable revision/checksum、license、eligible
   split 与 return-test reservation。
2. Source inventory 只能检查 schema/aggregate metadata，还是也可检查一小批明确声明的
   instance。
3. Behavioral feasibility 的第一个 native task 或 task pair。
4. Primary model/tokenizer 的 immutable exact revision；Qwen 已排除。
5. Native prompt regime、decoding、behavioral gate 与 correctness parsing。
6. Activation measurement unit、capture scope、alignment 与 storage budget。
7. Pattern-discovery、MI/predictive、trajectory、uncertainty、multiplicity 与 transfer method。
8. Perturbation family 与后续 intervention evidence 的边界。

这些决定在约束代码或主要实验前，必须在 `DECISIONS.md` 中解决。

## 10. 文献追踪与差异性规则

无论何时遇到直接相关的新工作，都应记录或报告其 primary source、日期、核心结果、与本项目
的重合、方法差异，以及对 novelty 或设计的具体影响。定期追踪补充这一持续义务，并且只在
出现实质相关进展时通知，不用常规搜索噪声打扰项目。
