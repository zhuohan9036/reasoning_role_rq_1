# Progress and evidence log

## Milestones

| Milestone | Status | Evidence/artifact | Next gate |
|---|---|---|---|
| P0: repository and planning scaffold | Complete and pushed | Research plan and repository history | None |
| P1: task-side calibration dataset | Complete and pushed | `runs/task-modeling-v1/REVIEW.md`; smoke fixture | Research review |
| P2a: behavioral calibration harness | Planning | `runs/behavioral-calibration-v1/` | Human review of three choices |
| P2b: real-model behavioral pilot | Blocked | No model run | Resolve O-001/O-002/O-009/O-013 and authorize server |
| P2c: instrumentation baseline | Not started | None | Behavioral gate plus O-004/O-008 |
| P3: model-side pattern discovery | Not started | None | Freeze discovery/evaluation protocol |
| P4: function-versus-structure tests | Not started | None | Pass leakage and confound audit |
| P5: stability and cross-task transfer | Not started | None | Freeze task-pair rationale |
| P6: second-model replication | Not started | None | Select smallest decisive replication set |

## Current task

`task-modeling-v1` was approved and completed locally on 2026-09-08 with both
pilot families, hidden intermediate task-side annotations, and Python 3.11. The
larger configuration and every server/model experiment remain unexecuted and
unauthorized.

The proposed next task is `behavioral-calibration-v1`. Its plan is awaiting
review and does not authorize code changes or a real-model run.

## Empirical conclusions

None. The current documents are plans, not evidence.

The successful data smoke test is engineering validation only. It does not
provide evidence for or against functional differentiation in a Transformer.

## Completed task: task-modeling-v1

- Date: 2026-09-08.
- Research goal: G0; infrastructure enabling later G2–G4 tests.
- Implementation revisions: `d574c3e` and reviewed fixture source `2d139b1`.
- Artifact: `tests/fixtures/task_calibration_smoke/manifest.json`.
- Result: 80 records generated and independently rechecked; deterministic replay,
  graph validation, balance checks, and cross-split overlap audits passed.
- Interpretation: the task-side calibration interface is locally operational;
  no model-side claim was tested.

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
