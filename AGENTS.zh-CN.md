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
- 当方案状态为 `awaiting_review` 时，不得开始实现。
- 方案获批后，只实现已批准的范围；任何偏离都写入任务 REVIEW，不得静默扩展。
- 未经用户明确授权，不得启动远程或服务器实验。
- 每个实施任务都必须以测试和 `runs/<task-id>/REVIEW.md` 收尾。

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
