# Implementation plan: pilot-a-design-v1

> 中文版：[PLAN.zh-CN.md](PLAN.zh-CN.md)

**Status:** paused before implementation; not eligible for implementation approval
**Plan version:** 2
**Scientific protocol:** `docs/PILOT_A.md`, version 0.2
**Code changes authorized:** no
**Model or server execution authorized:** no

## 1. Objective

> This plan is retained as planning history. Pilot A0 must establish target-task
> grounding before any element can return in a scientific Pilot A plan. Do not
> implement this plan. See `runs/pilot-a0-target-grounding-v1/PLAN.md`.

Implement the then-proposed Pilot A task instrument independently of the existing
calibration task choices. The implementation must produce deterministic typed
programs, four matched structural cells, direct-read controls, paired renderings,
semantic-disjoint discovery and confirmation splits, shortcut audits, and a
compact local fixture. It must not load or run a language model.

## 2. Step 1: freeze the machine-readable task specification

Create a versioned Pilot A configuration that fixes:

- `Symbol8` and `Boolean` encodings at the canonical level;
- structural signatures, matched functional subtypes, and their exact semantics;
- parameter sets and rejection rules for degenerate programs;
- exact six-node C1-C4 graph templates;
- balancing axes and target counts;
- direct-read control construction;
- rendering families and operator-name randomization;
- discovery, confirmation, and control split rules;
- generator version, seed policy, and schema version.

Tokenizer-dependent display symbols remain an explicit unresolved rendering
field until a model revision is selected. Local tests use a declared placeholder
symbol bank and do not claim model compatibility.

## 3. Step 2: implement typed canonical programs

Introduce typed program nodes and validation that enforce input/output types,
acyclicity, a unique output, complete dependency references, deterministic
execution, and event-trace agreement. Each program records both the full
presented graph and the answer-relevant reference graph so distractors or control
material cannot silently become active computation.

The reference interpreter executes canonical semantics only. It must not parse
natural-language prompts and must not encode assumptions about model execution.

## 4. Step 3: implement the matched cell generator

Generate C1-C4 from explicit graph templates:

- C1: serial dependencies with externally supplied control;
- C2: fork-join dependencies with externally supplied control;
- C3: serial dependencies with an intermediate-state predicate;
- C4: fork-join dependencies with an intermediate-state predicate.

Within each valid contrast, match node count, structural-signature multiset where
logically possible, functional-subtype frequencies, answer frequencies,
parameter frequencies, operation placement,
prompt budget, and rendering count. Record every residual mismatch as a factor
rather than asserting perfect matching.

Reject constant-output, unused-active-node, unreachable-output, duplicate-
semantic, trivial-copy, and otherwise degenerate core programs. Construct
direct-read controls deliberately rather than allowing them to arise by accident.

## 5. Step 4: implement rendering without semantic leakage

Provide two paired renderings for every canonical core instance:

1. neutral symbolic order;
2. renamed and reordered surface form.

Operator display names are sampled independently of operation semantics.
Templates expose the information needed to solve the program but never the
task-side category names. Renderers preserve canonical identity and target, and
record exact template, vocabulary, order, and name-map provenance.

Aligned-trace and final-answer prompts are represented as separate render modes.
R1 must render exactly six state values in fixed delimiter slots and expose a
machine-readable mapping from every event to the delimiter immediately before
its value. No activation capture is implemented in this task.

## 6. Step 5: create leakage-resistant datasets

Generate:

- 1,024 discovery canonical instances: 32 per `cell x final answer`;
- 1,024 semantically disjoint confirmation instances with the same balance;
- at least 512 direct-read control instances;
- two paired renderings per core instance.

Every core program has exactly six answer-relevant nodes. Balance C1-C4 and all
eight final answers according to the protocol. Program-length generalization is
deferred. Split on semantic identity before rendering. Audit canonical, prompt,
parameter, and graph-template overlap separately.

## 7. Step 6: implement shortcut and balance audits

Implement deterministic baselines for answer frequency, direct input copying,
last displayed rule/value, operator-name cues, prompt length, and task-cell
metadata. These are dataset audits, not model-side analyses. The dataset report
must show counts and target distributions for every declared stratum and list
all residual imbalances.

Add an identifiability audit for each functional contrast. It must reject any
comparison whose label is deterministically recoverable from structural
signature, graph degree, event index, prompt region, output token, or task cell.
The two subtypes in each contrast must have identical position distributions and
co-occur at every analyzed position. The unary contrast must span at least two
positions. Single-position binary, predicate, and conditional contrasts are
allowed but cannot support position-generalization claims.

## 8. Step 7: preserve old calibration artifacts without privileging them

Do not use `function_composition` or `relational_path` as Pilot A scientific
cells unless a later reviewed plan says so. Preserve their code and fixtures as
regression coverage during this bounded implementation. Shared infrastructure
may be reused only when it supports the new specification without importing the
old task assumptions.

## 9. Step 8: local validation

Run no-network Python 3.11 checks for:

- reference-interpreter correctness and trace agreement;
- type, graph, and degeneracy validation;
- deterministic replay under fixed seeds;
- exact count and balance invariants;
- functional-subtype identifiability invariants;
- semantic-disjoint splits and overlap audits;
- paired-rendering equivalence;
- operator-name independence;
- shortcut-baseline behavior;
- malformed-config rejection;
- existing regression suite;
- JSON/YAML validity, bilingual links, and `git diff --check`.

A small deterministic fixture may be committed later only after implementation
approval and review. The full pilot dataset remains generated output.

## 10. Proposed file scope

| Path | Action | Purpose |
|---|---|---|
| `src/reasoning_role/tasks/pilot_a_program.py` | create | typed programs, matched subtypes, interpreter, six-node graph templates |
| `src/reasoning_role/tasks/pilot_a_controls.py` | create | direct-read and audit controls |
| `src/reasoning_role/tasks/schema.py` | modify if required | typed event and graph metadata |
| `src/reasoning_role/tasks/registry.py` | modify | register the new task instrument |
| `src/reasoning_role/data/generate.py` | modify or bypass through a new module | support non-chain factor schemas without treating old assumptions as normative |
| `src/reasoning_role/data/pilot_a.py` | create if separation is cleaner | Pilot A generation and audits |
| `configs/data/pilot_a_v1.yaml` | create | frozen local generation contract |
| `scripts/generate_pilot_a.py` | create if the generic CLI is insufficient | checkout-local entry point |
| `tests/tasks/test_pilot_a_program.py` | create | semantics, typing, graph, degeneracy tests |
| `tests/data/test_pilot_a_generation.py` | create | determinism, balance, identifiability, split, rendering, shortcut tests |
| `tests/fixtures/pilot_a_smoke/` | create | compact deterministic engineering fixture |
| `docs/DATA.md` and counterpart | modify | schema, split, and interpretation boundaries |
| `docs/EVALUATION.md` and counterpart | modify | behavior gates and response regimes |
| `runs/pilot-a-design-v1/REVIEW.md` and counterpart | create after implementation | delivery and validation handoff |

The executor may choose between extending `generate.py` and creating a separate
Pilot A module only after showing that the choice does not reintroduce the old
linear-chain factor schema. Any path expansion requires review.

## 11. Subsequent gates

This implementation ends after local generation and validation. The following
remain separate future actions:

1. resolve exact Mistral model and tokenizer SHAs and verify single-token symbols;
2. create and review a behavior-only server run contract;
3. run and review the behavioral feasibility gate;
4. create and review an R1 residual-stream capture contract;
5. implement discovery and confirmation analyses from separately frozen plans.

## 12. Known open choices

- Exact immutable Mistral checkpoint and tokenizer revision.
- Whether Llama is used as an alternative pilot or later replication model.
- Tokenizer-compatible render symbol bank.
- Exact regularization, score, uncertainty estimator, clustering method, and
  multiplicity policy for model-side analysis.
- R2 measurement unit and alignment rule.

These choices are inactive while this plan is paused. Target grounding now
blocks any local canonical-task implementation under this task ID.

## 13. Approval gate

This review gate is superseded by `pilot-a0-target-grounding-v1`. This plan is not
eligible for implementation approval. A future Pilot A plan may reuse only
elements that receive source-based grounding and explicit renewed approval.
