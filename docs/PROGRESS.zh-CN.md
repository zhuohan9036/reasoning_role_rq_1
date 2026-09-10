# 进度与证据日志

> English: [PROGRESS.md](PROGRESS.md)

## 里程碑

| 里程碑 | 状态 | 证据/产物 | 下一门禁 |
|---|---|---|---|
| P0：仓库与规划框架 | 已完成并推送 | 研究方案与仓库历史 | 无 |
| P0b：任务 formalism 与 Codex 交接规格 | 已完成并推送 | `runs/research-specification-v1/REVIEW.md`；revision `901507d` | 无 |
| P0c：候选 Pilot A calibration sandbox | 协议 v0.2 已写入；实施暂停 | `docs/PILOT_A.zh-CN.md`；`runs/pilot-a-design-v1/PLAN.zh-CN.md` v2 | Pilot A0 grounding |
| P0d：Pilot A0 native-source 与 model-first 方案 | 协议 v0.2、方案 v2 已生成；等待审核 | `docs/PILOT_A0.zh-CN.md`；`runs/pilot-a0-target-grounding-v1/PLAN.zh-CN.md` | 解决 source provenance/access 选择 |
| P1：任务侧校准数据集 | 已完成并推送 | `runs/task-modeling-v1/REVIEW.md`；smoke fixture | 研究审核 |
| P2a：行为校准框架 | 已完成并推送 | `runs/behavioral-calibration-v1/REVIEW.md`；fake smoke fixture | 研究审核与工作规范更新 |
| P2b：真实模型行为 pilot | 阻塞 | 尚无模型运行 | 完成 grounded Pilot A 设计，再解决模型/服务器要求 |
| P2c：instrumentation baseline | 未开始 | 无 | 行为门禁以及 O-004/O-008 |
| P3：模型侧模式发现 | 未开始 | 无 | 冻结 discovery/evaluation protocol |
| P4：function-versus-structure 检验 | 未开始 | 无 | 通过 leakage 与 confound audit |
| P5：稳定性与跨任务迁移 | 未开始 | 无 | 冻结 task-pair rationale |
| P6：第二模型复现 | 未开始 | 无 | 选择最小的决定性复现集合 |

## 当前任务

`pilot-a0-target-grounding-v1` 现包含 protocol v0.2 与 plan v2，规定 no-annotation source
inventory 和 model-first 路线：benchmark-faithful native inference、activation/transition
trajectory、label-free within-task discovery、冻结的 cross-task transfer，以及后续有边界的
interpretation。GSM8K、DROP、MuSiQue-Ans v1.0 与两个 BIG-Bench task 是已接受的初始
source stratum。准确 source revision、license、split reservation 与 access 仍待决定。实施、
benchmark inspection/download、代码、模型、activation、服务器、commit 与 push 均未授权。

新的 manual annotation 与 synthetic task construction 被冻结为 fallback tool。名为
`RQ1 文献差异性追踪` 的 recurring app automation 已启用，只报告实质相关的新研究或方法
变化；日常项目工作中遇到的相关工作也必须主动提示。

`pilot-a-design-v1` 记录 protocol v0.2 和 plan v2。Functional subtype 只在 matched
structural signature 内比较；每个核心 program 固定包含六个 answer-relevant node；R1
measurement 固定在每个 predicted state symbol 之前的 delimiter。方案保留四个
topology/control cell、negative control、discovery/confirmation 分离和分阶段门禁。Qwen
已排除。现有 generator 是非权威 artifact。由于尚未建立与目标总体的连接，该任务设计现
为候选 calibration sandbox；其实施方案已在代码修改前暂停。

`research-specification-v1` 于 2026-09-09 完成实施、审核、commit 与 push，revision 为
`901507d`。它形式化任务侧对象，区分 pilot 启发的 construct 定义与独立确认，并定义规划
对话到 Codex 的文档交接。它没有修改 executable code，也没有产生经验性证据。

`task-modeling-v1` 于 2026-09-08 获批并在本地完成，包含两个 calibration family、隐藏
的任务侧中间 annotation 和 Python 3.11 支持。这两个 family 是工程 artifact，而不是
已接受的 Pilot A 科学任务。较大的配置以及所有服务器/模型实验均未执行，也未获得授权。

`behavioral-calibration-v1` 于 2026-09-08 获批并在本地完成，采用 final-answer-only
prompt、通用 Hugging Face adapter 和临时阈值。80-record 离线假后端运行只验证框架。
下载与真实模型/服务器运行仍未授权。

## 经验结论

无。当前文档记录的是方案，不是经验性证据。

成功的数据 smoke test 与行为 fake smoke test 都只是工程验证，不能作为支持或否定
Transformer 中功能分化的证据。

## 文档同步

2026-09-08，仓库中 17 份面向人的 Markdown 文档均已配对以 `.zh-CN.md` 结尾的同步
中文版本，并加入双向语言链接。机器可读契约和生成 artifact 继续保持单一来源。

同一次更新还确立了相互独立的讨论、计划生成、实施和服务器 run 授权，并为大型服务器
结果规定了被 Git 忽略的本地交接路径。没有启动新研究计划、模型运行或服务器操作。

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
