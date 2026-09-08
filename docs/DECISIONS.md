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
| O-001 | Exact primary and replication models/revisions | Instrumentation implementation |
| O-002 | Direct-answer versus visible-scratchpad conditions | Prompt and trace design |
| O-003 | Final pilot task families after calibration | Primary dataset freeze |
| O-004 | Model-side measurement unit | Trace-capture implementation |
| O-005 | Discovery and stability method | Confirmatory model-side analysis |
| O-006 | Token/event alignment protocol | Functional correspondence tests |
| O-007 | Main statistical model and multiplicity policy | Confirmatory analysis |
| O-008 | Accuracy threshold and example inclusion policy | Activation collection |
| O-009 | Server GPU, CUDA, storage, scheduler, and environment | Any server run |
| O-010 | Dataset size and storage location for primary runs | Dataset freeze |
| O-013 | Exact pilot model and tokenizer revisions | Real-model pilot run |

## Decision-change policy

When a decision changes, append a new entry rather than silently rewriting its
rationale. Record the affected run IDs and whether existing artifacts must be
regenerated. Implementation plans may instantiate an open choice only when the
choice is local, reversible, and explicitly labeled as provisional.
