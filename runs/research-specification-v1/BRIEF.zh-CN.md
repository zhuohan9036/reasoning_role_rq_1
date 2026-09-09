# 任务需求：research-specification-v1

> English: [BRIEF.md](BRIEF.md)

**状态：** 已在本地实施；等待人类审核
**研究范围：** RQ1 任务侧形式化与规划到 Codex 的治理流程

## 期望结果

形成一份可审核的文档修订，使 RQ1 中的任务侧对象具有明确结构，同时不把这些对象视为
模型内部算法。修订还必须定义从规划对话到 Codex 实施任务的清晰交接，并以文档作为
持久接口。

## 必需内容

1. 区分工作流任务、推理任务族、任务实例、任务侧参考结构、候选操作和模型侧模式。
2. 定义最小、带版本的任务族规格和 canonical instance 规格。
3. 定义 reference dependency graph 的语义和证据边界。
4. 当存在多种有效解法时，允许使用单一参考图、有效图集合或共享 partial-order
   constraint。
5. 区分 pilot 前最低限度的任务建模与 pilot 启发的探索性细化。
6. 把 candidate operation 和任务侧 cross-task correspondence 视为假设，而不是模型侧
   经验结果。
7. 要求 pilot 启发的定义在未参与定义的 instance、task condition 或 model 上评估前先
   冻结。
8. 定义规划对话、Codex 计划、人类审核、Codex 实施和 review report 之间的交接。
9. 将最终规则同步写入中英文仓库指令、决策和进度记录。

## 验收标准

1. 研究规格明确说明每个任务侧对象包含什么，以及对象之间如何关联。
2. Prompt rendering 与 canonical task identity 被明确分离。
3. 任务侧参考结构不被描述为模型唯一必需的算法。
4. 允许探索性细化，但不能使用定义它的同一证据完成确认。
5. 任务侧 correspondence hypothesis 与模型侧 empirical correspondence 使用不同术语。
6. 未来 Codex 实施不能仅凭非正式对话开始；必须具有已批准且带版本的计划契约。
7. 所有面向人的 Markdown 修改均保持中英文同步。
8. 实施 review 能够按本 brief 检查每一条修改路径。

## 范围外

- 选择最终 pilot task family。
- 选择模型、tokenizer、activation measurement、clustering method 或统计模型。
- 在本任务中重新标注现有 fixture 或修改数据 schema。
- 修改源代码、测试、配置或生成 artifact。
- 下载或运行模型、服务器执行或 activation capture。
- 声称 candidate operation 或 cross-task correspondence 已经得到经验确认。

## 已冻结的讨论共识

当前 `docs/RESEARCH.md` 尚未作为完整冻结规格予以接受。其核心问题、范围边界、竞争解释
和报告规范已经接受；研究目标和证据阶段继续作为工作路线图。任务侧概念层级和阶段 A
必须先补充结构化 formalism，之后才能接受完整研究规格。

操作交接采用：规划对话冻结需求；Codex 在明确授权后生成可审核计划；用户审核计划；
Codex 仅在第二次批准后实施；最后使用中英文 review 记录交付、验证、偏离和下一门禁。
