# 验收报告：behavioral-calibration-v1

> English: [REVIEW.md](REVIEW.md)

**状态：** 已通过本地验收检查
**审核日期：** 2026-09-08
**实现 commit：** `4797581`、`17fda49`
**已提交 fixture 的 source：** 干净 revision `17fda49`

## 结果

已实现获批的 model-output-only 行为校准框架。它使用 strict whole-output scoring 评估
final answer，将失败尝试保留在所有 denominator 中，并记录可复现性 metadata。本次
审核既未加载真实模型，也未采集 activation，更没有提供 functional differentiation
的证据。

## 已交付

- 带版本的 request、backend-result 和 per-example evaluation record。
- Backend-neutral interface 与 deterministic fake backend。
- 通用 Hugging Face causal-LM adapter：采用 lazy optional import，要求 exact
  model/tokenizer revision，显式指定 prompt mode，设置 evaluation mode，冻结 parameter，
  使用 greedy generation，并只在 inference context 中执行。
- Symbol 和 vector answer encoding 的 strict whole-output parser。
- Atomic batch checkpoint、compatible-run resume、provenance comparison，以及对
  duplicate/missing/reordered result 的拒绝。
- 基于所有 attempt 的 JSON/CSV summary，包含指定 nuisance stratum、family by chain
  length、95% Wilson interval 和显式 provisional gate decision。
- Source data、configuration、code、backend、environment、input 与 output 的 hash 或
  identity。
- Offline configuration、未解决的 server template、protocol 文档、自动化测试，以及
  已提交的 80-record fake-run fixture。

## 验收证据

| 检查 | 结果 |
|---|---|
| Python 基线 | Python 3.11.16 通过 |
| Editable package 与 CLI | 未下载可选模型 package 时通过 |
| 自动化测试 | 51/51 通过 |
| 编译与 diff 检查 | 通过 |
| 离线 fake evaluation | 尝试 80 条，完成 80 条，无 missing 或 duplicate ID |
| 稳定复现 | 固定 provenance 时 record、run state、summary JSON 和 summary CSV 均逐字节复现 |
| 严格评分 | explanation、embedded answer、extra text、malformed vector 和 Unicode lookalike 均被拒绝 |
| Failure accounting | 6 个 structured failure 保留在全部 80 次尝试中 |
| Summary 对账 | 60 个 trimmed-exact、66 个 format-valid、14 个 invalid-or-failed；所有 denominator 均为 80 |
| Resume 安全 | 中断后可恢复；config change 和 duplicate checkpoint 明确失败 |
| Frozen-model contract | Stub test 验证 exact revision、chat-template identity、evaluation mode、frozen parameter、greedy decoding 和 disabled gradient |
| Manifest 完整性 | 记录的四个 output hash 均通过验证 |
| 真实模型/服务器/activation | 按要求未执行 |

主要本地命令：

```bash
.venv/bin/python -m unittest discover -s tests -v
```

已提交的工程 artifact 位于 `tests/fixtures/behavioral_smoke/`。其 manifest 把运行绑定到
task-data hash、configuration、backend identity、source-tree hash 和干净 code revision。

## 假结果的解释

假后端有意输出 correct、wrong、invalid 和 failed 的混合结果。因此，它的总体 75%
trimmed exact-match 和 17.5% invalid-or-inference-failure rate 不通过临时门禁。这是预期
的测试输入，不是任何 Transformer 的结果，不构成支持或否定论文假设的证据。该 fixture
只用于证明 metric 与负结果分支的实现正确。

## 方案偏离与实现选择

- 未安装真实 `torch`、`transformers` 或 `accelerate` package。Hugging Face 路径使用
  受控 stub 检查，因此任务保持在“不下载、不运行真实模型”的批准边界内。
- 模型依赖采用兼容的最低版本，而非固定的 server environment，因为服务器和目标
  checkpoint 尚未解决。
- Server configuration 继续是带有 replacement marker、明显不可直接运行的 template。
- 只有在实现具有干净 Git revision 后才生成已提交 fake fixture，因此其代码 identity
  有明确含义。

## 限制与延后验证

- Hugging Face adapter 尚未在实际安装的 Transformers version、真实 tokenizer/chat
  template、真实 checkpoint 或 GPU placement 上运行。这些兼容性检查属于获批后的
  server pilot。
- Exact model、tokenizer 和 immutable revision；base/instruction checkpoint；prompt
  template；CUDA/GPU environment；dependency lock 均未确定。
- 当前 80-record task fixture 是工程样本，不是经过 power 设计的行为数据集。短链条
  semantic support 的限制仍然存在。
- 后续通过 behavioral gate 只表示可以继续 task/data design；它不能确立模型内部
  computation pattern 或 reasoning role。

## 服务器交接门禁

真实模型运行前，应解决 model 和 environment 的待定选择，补完 `SERVER.md`，固定
software environment，检查 exact prompt template，并明确授权下载与执行。第一个
server step 应是一个供人工检查的小 batch，随后运行完整 behavioral pilot 和一个
deterministic-subset replay。Activation capture 仍在本任务范围外。

## 交接

本地实施任务已经完成。本报告不授权任何下一实施任务。进一步规划前应先更新工作规范。
