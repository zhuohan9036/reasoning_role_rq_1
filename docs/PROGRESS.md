# Progress and evidence log

## Milestones

| Milestone | Status | Evidence/artifact | Next gate |
|---|---|---|---|
| P0: repository and planning scaffold | Complete locally | Research and approved task plan; local commit `9896194` | Push when authorized |
| P1: task-side calibration dataset | Complete locally | `runs/task-modeling-v1/REVIEW.md`; smoke fixture | Human review; decide whether to push |
| P2: behavioral and instrumentation baseline | Not started | None | Resolve O-001, O-002, O-004, O-008 |
| P3: model-side pattern discovery | Not started | None | Freeze discovery/evaluation protocol |
| P4: function-versus-structure tests | Not started | None | Pass leakage and confound audit |
| P5: stability and cross-task transfer | Not started | None | Freeze task-pair rationale |
| P6: second-model replication | Not started | None | Select smallest decisive replication set |

## Current task

`task-modeling-v1` was approved and completed locally on 2026-09-08 with both
pilot families, hidden intermediate task-side annotations, and Python 3.11. The
larger configuration and every server/model experiment remain unexecuted and
unauthorized.

## Empirical conclusions

None. The current documents are plans, not evidence.

The successful data smoke test is engineering validation only. It does not
provide evidence for or against functional differentiation in a Transformer.

## Completed task: task-modeling-v1

- Date: 2026-09-08.
- Research goal: G0; infrastructure enabling later G2–G4 tests.
- Implementation revision: `d574c3e`.
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
