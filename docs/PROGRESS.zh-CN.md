# 进度与证据日志

> English: [PROGRESS.md](PROGRESS.md)

## 里程碑

| 里程碑 | 状态 | 证据/产物 | 下一门禁 |
|---|---|---|---|
| P0：仓库与规划框架 | 已完成并推送 | 研究方案与仓库历史 | 无 |
| P1：任务侧校准数据集 | 已完成并推送 | `runs/task-modeling-v1/REVIEW.md`；smoke fixture | 研究审核 |
| P2a：行为校准框架 | 已完成并推送 | `runs/behavioral-calibration-v1/REVIEW.md`；fake smoke fixture | 研究审核与工作规范更新 |
| P2b：真实模型行为 pilot | 阻塞 | 尚无模型运行 | 解决 O-001/O-002/O-009/O-013 并授权服务器 |
| P2c：instrumentation baseline | 未开始 | 无 | 行为门禁以及 O-004/O-008 |
| P3：模型侧模式发现 | 未开始 | 无 | 冻结 discovery/evaluation protocol |
| P4：function-versus-structure 检验 | 未开始 | 无 | 通过 leakage 与 confound audit |
| P5：稳定性与跨任务迁移 | 未开始 | 无 | 冻结 task-pair rationale |
| P6：第二模型复现 | 未开始 | 无 | 选择最小的决定性复现集合 |

## 当前任务

`task-modeling-v1` 于 2026-09-08 获批并在本地完成，包含两个 pilot family、隐藏的任务侧
中间 annotation 和 Python 3.11 支持。较大的配置以及所有服务器/模型实验均未执行，也
未获得授权。

`behavioral-calibration-v1` 于 2026-09-08 获批并在本地完成，采用 final-answer-only
prompt、通用 Hugging Face adapter 和临时阈值。80-record 离线假后端运行只验证框架。
下载与真实模型/服务器运行仍未授权。

## 经验结论

无。当前文档记录的是方案，不是经验性证据。

成功的数据 smoke test 与行为 fake smoke test 都只是工程验证，不能作为支持或否定
Transformer 中功能分化的证据。

## 文档同步

2026-09-08，仓库中 15 份面向人的 Markdown 文档均已配对以 `.zh-CN.md` 结尾的同步
中文版本，并加入双向语言链接。机器可读契约和生成 artifact 继续保持单一来源。

## 已完成任务：task-modeling-v1

- 日期：2026-09-08。
- 研究目标：G0；为后续 G2–G4 检验提供基础设施。
- 实现 revision：`d574c3e`；经审核 fixture 的 source revision 为 `2d139b1`。
- 产物：`tests/fixtures/task_calibration_smoke/manifest.json`。
- 结果：生成并独立复核 80 条 record；deterministic replay、graph validation、balance
  check 和 cross-split overlap audit 全部通过。
- 解释：任务侧校准接口已在本地可用；没有检验任何模型侧结论。

## 已完成任务：behavioral-calibration-v1

- 日期：2026-09-08。
- 研究目标：G0 行为校准；G1–G4 的前置条件。
- 实现 revision：`4797581` 和 `17fda49`；fake fixture 由干净 revision `17fda49`
  生成。
- 产物：`tests/fixtures/behavioral_smoke/run_manifest.json`。
- 结果：80/80 个尝试 record 完整对账；deterministic replay、strict parsing、
  resume/provenance rejection、summary denominator 和 stubbed frozen-model adapter
  contract 均通过本地检查。
- 解释：评估框架已在本地可用。假后端的 75% exact-match 是有意构造的合成结果，
  不是模型证据，也不是研究门禁失败。
- 延后事项：选定 immutable model/tokenizer revision，补完服务器规格，授权下载与执行，
  并运行真实行为 pilot。

## 更新模板

每个完成的任务或实验应追加：

- 日期与 run ID；
- 研究目标与被检验 claim；
- exact configuration 和 code revision；
- artifact location 与 checksum；
- 计划内与计划外 deviation；
- 带不确定性的结果；
- 证据能够支持的最弱解释；
- failed check、alternative explanation 和下一决策。
