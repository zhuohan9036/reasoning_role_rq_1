# 任务需求：pilot-a0-target-grounding-v1

> English: [BRIEF.md](BRIEF.md)

**状态：** 修订规划产物已生成；实施等待审核
**Brief 版本：** 2
**研究范围：** no-annotation source inventory 与 model-first 路线

## 期望结果

准备一条从原生主流 reasoning task 到 label-free model-side pattern discovery 的直接、可审计
路径。当前实施只产生 source inventory；behavioral run、activation capture、analysis、
transfer 与 interpretation 分别需要后续方案。

## 已冻结要求

1. 初始总体是英语、纯文本、客观评分、self-contained multi-step reasoning。
2. 初始 source stratum 为 GSM8K、DROP、MuSiQue-Ans v1.0，以及 BIG-Bench
   `logical_deduction` 与 `tracking_shuffled_objects`。
3. Native inference 保留 benchmark semantics，不强加 operation label、symbolic state slot 或
   forced execution trace。
4. Discovery 从 model-side activation/transition pattern 开始，而不是从研究者定义的 operation
   vocabulary 开始。
5. Within-task recurrence 先于冻结的 cross-task transfer。
6. MI 是 information association 的一种 diagnostic，不是 operation detector 或 causal test。
7. Native rationale、DAG 与 generator metadata 是可选 source artifact，不是唯一算法或
   model-side ground truth。
8. 新 manual annotation 与 synthetic task construction 只有在 documented identification
   failure 和单独授权后才可作为 fallback tool。
9. `Symbol8`、拟议 function pair 与 C1–C4 继续作为非活动 calibration idea。
10. 无论何时发现相关新研究，都应主动提示；同时定期追踪文献，重点维护项目差异性。

## 当前实施验收标准

- 记录准确 official source location、immutable revision 或 checksum、license、native ID
  scheme 与 eligible split。
- 对每个 source 盘点 correctness semantics、native metadata、source 自带 structural
  artifact、prompt affordance、perturbation affordance 与已知 leakage/grouping risk。
- Inventory 不创建 task-operation label，也不人工 reconstruction solution graph。
- Suitability matrix 推荐最小初始 native behavioral pilot，并说明每个被拒绝或延后 source
  当前不能支持什么。
- 分别规定 behavior、activation capture、label-free discovery、cross-task transfer 与
  interpretation 的下一任务边界。

## 尚未解决的选择

- 准确 immutable source revision、license、eligible split 与 access mode。
- Behavioral feasibility 的初始 source task 或 task pair。
- Model、native prompt regime、decoding 与 behavioral gate。
- Activation measurement unit 与 storage budget。
- Pattern-discovery、MI/predictive、trajectory 与 transfer method。
- Perturbation family 与后续 intervention boundary。

## 本次规划动作范围外

- Benchmark download 或 source-instance inspection。
- 新 annotation 或 task decomposition。
- Source code、test、configuration 或 fixture。
- 模型选择、下载、inference、activation capture 或 analysis。
- Synthetic task implementation。
- Server execution、commit 或 push。

