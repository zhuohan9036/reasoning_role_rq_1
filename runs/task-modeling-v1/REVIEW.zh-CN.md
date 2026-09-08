# 验收报告：task-modeling-v1

> English: [REVIEW.md](REVIEW.md)

**状态：** 已通过本地验收检查
**审核日期：** 2026-09-08
**实现 commit：** `d574c3e`；经审核 fixture 的 source revision 为 `2d139b1`

## 结果

已实现获批的任务侧校准基础。它为 symbolic function composition 和 relational path
composition 生成确定性、平衡且可审计的 record。它不加载模型，也不提出模型侧结论。

## 已交付

- 带版本的 canonical record、dependency graph 和隐藏 task-side trace schema。
- 两个带有 family-local candidate operation 的 deterministic task family。
- 从 canonical problem 重新计算答案的 reference solver。
- Compact/prose template、不同 surface vocabulary，以及每个 family 的两种 answer
  encoding。
- 严格的 factor-cell expansion 与 configuration validation。
- IID、surface、template 和 length holdout 语义。
- 全局 semantic-identity exclusion，以及 canonical-problem 和 prompt-hash overlap audit。
- 稳定 JSONL serialization、provenance manifest、joint factor-cell count、file hash 和
  non-overwriting output behavior。
- checkout-local 与已安装 package 的命令行入口。
- Smoke config、延后的较大配置、数据文档、23 项自动化测试，以及包含 80 条 record
  的已提交 fixture。

## 验收证据

| 检查 | 结果 |
|---|---|
| Python 基线 | Python 3.11.16 通过 |
| Editable package 安装 | 无网络、关闭 build isolation 时通过 |
| 自动化测试 | 23/23 通过 |
| 编译检查 | `src/`、`scripts/` 和 `tests/` 通过 |
| Smoke record | 共 80 条；每个 split 16 条；每个 split 中每个 family 8 条 |
| 确定性复现 | 固定 provenance 时 JSONL 和完整输出逐字节一致 |
| Target 验证 | 80/80 从 canonical problem 重新计算一致 |
| Graph 验证 | 80/80 通过 DAG 与 trace-consistency 检查 |
| 因子平衡 | 每个请求的 smoke joint factor cell 数量均为 1 |
| Split leakage | semantic、canonical-problem 和 prompt-hash overlap 均为零 |
| Manifest 完整性 | 所有已记录 artifact 的 SHA-256 hash 均通过验证 |
| 隐藏 annotation | 默认 renderer 从不读取或暴露 task-side trace |
| 服务器/模型执行 | 按要求未执行 |

主要本地命令：

```bash
.venv/bin/python -m unittest discover -s tests -v
```

已提交的 smoke artifact 位于 `tests/fixtures/task_calibration_smoke/`；其 manifest 记录
了用于生成它的精确干净 implementation revision。

## 方案偏离与实现选择

- Property-style coverage 使用标准库 `unittest` 中的 deterministic parameter sweep，
  没有新增 Hypothesis。Pytest 仍是可选开发依赖，测试兼容两种 runner。
- 较大的 `task_calibration_v1.yaml` 只完成配置验证，并未执行，符合服务器执行门禁。
- 仓库内的 Conda 环境只用于本地 Python 3.11 验证，并被 Git 忽略。

## 独立性与限制

- Function-composition 验证从 canonical mapping 和 query 重新计算结果，但不可避免地
  使用 generator 输出的同一 mapping representation。
- Relational verification 通过 graph search 完成，并忽略已存储的 relevance flag 和
  target，因此独立性更强。
- Semantic ID 排除了 template、vocabulary、answer encoding 和 presentation order。
  但 function family 尚未在抽象域 symbol 的所有可能 renaming 下对问题进行 canonicalize。
  后续 leakage audit 应决定科学上是否需要这种更强的 isomorphism equivalence。
- 短 relational chain 的 semantic support 较小。因此，延后的较大配置对每个交叉
  factor cell 只生成一个 record，并且任何 scale increase 前都必须审计。
- 这些测试证明 generator 的工程正确性，不证明所选任务足以诱发目标模型的多步推理。

## 延后的服务器验证

未执行任何服务器操作。`SERVER.md` 补全且执行获得明确授权后：

1. 重建提交中记录的环境；
2. 重新运行完整测试；
3. 在 scratch storage 中运行两次 `task_calibration_v1.yaml`；
4. 比较 hash 并重新验证每个 record；
5. 记录 runtime、peak RAM、storage size、environment 和 Git revision。

## 研究交接

下一次讨论应校准两个 task family 是否都能在候选冻结模型中可靠诱发多步行为，并在
规划任何 activation-capture 实现前解决 O-001、O-002、O-004 和 O-008。
