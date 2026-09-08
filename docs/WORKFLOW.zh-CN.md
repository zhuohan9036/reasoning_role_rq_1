# 从讨论到执行的工作流

> English: [WORKFLOW.md](WORKFLOW.md)

## 目的

本项目把研究讨论、计划生成、代码实施和服务器执行划分为需要分别授权的阶段。一次有
价值的讨论、一个看似合理的动作、一份获批方案和一次获得授权的实验，并不是同一个
决定。

Assistant 不得因为用户赞同某个 idea、认可较早阶段、仓库或方案已经存在，便推断后续
阶段也获得了授权。

## 状态模型

| 状态 | 允许的工作 | 对仓库的影响 | 离开条件 |
|---|---|---|---|
| `DISCUSSING` | 多轮研究与工程讨论；比较替代方案；识别不确定性 | 无，除非另行明确授权文档修改 | Assistant 提供动作预告 |
| `ACTION_AWAITING_APPROVAL` | 澄清或修改拟议的规划动作 | 无 | 用户明确授权生成计划 |
| `PLAN_GENERATION_AUTHORIZED` | 固化已同意的 brief 并生成规划 artifact | 只涉及动作预告列出的文件和 Git 行为 | 规划 artifact 完成验证并报告 |
| `PLAN_AWAITING_REVIEW` | 回答问题和修改方案 | 只修改计划/文档 | 用户明确批准实施 |
| `IMPLEMENTATION_AUTHORIZED` | 实现获批范围并执行获批本地检查 | 获批的代码、测试、配置、文档和已声明 Git 动作 | 本地验收和 review 完成 |
| `IMPLEMENTATION_REVIEW` | 展示变更、测试、偏离、限制和审核路径 | 除非进一步授权，只做 review 修正 | 用户接受、要求修改或讨论下一动作 |
| `SERVER_AWAITING_APPROVAL` | 准备精确 run 预告和命令，但不执行 | 只修改服务器方案/配置 | 用户授权具名 server run 或命令范围 |
| `SERVER_AUTHORIZED` | 只执行已授权的服务器范围 | 服务器端输出和声明的小型 handoff | Run 停止、完成、失败或到达新门禁 |
| `RESULT_REVIEW` | 只读验证传回的证据并讨论解释 | 不写仓库；只检查被忽略的本地 handoff 或获批挂载路径 | 用户接受解释、要求更多证据或授权报告动作 |
| `RESULT_REPORT_AUTHORIZED` | 创建获批的小型结果报告，并且只提升已声明的证据 | `results/<run-id>/` 中已声明的文件和已披露 Git 行为 | 报告完成验证并交回审核 |

如果当前状态或用户指令存在歧义，必须停留在更早、授权更少的状态，并只询问一个聚焦
问题。

## 先讨论规则

每个候选研究或代码任务都从 `DISCUSSING` 开始。用户与 assistant 可以根据需要多轮
往返。在这一阶段，assistant 可以：

- 重述研究问题和相互竞争的解释；
- 提出或批评 method、control、baseline、task 和 metric；
- 识别隐藏 assumption、confound、dependency 和 server unknown；
- 比较不同任务边界和验收标准；
- 在对话中总结暂时共识与未解决问题。

仅有讨论不授权创建 `BRIEF.md`、`PLAN.md`、`plan.json`，不授权修改代码、下载、会改变
项目 artifact 的本地执行、Git 操作或服务器执行。

## 必需的动作预告

生成计划前，assistant 必须发布一个清晰可见的动作预告，包含以下全部字段：

1. action ID 和 task ID；
2. 当前状态与请求进入的下一状态；
3. 拟议的具体动作；
4. 研究目标和有边界的结果；
5. 将被固化的讨论共识；
6. 仍保持开放的事项和 assumption；
7. 要创建或修改的精确文件；
8. 中文、英文和结构化的主要审核路径；
9. 将执行的 validation；
10. Git 行为：不提交、只本地提交，或提交并推送；
11. 明确的范围外事项，包括适用时的代码、下载、本地模型执行和服务器执行；
12. 正在请求的授权语句。

推荐格式：

```text
【动作等待授权】

动作 ID：<action-id>
任务 ID：<task-id>
动作类型：只生成实施规划
将执行：<有边界的描述>
将固化的共识：<讨论摘要>
仍未解决：<开放事项>

产出：
- runs/<task-id>/BRIEF.md
- runs/<task-id>/BRIEF.zh-CN.md
- runs/<task-id>/SERVER.md
- runs/<task-id>/SERVER.zh-CN.md
- runs/<task-id>/PLAN.md
- runs/<task-id>/PLAN.zh-CN.md
- runs/<task-id>/plan.json

主要审核入口：
- 中文：runs/<task-id>/PLAN.zh-CN.md
- 英文：runs/<task-id>/PLAN.md
- 结构化：runs/<task-id>/plan.json

验证：<检查项>
Git 行为：<不提交 | 提交到本地 | 提交并推送>
不会执行：<明确的范围外事项>
请求授权语句：“认可该动作，生成计划。”
```

用户可以修改任意字段。在用户明确接受最终动作预告前，不执行该动作。

## 规划授权与产物

推荐授权语句：

```text
认可该动作，生成计划。
```

含义明确的等价表达也可以接受。该授权只覆盖动作预告列出的文件、validation 和 Git
行为。

规划动作通常产生：

- `BRIEF.md` 和 `BRIEF.zh-CN.md`：冻结后的讨论结果，即用户真正需要的结果、验收标准、
  边界和已经解决的选择；
- `SERVER.md` 和 `SERVER.zh-CN.md`：已知环境事实、未知项，以及本地/服务器验证划分；
- `PLAN.md` 和 `PLAN.zh-CN.md`：供人审核的实施提议；
- `plan.json`：唯一的机器可读实施契约；
- 若动作预告已声明，可有限同步更新 `DECISIONS` 或 `PROGRESS`。

在实施获批前，规划文件状态必须为 `awaiting_review`。完成回执必须链接精确审核路径，
并明确说明没有接触代码、下载、模型和服务器。

## 实施授权

推荐授权语句：

```text
方案通过，开始实现。
```

含义明确的等价表达也可以接受。实施授权只覆盖已审核方案中的范围内文件和本地检查。
它不授权：

- 扩大范围；
- 未被明确包含的真实模型下载或执行；
- 远程或服务器命令；
- 破坏性数据操作；
- 方案或动作预告中没有披露的 Git 动作。

实施以 `REVIEW.md` 和 `REVIEW.zh-CN.md` 结束，其中记录已交付文件、测试、偏离、限制、
没有执行的动作、commit/push 状态和下一门禁。

## 服务器授权

服务器执行始终单独授权。请求服务器授权前，assistant 必须提供：

- run ID 和 research task ID；
- exact code commit 与 clean/dirty state 要求；
- configuration 和 dataset hash；
- exact model 和 tokenizer revision；
- server destination 和 output root；
- exact command 或有边界的 command sequence；
- 预计资源与 stopping condition；
- resume/retry behavior；
- output、大文件策略和 handoff package；
- activation capture 是否在范围内。

推荐授权语句：

```text
授权服务器运行 <run-id>，命令范围按上述说明执行。
```

对一次 run 的授权不涵盖后续 run、改变配置的 retry、额外 model、activation capture 或
后续实验。

## 完成回执契约

每一个已授权动作结束时，assistant 必须报告：

1. 完成的动作及其 ID；
2. 实际执行的事项；
3. 明确未执行的事项；
4. 每个产物及其审核路径；
5. validation result 与已知 failure；
6. 相对获批动作或方案的 deviation；
7. Git commit 与 remote synchronization 状态；
8. 科学解释边界；
9. 下一步所需的精确授权。

完成回执用于导航；文件才是持久的权威来源。

## Git 行为

Git 行为绝不隐含。每个动作预告必须说明将：

- 保持变更未提交，供本地审核；
- 只创建本地 commit；
- 或创建 commit 并推送到具名 remote branch。

规划授权与实施授权只覆盖已披露的 Git 行为。大型服务器 artifact 永不进入 Git；参见
`SERVER_HANDOFF.md`。
