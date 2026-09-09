# Discussion-to-execution workflow

> 中文版：[WORKFLOW.zh-CN.md](WORKFLOW.zh-CN.md)

## Purpose

This project separates research discussion, plan generation, implementation,
and server execution into independently authorized stages. A useful discussion,
a plausible action, an approved plan, and an authorized experiment are not the
same decision.

The assistant must never infer later-stage authorization from enthusiasm,
agreement with an idea, approval of an earlier stage, or the existence of a
repository and plan.

## Planning-conversation to Codex handoff

The workflow is role- and document-based even when planning and implementation
occur in different clients:

1. The **planning conversation** discusses the science and engineering, records
   tentative consensus in the conversation, and does not modify the repository.
2. After an approved action preview, **Codex plan generation** creates bilingual
   `BRIEF`, `SERVER`, and `PLAN` documents plus one `plan.json` in
   `awaiting_review` state.
3. **Human review** accepts, rejects, or revises that contract. Informal agreement
   with an idea is not implementation approval.
4. After separate explicit approval, **Codex implementation** changes only the
   approved paths and runs only the approved checks.
5. A bilingual **review handoff** records actual delivery, validation,
   deviations, omissions, Git state, scientific boundaries, and the next gate.

`plan.json` is the machine-readable implementation contract; the bilingual
documents are the primary human review paths. If the conversations occur in
different clients, the destination Codex task must be given the exact task ID,
plan path, approved revision or working-tree state, and Git behavior. A handoff
does not carry authorization beyond the state recorded in the plan.

## State model

| State | Permitted work | Repository effect | Exit condition |
|---|---|---|---|
| `DISCUSSING` | Iterative research and engineering discussion; compare alternatives; identify uncertainty | None unless a separate documentation edit is explicitly authorized | Assistant presents an action preview |
| `ACTION_AWAITING_APPROVAL` | Clarify or revise the proposed planning action | None | User explicitly authorizes plan generation |
| `PLAN_GENERATION_AUTHORIZED` | Freeze the agreed brief and generate planning artifacts | Only the files and Git behavior named in the action preview | Planning artifacts are validated and reported |
| `PLAN_AWAITING_REVIEW` | Answer questions and revise the plan | Plan/document edits only | User explicitly approves implementation |
| `IMPLEMENTATION_AUTHORIZED` | Implement the approved scope and run approved local checks | Approved code, tests, configuration, documentation, and declared Git action | Local acceptance work and review are complete |
| `IMPLEMENTATION_REVIEW` | Present changes, tests, deviations, limitations, and review paths | Review corrections only unless further work is authorized | User accepts, requests revisions, or discusses the next action |
| `SERVER_AWAITING_APPROVAL` | Prepare an exact run preview and commands without execution | Server plan/configuration only | User authorizes the named server run or command scope |
| `SERVER_AUTHORIZED` | Execute only the authorized server scope | Server-side outputs plus declared compact handoff | Run stops, completes, fails, or reaches a new approval gate |
| `RESULT_REVIEW` | Verify transferred evidence read-only and discuss interpretation | No repository writes; inspect only the ignored local handoff or approved mount | User accepts the interpretation, requests more evidence, or authorizes a report action |
| `RESULT_REPORT_AUTHORIZED` | Create the approved compact result report and promote only declared evidence | Declared files under `results/<run-id>/` and disclosed Git behavior | Report is validated and returned for review |

If the current state or a user instruction is ambiguous, remain in the earlier,
less-authorized state and ask one focused question.

## Discussion-first rule

Every prospective research or code task starts in `DISCUSSING`. The user and
assistant may volley back and forth for as long as needed. During this stage the
assistant may:

- restate the research question and competing explanations;
- propose or criticize methods, controls, baselines, tasks, and metrics;
- identify hidden assumptions, confounds, dependencies, and server unknowns;
- compare alternative task boundaries and acceptance criteria; and
- summarize tentative agreement and unresolved questions in the conversation.

Discussion alone does not authorize creation of `BRIEF.md`, `PLAN.md`,
`plan.json`, code changes, downloads, local execution that mutates project
artifacts, Git operations, or server execution.

## Required action preview

Before generating a plan, the assistant must post a visible action preview with
all of the following fields:

1. action ID and task ID;
2. current state and requested next state;
3. concrete action being proposed;
4. research goal and bounded outcome;
5. discussion consensus that will be frozen;
6. unresolved items and assumptions that will remain open;
7. exact files to create or modify;
8. primary Chinese, English, and structured review paths;
9. validation that will be performed;
10. Git behavior: no commit, local commit, or commit and push;
11. explicit exclusions, including code, downloads, local model execution, and
    server execution where applicable; and
12. the authorization phrase being requested.

Recommended form:

```text
[ACTION AWAITING AUTHORIZATION]

Action ID: <action-id>
Task ID: <task-id>
Action type: generate implementation plan only
Will do: <bounded description>
Consensus to freeze: <discussion summary>
Unresolved: <open items>

Outputs:
- runs/<task-id>/BRIEF.md
- runs/<task-id>/BRIEF.zh-CN.md
- runs/<task-id>/SERVER.md
- runs/<task-id>/SERVER.zh-CN.md
- runs/<task-id>/PLAN.md
- runs/<task-id>/PLAN.zh-CN.md
- runs/<task-id>/plan.json

Primary review:
- Chinese: runs/<task-id>/PLAN.zh-CN.md
- English: runs/<task-id>/PLAN.md
- Structured: runs/<task-id>/plan.json

Validation: <checks>
Git behavior: <none | commit | commit and push>
Will not do: <explicit exclusions>
Authorization requested: "Approve this action and generate the plan."
```

The user may revise any field. No action occurs until the user explicitly
accepts the resulting preview.

## Planning authorization and outputs

The recommended authorization phrase is:

```text
Approve this action and generate the plan.
```

An unambiguous equivalent is acceptable. This authorizes only the files,
validation, and Git behavior listed in the action preview.

The planning action normally produces:

- `BRIEF.md` and `BRIEF.zh-CN.md`: the frozen outcome of the discussion—what the
  user actually wants, acceptance criteria, boundaries, and resolved choices;
- `SERVER.md` and `SERVER.zh-CN.md`: known environment facts, unknowns, and the
  local/server validation split;
- `PLAN.md` and `PLAN.zh-CN.md`: the human-reviewable implementation proposal;
- `plan.json`: the single machine-readable implementation contract; and
- limited synchronized updates to `DECISIONS` or `PROGRESS` when declared.

Planning files must have status `awaiting_review` until implementation approval.
The completion message must link the exact review paths and explicitly state
that code, downloads, models, and servers were not touched.

## Implementation authorization

The recommended phrase is:

```text
The plan is approved. Begin implementation.
```

An unambiguous equivalent is acceptable. Implementation authorization covers
only the in-scope files and local checks in the reviewed plan. It does not
authorize:

- scope expansion;
- real-model downloads or execution unless explicitly included;
- remote or server commands;
- destructive data operations; or
- a Git action not disclosed in the plan/action preview.

For cross-client handoff, the recommended authorization names the executor,
task, scope, and Git behavior, for example:

```text
Authorize Codex to implement <task-id> according to the reviewed plan; keep the
changes uncommitted and do not push.
```

Implementation ends with `REVIEW.md` and `REVIEW.zh-CN.md`, including delivered
files, tests, deviations, limitations, actions not performed, commit/push state,
and the next gate.

## Server authorization

Server execution is always separate. Before requesting it, the assistant must
present:

- run ID and research task ID;
- exact code commit and clean/dirty state requirement;
- configuration and dataset hashes;
- exact model and tokenizer revisions;
- server destination and output root;
- exact command or bounded command sequence;
- estimated resources and stopping conditions;
- resume/retry behavior;
- outputs, large-artifact policy, and handoff package; and
- confirmation that activation capture is in or out of scope.

Recommended authorization phrase:

```text
Authorize server run <run-id> with the stated command scope.
```

Authorization for one run does not authorize later runs, retries that change the
configuration, additional models, activation capture, or follow-up experiments.

## Completion notice contract

At the end of every authorized action, the assistant must report:

1. the action that completed and its ID;
2. what was actually performed;
3. what was explicitly not performed;
4. every output and its review path;
5. validation results and known failures;
6. deviations from the approved action or plan;
7. Git commit and remote synchronization state;
8. scientific interpretation boundary; and
9. the exact next authorization required.

The completion notice is a navigation aid. The files remain the durable source
of truth.

## Git behavior

Git behavior is never implicit. Each action preview states whether it will:

- leave changes uncommitted for local review;
- create a local commit only; or
- create a commit and push it to the named remote branch.

Planning approval and implementation approval authorize only the disclosed Git
behavior. Large server artifacts never enter Git; see `SERVER_HANDOFF.md`.
