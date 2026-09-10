# Decision log

> 中文版：[DECISIONS.zh-CN.md](DECISIONS.zh-CN.md)

This file separates established research commitments from provisional working
hypotheses and unresolved choices. A convenience of implementation is not a
scientific commitment.

## Accepted decisions

### D-001 — RQ1 is a characterization question

**Status:** accepted
**Decision:** The paper asks whether functional differentiation exists, what it
tracks, how stable it is, and how far it generalizes. Correlation, probing,
clustering, or representation similarity alone will not be described as causal
evidence.

### D-002 — Task-side and model-side structure remain distinct

**Status:** accepted
**Decision:** Generator traces, dependency graphs, and candidate operation labels
are external task descriptions. Model-side patterns will be measured
independently before correspondence is interpreted.

### D-003 — Competing explanations remain live

**Status:** accepted
**Decision:** Structural-only, task-specific, cross-task reusable, and
implementation-mobile explanations will all be tested. Negative and mixed
results are valid outcomes.

### D-004 — Frozen pretrained models provide primary evidence

**Status:** accepted
**Decision:** The main claims will rely on frozen pretrained Transformers with
mechanistic access. Training or adaptation may be used only as a separately
identified diagnostic.

### D-005 — Physical component identity does not define functional identity

**Status:** accepted
**Decision:** Fixed head, MLP, or layer indices may be measured but cannot by
themselves define a reasoning role.

### D-006 — First implementation task is task calibration

**Status:** accepted
**Decision:** The first bounded code task will implement a canonical task-record
schema, deterministic generators and reference solvers for two pilot task
families, leakage-resistant splits, manifests, and validation tests. It will not
load a Transformer or implement model-side analysis.

### D-007 — Intermediate task states remain hidden annotations

**Status:** accepted
**Decision:** Canonical records may retain intermediate task-side states for
validation and later alignment research, but default prompts must never expose
them. They are generator provenance, not model chain of thought.

### D-008 — Python 3.11 is the project baseline

**Status:** accepted
**Decision:** Code targets Python 3.11. Local verification on a newer compatible
Python version may supplement but does not replace the required Python 3.11
compatibility check.

### D-009 — Task-side calibration v1 is locally accepted

**Status:** accepted
**Decision:** `task-modeling-v1` passed its local acceptance checks. Its smoke
run is engineering validation only and provides no evidence for or against
model-side functional differentiation.

### D-010 — Behavioral calibration is the proposed next task

**Status:** accepted
**Decision:** The next bounded task will build a model-output-only behavioral
evaluation harness with a fake local backend and a generic frozen Hugging Face
adapter. Activation capture and real-model execution remain separate gates.

### D-011 — Behavioral pilot uses final-answer-only prompts

**Status:** accepted
**Decision:** Behavioral calibration v1 uses the existing final-answer-only
prompts, greedy decoding, and no visible scratchpad. Any scratchpad comparison
must be planned as a separate experimental condition.

### D-012 — Behavioral pilot thresholds are provisional engineering gates

**Status:** accepted
**Decision:** The provisional gate is 80% overall trimmed exact match, 60% for
every evaluated chain-length cell, and at most 5% invalid-format or inference
failures. Passing does not support a paper claim or authorize mechanistic use.

### D-013 — Human-facing documentation is bilingual

**Status:** accepted
**Decision:** Every human-facing Markdown document has an English version and a
synchronized Chinese counterpart using the `.zh-CN.md` suffix. Code,
configuration, generated artifacts, and machine-readable contracts such as
`plan.json` remain single-source unless a later approved plan says otherwise.

### D-014 — Discussion, planning, and implementation require separate approval

**Status:** accepted
**Decision:** Every prospective task begins with iterative discussion. Before
creating planning files, the assistant must present a concrete action preview
that identifies the action, outputs, review paths, Git behavior, and exclusions.
The user must explicitly authorize plan generation. That authorization creates
reviewable planning artifacts only; implementation requires a second explicit
approval, and server execution requires a third run-specific approval.

### D-015 — Server results use an ignored local handoff bundle

**Status:** accepted
**Decision:** Large server artifacts remain outside Git. Each server run produces
a compact manifest, summary, diagnostics, and artifact index that can be copied
to `artifacts/server-results/<run-id>/` for local review. Only reviewed compact
evidence and bilingual reports may be promoted to `results/<run-id>/` and
committed.

### D-016 — Task-side objects use a versioned structural formalism

**Status:** accepted
**Decision:** A task family specifies its instance distribution, correctness
semantics, reference-solution interface, rendering family, controlled and
nuisance variables, semantic identity, reference dependency representation,
version, and provenance. Canonical instances and rendered prompts remain
separate objects. A workflow task ID is not a reasoning task.

### D-017 — Pilot-informed constructs require independent confirmation

**Status:** accepted
**Decision:** A thin task specification is required before exploratory model
pilots. Pilot evidence may motivate revised task decompositions, candidate
operations, or cross-task hypotheses, but the revision must receive a new
version and be frozen before evaluation on untouched evidence. Candidate
operations and task-side correspondences are hypotheses; model-side empirical
correspondence is a result.

### D-018 — Planning and Codex implementation use an explicit document handoff

**Status:** accepted
**Decision:** The planning conversation freezes bounded requirements without
editing the repository. After an approved action preview, Codex creates
reviewable planning artifacts. Human plan review and explicit implementation
approval precede Codex changes. `plan.json` is the machine-readable contract;
bilingual plans and reviews are the human interface. Commit, push, model, and
server permissions remain separately declared.

### D-019 — Pilot A is a pattern-discovery and measurement-validation pilot

**Status:** accepted
**Decision:** Pilot A develops a controlled measurement environment and may only
support claims scoped to the named model, task distribution, and response
regime. It does not establish universal primitives, general reasoning roles,
cross-domain generality, or causal necessity.

### D-020 — Pilot A uses a matched task-language design

**Status:** accepted
**Decision:** A provisional typed task language crosses serial versus fork-join
topology with externally supplied versus intermediate-state-computed control.
Transform, merge, predicate, and select are task-language categories only. A
direct-read control, paired rerenderings, and untouched semantic instances are
required. The detailed protocol is `docs/PILOT_A.md`.

### D-021 — Existing generators do not define Pilot A

**Status:** accepted
**Decision:** The implemented `function_composition` and `relational_path`
families are non-authoritative engineering calibration artifacts. Pilot A design
is derived from the scientific contrasts and may reuse, replace, or bypass their
infrastructure without granting their task assumptions privileged status.

### D-022 — Pilot A excludes Qwen and defaults to a Mistral-class model

**Status:** accepted
**Decision:** Qwen models are excluded from Pilot A. The working default is a
frozen instruction-tuned Mistral model in the 7B class, currently
`mistralai/Mistral-7B-Instruct-v0.3`; a comparable Llama instruct checkpoint is
the preferred alternative. Exact immutable model and tokenizer revisions remain
required before execution.

### D-023 — Pilot A stages behavior, aligned measurement, and confirmation

**Status:** accepted
**Decision:** Behavior is evaluated before activations. The first measurement is
the residual stream at aligned events in an explicit trace regime. Pattern
definitions are frozen before untouched confirmation. Final-answer-only
measurement, head/MLP capture, interventions, and semantic-domain replication
require later bounded plans.

### D-024 — Functional contrasts must match structural signatures

**Status:** accepted; supersedes the coarse-label detail in D-020
**Decision:** Transform, merge, predicate, and select are structural task-language
families, not the primary functional labels. Pilot A compares functional
subtypes only within identical input/output signatures: `shift/reflect`,
`add_merge/subtract_merge`, `parity/upper_half`, and
`select_if/select_unless`. Core programs have six answer-relevant nodes. R1
measures the residual stream at the fixed delimiter immediately before each
state symbol. Functional-subtype labels must pass a pre-model identifiability
audit against graph and position metadata.

### D-025 — Target-task grounding precedes the scientific Pilot A task

**Status:** accepted; supersedes the implementation-ready implication of
D-019 through D-024, while retaining their calibration and control principles
**Decision:** The paper's intended destination is current mainstream textual
multi-step reasoning. Before selecting the scientific Pilot A task, the project
must freeze a target-task population, reconstruct a provenance-backed source
sample independently of model activations, derive candidate motifs from that
audit, and require an abstraction map plus return-to-source test for every
benchmark-derived microtask. `Symbol8`, its proposed function pairs, and C1-C4
are relegated to candidate calibration-sandbox status unless Pilot A0 grounds
them. The `pilot-a-design-v1` implementation plan is paused before code changes.

### D-026 — Discovery starts from native inference and model-side patterns

**Status:** accepted; supersedes the annotation-first and controlled-task-first
method implied by D-023 through D-025
**Decision:** The primary route begins with successful, benchmark-faithful native
inference on the accepted source strata. It captures model-side activation and
transition trajectories, discovers recurring within-task patterns without
task-operation labels, freezes those patterns, and tests cross-task transfer
before assigning a functional interpretation. Generated reasoning is behavior,
not latent ground truth. Mutual information is an auxiliary association
diagnostic, not an operation detector or causal test. New manual annotation and
synthetic task construction are deferred fallback tools that require a named
identification failure, a new bounded plan, and explicit approval.

### D-027 — Maintain an active literature-differentiation watch

**Status:** accepted
**Decision:** Whenever directly relevant research is encountered, report its
primary source, date, core result, overlap with this project, methodological
difference, and implication for novelty or design. A recurring literature watch
supplements this continuous rule and notifies only on materially relevant new
work or methodological change.

## Working hypotheses

These guide experimental design but are not assumed true.

### WH-001 — Function-related signal may survive structural controls

At least some internal computation patterns may predict a candidate operation on
held-out layers, positions, or reasoning steps better than structure-only and
permuted-label baselines.

### WH-002 — Some patterns may transfer across controlled task families

Tasks with different semantics and surface forms but a carefully justified
shared computation may exhibit cross-task correspondence. Transfer may be
partial or absent.

### WH-003 — Functional stability may exceed component stability

A computation-level pattern may be stable even when its physical implementation
shifts across components, inputs, or architectures.

## Open decisions

| ID | Decision needed | Required before |
|---|---|---|
| O-001 | Exact Mistral model/tokenizer revisions and later replication model | Any real-model run |
| O-003 | Exact repositories, immutable revisions/checksums, licenses, eligible splits, and return-test reservations for accepted source strata | Any source inventory implementation |
| O-005 | Exact readout, discovery, and stability methods | Model-side analysis implementation |
| O-006 | R2 final-answer-only measurement unit and alignment | R2 activation capture |
| O-007 | Uncertainty estimator and multiplicity policy | Confirmation analysis |
| O-009 | Server GPU, CUDA, storage, scheduler, and environment | Any server run |
| O-013 | Tokenizer-compatible single-token `Symbol8` rendering and delimiter bank, only if retained | Any real-model run using v0.2 elements |
| O-014 | Source access mode and whether inventory may inspect schemas only or a small declared instance set | Pilot A0 implementation |
| O-015 | First native task/task pair, benchmark-faithful prompt, decoding, and behavioral gate | Native behavioral pilot plan |
| O-016 | Activation unit, capture scope, alignment, storage, MI/predictive, trajectory, and transfer methods | Model-side instrumentation and analysis plans |

## Decision-change policy

When a decision changes, append a new entry rather than silently rewriting its
rationale. Record the affected run IDs and whether existing artifacts must be
regenerated. Implementation plans may instantiate an open choice only when the
choice is local, reversible, and explicitly labeled as provisional.
