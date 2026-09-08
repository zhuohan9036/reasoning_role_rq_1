# Reasoning Role RQ1

> 中文版：[README.zh-CN.md](README.zh-CN.md)

This repository supports a characterization study of whether frozen pretrained
Transformers exhibit stable functional differentiation during multi-step
reasoning.

The project deliberately distinguishes:

- task-side descriptions of required computation;
- model-side patterns measured from internal computation; and
- stronger interpretations such as a reusable "reasoning role."

The current repository contains the initial research plan, the approved
task-calibration milestone, and a locally verified behavioral-evaluation
harness. It contains no activation analysis or completed real-model experiment.

## Current workflow state

1. Research plan drafted.
2. `task-modeling-v1` implemented and verified locally on Python 3.11.
3. `behavioral-calibration-v1` implemented and verified locally with an offline
   fake backend; this is engineering evidence only.
4. Real-model downloads and server execution remain unauthorized and have not
   started.

## Repository layout

- `docs/RESEARCH.md`: research question, hypotheses, evidence plan, and scope.
- `docs/DECISIONS.md`: accepted decisions, working hypotheses, and open choices.
- `docs/PROGRESS.md`: milestone and evidence log.
- `docs/WORKFLOW.md`: discussion, planning, implementation, and authorization gates.
- `docs/SERVER_HANDOFF.md`: compact server-result transfer and review contract.
- `runs/<task-id>/BRIEF.md`: the requested outcome for one bounded task.
- `runs/<task-id>/SERVER.md`: execution-environment assumptions and unknowns.
- `runs/<task-id>/PLAN.md`: human-readable implementation plan.
- `runs/<task-id>/plan.json`: structured implementation contract.
- `artifacts/server-results/<run-id>/`: ignored local handoff bundles copied from
  a server.
- `results/<run-id>/`: reviewed compact evidence and bilingual result reports.

Human-facing Markdown documents have synchronized Chinese counterparts with the
`.zh-CN.md` suffix. Machine-readable files such as `plan.json` remain a single
canonical version.

Large datasets, model weights, activation dumps, and full experiment logs must
not be committed. Commit small manifests, summaries, figures, and the exact
configuration needed to reproduce them.
