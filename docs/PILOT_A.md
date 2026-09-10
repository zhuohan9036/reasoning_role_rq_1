# Pilot A protocol: pattern discovery and measurement validation

> 中文版：[PILOT_A.zh-CN.md](PILOT_A.zh-CN.md)

**Status:** candidate calibration sandbox; scientific-task status paused pending Pilot A0
**Protocol version:** 0.2
**Last updated:** 2026-09-10

> **Bridge notice:** Pilot A0 now follows a native-inference, model-first route.
> `Symbol8`, the proposed function pairs, and C1-C4 remain an inactive calibration
> fallback. They must not be implemented or treated as the scientific Pilot A task
> unless a later identification failure is documented and a separate plan restoring
> them is reviewed and explicitly approved. See [PILOT_A0.md](PILOT_A0.md).

## 1. Purpose and claim ceiling

Pilot A is a pattern-discovery and measurement-validation pilot. It asks whether
model-side computation patterns can be measured reproducibly in a deliberately
bounded task environment, whether those patterns survive structural controls,
and which task dimensions most affect them.

Pilot A may support only the following kind of statement:

> In the named frozen model, response regime, and controlled task distribution,
> a reproducible model-side pattern was or was not associated with a provisional
> functional subtype within a matched structural signature after the declared
> controls.

It cannot establish universal computational primitives, general reasoning roles,
cross-domain generality, or causal necessity. Its task language is a diagnostic
instrument rather than a proposed ontology of reasoning.

## 2. Questions

Pilot A has four ordered questions:

1. Can the model solve every core task cell accurately enough for interpretable
   sampling without selective exclusion?
2. Can task events be aligned to model measurements reproducibly?
3. Within a matched input/output signature, does activation information
   distinguish provisional functional subtypes beyond layer, token position,
   event index, values, topology, and rendering?
4. Do discovered patterns survive untouched instances and controlled changes in
   topology, control regime, and surface realization?

The pilot does not proceed to a later question when the earlier prerequisite
fails.

## 3. Controlled task language v0.2

### 3.1 Types and values

- `Symbol8`: eight values with a balanced answer distribution. The concrete
  render symbols must each be a single token under the selected tokenizer.
- `Boolean`: two balanced values used only for controlled routing.
- Every program is deterministic and has an executable reference solver.
- Canonical programs and rendered prompts remain separate objects.

### 3.2 Structural signatures and provisional functional subtypes

Structural node type and functional subtype are distinct fields. Structural
types describe graph arity and value types; they are controls, not the primary
functional labels.

| Structural signature | Provisional functional contrast |
|---|---|
| `Symbol8 -> Symbol8` | `shift` versus `reflect` |
| `Symbol8 x Symbol8 -> Symbol8` | `add_merge` versus `subtract_merge` |
| `Symbol8 -> Boolean` | `parity` versus `upper_half` |
| `Boolean x Symbol8 x Symbol8 -> Symbol8` | `select_if` versus `select_unless` |

`direct_read` remains a negative-control target that can be read without
composition. The coarse terms transform, merge, predicate, and select describe
structural task-language families only. They must not be used as the primary
functional prediction target because their arity and type signatures differ.

All categories remain task-side hypotheses. They are not assumed to be atomic,
complete, cognitively privileged, or used by the model.

### 3.3 Reference semantics

The first implementation proposal uses small modular functions so every state is
auditable and answer values can be balanced:

- `shift_k(x) = (x + k) mod 8`, with non-zero odd `k`;
- `reflect_k(x) = (k - x) mod 8`;
- `add_merge_k(x, y) = (x + y + k) mod 8`;
- `subtract_merge_k(x, y) = (x - y + k) mod 8`;
- `parity_k(x) = (x + k) mod 2`;
- `upper_half_k(x) = 1` when `(x + k) mod 8 >= 4`, otherwise `0`;
- `select_if(b, x, y) = x` when `b = 1`, otherwise `y`;
- `select_unless(b, x, y) = y` when `b = 1`, otherwise `x`.

Operator display names are randomized independently of semantics. Exact allowed
parameters, degeneracy checks, and sampling weights must be frozen in the
machine-readable implementation configuration before data generation. These
particular functions may be revised before implementation review if behavioral
feasibility or an identified confound justifies the change; any revision creates
a new task-language version.

## 4. Core matched design

Pilot A uses one task language rather than a collection of unrelated benchmark
tasks. The core design crosses two primary task dimensions.

| Cell | Dependency topology | Control source |
|---|---|---|
| C1 | serial | externally supplied |
| C2 | fork-join | externally supplied |
| C3 | serial | computed from an intermediate state |
| C4 | fork-join | computed from an intermediate state |

### 4.1 Topology templates

Every core program has exactly six answer-relevant nodes. External-control cells
contain four unary transformations, one binary merge, and one conditional node.
Computed-control cells contain three unary transformations, one binary merge,
one predicate, and one conditional node. A serial template makes the second
unary node depend on the first. A fork-join template applies the first two unary
nodes to separate inputs before merging them. Within each control regime,
topology contrasts must match the structural-signature multiset, functional-
subtype frequencies, active-node count, answer distribution, and rendering
budget.

Using `U`, `B`, `P`, and `C` for unary, binary, predicate, and conditional nodes,
the anchor dependency templates are:

- C1: `u1=U(x); u2=U(u1); m=B(u2,y); u3=U(m); s=C(q,u3,u2); o=U(s)`;
- C2: `u1=U(x); u2=U(y); m=B(u1,u2); u3=U(m); s=C(q,u3,u1); o=U(s)`;
- C3: `u1=U(x); u2=U(u1); m=B(u2,y); p=P(m); s=C(p,m,u2); o=U(s)`;
- C4: `u1=U(x); u2=U(y); m=B(u1,u2); p=P(m); s=C(p,m,u1); o=U(s)`.

Here `q` is the externally supplied Boolean and `o` is the target. Functional
subtypes are sampled at each compatible structural node under the balance rules.

### 4.2 Control templates

In the external-control condition, the selector is supplied as a query input. In
the computed-control condition, the selector is produced by a predicate over an
intermediate state. Prompt length and total displayed information are matched as
closely as possible, but the source of the control value is the intended
manipulation and cannot be treated as an incidental difference.

### 4.3 Operation placement

Within every functional contrast, the paired subtypes must have exactly matched
event-index and prompt-region distributions. At every analyzed position, both
subtypes of the same structural signature must occur. The unary contrast must
span multiple event indices so it can support a held-out-position test. Binary,
predicate, or conditional contrasts may be limited to one matched position in
the core pilot; such results are explicitly position-matched rather than
position-generalized. Operator display names, input values, output values, final
answers, and parameters are balanced within each `topology x control` stratum.

Before data acceptance, an identifiability audit must prove that the functional-
subtype label is not deterministically recoverable from structural signature,
graph degree, event index, prompt region, output token, or task cell. Comparisons
that fail this audit are excluded by design before model measurements, not after
results are observed.

## 5. Controls and nuisance factors

### 5.1 Task controls

- `N1 direct-read`: matched rule inventory, approximate prompt length, symbols,
  and answer distribution, but no multi-step composition is needed.
- `N2 same-program rerender`: the same canonical program is rendered with a new
  operator-name permutation, vocabulary, statement order, and template.
- `N3 untouched instances`: new semantic identities generated after discovery
  choices are frozen.

### 5.2 Statistical nulls

- Candidate-operation labels permuted within matched layer, event-index,
  position, output-value, and task-cell strata.
- Metadata-only prediction using layer, token position, event index, input and
  output values, topology, control regime, length, and rendering.
- Structure-only comparisons that omit the functional subtype.

### 5.3 Nuisance variables

The protocol records and balances or controls structural signature, graph
degree, active-node count, prompt-token
length, event index, statement order, vocabulary, operator display names, answer
symbol, template, input and output states, model correctness, and decoding
status. Difficulty is measured behaviorally rather than inferred from nominal
program length alone.

## 6. Data and split plan

Every core program contains six answer-relevant nodes. For each of C1-C4:

- eight balanced final-answer values;
- 32 independent canonical instances per `cell x answer` stratum.

This yields 1,024 canonical instances in the discovery split and another 1,024
semantically disjoint instances in the untouched confirmation split. At least
512 additional canonical instances form the direct-read control pool.

Every core canonical instance receives two paired renderings: a neutral symbolic
rendering and a renamed/reordered rendering. Split identity is based on canonical
semantic identity, never prompt text. Generator seeds, schema version, task-
language version, configuration hash, solver result, reference graph, and exact
rendering provenance are recorded.

Program-length generalization is deferred to a separately planned robustness
extension after the core measurement passes. These counts are pilot design
constants, not a formal power calculation. The
pilot reports confidence intervals and effective correct-sample counts. Any
increase in sample count must be decided without inspecting functional results.

## 7. Model and response regimes

### 7.1 Model policy

Qwen models are excluded from Pilot A at the user's request. The working primary
candidate is an open-weight, frozen, instruction-tuned Mistral model in the 7B
class; `mistralai/Mistral-7B-Instruct-v0.3` is the default implementation target.
An approximately 8B Llama instruct model is the preferred alternative if access,
license terms, and server resources permit.

The exact model and tokenizer repositories and immutable full commit SHAs must
be written into the run configuration before any download or execution. A branch
name such as `main` is not an acceptable revision. The pilot model is a
measurement instrument and is not automatically the final paper model.

### 7.2 Response regimes

- `R1 aligned_trace`: six intermediate state symbols in a fixed delimiter format,
  for example `| A | B | C | D | E | F |`. Every display symbol and delimiter
  used for alignment must be tokenizer-audited. This is the primary regime for
  alignment and measurement development.
- `R2 final_answer_only`: only the final answer. It tests whether an R1 finding
  depends completely on explicit trace scaffolding.

R1 and R2 are separate experimental conditions. R1 evidence cannot be described
as evidence about unscaffolded latent reasoning. R2 activation analysis begins
only after its measurement unit and alignment rule are separately frozen.

## 8. Behavioral feasibility stage

Behavior is evaluated before functional activation results are inspected. For
every task cell:

- R1 full-trace exact-match accuracy must be at least 80%;
- final-state accuracy and per-event accuracy are reported separately but do not
  replace the full-trace gate;
- invalid-format rate must be at most 2%;
- all attempts remain in the denominator;
- simple answer-frequency, input-copy, final-rule, and lexical-name heuristics
  are reported;
- no failed cell or functional subtype may be silently excluded from mechanistic
  analysis;
- the primary activation sample contains only fully correct R1 traces; incorrect
  traces are retained for a separately labeled secondary diagnostic.

The 80% threshold is a predeclared engineering progression rule, not a
scientific effect threshold. A failed cell triggers, in order: formatting and
tokenization audit; rendering simplification with unchanged canonical semantics;
model-candidate review; or rejection of the task design. Activation results may
not be used to choose among these repairs.

## 9. Measurement stage

### 9.1 First measurement unit

The first bounded measurement is the residual-stream vector at the fixed
delimiter token immediately before each R1 state symbol: the position whose
hidden state predicts that state, rather than a position that has already
received the state's token embedding. It is captured at every layer. The
post-state position may be retained only as a declared sensitivity measurement.
Each observation carries instance, program, event, task cell, layer, token
position, event index, structural signature, functional subtype, input state,
output state, correctness, and rendering metadata.

Head outputs, MLP outputs, intervention fingerprints, and broad metric searches
are deferred. They require separate justification after residual-stream
measurement reliability is known.

### 9.2 Reliability checks

- At least 99% of eligible fully correct traces must align to the six declared
  pre-output delimiter positions.
- Deterministic replay must reproduce token sequences and activations within the
  recorded numerical tolerance.
- Paired renderings must preserve canonical identity and target.
- Missing, duplicate, or misordered event records invalidate the run.

## 10. Analysis stage

### 10.1 Primary diagnostic analysis

Separate grouped, cross-validated linear readouts predict functional subtype
within each matched structural signature. A pooled transform-versus-merge-
versus-select classifier is not a primary functional test. Semantic instances,
not event rows, define data groups. The principal quantity is the incremental
held-out performance of activation plus metadata over metadata alone.

Cross-classification is mandatory:

1. train on some event indices and evaluate on held-out event indices when the
   contrast spans multiple positions; this is required for the unary contrast;
2. train on one rendering and evaluate on its paired rerendering;
3. train on one topology or control level and evaluate on the matched alternative
   when the same structural signature and functional contrast are valid in both;
4. compare every result with stratified label permutations.

Scores, uncertainty intervals, class balance, and all failed transfers are
reported. Predictability is called functional-subtype-associated signal, not a
role.

### 10.2 Label-free discovery

On the discovery split only, activations may be residualized against declared
metadata and explored over a predeclared range of clustering granularities. The
number of clusters may not be selected by maximizing agreement with task labels.
Bootstrap stability and sensitivity to preprocessing are reported. Pattern
definitions are frozen before examining the untouched confirmation split.

## 11. Progression rules

### Green

Proceed when all core behavioral cells pass, alignment is at least 99%, a
functional-subtype-associated signal survives held-out position and rendering controls,
and the direction replicates on untouched instances against both metadata-only
and permutation baselines.

### Yellow

Restrict the interpretation when a pattern is limited to one task cell, position,
topology, rendering, or R1. Such a result is task-, structure-, surface-, or
scaffold-specific until further evidence exists.

### Red

Stop or redesign when behavior is inadequate, alignment is unreliable, effects
vanish under structural controls, confirmation fails, or conclusions depend
strongly on an unplanned preprocessing or metric choice. A red outcome is valid
and must not trigger an unrestricted search for a favorable analysis.

## 12. Post-pilot route selection

- Stable patterns across topology, control, rendering, and untouched instances:
  pursue a narrow falsifiable diagnostic decomposition, then add a true semantic-
  domain replication.
- Stable patterns confined to one schema: expand empirical task sampling and use
  task as a sampled source of uncertainty before broader claims.
- Patterns dominated by topology, step, or position: study structural
  organization and do not promote a functional-role interpretation.
- A task language that later receives a mathematically justified basis: consider
  a separate formal-completeness program.
- No reliable pattern: report the negative pilot after measurement-validity
  checks or redesign the measurement construct.

## 13. Execution order and gates

1. Complete and review Pilot A0 target-task grounding.
2. Decide which elements of this candidate sandbox are retained, revised,
   calibration-only, or rejected.
3. Freeze a new scientific Pilot A protocol and implementation contract.
4. Implement only the newly accepted task language, controls, generator, splits,
   and tests locally.
5. Validate determinism, balance, solver agreement, rendering pairs, and leakage.
6. Freeze exact model/tokenizer SHAs and server configuration.
7. Run behavior only and review the behavioral gate.
8. Separately authorize and run R1 residual-stream capture.
9. Complete discovery analysis and freeze pattern/analysis definitions.
10. Run untouched confirmation and the predeclared return-to-source test.
11. Optionally plan R2 and cross-family replication.
12. Choose the post-pilot research route and update the claim boundary.

Code implementation, downloads, model execution, activation capture, server
execution, and Git publication each remain subject to their documented gates.
