# Progress and evidence log

> 中文版：[PROGRESS.zh-CN.md](PROGRESS.zh-CN.md)

## Milestones

| Milestone | Status | Evidence/artifact | Next gate |
|---|---|---|---|
| P0: repository and planning scaffold | Complete and pushed | Research plan and repository history | None |
| P0b: task formalism and Codex handoff specification | Complete and pushed | `runs/research-specification-v1/REVIEW.md`; revision `901507d` | None |
| P0c: candidate Pilot A calibration sandbox | Protocol v0.2 documented; implementation paused | `docs/PILOT_A.md`; `runs/pilot-a-design-v1/PLAN.md` v2 | Pilot A0 grounding |
| P0d: Pilot A0 native-source and model-first plan | Protocol v0.2 and plan v2 generated; awaiting review | `docs/PILOT_A0.md`; `runs/pilot-a0-target-grounding-v1/PLAN.md` | Resolve source provenance/access choices |
| P1: task-side calibration dataset | Complete and pushed | `runs/task-modeling-v1/REVIEW.md`; smoke fixture | Research review |
| P2a: behavioral calibration harness | Complete and pushed | `runs/behavioral-calibration-v1/REVIEW.md`; fake smoke fixture | Research review and working-norm update |
| P2b: real-model behavioral pilot | Blocked | No model run | Complete grounded Pilot A design, then resolve model/server requirements |
| P2c: instrumentation baseline | Not started | None | Behavioral gate plus O-004/O-008 |
| P3: model-side pattern discovery | Not started | None | Freeze discovery/evaluation protocol |
| P4: function-versus-structure tests | Not started | None | Pass leakage and confound audit |
| P5: stability and cross-task transfer | Not started | None | Freeze task-pair rationale |
| P6: second-model replication | Not started | None | Select smallest decisive replication set |

## Current task

`pilot-a0-target-grounding-v1` now contains protocol v0.2 and plan v2 for a no-
annotation source inventory and a model-first route: benchmark-faithful native
inference, activation/transition trajectories, label-free within-task discovery,
frozen cross-task transfer, and later bounded interpretation. GSM8K, DROP,
MuSiQue-Ans v1.0, and two BIG-Bench tasks are the accepted initial source
strata. Exact source revisions, licenses, split reservations, and access remain
open. Implementation, benchmark inspection/download, code, models, activations,
servers, commit, and push are unauthorized.

New manual annotation and synthetic task construction are frozen as fallback
tools only. A recurring app automation named `RQ1 文献差异性追踪` is active and
will report only materially relevant new research or methodological changes;
relevant work encountered during ordinary project work must also be surfaced.

`pilot-a-design-v1` records protocol v0.2 and plan v2. Functional subtypes
are compared only within matched structural signatures; every core program has
six answer-relevant nodes; and R1 measurement is fixed at the delimiter before
each predicted state symbol. It retains the four topology/control cells,
negative controls, discovery/confirmation separation, and staged gates. Qwen is
excluded. Existing generators are non-authoritative. The task design is now a
candidate calibration sandbox because its connection to the target population
was not established. Its implementation plan is paused before code changes.

`research-specification-v1` was implemented, reviewed, committed, and pushed on
2026-09-09 as revision `901507d`. It formalizes task-side objects, separates
pilot-informed construct definition from independent confirmation, and defines
the planning-conversation to Codex document handoff. It changed no executable
code and created no empirical evidence.

`task-modeling-v1` was approved and completed locally on 2026-09-08 with two
calibration families, hidden intermediate task-side annotations, and Python
3.11. Those families are engineering artifacts rather than accepted Pilot A
scientific tasks. The larger configuration and every server/model experiment
remain unexecuted and unauthorized.

`behavioral-calibration-v1` was approved and completed locally on 2026-09-08 with
final-answer-only prompts, a generic Hugging Face adapter, and the provisional
thresholds. The 80-record offline fake run verifies the harness only. Downloads
and real-model/server runs remain unauthorized.

## Empirical conclusions

None. The current documents are plans, not evidence.

The successful data and behavioral fake smoke tests are engineering validation
only. They do not provide evidence for or against functional differentiation in
a Transformer.

## Documentation synchronization

On 2026-09-08, all 17 human-facing Markdown documents were paired with
synchronized Chinese versions using the `.zh-CN.md` suffix and reciprocal
language links. Machine-readable contracts and generated artifacts remain
single-source.

The same update established separate discussion, plan-generation,
implementation, and server-run approvals plus an ignored local handoff path for
large server results. No research plan, model run, or server action was started.

## Completed task: task-modeling-v1

- Date: 2026-09-08.
- Research goal: G0; infrastructure enabling later G2–G4 tests.
- Implementation revisions: `d574c3e` and reviewed fixture source `2d139b1`.
- Artifact: `tests/fixtures/task_calibration_smoke/manifest.json`.
- Result: 80 records generated and independently rechecked; deterministic replay,
  graph validation, balance checks, and cross-split overlap audits passed.
- Interpretation: the task-side calibration interface is locally operational;
  no model-side claim was tested.

## Completed task: behavioral-calibration-v1

- Date: 2026-09-08.
- Research goal: G0 behavioral calibration; prerequisite for G1–G4.
- Implementation revisions: `4797581` and `17fda49`; fake fixture generated
  from clean revision `17fda49`.
- Artifact: `tests/fixtures/behavioral_smoke/run_manifest.json`.
- Result: 80/80 attempted records reconciled; deterministic replay, strict
  parsing, resume/provenance rejection, summary denominators, and the stubbed
  frozen-model adapter contract passed local checks.
- Interpretation: the evaluation harness is locally operational. The fake
  backend's 75% exact-match result is deliberately synthetic and is not model
  evidence or a failed research gate.
- Deferred: select immutable model/tokenizer revisions, complete the server
  specification, authorize downloads/execution, and run the real behavioral
  pilot.

## Update template

For each completed task or experiment, append:

- date and run ID;
- research goal and claim tested;
- exact configuration and code revision;
- artifact locations and checksums;
- planned and unplanned deviations;
- result with uncertainty;
- weakest justified interpretation;
- failed checks, alternative explanations, and next decision.
