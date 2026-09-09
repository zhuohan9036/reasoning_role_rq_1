# Pilot A 协议：模式发现与测量验证

> English: [PILOT_A.md](PILOT_A.md)

**状态：** 科学设计已接受；尚未授权代码实施
**协议版本：** 0.1
**最后更新：** 2026-09-09

## 1. 目的与结论上限

Pilot A 是 pattern-discovery and measurement-validation pilot。它考察：在一个有意限制
范围的任务环境中，能否重复测量模型侧 computation pattern；这些 pattern 能否经受结构
控制；以及哪些任务维度最影响这些 pattern。

Pilot A 最多支持如下类型的陈述：

> 在具名冻结模型、response regime 和受控任务分布中，经过已声明的控制后，某个可重复
> 的模型侧 pattern 与临时任务侧 computation category 存在或不存在关联。

它不能确立通用 computational primitive、一般 reasoning role、跨领域普遍性或因果必要
性。它的 task language 是诊断仪器，不是 reasoning ontology 提案。

## 2. 研究问题

Pilot A 依次回答四个问题：

1. 模型能否在不选择性排除 cell 的前提下，以足够高的准确率完成全部核心任务 cell？
2. 任务事件能否与模型测量形成可重复 alignment？
3. 在控制 layer、token position、event index、数值、topology 和 rendering 后，activation
   是否仍能区分临时 computation category？
4. 发现的 pattern 能否保持在 untouched instance，以及受控变化的 topology、control
   regime 和 surface realization 上？

较早的前置问题失败时，pilot 不进入后续问题。

## 3. 受控 task language v0.1

### 3.1 类型与取值

- `Symbol8`：八个取值，使答案分布可以严格平衡。选定 tokenizer 后，每个实际渲染符号
  都必须是单 token。
- `Boolean`：两个平衡取值，只用于受控 routing。
- 每个 program 都是 deterministic，并具有 executable reference solver。
- Canonical program 与 rendered prompt 始终是不同对象。

### 3.2 临时 computation category

- `transform`：把一个 `Symbol8` 状态映射为另一个状态。
- `merge`：把两个 `Symbol8` 状态合并为一个状态。
- `predicate`：从 `Symbol8` 状态得到一个 `Boolean`。
- `select`：依据 `Boolean` 从两个 `Symbol8` 状态中选择一个。
- `direct_read`：无需组合、可以直接读取答案的 negative control。

这些名称只描述 task-language semantics。不能假定它们具有 atomic、complete、cognitively
privileged 地位，也不能假定模型使用这些 operation。比较 external 与 computed control
时，condition-source event 单独分析。

### 3.3 Reference semantics

第一版实施提议使用小型 modular function，使每个状态可审计，并使答案取值可以平衡：

- `transform_k(x) = (x + k) mod 8`，其中 `k` 是非零奇数；
- `merge_k(x, y) = (x + 2y + k) mod 8`；
- 当 `(x + k) mod 8 >= 4` 时，`predicate_k(x) = 1`，否则为 `0`；
- 当 `b = 1` 时，`select(b, x, y) = x`，否则为 `y`。

Operation 的显示名称与 semantics 独立随机化。准确参数集合、退化检查和采样权重必须在
生成数据前冻结于机器可读实施配置。若行为可行性或已识别 confound 在实施审核前证明
需要修改这些函数，可以修改；任何修改都产生新的 task-language version。

## 4. 核心 matched design

Pilot A 使用一个共同 task language，而不是一组互不相关的 benchmark task。核心设计
交叉两个主要任务维度。

| Cell | Dependency topology | Control source |
|---|---|---|
| C1 | serial | externally supplied |
| C2 | fork-join | externally supplied |
| C3 | serial | computed from an intermediate state |
| C4 | fork-join | computed from an intermediate state |

### 4.1 Topology template

每个 program 包含具名输入、两个早期 transform、一个 merge、一个 select 和一个最终
transform。Serial template 让第二个 transform 依赖第一个；fork-join template 让两个
transform 分别作用于不同输入，然后再 merge。在同一个 control regime 内，topology
contrast 必须匹配 operation multiset、active-node count、答案分布和 rendering budget。

### 4.2 Control template

在 external-control 条件中，selector 作为 query input 提供；在 computed-control 条件中，
selector 由一个 intermediate state 上的 predicate 得到。两组尽可能匹配 prompt length
和展示信息总量；但 control value 的来源正是目标 manipulation，不能把它当作偶然差异。

### 4.3 Operation placement

在生成实例中，每个适用的 operation category 必须等频出现在每个兼容 event index 和
prompt region。每个 `topology x control x active-length` stratum 内要平衡 operation
显示名称、input value、output value、final answer 和参数。若某项 operation comparison
能够被未匹配的 graph degree 或 output token 确定，则必须排除该 comparison。

## 5. Control 与 nuisance factor

### 5.1 Task control

- `N1 direct-read`：匹配 rule inventory、近似 prompt length、symbol 和答案分布，但不
  需要 multi-step composition。
- `N2 same-program rerender`：同一个 canonical program 使用新的 operator-name
  permutation、vocabulary、statement order 和 template 渲染。
- `N3 untouched instances`：冻结 discovery choice 后，使用新 semantic identity 生成。

### 5.2 Statistical null

- 在匹配的 layer、event-index、position、output-value 和 task-cell strata 内置换
  candidate-operation label。
- 仅使用 layer、token position、event index、input/output value、topology、control
  regime、length 和 rendering 的 metadata-only prediction。
- 不包含 candidate-operation category 的 structure-only comparison。

### 5.3 Nuisance variable

协议记录并平衡或控制 active-node count、prompt-token length、event index、statement
order、vocabulary、operation 显示名称、answer symbol、template、input/output state、
model correctness 和 decoding status。Difficulty 由行为数据测量，不能只根据 nominal
program length 推断。

## 6. 数据与 split 方案

对 C1–C4 的每一个 cell：

- active-node level：4 和 6；
- 八个平衡的 final-answer value；
- 每个 `cell x length x answer` stratum 有 16 个独立 canonical instance。

因此 discovery split 有 1,024 个 canonical instance，untouched confirmation split 有
另外 1,024 个 semantic disjoint instance。Direct-read control pool 至少包含 512 个
additional canonical instance。

每个核心 canonical instance 产生两个 paired rendering：neutral symbolic rendering，
以及 renamed/reordered rendering。Split identity 依据 canonical semantic identity，而非
prompt text。必须记录 generator seed、schema version、task-language version、configuration
hash、solver result、reference graph 和完整 rendering provenance。

这些数量是 pilot design constant，不是正式 power calculation。Pilot 必须报告置信区间
与有效正确样本数。任何增加样本量的决定都必须在查看 functional result 前作出。

## 7. 模型与 response regime

### 7.1 模型政策

根据用户要求，Pilot A 排除 Qwen 模型。当前主候选是 7B 级、open-weight、冻结的
instruction-tuned Mistral；默认实施目标为 `mistralai/Mistral-7B-Instruct-v0.3`。若访问
权限、许可条款和服务器资源允许，约 8B 的 Llama instruct model 是首选替代。

任何下载或执行前，必须把准确 model/tokenizer repository 和 immutable full commit SHA
写入 run configuration。`main` 之类 branch 名称不是可接受 revision。Pilot model 是
测量仪器，不会自动成为最终论文模型。

### 7.2 Response regime

- `R1 aligned_trace`：输出固定长度 intermediate-state symbol sequence。用于建立清晰的
  event alignment 和开发测量方法。
- `R2 final_answer_only`：只输出最终答案。用于检验 R1 finding 是否完全依赖显式 trace
  scaffold。

R1 与 R2 是不同实验条件。不能把 R1 证据描述成 unscaffolded latent reasoning 的证据。
只有另行冻结 R2 的 measurement unit 和 alignment rule 后，才能开始 R2 activation
analysis。

## 8. 行为可行性阶段

必须先评估行为，之后才能检查 functional activation result。对每一个
`task cell x active length` stratum：

- trimmed exact-match accuracy 至少为 80%；
- invalid-format rate 至多为 2%；
- 所有 attempt 都保留在 denominator 中；
- 报告简单 answer-frequency、input-copy、final-rule 和 lexical-name heuristic；
- 不得静默排除未通过的 cell 后再进行 mechanistic analysis。

80% 是预先声明的工程推进规则，不是科学效应阈值。Cell 未通过时依次执行：format 与
tokenization audit；在 canonical semantics 不变的前提下简化 rendering；审核候选模型；
或拒绝该任务设计。不得利用 activation result 在这些修复方案之间进行选择。

## 9. 测量阶段

### 9.1 第一测量单位

第一项有边界的 measurement 是 R1 中每个 aligned state-output event、每个 layer 的
residual-stream vector。每条 observation 带有 instance、program、event、task cell、
layer、token position、event index、operation category、input state、output state、
correctness 和 rendering metadata。

Head output、MLP output、intervention fingerprint 和宽泛 metric search 暂缓。只有知道
residual-stream measurement 的可靠性后，才能分别论证这些扩展。

### 9.2 Reliability check

- 至少 99% 的 eligible correct trace 能与声明的 event slot 对齐。
- Deterministic replay 在记录的数值容差内复现 token sequence 与 activation。
- Paired rendering 保持相同 canonical identity 与 target。
- 缺失、重复或顺序错误的 event record 使 run 无效。

## 10. 分析阶段

### 10.1 Primary diagnostic analysis

使用 grouped、cross-validated linear readout 预测临时 computation category。数据 group
由 semantic instance 而非 event row 定义。主要量是 activation 加 metadata 相对于只用
metadata 的 held-out performance 增量。

必须执行 cross-classification：

1. 在部分 event index 上训练，在 held-out event index 上评估；
2. 在一种 rendering 上训练，在 paired rerendering 上评估；
3. 在一种 topology 或 control level 上训练，在 operation 对两者都适用时，于 matched
   alternative 上评估；
4. 每个结果与 stratified label permutation 比较。

报告 score、不确定性区间、class balance 和所有失败的 transfer。Predictability 称为
operation-associated signal，而不是 role。

### 10.2 Label-free discovery

只在 discovery split 上，可以先针对已声明 metadata 做 residualization，再在预先声明的
多个 clustering granularity 上探索。不得通过最大化与 task label 的一致性来选择 cluster
数量。报告 bootstrap stability 和 preprocessing sensitivity。查看 untouched confirmation
split 前，必须冻结 pattern definition。

## 11. 推进规则

### Green

所有核心行为 cell 通过、alignment 至少 99%、operation-associated signal 经受 held-out
position 和 rendering control，并且效应方向在 untouched instance 上相对 metadata-only
与 permutation baseline 得到复现时，进入下一阶段。

### Yellow

若 pattern 只存在于一个 task cell、position、topology、rendering 或 R1，则限制解释。
在获得更多证据前，它只能称为 task-specific、structure-specific、surface-specific 或
scaffold-specific pattern。

### Red

如果行为不足、alignment 不可靠、效应在结构控制后消失、confirmation 失败，或结论强烈
依赖未计划的 preprocessing/metric choice，则停止或重新设计。Red 是有效结果，不能触发
不受限制地搜索有利分析。

## 12. Pilot 后的路线选择

- Pattern 跨 topology、control、rendering 和 untouched instance 稳定：采用较窄且可证伪
  的 diagnostic decomposition，再加入真正的 semantic-domain replication。
- Pattern 局限于单一 schema：扩大经验 task sampling，并在提出更广结论前把 task 作为
  uncertainty 的抽样来源。
- Pattern 主要由 topology、step 或 position 主导：研究 structural organization，不升级
  为 functional-role interpretation。
- Task language 后续获得数学上有依据的 basis：另行考虑 formal-completeness program。
- 没有可靠 pattern：完成 measurement-validity check 后报告 negative pilot，或重新设计
  measurement construct。

## 13. 执行顺序与门禁

1. 冻结本协议与实施合同。
2. 在本地实现 task language、control、generator、split 和 test。
3. 验证 determinism、balance、solver agreement、rendering pair 和 leakage。
4. 冻结准确 model/tokenizer SHA 与服务器配置。
5. 只运行 behavior，并审核 behavioral gate。
6. 单独授权并运行 R1 residual-stream capture。
7. 完成 discovery analysis，并冻结 pattern/analysis definition。
8. 运行 untouched confirmation。
9. 可选地规划 R2 和一个 semantic-domain replication。
10. 选择 post-pilot research route，并更新 claim boundary。

代码实施、下载、模型执行、activation capture、服务器执行和 Git 发布仍分别服从已有
门禁。

