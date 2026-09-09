# 实施审核：research-specification-v1

> English: [REVIEW.md](REVIEW.md)

**状态：** 已实施并通过本地验证；等待人类审核
**审核日期：** 2026-09-09
**Git 行为：** 未提交；未 push

## 结果

已完成获批的纯文档修订。研究规格现在定义了带版本的任务侧对象，允许 pilot 启发的
探索性细化，但要求随后冻结并使用 held-out 证据确认；同时保持任务侧假设与模型侧经验
结果的区分。工作流和仓库指令现在定义了从规划对话到 Codex 的明确文档交接。

未修改 executable code、测试、配置、fixture、生成 artifact、模型或服务器状态。

## 已交付修改

- `docs/RESEARCH.md` 与 `docs/RESEARCH.zh-CN.md`：区分 workflow task 与 reasoning
  task；定义 task-family specification、canonical instance、reference dependency
  representation、candidate operation、两层 correspondence 和分阶段承诺。
- `docs/WORKFLOW.md` 与 `docs/WORKFLOW.zh-CN.md`：定义规划对话、Codex 计划生成、人类
  审核、Codex 实施和 review 交接；增加明确的跨客户端授权格式。
- `docs/DECISIONS.md` 与 `docs/DECISIONS.zh-CN.md`：追加已接受决策 D-016 至 D-018，
  不改写较早理由。
- `docs/PROGRESS.md` 与 `docs/PROGRESS.zh-CN.md`：记录本地文档里程碑，不声称经验进展。
- `AGENTS.md` 与 `AGENTS.zh-CN.md`：使术语、分阶段承诺和跨客户端交接成为未来 Codex
  task 的操作约束。
- 本中英文 review 记录实施情况和下一门禁。

## 验证

- `plan.json` 可以成功解析。
- 每一份面向人的 Markdown 都具有双语 counterpart 和双向语言链接。
- 修订范围内的 task、operation、correspondence、model-side 和因果术语审核通过。
- Reference dependency structure 保持为外部规格，不被描述为模型机制。
- Pilot 启发的 construct 需要版本化、冻结并使用未参与定义的证据确认。
- 修改路径符合获批文档范围，另包含本任务规划产物的生命周期状态更新。
- `git diff --check` 通过。
- 因为 executable code 不在范围内，未运行测试套件。

## 偏离

实施文件表没有列出对现有 `BRIEF`、`PLAN` 和 `plan.json` 的管理性状态更新。为避免已获
授权实施后合同仍被错误标记为 `awaiting_review`，更新了这些 task-local 文件。这没有
改变科学或实施范围。

## 科学边界

本次修订只确立研究定义和治理规则。它不选择最终 task family 或 operation，不确立
cross-task correspondence，不测量模型，也不提供 functional differentiation 或 reasoning
role 的证据。

## 下一门禁

需要人类审核。接受这些本地文档修改，不授权 commit、push、模型下载、实验或服务器动作。

