# 任务需求：behavioral-calibration-v1

> English: [BRIEF.md](BRIEF.md)

**状态：** 已实现并通过本地验证
**研究阶段：** 阶段 B，行为校准
**研究目标：** G0 校准；G1–G4 的前置条件

## 期望结果

构建一个可复现的行为评估框架，用于判断某个候选的冻结 causal language model 是否
能足够可靠地解决两个 pilot task family，从而值得开展后续 mechanistic analysis。

本任务只评估模型输出。不得采集 activation、给模型侧计算分配标签、对 component 做
clustering，或声称发现了 functional differentiation 的证据。

## 提议的主条件

- 使用 record 中 final-answer-only 的 prompt。
- 在 evaluation mode 中以 greedy decoding 运行冻结模型。
- 不暴露 `task_side_trace` 或中间任务状态。
- 不要求可见 chain of thought。
- 保留精确渲染后的 model input 和 raw completion 以供审计。

如果后续希望加入 visible-scratchpad 条件，必须将其作为独立规划的实验条件，而不能
作为未记录的 fallback。

## 必需产物

1. 带版本的 record，把每个 completion 关联到 data、instance、model、tokenizer、
   prompt-format 和 generation revision。
2. Backend-neutral inference interface、deterministic fake backend，以及冻结的
   Hugging Face causal-LM backend。
3. 每个 family 和 answer encoding 的 strict whole-output parser。
4. Per-example JSONL，包含 exact input、raw completion、parsing、correctness、timing、
   token count 和 failure。
5. Summary JSON/CSV，按 family、split、length、distractor、presentation order、
   template、vocabulary 和 answer encoding 分层。
6. Run manifest、safe resume、failure accounting 和 content hash。
7. 区分 engineering success 与 task/model empirical adequacy 的 eligibility report。
8. 本地测试与 `REVIEW.md`；在单独授权前不运行服务器。

## 提议的 pilot 判断规则

一个 family 在以下条件下可以暂时进入下一轮数据设计：

- 总体 trimmed exact-match accuracy 至少 80%；
- 每个评估到的 chain-length cell 至少 60%；
- invalid-format 或 inference-failure rate 不超过 5%。

这些是工程校准阈值，不是推断性证据。当前数据集无法确立论文结论，也无法确立经过
power 设计的 inclusion threshold。

## 本地验收标准

1. 使用 fake backend，在无网络、无权重条件下对已提交 fixture 完成完整流程。
2. 固定 provenance 后，稳定的科学输出能够逐字节复现。
3. Parser 拒绝 malformed、contaminated 和 adversarial output，不会从无效解释中抽取
   一个正确答案。
4. Resume 跳过已完成 ID、拒绝不兼容 manifest，且不会重复或静默覆盖 record。
5. Summary 与 per-example output 精确对账，并把所有 failure 保留在 denominator 中。
6. Manifest 记录 data hash、code/config revision、exact model/tokenizer revision、prompt
   formatting、decoding、dependency 和 hardware metadata。
7. 不下载模型，以 stub test 验证 frozen parameter 与 disabled gradient。

## 服务器验收标准

在 model、environment、data size 和 execution 获批后：

1. 完成一个小型 real-model run，并人工检查。
2. Pilot 完整执行，不存在 missing 或 duplicated instance。
3. 固定 greedy-decoding subset 可以复现，或者明确暴露 backend nondeterminism。
4. 报告包含所有必需 strata 和 Wilson confidence interval。
5. 只有小型 summary 与 manifest 返回 Git。

## 范围外

- 在缺少硬件信息时最终选择模型。
- 本地模型下载或任何 real-model/server run。
- Visible chain of thought 或 scratchpad evaluation。
- Activation、hook、attribution、probing、clustering、patching 或 ablation。
- 扩展 generator semantic support。
- 把 behavioral success 当作 reasoning role 的证据。

## 已解决的审核问题

2026-09-08 批准：

1. 使用 final-answer-only，不显示 scratchpad。
2. 在 exact model/server 选定前先实现通用 Hugging Face adapter。
3. 接受 80% overall / 60% per-length / 5% failure 规则作为临时 engineering gate。

真实模型运行前必须补充 exact model 和 server 详情，但本地框架实现不需要等待这些信息。
