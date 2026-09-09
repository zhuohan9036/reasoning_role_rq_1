# 实施方案：research-specification-v1

> English: [PLAN.md](PLAN.md)

**状态：** 已实施并通过本地验证；等待人类审核
**方案版本：** 1
**文档修改授权：** 是，仅限本地且保持未提交
**代码修改授权：** 否
**服务器执行授权：** 否

## 1. 目标

修订研究与工作流文档，使任务侧计算对象具有明确结构、证据地位得到清楚说明，并使规划
对话能够把一个已批准、有边界的合同交给 Codex，而不隐含授权实施。

## 2. 提议的任务侧 formalism

研究规格将定义以下带版本的外部对象。精确数学记号可以在实施时调整，但下列语义区分
必须保留。

### 任务族规格

一个 task family specification 包含：

- instance space 以及生成或采样分布；
- input、query、output 和 correctness semantics；
- reference-solution interface；
- 将 canonical instance 映射为 prompt 的 rendering family；
- controlled factor 与 nuisance variable；
- semantic identity 与 split rule；
- 一种明确声明的 reference dependency structure；
- version identifier 与 provenance。

Task family 是外部研究对象。它不表示模型使用相同变量或遵循 reference solver。

### Canonical task instance

一个 canonical instance 包含：

- task-family 和 schema version；
- canonical problem 与 query；
- 由任务正确性语义定义的 target；
- controlled variable 与 nuisance variable；
- 在适用范围内独立于 rendering 的 semantic identity；
- reference dependency structure 及其 provenance；
- 零个或多个临时 task-side annotation；
- 与 canonical identity 分开产生的一个或多个 rendered prompt。

### Reference dependency structure

文档将区分三种允许的表示：

1. 某一个明确 reference solver 的 graph；
2. 一组或一族有效 solution graph；
3. 某个明确限定的有效解法类别共同满足的 partial-order constraint。

所选表示必须说明 node、edge、intermediate state 和 execution semantics 的含义。在没有
独立证据时，不得称其为模型 graph 或唯一必需算法。

### Candidate operation 与 correspondence

Candidate operation 是对 node 或 transition 提出的临时 task-side equivalence claim。
必须说明其 identity criterion、granularity、scope 和 version。它可以由理论、任务语义或
探索性证据启发，但不是模型侧发现。

Task-side cross-task correspondence 是一项预先规定的假设：两个任务侧 operation 共享
某种相关计算性质。Model-side empirical correspondence 是另一类结果，需要独立测量的
pattern、结构性 control、held-out evaluation、不确定性以及适当的 negative-control
comparison。

## 3. 分阶段承诺规则

在 exploratory pilot 前，一个任务必须具有足以确定 instance、answer、provenance、
rendering 和主要结构 covariate 的薄规格。细粒度 operation label 与 cross-task mapping
可以暂不设定。

探索性模型证据可以启发修订后的 task decomposition 或 role vocabulary。每一次这类修订
都必须记录启发它的证据、获得新版本，并在 confirmatory evaluation 前冻结。用于定义或
选择 construct 的证据，不能同时被报告为该 construct 的独立确认。

后续实施将要求通过以下一种或多种方式进行 held-out evaluation：未参与定义的 instance、
held-out structural condition、新 task pair 或额外冻结模型。精确 partition 仍由未来具体
实验方案决定。

## 4. 规划到 Codex 的交接

工作流和仓库指令将定义以下职责：

1. **规划对话：** 讨论科学与工程问题，识别开放选择，在不修改仓库的情况下冻结有边界
   的共识。
2. **计划生成门禁：** 展示动作预告并获得明确批准后，Codex 才能创建或修改规划产物。
3. **Codex 规划产物：** 生成中英文 `BRIEF`、`SERVER`、`PLAN` 和一个 `plan.json`，状态
   均为 `awaiting_review`。
4. **人类审核：** 接受、拒绝或修改方案。非正式赞同一个想法不授权实施。
5. **Codex 实施：** 获得第二次明确批准后，只修改获批文件、只运行获批检查；出现偏离时
   必须记录，不得静默扩展范围。
6. **Review 交接：** 生成中英文 `REVIEW`，报告实际修改、检查、未执行事项、Git 状态、
   科学边界和下一门禁。
7. **服务器分离：** 每个有边界的服务器 run 都需要另一项具名授权。

该合同以文档和状态为基础，因此即使规划与实施发生在不同客户端，也仍然可以审核。

## 5. 实施获批后的计划修改

| 路径 | 动作 | 目的 |
|---|---|---|
| `docs/RESEARCH.md` 与 `.zh-CN.md` | 修改 | 增加结构化任务侧对象、分阶段承诺和 correspondence 区分 |
| `docs/WORKFLOW.md` 与 `.zh-CN.md` | 修改 | 定义规划对话到 Codex 的交接与 review 职责 |
| `docs/DECISIONS.md` 与 `.zh-CN.md` | 修改 | 记录已接受 formalism、证据地位和交接决策 |
| `docs/PROGRESS.md` 与 `.zh-CN.md` | 修改 | 记录规格审核状态，不声称经验进展 |
| `AGENTS.md` 与 `AGENTS.zh-CN.md` | 修改 | 使交接和任务侧术语成为未来 Codex 工作的操作约束 |
| `runs/research-specification-v1/REVIEW.md` 与 `.zh-CN.md` | 创建 | 记录交付、验证、偏离和下一门禁 |

不包含任何源代码、测试、配置、fixture 或生成 artifact。

## 6. 实施顺序

1. 增加术语，区分 workflow task 与 reasoning task。
2. 增加 task-family、canonical-instance 和 dependency-structure formalism。
3. 增加 candidate-operation 与两层 correspondence 区分。
4. 增加薄规格、探索性细化、冻结和 held-out confirmation 规则。
5. 更新证据阶段，但不选择最终 task 或 method。
6. 把规划到 Codex 的交接合同加入工作流文档和 agent 指令。
7. 追加已接受决策，不改写历史理由。
8. 把进度更新为文档里程碑，而不是经验性证据。
9. 创建同步的中英文实施 review。

## 7. 验证

- 解析 `plan.json` 并检查其与本方案逐项一致。
- 确认每一份面向人的 Markdown 都有同步 counterpart 和双向语言链接。
- 搜索 task、operation、correspondence、model-side 和因果术语的不一致用法。
- 确认没有把 reference graph 变成模型机制。
- 确认 pilot 启发的 construct 需要独立 held-out confirmation。
- 确认修改路径符合获批 allowlist。
- 检查 `git diff --check` 和仓库状态。
- 因为范围内没有 executable code，不运行测试套件。

## 8. 开放的实施选择

- 数学表示可以采用 tuple、typed schema 或 prose-plus-schema，只要所有必需语义明确。
- 研究文档可以把三种 dependency representation 作为通用接口，而不在全项目中只选择
  一种。
- 未来实验方案将选择精确 exploratory/confirmatory split 和 reviewer-independence
  procedure。
- 未来代码任务必须分别声明 branch、commit 和 push 行为；本任务不制定统一 Git 政策。

## 9. 范围外

- 实现或修改 task generator。
- 改写现有 fixture schema。
- 选择 shared operation 或最终 task pair。
- 选择模型侧 measurement 或 analysis method。
- 运行测试、模型、实验、下载或服务器命令。
- 未经单独授权创建 Git commit 或 push。

## 10. 审核门禁

本方案不授权实施文档修改。审核中文、英文或结构化方案后，用户可以使用以下语句批准
实施：

```text
方案通过，开始实现。
```

含义明确的等价指令也可以接受。实施授权只覆盖本文列出的路径、验证、范围外事项和 Git
行为。
