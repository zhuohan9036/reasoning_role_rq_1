# Reasoning Role RQ1

This repository supports a characterization study of whether frozen pretrained
Transformers exhibit stable functional differentiation during multi-step
reasoning.

The project deliberately distinguishes:

- task-side descriptions of required computation;
- model-side patterns measured from internal computation; and
- stronger interpretations such as a reusable "reasoning role."

The current repository contains an initial research plan and a proposed first
implementation task. No experimental code has been approved or implemented.

## Current workflow state

1. Research plan drafted.
2. First implementation plan drafted under `runs/task-modeling-v1/`.
3. Human review required before implementation begins.

## Repository layout

- `docs/RESEARCH.md`: research question, hypotheses, evidence plan, and scope.
- `docs/DECISIONS.md`: accepted decisions, working hypotheses, and open choices.
- `docs/PROGRESS.md`: milestone and evidence log.
- `runs/<task-id>/BRIEF.md`: the requested outcome for one bounded task.
- `runs/<task-id>/SERVER.md`: execution-environment assumptions and unknowns.
- `runs/<task-id>/PLAN.md`: human-readable implementation plan.
- `runs/<task-id>/plan.json`: structured implementation contract.

Large datasets, model weights, activation dumps, and full experiment logs must
not be committed. Commit small manifests, summaries, figures, and the exact
configuration needed to reproduce them.
