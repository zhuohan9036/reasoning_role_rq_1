# Pilot A 协议：模式发现与测量验证

> English: [PILOT_A.md](PILOT_A.md)

**状态：** 候选 calibration sandbox；科学任务状态暂停，等待 Pilot A0
**协议版本：** 0.2
**最后更新：** 2026-09-10

> **桥接提示：** Pilot A0 现在采用 native-inference、model-first 路线。`Symbol8`、拟议
> function pair 与 C1–C4 仅保留为非活动 calibration fallback。只有在后续记录了具名的
> identification failure，并且另行审核、明确批准恢复它们的计划之后，才能实施；在此之前
> 不得把它们视为科学 Pilot A 任务。见 [PILOT_A0.zh-CN.md](PILOT_A0.zh-CN.md)。

## 1. 目的与结论上限

Pilot A 是 pattern-discovery and measurement-validation pilot。它考察：在一个有意限制
范围的任务环境中，能否重复测量模型侧 computation pattern；这些 pattern 能否经受结构
控制；以及哪些任务维度最影响这些 pattern。

Pilot A 最多支持如下类型的陈述：

> 在具名冻结模型、response regime 和受控任务分布中，经过已声明的控制后，某个可重复
> 的模型侧 pattern 与相同 structural signature 内的临时 functional subtype 存在或不存在
> 关联。

它不能确立通用 computational primitive、一般 reasoning role、跨领域普遍性或因果必要
性。它的 task language 是诊断仪器，不是 reasoning ontology 提案。

## 2. 研究问题

Pilot A 依次回答四个问题：

1. 模型能否在不选择性排除 cell 的前提下，以足够高的准确率完成全部核心任务 cell？
2. 任务事件能否与模型测量形成可重复 alignment？
3. 在相同 input/output signature 内，控制 layer、token position、event index、数值、
   topology 和 rendering 后，activation 是否仍能区分临时 functional subtype？
4. 发现的 pattern 能否保持在 untouched instance，以及受控变化的 topology、control
   regime 和 surface realization 上？

较早的前置问题失败时，pilot 不进入后续问题。

## 3. 受控 task language v0.2

### 3.1 类型与取值

- `Symbol8`：八个取值，使答案分布可以严格平衡。选定 tokenizer 后，每个实际渲染符号
  都必须是单 token。
- `Boolean`：两个平衡取值，只用于受控 routing。
- 每个 program 都是 deterministic，并具有 executable reference solver。
- Canonical program 与 rendered prompt 始终是不同对象。

### 3.2 Structural signature 与临时 functional subtype

Structural node type 与 functional subtype 是不同字段。Structural type 描述 graph arity
和 value type，是 control，不是主要 functional label。

| Structural signature | 临时 functional contrast |
|---|---|
| `Symbol8 -> Symbol8` | `shift` 对 `reflect` |
| `Symbol8 x Symbol8 -> Symbol8` | `add_merge` 对 `subtract_merge` |
| `Symbol8 -> Boolean` | `parity` 对 `upper_half` |
| `Boolean x Symbol8 x Symbol8 -> Symbol8` | `select_if` 对 `select_unless` |

`direct_read` 继续作为无需组合、可直接读取答案的 negative control。Transform、merge、
predicate 和 select 等粗粒度术语只描述 task-language structural family。由于它们的 arity
和 type signature 不同，不能把它们当作主要 functional prediction target。

所有 category 仍是任务侧假设。不能假定它们具有 atomic、complete、cognitively privileged
地位，也不能假定模型使用这些 operation。

### 3.3 Reference semantics

第一版实施提议使用小型 modular function，使每个状态可审计，并使答案取值可以平衡：

- `shift_k(x) = (x + k) mod 8`，其中 `k` 是非零奇数；
- `reflect_k(x) = (k - x) mod 8`；
- `add_merge_k(x, y) = (x + y + k) mod 8`；
- `subtract_merge_k(x, y) = (x - y + k) mod 8`；
- `parity_k(x) = (x + k) mod 2`；
- 当 `(x + k) mod 8 >= 4` 时，`upper_half_k(x) = 1`，否则为 `0`；
- 当 `b = 1` 时，`select_if(b, x, y) = x`，否则为 `y`；
- 当 `b = 1` 时，`select_unless(b, x, y) = y`，否则为 `x`。

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

每个核心 program 固定包含六个 answer-relevant node。External-control cell 包含四个 unary
transformation、一个 binary merge 和一个 conditional node。Computed-control cell 包含三个
unary transformation、一个 binary merge、一个 predicate 和一个 conditional node。
Serial template 让第二个 unary node 依赖第一个；fork-join template 让前两个 unary node
分别作用于不同输入，然后再 merge。在同一个 control regime 内，topology contrast 必须
匹配 structural-signature multiset、functional-subtype frequency、active-node count、答案
分布和 rendering budget。

用 `U`、`B`、`P` 和 `C` 分别表示 unary、binary、predicate 和 conditional node，anchor
dependency template 为：

- C1：`u1=U(x); u2=U(u1); m=B(u2,y); u3=U(m); s=C(q,u3,u2); o=U(s)`；
- C2：`u1=U(x); u2=U(y); m=B(u1,u2); u3=U(m); s=C(q,u3,u1); o=U(s)`；
- C3：`u1=U(x); u2=U(u1); m=B(u2,y); p=P(m); s=C(p,m,u2); o=U(s)`；
- C4：`u1=U(x); u2=U(y); m=B(u1,u2); p=P(m); s=C(p,m,u1); o=U(s)`。

其中 `q` 是 externally supplied Boolean，`o` 是 target。每个兼容 structural node 上的
functional subtype 按平衡规则采样。

### 4.2 Control template

在 external-control 条件中，selector 作为 query input 提供；在 computed-control 条件中，
selector 由一个 intermediate state 上的 predicate 得到。两组尽可能匹配 prompt length
和展示信息总量；但 control value 的来源正是目标 manipulation，不能把它当作偶然差异。

### 4.3 Operation placement

在每项 functional contrast 内，成对 subtype 必须具有完全匹配的 event-index 与 prompt-
region distribution。每个被分析的位置都必须同时包含具有相同 structural signature 的
两个 subtype。Unary contrast 必须覆盖多个 event index，以支持 held-out-position test。
Binary、predicate 或 conditional contrast 在核心 pilot 中可以只占一个 matched position；
此类结果明确属于 position-matched，而非 position-generalized。每个 `topology x control`
stratum 内要平衡 operation 显示名称、input value、output value、final answer 和参数。

数据验收前，identifiability audit 必须证明 functional-subtype label 不能由 structural
signature、graph degree、event index、prompt region、output token 或 task cell 确定性恢复。
未通过的 comparison 在模型测量前按设计排除，不能在观察结果后再决定。

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
- 不包含 functional subtype 的 structure-only comparison。

### 5.3 Nuisance variable

协议记录并平衡或控制 structural signature、graph degree、active-node count、prompt-token
length、event index、statement
order、vocabulary、operation 显示名称、answer symbol、template、input/output state、
model correctness 和 decoding status。Difficulty 由行为数据测量，不能只根据 nominal
program length 推断。

## 6. 数据与 split 方案

每个核心 program 固定包含六个 answer-relevant node。对 C1–C4 的每一个 cell：

- 八个平衡的 final-answer value；
- 每个 `cell x answer` stratum 有 32 个独立 canonical instance。

因此 discovery split 有 1,024 个 canonical instance，untouched confirmation split 有
另外 1,024 个 semantic disjoint instance。Direct-read control pool 至少包含 512 个
additional canonical instance。

每个核心 canonical instance 产生两个 paired rendering：neutral symbolic rendering，
以及 renamed/reordered rendering。Split identity 依据 canonical semantic identity，而非
prompt text。必须记录 generator seed、schema version、task-language version、configuration
hash、solver result、reference graph 和完整 rendering provenance。

Program-length generalization 延后到核心测量通过后另行规划的 robustness extension。
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

- `R1 aligned_trace`：用固定 delimiter 格式输出六个 intermediate-state symbol，例如
  `| A | B | C | D | E | F |`。用于 alignment 的每个 display symbol 和 delimiter 都必须
  经过 tokenizer audit。该条件用于建立清晰 event alignment 和开发测量方法。
- `R2 final_answer_only`：只输出最终答案。用于检验 R1 finding 是否完全依赖显式 trace
  scaffold。

R1 与 R2 是不同实验条件。不能把 R1 证据描述成 unscaffolded latent reasoning 的证据。
只有另行冻结 R2 的 measurement unit 和 alignment rule 后，才能开始 R2 activation
analysis。

## 8. 行为可行性阶段

必须先评估行为，之后才能检查 functional activation result。对每一个 task cell：

- R1 full-trace exact-match accuracy 至少为 80%；
- 单独报告 final-state accuracy 与 per-event accuracy，但二者不能替代 full-trace gate；
- invalid-format rate 至多为 2%；
- 所有 attempt 都保留在 denominator 中；
- 报告简单 answer-frequency、input-copy、final-rule 和 lexical-name heuristic；
- 不得静默排除未通过的 cell 或 functional subtype 后再进行 mechanistic analysis；
- Primary activation sample 只包含整条 R1 trace 正确的 instance；错误 trace 保留为单独
  标记的 secondary diagnostic。

80% 是预先声明的工程推进规则，不是科学效应阈值。Cell 未通过时依次执行：format 与
tokenization audit；在 canonical semantics 不变的前提下简化 rendering；审核候选模型；
或拒绝该任务设计。不得利用 activation result 在这些修复方案之间进行选择。

## 9. 测量阶段

### 9.1 第一测量单位

第一项有边界的 measurement 是 R1 中每个 state symbol 之前的固定 delimiter token 上、
每个 layer 的 residual-stream vector。该位置的 hidden state 正在预测对应 state，而不是
已经接收该 state 的 token embedding。State 之后的位置只能作为已声明的 sensitivity
measurement 保留。每条 observation 带有 instance、program、event、task cell、layer、
token position、event index、structural signature、functional subtype、input state、
output state、correctness 和 rendering metadata。

Head output、MLP output、intervention fingerprint 和宽泛 metric search 暂缓。只有知道
residual-stream measurement 的可靠性后，才能分别论证这些扩展。

### 9.2 Reliability check

- 至少 99% 的 eligible fully correct trace 能与六个声明的 pre-output delimiter position
  对齐。
- Deterministic replay 在记录的数值容差内复现 token sequence 与 activation。
- Paired rendering 保持相同 canonical identity 与 target。
- 缺失、重复或顺序错误的 event record 使 run 无效。

## 10. 分析阶段

### 10.1 Primary diagnostic analysis

在每个 matched structural signature 内，分别使用 grouped、cross-validated linear
readout 预测 functional subtype。Pooled transform-versus-merge-versus-select classifier
不是主要 functional test。数据 group 由 semantic instance 而非 event row 定义。主要量
是 activation 加 metadata 相对于只用 metadata 的 held-out performance 增量。

必须执行 cross-classification：

1. 当 contrast 覆盖多个位置时，在部分 event index 上训练并在 held-out event index 上评估；
   unary contrast 必须执行此项；
2. 在一种 rendering 上训练，在 paired rerendering 上评估；
3. 在一种 topology 或 control level 上训练，在相同 structural signature 与 functional
   contrast 对两者都适用时，于 matched alternative 上评估；
4. 每个结果与 stratified label permutation 比较。

报告 score、不确定性区间、class balance 和所有失败的 transfer。Predictability 称为
functional-subtype-associated signal，而不是 role。

### 10.2 Label-free discovery

只在 discovery split 上，可以先针对已声明 metadata 做 residualization，再在预先声明的
多个 clustering granularity 上探索。不得通过最大化与 task label 的一致性来选择 cluster
数量。报告 bootstrap stability 和 preprocessing sensitivity。查看 untouched confirmation
split 前，必须冻结 pattern definition。

## 11. 推进规则

### Green

所有核心行为 cell 通过、alignment 至少 99%、functional-subtype-associated signal 经受 held-out
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

1. 完成并审核 Pilot A0 target-task grounding。
2. 决定本候选 sandbox 的哪些元素被保留、修订、仅作 calibration 或拒绝。
3. 冻结新的科学 Pilot A 协议与实施合同。
4. 只在本地实施新获接受的 task language、control、generator、split 和 test。
5. 验证 determinism、balance、solver agreement、rendering pair 和 leakage。
6. 冻结准确 model/tokenizer SHA 与服务器配置。
7. 只运行 behavior，并审核 behavioral gate。
8. 单独授权并运行 R1 residual-stream capture。
9. 完成 discovery analysis，并冻结 pattern/analysis definition。
10. 运行 untouched confirmation 与预先声明的 return-to-source test。
11. 可选地规划 R2 与 cross-family replication。
12. 选择 post-pilot research route，并更新 claim boundary。

代码实施、下载、模型执行、activation capture、服务器执行和 Git 发布仍分别服从已有
门禁。
