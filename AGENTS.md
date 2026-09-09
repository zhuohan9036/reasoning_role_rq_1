# Repository instructions

> 中文版：[AGENTS.zh-CN.md](AGENTS.zh-CN.md)

## Scientific scope

The paper asks whether frozen pretrained Transformers display stable functional
differentiation during multi-step reasoning. RQ1 is a characterization study.
Do not turn correlational evidence into a causal claim.

Maintain these distinctions in code, documentation, and reports:

1. A workflow task ID names a bounded repository action; it is not a reasoning
   task family or task instance.
2. A task-side dependency structure describes one reference solver, a family of
   valid solution graphs, or declared partial-order constraints. It is not a
   claim about the model's internal algorithm.
3. An observed model-side cluster or pattern is not automatically a reasoning
   role.
4. Component identity, layer, token position, and reasoning step are possible
   confounds, not definitions of functional identity.
5. Candidate operations and task-side cross-task correspondences are
   provisional hypotheses. Do not describe them as atomic, universal, or
   cognitively fundamental without evidence.
6. Model-side empirical correspondence is a result requiring independent
   measurement, structural controls, and held-out evaluation.
7. Negative, partial, task-specific, distributed, and implementation-varying
   outcomes are valid results.

Before an exploratory model pilot, require a thin task specification covering
instances, answers, provenance, rendering, and major structural covariates.
Version and freeze any pilot-informed task decomposition or role vocabulary
before testing it on untouched evidence.

Primary evidence should come from frozen pretrained models with mechanistic
access. Controlled or adapted models may be diagnostic instruments, but must be
reported separately from naturally occurring organization.

## Workflow gates

- Treat the planning conversation and Codex execution as separate roles even if
  they occur in the same client. The conversation freezes bounded requirements;
  Codex acts only from an explicitly authorized document state.

- Read `docs/RESEARCH.md`, `docs/DECISIONS.md`, and the relevant `runs/<task-id>/`
  files before changing code.
- Work on one bounded task at a time.
- Start every prospective task in a discussion-only state. Discussion may be
  iterative and does not authorize planning-file generation, repository edits,
  code changes, downloads, or execution.
- Before generating a plan, present an explicit action preview in the
  conversation. It must name the task, the proposed planning action, frozen
  discussion consensus, unresolved items, exact outputs and review paths, Git
  behavior, exclusions, and the authorization phrase being requested.
- Generate `BRIEF.md`, `SERVER.md`, `PLAN.md`, their Chinese counterparts, and
  `plan.json` only after the user explicitly authorizes the planning action.
  Planning authorization does not authorize implementation.
- Do not implement a task while its plan status is `awaiting_review`.
- For cross-client handoff, identify the exact task ID, plan path, approved
  revision or working-tree state, and Git behavior. Do not infer authorization
  from the existence of a plan.
- After explicit implementation approval, implement only the approved in-scope
  items and local checks. Record deviations in the task review rather than
  silently expanding scope.
- Treat remote/server execution as a separate gate. Require explicit
  authorization for the named run or command scope even when implementation was
  already approved.
- End each implementation task with tests and `runs/<task-id>/REVIEW.md`.
- At the end of every planning, implementation, or server-review action, report
  what ran, what did not run, all outputs and review paths, validation results,
  the Git commit/push state, and the exact next approval required.
- Follow the full state and authorization contract in `docs/WORKFLOW.md`.

## Server-result handoff

- Follow `docs/SERVER_HANDOFF.md` for server-to-local result transfer.
- Git does not carry uncommitted server artifacts. Place a compact handoff bundle
  under the ignored local path `artifacts/server-results/<run-id>/` or provide an
  explicitly accessible mounted path.
- Keep large weights, activations, checkpoints, and full logs on the server.
  Record their server location, size, checksum, schema, and producing revision
  in `artifact_index.json`.
- Verify the handoff manifest and checksums before analysis. Request only the
  smallest additional slice needed when compact results are insufficient.
- Commit only reviewed compact evidence and bilingual reports under
  `results/<run-id>/`; never commit the ignored handoff bundle itself.

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
