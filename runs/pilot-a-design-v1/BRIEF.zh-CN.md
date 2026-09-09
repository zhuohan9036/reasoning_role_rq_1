# 任务需求：pilot-a-design-v1

> English: [BRIEF.md](BRIEF.md)

**状态：** 规划产物已生成；实施等待审核
**研究范围：** Pilot A 任务设计与实施交接

## 期望结果

把已接受的 Pilot A 科学设计转化为可审核的实施合同，同时不把现有 task generator 当作
权威。后续实施将创建新的受控 task language、matched task cell、negative control、相互
独立的 discovery/confirmation 数据和本地验证。

## 已冻结要求

1. Pilot A 只用于 pattern discovery 与 measurement validation。
2. 结论上限限制在具名 model、task distribution 和 response regime 内。
3. Task language 是临时实验仪器，不作完备性主张。
4. 核心设计交叉 serial/fork-join topology 与 externally supplied/computed control。
5. Candidate computation 为 transform、merge、predicate 和 select，并设置 direct-read
   negative control。
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
- 实现并报告简单 shortcut heuristic。
- 除非获批方案明确替换，现有 calibration fixture 继续通过。
- 本地测试不接触 model、tokenizer 或 server。

## 当前规划动作的范围外事项

- 修改源代码、测试、配置或 fixture。
- 下载或运行模型。
- Activation capture 或分析。
- 服务器执行。
- Commit 或 push。

