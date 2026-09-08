# 行为校准协议

> English: [EVALUATION.md](EVALUATION.md)

## 解释边界

行为校准用于判断冻结模型回答 pilot task 的可靠程度，是否足以支持后续机制研究。
Accuracy、formatting 或 failure rate 都不能确立内部 computation pattern、functional
differentiation 或 reasoning role。

本阶段不采集 activation。任务侧 dependency graph 和 `task_side_trace` 永远不会发送
给 inference backend。

## v1 主条件

- 使用现有 final-answer-only task prompt。
- 不要求可见 scratchpad 或 chain of thought。
- 冻结模型处于 evaluation mode，并关闭 gradient。
- 只使用 greedy decoding。
- 保留 template 处理后的精确最终输入和 raw completion。
- 所有尝试过的 example（包括失败）都保留在 metric denominator 中。

任何 visible-scratchpad 条件都需要独立方案，因为它会改变可观测 token sequence，也
可能改变模型内部计算。

## Metric

`trimmed_exact` 是主要 metric，只移除字符串两端空白。`raw_exact` 保留原始文本的
逐字节行为。`format_valid` 要求去除两端空白后的完整 completion 符合预期 encoding。
只有 whole-output check 成功后，`parsed_exact` 才比较解析后的值。

Parser 绝不在解释文本中搜索嵌入的答案。例如，即使 `(1,0)` 正确，
`The answer is (1,0).` 仍被判定为无效。这样可以防止后处理掩盖 prompt-following 或
output-control failure。

每个 summary 都包含 count、rate 和 trimmed exact match 的 95% Wilson interval。
Summary 按任务与 nuisance factor 分层，包括 family、split、length、distractor、
presentation order、template、vocabulary 和 answer encoding。

## 临时适用性门禁

该门禁仅用于 pilot 工程决策。一个 task family 在以下条件全部满足时通过：

- 总体 trimmed exact match 至少 80%；
- 每个观察到的 chain-length cell 至少 60%；
- invalid-format 或 inference-failure rate 不超过 5%。

该阈值没有为论文结论进行 power 设计。它只用于决定下一分支：扩展或冻结数据、重新
设计某一 task family、重新考虑模型或 prompt，或者规划 scratchpad manipulation。

## 假后端

假后端用于验证框架，不代表模型行为。它根据 source instance ID，以确定性方式分配
correct、valid-but-wrong、invalid-extra-text 和 structured failure 结果。
假结果可以作为工程 fixture 提交，但绝不能出现在经验结果表中。

## Hugging Face 后端

真实后端要求明确的 model revision 和 tokenizer revision。默认只使用本地文件并设置
`trust_remote_code: false`；它记录 plain 与 chat-template formatting，设置 evaluation
mode，冻结 parameter，并在 inference-only context 中执行 generation。

模型依赖是可选项：

```bash
python -m pip install -e '.[model]'
```

除非单独获得授权并与目标服务器环境匹配，否则本任务不得安装或下载这些依赖。

## 本地假后端运行

在仓库根目录执行：

```bash
python scripts/evaluate_behavior.py \
  --config configs/eval/behavioral_smoke_fake.yaml \
  --output /new/output/directory
```

输出目录必须是新目录。若要恢复一个中断但兼容的运行，添加 `--resume`。Resume 会拒绝
source code、configuration、data selection 或 backend identity 的变化。

输出包括 `records.jsonl`、`summary.json`、`summary.csv`、`run_state.json` 和
`run_manifest.json`。Manifest 包含 hash 和 provenance，但不包含模型权重。提交的科学
artifact 有意排除机器专属路径。

## 服务器门禁

任何真实模型运行前，必须补完 `runs/behavioral-calibration-v1/SERVER.md`，选定 exact
model/tokenizer revision，审核 chat formatting，固定模型软件环境，并明确获得下载和
执行授权。本任务不允许采集 activation。
