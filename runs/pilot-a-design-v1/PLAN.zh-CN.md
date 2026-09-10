# 实施方案：pilot-a-design-v1

> English: [PLAN.md](PLAN.md)

**状态：** 实施前暂停；不具备实施批准资格
**方案版本：** 2
**科学协议：** `docs/PILOT_A.zh-CN.md`，版本 0.2
**代码修改已授权：** 否
**模型或服务器执行已授权：** 否

## 1. 目标

> 本方案作为规划历史保留。Pilot A0 必须在任何元素重新进入科学 Pilot A 方案前建立
> target-task grounding。不得实施本方案。见
> `runs/pilot-a0-target-grounding-v1/PLAN.zh-CN.md`。

独立于现有校准任务选择，实现当时拟议的 Pilot A task instrument。实施必须生成
deterministic typed program、四个 matched structural cell、direct-read control、paired
rendering、semantic-disjoint discovery/confirmation split、本地 shortcut audit 和紧凑
fixture。不得加载或运行语言模型。

## 2. 步骤 1：冻结机器可读 task specification

创建带版本的 Pilot A 配置，固定：

- canonical 层面的 `Symbol8` 与 `Boolean` encoding；
- structural signature、matched functional subtype 及其精确 semantics；
- 参数集合和退化 program 拒绝规则；
- 准确的六节点 C1–C4 graph template；
- balancing axis 与目标 count；
- direct-read control construction；
- rendering family 与 operation-name randomization；
- discovery、confirmation 和 control split rule；
- generator version、seed policy 和 schema version。

在选定模型 revision 前，tokenizer-dependent display symbol 是显式未解决的 rendering
字段。本地测试使用声明的 placeholder symbol bank，不声称与模型兼容。

## 3. 步骤 2：实现 typed canonical program

引入 typed program node 和 validation，强制 input/output type、acyclicity、唯一输出、完整
dependency reference、deterministic execution 和 event-trace agreement。每个 program 同时
记录完整 presented graph 与 answer-relevant reference graph，防止 distractor 或 control
material 静默变成 active computation。

Reference interpreter 只执行 canonical semantics。它不得解析自然语言 prompt，也不得
编码模型如何执行的假设。

## 4. 步骤 3：实现 matched-cell generator

从显式 graph template 生成 C1–C4：

- C1：serial dependency，externally supplied control；
- C2：fork-join dependency，externally supplied control；
- C3：serial dependency，intermediate-state predicate；
- C4：fork-join dependency，intermediate-state predicate。

在每项有效 contrast 内，匹配 node count、逻辑允许时的 structural-signature multiset、
functional-subtype frequency、answer frequency、parameter frequency、operation placement、
prompt budget 和 rendering count。
所有剩余 mismatch 必须记录为 factor，不能宣称完美匹配。

拒绝 constant-output、unused-active-node、unreachable-output、duplicate-semantic、
trivial-copy 和其他退化核心 program。Direct-read control 必须有意构造，不能由退化实例
偶然产生。

## 5. 步骤 4：实现无语义泄漏的 rendering

每个核心 canonical instance 提供两个 paired rendering：

1. neutral symbolic order；
2. renamed and reordered surface form。

Operation 显示名称独立于 operation semantics 采样。Template 暴露求解所需信息，但不暴露
任务侧 category 名称。Renderer 保持 canonical identity 与 target，并记录准确 template、
vocabulary、order 和 name-map provenance。

Aligned-trace 与 final-answer prompt 作为不同 render mode。R1 必须在固定 delimiter slot
中准确渲染六个 state value，并提供每个 event 到其 value 之前 delimiter 的机器可读映射。
本任务不实现 activation capture。

## 6. 步骤 5：创建抗泄漏数据集

生成：

- 1,024 个 discovery canonical instance：每个 `cell x final answer` 32 个；
- 1,024 个具有相同平衡的 semantic-disjoint confirmation instance；
- 至少 512 个 direct-read control instance；
- 每个核心 instance 两个 paired rendering。

每个核心 program 固定包含六个 answer-relevant node。按照协议平衡 C1–C4 和全部八种
final answer。Program-length generalization 延后。在 rendering 前按 semantic identity
切分。分别审计 canonical、prompt、parameter 和 graph-template overlap。

## 7. 步骤 6：实现 shortcut 与 balance audit

实现 deterministic baseline：answer frequency、direct input copying、last displayed
rule/value、operator-name cue、prompt length 和 task-cell metadata。这些是 dataset audit，
不是模型侧分析。Dataset report 必须展示每个声明 stratum 的 count 与 target distribution，
并列出所有剩余 imbalance。

为每个 functional contrast 加入 identifiability audit。若 label 能够由 structural
signature、graph degree、event index、prompt region、output token 或 task cell 确定性
恢复，则拒绝该 comparison。每项 contrast 的两个 subtype 必须具有完全相同的位置分布，
并同时出现在每个被分析的位置。Unary contrast 必须覆盖至少两个位置。Binary、predicate
和 conditional contrast 可以只占一个位置，但不能支持 position-generalization claim。

## 8. 步骤 7：保留旧校准 artifact，但不赋予权威地位

除非后续审核方案另有规定，不把 `function_composition` 或 `relational_path` 用作 Pilot A
科学 cell。在这个有边界的实施中，保留其代码与 fixture 作为 regression coverage。只有
不会引入旧任务假设时，才能复用共享基础设施。

## 9. 步骤 8：本地验证

执行无网络的 Python 3.11 检查：

- reference-interpreter correctness 与 trace agreement；
- type、graph 和 degeneracy validation；
- 固定 seed 的 deterministic replay；
- 精确 count 与 balance invariant；
- functional-subtype identifiability invariant；
- semantic-disjoint split 与 overlap audit；
- paired-rendering equivalence；
- operator-name independence；
- shortcut-baseline behavior；
- malformed-config rejection；
- 现有 regression suite；
- JSON/YAML validity、双语链接和 `git diff --check`。

只有获得实施批准并通过审核后，才能提交小型 deterministic fixture。完整 pilot dataset
保持为 generated output。

## 10. 拟议文件范围

| 路径 | 动作 | 用途 |
|---|---|---|
| `src/reasoning_role/tasks/pilot_a_program.py` | 新建 | typed program、matched subtype、interpreter、六节点 graph template |
| `src/reasoning_role/tasks/pilot_a_controls.py` | 新建 | direct-read 与 audit control |
| `src/reasoning_role/tasks/schema.py` | 必要时修改 | typed event 与 graph metadata |
| `src/reasoning_role/tasks/registry.py` | 修改 | 注册新 task instrument |
| `src/reasoning_role/data/generate.py` | 修改或由新模块绕过 | 支持非 chain factor schema，且不把旧假设设为规范 |
| `src/reasoning_role/data/pilot_a.py` | 分离更清晰时新建 | Pilot A generation 与 audit |
| `configs/data/pilot_a_v1.yaml` | 新建 | 冻结的本地生成合同 |
| `scripts/generate_pilot_a.py` | 通用 CLI 不足时新建 | checkout-local entry point |
| `tests/tasks/test_pilot_a_program.py` | 新建 | semantics、typing、graph、degeneracy test |
| `tests/data/test_pilot_a_generation.py` | 新建 | determinism、balance、identifiability、split、rendering、shortcut test |
| `tests/fixtures/pilot_a_smoke/` | 新建 | 紧凑 deterministic engineering fixture |
| `docs/DATA.md` 及中文对应版 | 修改 | schema、split 与解释边界 |
| `docs/EVALUATION.md` 及中文对应版 | 修改 | behavior gate 与 response regime |
| `runs/pilot-a-design-v1/REVIEW.md` 及中文对应版 | 实施后新建 | 交付与 validation handoff |

Executor 只有在说明不会重新引入旧 linear-chain factor schema 后，才能在扩展
`generate.py` 与创建独立 Pilot A 模块之间选择。扩大任何路径范围都需要审核。

## 11. 后续门禁

本实施在本地 generation 与 validation 后结束。以下是相互独立的后续动作：

1. 解析准确 Mistral model/tokenizer SHA，并验证 single-token symbol；
2. 创建并审核 behavior-only server run 合同；
3. 运行并审核 behavioral feasibility gate；
4. 创建并审核 R1 residual-stream capture 合同；
5. 根据分别冻结的方案实施 discovery 和 confirmation analysis。

## 12. 已知开放选择

- Mistral checkpoint 与 tokenizer 的 immutable exact revision。
- Llama 用作 alternative pilot 还是后续 replication model。
- Tokenizer-compatible render symbol bank。
- 模型侧分析的准确 regularization、score、uncertainty estimator、clustering method 和
  multiplicity policy。
- R2 measurement unit 与 alignment rule。

本方案暂停期间，这些选择均不活动。Target grounding 现在阻塞本 task ID 下的任何本地
canonical-task implementation。

## 13. 审核门禁

本审核门禁已由 `pilot-a0-target-grounding-v1` 取代。本方案不具备实施批准资格。未来 Pilot
A 方案只能复用获得 source-based grounding 并重新明确获批的元素。
