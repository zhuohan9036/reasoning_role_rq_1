# Repository instructions

> 中文版：[AGENTS.zh-CN.md](AGENTS.zh-CN.md)

## Scientific scope

The paper asks whether frozen pretrained Transformers display stable functional
differentiation during multi-step reasoning. RQ1 is a characterization study.
Do not turn correlational evidence into a causal claim.

Maintain these distinctions in code, documentation, and reports:

1. A task-side computation graph describes a generator or an externally
   specified solution procedure. It is not a claim about the model's internal
   algorithm.
2. An observed model-side cluster or pattern is not automatically a reasoning
   role.
3. Component identity, layer, token position, and reasoning step are possible
   confounds, not definitions of functional identity.
4. Candidate operations are provisional labels. Do not describe them as atomic,
   universal, or cognitively fundamental without evidence.
5. Negative, partial, task-specific, distributed, and implementation-varying
   outcomes are valid results.

Primary evidence should come from frozen pretrained models with mechanistic
access. Controlled or adapted models may be diagnostic instruments, but must be
reported separately from naturally occurring organization.

## Workflow gates

- Read `docs/RESEARCH.md`, `docs/DECISIONS.md`, and the relevant `runs/<task-id>/`
  files before changing code.
- Work on one bounded task at a time.
- Do not implement a task while its plan status is `awaiting_review`.
- After approval, implement only the approved in-scope items. Record deviations
  in the task review rather than silently expanding scope.
- Do not start remote/server experiments unless the user explicitly authorizes
  them.
- End each implementation task with tests and `runs/<task-id>/REVIEW.md`.

## Documentation languages

- Every human-facing Markdown document must have an English version and a
  Chinese counterpart named with the `.zh-CN.md` suffix. Keep both versions
  semantically synchronized in the same change.
- Each language version must link to its counterpart near the top of the file.
- Code, configuration, generated artifacts, and machine-readable contracts such
  as `plan.json` remain single-source unless an approved plan requires otherwise.

## Reproducibility

- Configuration, seeds, data-generation version, code revision, environment,
  and output schema must be recorded for every experiment.
- Keep small validation fixtures and summary results in Git. Keep large data,
  weights, activations, checkpoints, and logs outside Git and record their paths,
  hashes, and generation commands.
- Prevent split leakage using semantic instance identities, not prompt strings
  alone.
- Prefer independently checkable invariants over snapshot-only tests.

## Engineering

- Target Python 3.11 unless an approved task plan says otherwise.
- Put reusable code under `src/`, entry points under `scripts/`, configurations
  under `configs/`, and tests under `tests/`.
- Avoid embedding workstation- or server-specific absolute paths in committed
  code and configuration.
- Keep generated natural-language prompts separate from canonical task records.
