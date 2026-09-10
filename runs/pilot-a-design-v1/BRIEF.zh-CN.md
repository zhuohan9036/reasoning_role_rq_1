# 任务需求：pilot-a-design-v1

> English: [BRIEF.md](BRIEF.md)

**状态：** 实施前暂停；由 target-grounding 审核取代
**研究范围：** Pilot A 任务设计与实施交接

## 期望结果

把当时拟议的 Pilot A 科学设计转化为可审核的实施合同，同时不把现有 task generator 当作
权威。后续实施将创建新的受控 task language、matched task cell、negative control、相互
独立的 discovery/confirmation 数据和本地验证。

本 brief 作为规划历史保留。Pilot A0 随后指出该设计缺少与预期目标任务总体的显式桥梁。
没有授权实施；见 `runs/pilot-a0-target-grounding-v1/PLAN.zh-CN.md`。

## 已冻结要求

1. Pilot A 只用于 pattern discovery 与 measurement validation。
2. 结论上限限制在具名 model、task distribution 和 response regime 内。
3. Task language 是临时实验仪器，不作完备性主张。
4. 核心设计交叉 serial/fork-join topology 与 externally supplied/computed control。
5. Structural node family 与 functional subtype 分开。主要 comparison 在 matched
   signature 内比较 `shift/reflect`、`add_merge/subtract_merge`、`parity/upper_half` 和
   `select_if/select_unless`。Direct-read 继续作为 negative control。
6. Surface、value、position、length 和 answer variable 必须平衡或显式控制。
7. Discovery 与 untouched confirmation 使用 semantic-disjoint identity。
8. 排除 Qwen；当前工作默认是冻结的 Mistral 7B instruct model，执行前必须提供 immutable
   exact revision。
9. 现有 task generator 是非权威校准 artifact；只能按照已接受设计决定复用、替换或绕过。

## 后续代码实施的验收标准

- Deterministic reference solver 验证每个 instance 与 event trace。
- 所有任务 cell 和 paired rendering 满足声明的 balance。
- Discovery、confirmation 和 control pool 在语义上互不重叠。
- Operation 显示名称不泄漏 computation identity。
- Functional subtype 不能由 signature、graph degree、event index、prompt region、output
  token 或 task cell 确定性恢复。
- 每个核心 program 固定包含六个 answer-relevant node。
- R1 在固定 delimiter slot 中输出六个值，并测量每个值之前 delimiter 位置的 residual
  stream。
- 实现并报告简单 shortcut heuristic。
- 除非获批方案明确替换，现有 calibration fixture 继续通过。
- 本地测试不接触 model、tokenizer 或 server。

## 当前规划动作的范围外事项

- 修改源代码、测试、配置或 fixture。
- 下载或运行模型。
- Activation capture 或分析。
- 服务器执行。
- Commit 或 push。
