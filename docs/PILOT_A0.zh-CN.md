# Pilot A0 协议：原生任务盘点与 model-first discovery bridge

> English: [PILOT_A0.md](PILOT_A0.md)

**状态：** 修订协议；等待人类审核
**协议版本：** 0.2
**最后更新：** 2026-09-10

## 1. 目的

Pilot A0 为从当前主流 reasoning task 直接进入 model-side discovery 准备路径。它不从发明
operation vocabulary、人工 decomposition benchmark 或实施 synthetic task language 开始。

主要顺序为：

> 原生任务 → 成功的 native inference → 内部 computation trajectory →
> within-task recurring pattern → 冻结的 cross-task transfer test → 谨慎的 functional
> interpretation

这条路线询问模型在解决任务时实际形成什么 computation pattern，而不是询问模型是否匹配
研究者预先定义的 operation list。Task-side 与 model-side structure 继续保持区分。

## 2. 已接受的目标范围

初始目标总体是：英语、纯文本、答案可客观检验、task-relevant premise 包含在输入或任务
规则中，并且需要多个相互依赖计算步骤的 reasoning task。

已接受的初始来源 stratum 为：

- 人工数学文字题，初始由 GSM8K 表示；
- 给定文本上的 discrete reasoning，初始由 DROP 表示；
- 具有原生 provenance 的 connected multi-hop question answering，初始由 MuSiQue-Ans
  v1.0 表示；
- 抽象演绎与状态追踪，初始由 BIG-Bench `logical_deduction` 与
  `tracking_shuffled_objects` 表示。

这些 stratum 使 task origin 与可观察 computation demand 多样化。它们不构成完备 ontology，
也不是所有 reasoning 的概率样本。External retrieval、开放式主观生成、多模态 perception、
code execution 与 formal theorem proving 不属于第一版总体。

在 source inspection 前，仍须冻结准确 repository、immutable revision、license、eligible
split 与 source access。

## 3. 不新增 annotation 规则

新的人工 task decomposition 不是默认方法。Pilot A0 首先只使用每个 source 原生提供的
信息：

- question、input、answer 与官方 correctness rule；
- benchmark-native ID、split、difficulty 或 size field；
- source 自带的 rationale、calculation trace、constituent question、DAG、supporting fact、
  template 或 generator metadata；
- 可复现的 prompt 与 inference provenance。

原生 rationale 与 graph 是 source artifact，不是唯一必要算法，也不是模型内部 computation
的描述。

只有 documented failure analysis 证明某个具体科学区分无法利用 native metadata、model-
side pattern、controlled input variation 或现有 source artifact 检验时，才可以提出 manual
annotation。此类 annotation 必须具有新的有边界方案与明确授权。

## 4. Native inference

Native inference 使用 benchmark 原始 task semantics 与 benchmark-faithful prompt。模型可以
生成自由形式 reasoning 与 final answer，但协议不强加研究者定义的 operation name、symbolic
state slot 或 forced execution trace。

每次 attempt 记录 prompt、decoding configuration、完整 response、parsed answer、correctness、
model/tokenizer revision 与 source-instance identity。所有 attempt 都保留在 behavioral
denominator 中。

生成的 reasoning text 是 behavioral artifact。它可以支持 token alignment 或 interpretation
hypothesis，但不能被接受为 latent computation 的忠实记录。

## 5. Model-side measurement object

第一 discovery 阶段可以在声明的 token 与 layer resolution 上检查：

- residual-stream state；
- attention 与 MLP sublayer 的 residual update；
- 跨 layer 或 generated-token window 的局部 state transition；
- 后续方案证明额外成本合理时的 attention/MLP output；
- 对 source-preserving 或 answer-changing input perturbation 的响应。

Measurement unit 必须在 confirmatory use 前冻结。初始中性术语为 `activation pattern`、
`transition pattern` 与 `candidate computation pattern`。Cluster 不自动成为 operation 或
reasoning role。

## 6. Label-free within-task discovery

Pattern discovery 不使用 task-operation label。它可以把 task family、correctness、native
instance metadata、token/layer coordinate 与声明的 perturbation identity 用作 control 或
evaluation variable。

一个 candidate within-task computation pattern 必须：

1. 跨 held-out correct instance 重复出现，而不是只存在于一个 prompt template；
2. 经受 layer、absolute token position、output length、lexical overlap、answer identity、
   difficulty 与 task-instance identity control；
3. 在允许有效 source-preserving variation 时，至少对一种变化保持稳定；
4. 优于 shuffled、structure-only 与 metadata-only baseline；
5. 在 untouched evaluation 前冻结定义。

错误 inference 作为单独 diagnostic 保留。不能从 behavior report 中静默删除，也不能与正确
trajectory 混合。

## 7. 信息论与预测性 diagnostic

Mutual information 和相关 measure 可以检验：控制已声明变量后，model-side pattern 是否
包含关于未来输出、答案、task identity、input variable、perturbation 或 correctness 的信息。

Mutual information 不是 operation detector。尤其是：

- answer information 可能只是 answer representation，而不是 computation；
- task-identity information 可能只反映 lexical 或 domain difference；
- observational dependence 不能说明信息被实际使用；
- 高维 continuous MI estimate 可能高度依赖 estimator。

因此 MI 必须与 held-out prediction、representation/transition similarity、trajectory
segmentation、permutation baseline 与 sensitivity analysis 共同使用。准确 estimator、
dimensionality treatment 与 null distribution 需要后续经过审核的分析方案。

## 8. Cross-task reuse test

Within-task pattern 只有通过 transfer 才成为 cross-task candidate：

1. 使用一个 source task 或预先声明 discovery set 发现并冻结 pattern definition；
2. 在 held-out task 上应用，不能根据该任务 outcome 重新定义 pattern；
3. 相对 layer、position、lexical、difficulty 与 task-identity baseline，检验 recurrence、
   transition similarity、predictive information 与 perturbation response；
4. 当 A-to-B 与 B-to-A 不同时报告 asymmetric transfer；
5. 把结果限制在被检验的 task 与 model 内。

共享 task label 或相似 answer format 不能建立 reuse。反过来，一个可迁移 model-side pattern
可以在尚无可靠 semantic operation 名称时先被报告。

## 9. Functional interpretation

Interpretation 跟随 discovery，而不是定义 discovery。证据可以来自：

- pattern 在模型生成 trajectory 中出现的时间与位置；
- native benchmark metadata 与 source 自带 structure；
- controlled input perturbation 及其 internal/output change；
- correct 与 incorrect inference comparison；
- 后续独立方案中的 targeted patching、ablation 或 controlled microtask。

在证据把它与 answer encoding、task identity、position、generic generation dynamics 和其他
structural explanation 区分前，interpretation 继续称为 `candidate computation`。除非另行
设计的 intervention 支持，强 causal claim 仍不属于 RQ1。

## 10. Task language v0.2 与 annotation 的状态

`Symbol8`、拟议 function pair 与 C1–C4 继续作为非活动 calibration-sandbox idea。它们不是
model-side discovery 的来源，也未获实施授权。

Synthetic task construction 与新的 manual annotation 都是 fallback tool。只有具名且未解决
的 identification problem 无法通过 native task、native source artifact、held-out transfer
或 controlled perturbation 处理时，才可重新考虑其中之一。实现方便本身不足以构成理由。

## 11. 证据阶梯

Pilot evidence 按以下顺序解释：

1. **measurement validity：** trajectory 与 metadata 得到可复现 capture 和 alignment；
2. **within-task recurrence：** 冻结的 pattern 经受 held-out instance 与声明 confound
   control；
3. **cross-task reuse：** 冻结 pattern 迁移到独立 held-out task；
4. **functional interpretation：** 汇合的 native 与 perturbational evidence 支持有边界的
   pattern account；
5. **causal role：** 需要单独 intervention design，不能由前面层级自动推出。

后续层级失败不会抹除较早结果，但会降低 claim ceiling。

## 12. 立即产物与后续门禁

Pilot A0 的立即实施应生成一个不新增 annotation 的 source inventory，记录准确 provenance、
native field、correctness semantics、已有 structural artifact、perturbation affordance，以及
对 native inference 和 model-side discovery 的适用性。

之后必须通过独立方案分别授权：

1. 所选 native task 上的 behavioral feasibility；
2. successful native inference 的 activation capture；
3. label-free within-task discovery 与 confirmation；
4. cross-task transfer；
5. targeted interpretation 或 fallback instrumentation。

本协议本身不授权模型、benchmark、代码、下载或服务器动作。

