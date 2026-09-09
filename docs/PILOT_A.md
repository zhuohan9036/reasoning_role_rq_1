# Pilot A protocol: pattern discovery and measurement validation

> 中文版：[PILOT_A.zh-CN.md](PILOT_A.zh-CN.md)

**Status:** accepted scientific design; implementation not yet authorized
**Protocol version:** 0.1
**Last updated:** 2026-09-09

## 1. Purpose and claim ceiling

Pilot A is a pattern-discovery and measurement-validation pilot. It asks whether
model-side computation patterns can be measured reproducibly in a deliberately
bounded task environment, whether those patterns survive structural controls,
and which task dimensions most affect them.

Pilot A may support only the following kind of statement:

> In the named frozen model, response regime, and controlled task distribution,
> a reproducible model-side pattern was or was not associated with a provisional
> task-side computation category after the declared controls.

It cannot establish universal computational primitives, general reasoning roles,
cross-domain generality, or causal necessity. Its task language is a diagnostic
instrument rather than a proposed ontology of reasoning.

## 2. Questions

Pilot A has four ordered questions:

1. Can the model solve every core task cell accurately enough for interpretable
   sampling without selective exclusion?
2. Can task events be aligned to model measurements reproducibly?
3. Does activation information distinguish provisional computation categories
   beyond layer, token position, event index, values, topology, and rendering?
4. Do discovered patterns survive untouched instances and controlled changes in
   topology, control regime, and surface realization?

The pilot does not proceed to a later question when the earlier prerequisite
fails.

## 3. Controlled task language v0.1

### 3.1 Types and values

- `Symbol8`: eight values with a balanced answer distribution. The concrete
  render symbols must each be a single token under the selected tokenizer.
- `Boolean`: two balanced values used only for controlled routing.
- Every program is deterministic and has an executable reference solver.
- Canonical programs and rendered prompts remain separate objects.

### 3.2 Provisional computation categories

- `transform`: map one `Symbol8` state to another.
- `merge`: combine two `Symbol8` states into one.
- `predicate`: derive a `Boolean` from a `Symbol8` state.
- `select`: choose between two `Symbol8` states using a `Boolean`.
- `direct_read`: a negative-control target that can be read without composition.

These names describe task-language semantics only. They are not assumed to be
atomic, complete, cognitively privileged, or used by the model. Predicate-source
events are analyzed separately when comparing external and computed control.

### 3.3 Reference semantics

The first implementation proposal uses small modular functions so every state is
auditable and answer values can be balanced:

- `transform_k(x) = (x + k) mod 8`, with non-zero odd `k`;
- `merge_k(x, y) = (x + 2y + k) mod 8`;
- `predicate_k(x) = 1` when `(x + k) mod 8 >= 4`, otherwise `0`;
- `select(b, x, y) = x` when `b = 1`, otherwise `y`.

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

Each program contains named inputs, two early transforms, one merge, one select,
and one final transform. A serial template makes the second transform depend on
the first. A fork-join template applies the two transforms to separate inputs
before merging them. Within each control regime, topology contrasts must match
the operation multiset, active-node count, answer distribution, and rendering
budget.

### 4.2 Control templates

In the external-control condition, the selector is supplied as a query input. In
the computed-control condition, the selector is produced by a predicate over an
intermediate state. Prompt length and total displayed information are matched as
closely as possible, but the source of the control value is the intended
manipulation and cannot be treated as an incidental difference.

### 4.3 Operation placement

Across generated instances, each eligible operation category must appear equally
often at each compatible event index and prompt region. Operator display names,
input values, output values, final answers, and parameters are balanced within
each `topology x control x active-length` stratum. The operation analysis must
exclude any comparison that is deterministically identified by an unmatched
graph degree or output token.

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
- Structure-only comparisons that omit the candidate-operation category.

### 5.3 Nuisance variables

The protocol records and balances or controls active-node count, prompt-token
length, event index, statement order, vocabulary, operator display names, answer
symbol, template, input and output states, model correctness, and decoding
status. Difficulty is measured behaviorally rather than inferred from nominal
program length alone.

## 6. Data and split plan

For each of C1-C4:

- active-node levels: 4 and 6;
- eight balanced final-answer values;
- 16 independent canonical instances per `cell x length x answer` stratum.

This yields 1,024 canonical instances in the discovery split and another 1,024
semantically disjoint instances in the untouched confirmation split. At least
512 additional canonical instances form the direct-read control pool.

Every core canonical instance receives two paired renderings: a neutral symbolic
rendering and a renamed/reordered rendering. Split identity is based on canonical
semantic identity, never prompt text. Generator seeds, schema version, task-
language version, configuration hash, solver result, reference graph, and exact
rendering provenance are recorded.

These counts are pilot design constants, not a formal power calculation. The
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

- `R1 aligned_trace`: a fixed-length sequence of intermediate state symbols.
  This is the primary regime for alignment and measurement development.
- `R2 final_answer_only`: only the final answer. It tests whether an R1 finding
  depends completely on explicit trace scaffolding.

R1 and R2 are separate experimental conditions. R1 evidence cannot be described
as evidence about unscaffolded latent reasoning. R2 activation analysis begins
only after its measurement unit and alignment rule are separately frozen.

## 8. Behavioral feasibility stage

Behavior is evaluated before functional activation results are inspected. For
every `task cell x active length` stratum:

- trimmed exact-match accuracy must be at least 80%;
- invalid-format rate must be at most 2%;
- all attempts remain in the denominator;
- simple answer-frequency, input-copy, final-rule, and lexical-name heuristics
  are reported;
- no failed cell may be silently excluded from mechanistic analysis.

The 80% threshold is a predeclared engineering progression rule, not a
scientific effect threshold. A failed cell triggers, in order: formatting and
tokenization audit; rendering simplification with unchanged canonical semantics;
model-candidate review; or rejection of the task design. Activation results may
not be used to choose among these repairs.

## 9. Measurement stage

### 9.1 First measurement unit

The first bounded measurement is the residual-stream vector at each aligned
state-output event and each layer in R1. Each observation carries instance,
program, event, task cell, layer, token position, event index, operation category,
input state, output state, correctness, and rendering metadata.

Head outputs, MLP outputs, intervention fingerprints, and broad metric searches
are deferred. They require separate justification after residual-stream
measurement reliability is known.

### 9.2 Reliability checks

- At least 99% of eligible correct traces must align to the declared event slots.
- Deterministic replay must reproduce token sequences and activations within the
  recorded numerical tolerance.
- Paired renderings must preserve canonical identity and target.
- Missing, duplicate, or misordered event records invalidate the run.

## 10. Analysis stage

### 10.1 Primary diagnostic analysis

A grouped, cross-validated linear readout predicts the provisional computation
category. Semantic instances, not event rows, define data groups. The principal
quantity is the incremental held-out performance of activation plus metadata
over metadata alone.

Cross-classification is mandatory:

1. train on some event indices and evaluate on held-out event indices;
2. train on one rendering and evaluate on its paired rerendering;
3. train on one topology or control level and evaluate on the matched alternative
   when the operation is valid in both;
4. compare every result with stratified label permutations.

Scores, uncertainty intervals, class balance, and all failed transfers are
reported. Predictability is called operation-associated signal, not a role.

### 10.2 Label-free discovery

On the discovery split only, activations may be residualized against declared
metadata and explored over a predeclared range of clustering granularities. The
number of clusters may not be selected by maximizing agreement with task labels.
Bootstrap stability and sensitivity to preprocessing are reported. Pattern
definitions are frozen before examining the untouched confirmation split.

## 11. Progression rules

### Green

Proceed when all core behavioral cells pass, alignment is at least 99%, an
operation-associated signal survives held-out position and rendering controls,
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

1. Freeze this protocol and the implementation contract.
2. Implement the task language, controls, generator, splits, and tests locally.
3. Validate determinism, balance, solver agreement, rendering pairs, and leakage.
4. Freeze exact model/tokenizer SHAs and server configuration.
5. Run behavior only and review the behavioral gate.
6. Separately authorize and run R1 residual-stream capture.
7. Complete discovery analysis and freeze pattern/analysis definitions.
8. Run untouched confirmation.
9. Optionally plan R2 and one semantic-domain replication.
10. Choose the post-pilot research route and update the claim boundary.

Code implementation, downloads, model execution, activation capture, server
execution, and Git publication each remain subject to their documented gates.

