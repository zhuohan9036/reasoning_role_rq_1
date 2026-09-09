# Implementation Review: research-specification-v1

> 中文：[REVIEW.zh-CN.md](REVIEW.zh-CN.md)

**Status:** implemented and locally validated; awaiting human review
**Review date:** 2026-09-09
**Git behavior:** uncommitted; not pushed

## Result

The approved documentation-only revision is implemented. The research
specification now defines versioned task-side objects, permits pilot-informed
exploratory refinement under a freeze-and-held-out-confirmation rule, and keeps
task-side hypotheses separate from model-side empirical results. The workflow
and repository instructions now define an explicit planning-conversation to
Codex document handoff.

No executable code, test, configuration, fixture, generated artifact, model, or
server state was changed.

## Delivered changes

- `docs/RESEARCH.md` and `docs/RESEARCH.zh-CN.md`: distinguish workflow tasks
  from reasoning tasks; define task-family specifications, canonical instances,
  reference dependency representations, candidate operations, two levels of
  correspondence, and staged commitment.
- `docs/WORKFLOW.md` and `docs/WORKFLOW.zh-CN.md`: define the planning
  conversation, Codex plan generation, human review, Codex implementation, and
  review handoff; add an explicit cross-client authorization form.
- `docs/DECISIONS.md` and `docs/DECISIONS.zh-CN.md`: add accepted decisions
  D-016 through D-018 without rewriting earlier rationale.
- `docs/PROGRESS.md` and `docs/PROGRESS.zh-CN.md`: record a local documentation
  milestone without claiming empirical progress.
- `AGENTS.md` and `AGENTS.zh-CN.md`: make the terminology, staged commitment,
  and cross-client handoff operational for future Codex tasks.
- This bilingual review records implementation and the next gate.

## Validation

- `plan.json` parses successfully.
- Every human-facing Markdown file has a bilingual counterpart and reciprocal
  language link.
- The task, operation, correspondence, model-side, and causal terminology audit
  passes for the revised scope.
- Reference dependency structures remain external specifications rather than
  model mechanisms.
- Pilot-informed constructs require versioning, freezing, and untouched
  evidence for confirmation.
- Changed paths match the approved documentation scope plus lifecycle status
  updates to this task's planning artifacts.
- `git diff --check` passes.
- No test suite was run because executable code was out of scope.

## Deviation

The implementation-file table did not list administrative status updates to the
existing `BRIEF`, `PLAN`, and `plan.json`. Those task-local files were updated so
the contract would not remain incorrectly marked `awaiting_review` after the
authorized implementation. This changes no scientific or implementation scope.

## Scientific boundary

This revision establishes research definitions and governance only. It does not
select final task families or operations, establish cross-task correspondence,
measure a model, or provide evidence for functional differentiation or
reasoning roles.

## Next gate

Human review is required. Acceptance of these local documentation changes does
not authorize a commit, push, model download, experiment, or server action.

