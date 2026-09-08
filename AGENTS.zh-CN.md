# 仓库协作说明

> English: [AGENTS.md](AGENTS.md)

## 科学范围

本论文研究冻结的预训练 Transformer 在多步推理中是否表现出稳定的功能分化。
RQ1 是一项刻画性研究。不得把相关性证据表述为因果结论。

在代码、文档和报告中始终保持以下区分：

1. 任务侧计算图描述的是生成器或外部规定的求解过程，并不表示模型内部算法。
2. 观察到的模型侧 cluster 或 pattern 不会自动成为 reasoning role。
3. component identity、layer、token position 和 reasoning step 是潜在混淆因素，
   而不是 functional identity 的定义。
4. candidate operation 是临时标签。没有证据时，不得将其描述为 atomic、
   universal 或 cognitively fundamental。
5. negative、partial、task-specific、distributed 以及随实现变化的结果都是有效结果。

主要证据应来自能够进行机制访问的冻结预训练模型。受控模型或适配模型可以作为
诊断工具，但必须与自然形成的组织结构分开报告。

## 工作流门禁

- 修改代码前阅读 `docs/RESEARCH.md`、`docs/DECISIONS.md` 和相关的
  `runs/<task-id>/` 文件。
- 每次只处理一个边界明确的任务。
- 每个候选任务都从“仅讨论”状态开始。讨论可以多轮往返，但不授权生成规划文件、
  修改仓库、改代码、下载或执行。
- 生成计划前，必须先在对话中提供明确的动作预告，其中写明 task、准备进行的规划
  动作、已冻结的讨论共识、未解决事项、精确产物与审核路径、Git 行为、范围外事项，
  以及正在请求的授权语句。
- 只有用户明确授权规划动作后，才可以生成 `BRIEF.md`、`SERVER.md`、`PLAN.md`、
  对应中文文件和 `plan.json`。规划授权不等于实施授权。
- 当方案状态为 `awaiting_review` 时，不得开始实现。
- 获得明确实施授权后，只实现获批范围和本地检查；任何偏离都写入任务 REVIEW，
  不得静默扩展。
- 远程或服务器执行属于独立门禁。即使实现已获批准，也必须对具名 run 或命令范围
  取得明确授权。
- 每个实施任务都必须以测试和 `runs/<task-id>/REVIEW.md` 收尾。
- 每个规划、实施或服务器结果审核动作结束时，都必须报告实际执行与未执行事项、
  全部产物与审核路径、验证结果、Git commit/push 状态，以及下一项所需授权。
- 完整状态与授权契约见 `docs/WORKFLOW.zh-CN.md`；执行时以同步英文版
  `docs/WORKFLOW.md` 为规范来源。

## 服务器结果交接

- 服务器到本地的结果传递遵循 `docs/SERVER_HANDOFF.zh-CN.md`；执行时以同步英文版
  `docs/SERVER_HANDOFF.md` 为规范来源。
- Git 无法传递未提交的服务器 artifact。小型交接包应放在本机被忽略的
  `artifacts/server-results/<run-id>/`，或者提供一个明确可访问的挂载路径。
- 大型 weight、activation、checkpoint 和完整日志保留在服务器；在
  `artifact_index.json` 中记录服务器位置、大小、checksum、schema 和生成它的 revision。
- 分析前验证 handoff manifest 和 checksum。若小型结果不足，只请求解决问题所需的
  最小额外切片。
- 只把审核后的小型证据和中英文报告提交到 `results/<run-id>/`；绝不提交被忽略的
  handoff bundle 本身。

## 文档语言

- 每一份面向人的 Markdown 文档都必须同时具有英文版和以 `.zh-CN.md` 结尾的
  中文对应版；两种语言必须在同一次变更中保持语义同步。
- 每种语言的文件都必须在顶部附近链接到另一语言版本。
- 代码、配置、生成产物，以及 `plan.json` 等机器可读契约保持单一来源，除非后续
  已批准方案另有要求。

## 可复现性

- 每次实验都必须记录配置、随机种子、数据生成版本、代码 revision、环境和输出
  schema。
- 小型验证 fixture 和汇总结果保存在 Git 中；大型数据、权重、activation、
  checkpoint 和日志保存在 Git 外，并记录其路径、hash 和生成命令。
- 使用 semantic instance identity 防止 split leakage，不能只比较 prompt 字符串。
- 优先使用可以独立检查的 invariant，而不是只有 snapshot 的测试。

## 工程约束

- 除非已批准任务方案另有规定，目标 Python 版本为 3.11。
- 可复用代码放在 `src/`，入口放在 `scripts/`，配置放在 `configs/`，测试放在
  `tests/`。
- 提交的代码和配置中不得嵌入工作站或服务器专属的绝对路径。
- 生成的自然语言 prompt 与 canonical task record 必须分开。
