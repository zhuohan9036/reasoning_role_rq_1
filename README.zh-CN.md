# Reasoning Role RQ1

> English: [README.md](README.md)

本仓库用于开展一项刻画性研究：冻结的预训练 Transformer 在执行多步推理时，
是否会呈现稳定的功能分化（functional differentiation）。

本项目刻意区分以下三个层面：

- 任务侧对所需计算的描述；
- 从模型内部计算中测得的模型侧模式；
- “可复用的推理角色（reasoning role）”等更强解释。

当前仓库包含初始研究方案、已经批准的任务校准里程碑，以及在本地通过验证的
行为评估框架。目前尚未完成 activation 分析或任何真实模型实验。

## 当前工作流状态

1. 研究方案已经起草。
2. `task-modeling-v1` 已在 Python 3.11 环境中完成本地实现与验证。
3. `behavioral-calibration-v1` 已使用离线假后端完成本地实现与验证；这些仅属于
   工程证据。
4. 真实模型下载和服务器执行仍未获得授权，也尚未启动。

## 仓库结构

- `docs/RESEARCH.zh-CN.md`：研究问题、假设、证据方案和范围。
- `docs/DECISIONS.zh-CN.md`：已接受的决策、工作假设和待定选择。
- `docs/PROGRESS.zh-CN.md`：里程碑和证据日志。
- `docs/WORKFLOW.zh-CN.md`：讨论、规划、实施和授权门禁。
- `docs/SERVER_HANDOFF.zh-CN.md`：小型服务器结果传递与审核契约。
- `runs/<task-id>/BRIEF.zh-CN.md`：一个有边界任务的实际目标。
- `runs/<task-id>/SERVER.zh-CN.md`：执行环境假设与未知项。
- `runs/<task-id>/PLAN.zh-CN.md`：人类可读的实施方案。
- `runs/<task-id>/plan.json`：结构化实施契约。
- `artifacts/server-results/<run-id>/`：从服务器复制回本机、被 Git 忽略的交接包。
- `results/<run-id>/`：经过审核的小型证据和中英文结果报告。

所有面向人的 Markdown 文档都具有以 `.zh-CN.md` 结尾的同步中文版本。
`plan.json` 等机器可读文件继续保持单一权威版本。

大型数据集、模型权重、activation dump、完整实验日志不得提交到 Git。Git 中只
提交小型 manifest、汇总结果、图表，以及复现实验所需的精确配置。
