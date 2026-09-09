# Implementation Plan: research-specification-v1

> 中文：[PLAN.zh-CN.md](PLAN.zh-CN.md)

**Status:** implemented and locally validated; awaiting human review
**Plan version:** 1
**Documentation changes authorized:** yes, local and uncommitted only
**Code changes authorized:** no
**Server execution authorized:** no

## 1. Objective

Revise the research and workflow documentation so that task-side computational
objects are structurally defined, their evidential status is explicit, and a
planning conversation can hand an approved, bounded contract to Codex without
implicitly authorizing implementation.

## 2. Proposed task-side formalism

The research specification will define the following versioned external
objects. Exact mathematical notation may be adjusted during implementation,
but the semantic distinctions are mandatory.

### Task family specification

A task family specification contains:

- an instance space and generation or sampling distribution;
- input, query, output, and correctness semantics;
- a reference-solution interface;
- a rendering family that maps canonical instances to prompts;
- controlled factors and nuisance variables;
- semantic identity and split rules;
- one declared form of reference dependency structure;
- a version identifier and provenance.

The task family is an external research object. It is not a claim that the model
represents the same variables or follows the reference solver.

### Canonical task instance

A canonical instance contains:

- a task-family and schema version;
- a canonical problem and query;
- a target defined by task correctness semantics;
- controlled and nuisance variables;
- a semantic identity independent of rendering where intended;
- a reference dependency structure and its provenance;
- zero or more provisional task-side annotations;
- one or more rendered prompts produced separately from canonical identity.

### Reference dependency structure

The documentation will distinguish three permitted representations:

1. a graph for one declared reference solver;
2. a set or family of valid solution graphs;
3. partial-order constraints shared by an explicitly scoped class of valid
   solutions.

The selected representation must state what its nodes, edges, intermediate
states, and execution semantics mean. It must not be called the model's graph or
a uniquely necessary algorithm without independent evidence.

### Candidate operations and correspondence

A candidate operation is a provisional task-side equivalence claim over nodes
or transitions. Its identity criteria, granularity, scope, and version must be
stated. It may be motivated by theory, task semantics, or exploratory evidence,
but it is not a model-side finding.

A task-side cross-task correspondence is a pre-specified hypothesis that two
task-side operations share a relevant computational property. Model-side
empirical correspondence is a separate result requiring independently measured
patterns, structural controls, held-out evaluation, uncertainty, and an
appropriate negative-control comparison.

## 3. Staged commitment policy

Before an exploratory pilot, a task must have a thin specification sufficient
to determine instances, answers, provenance, rendering, and major structural
covariates. Fine-grained operation labels and cross-task mappings may remain
unset.

Exploratory model evidence may motivate a revised task decomposition or role
vocabulary. Every such revision must record the evidence that motivated it,
receive a new version, and be frozen before confirmatory evaluation. Evidence
used to define or select a construct cannot also be reported as its independent
confirmation.

The later implementation will require held-out evaluation through one or more
of: untouched instances, held-out structural conditions, a new task pair, or an
additional frozen model. The exact partition remains a future experiment-level
decision.

## 4. Planning-to-Codex handoff

The workflow and repository instructions will define these responsibilities:

1. **Planning conversation:** discuss science and engineering, identify open
   choices, and freeze a bounded consensus without modifying the repository.
2. **Plan-generation gate:** show an action preview and obtain explicit approval
   before Codex creates or revises planning artifacts.
3. **Codex planning artifact:** produce bilingual `BRIEF`, `SERVER`, and `PLAN`
   documents plus one `plan.json`, all in `awaiting_review` state.
4. **Human review:** accept, reject, or revise the plan. Informal agreement with
   an idea does not authorize implementation.
5. **Codex implementation:** after separate explicit approval, change only the
   approved files, run only approved checks, and record deviations rather than
   expanding scope silently.
6. **Review handoff:** produce bilingual `REVIEW` documents that report actual
   changes, checks, omissions, Git state, scientific boundaries, and the exact
   next gate.
7. **Server separation:** require another named authorization for every bounded
   server run.

The contract is document- and state-based so it remains auditable even when the
planning and implementation conversations occur in different clients.

## 5. Planned file changes after implementation approval

| Path | Action | Purpose |
|---|---|---|
| `docs/RESEARCH.md` and `.zh-CN.md` | modify | Add structured task-side objects, staged commitment, and correspondence distinctions |
| `docs/WORKFLOW.md` and `.zh-CN.md` | modify | Define planning-conversation to Codex handoff and review responsibilities |
| `docs/DECISIONS.md` and `.zh-CN.md` | modify | Record accepted formalism, evidential status, and handoff decisions |
| `docs/PROGRESS.md` and `.zh-CN.md` | modify | Record specification-review status without claiming empirical progress |
| `AGENTS.md` and `AGENTS.zh-CN.md` | modify | Make the handoff and task-side terminology operational for future Codex work |
| `runs/research-specification-v1/REVIEW.md` and `.zh-CN.md` | create | Record delivery, validation, deviations, and next gate |

No source code, test, configuration, fixture, or generated artifact is included.

## 6. Implementation sequence

1. Add terminology that distinguishes workflow tasks from reasoning tasks.
2. Add the task-family, canonical-instance, and dependency-structure formalism.
3. Add the candidate-operation and two-level correspondence distinction.
4. Add the thin-specification, exploratory-refinement, freeze, and held-out
   confirmation policy.
5. Update the evidence stages without selecting final tasks or methods.
6. Add the planning-to-Codex handoff contract to workflow documentation and
   agent instructions.
7. Append accepted decisions rather than rewriting historical rationale.
8. Update progress as a documentation milestone, not empirical evidence.
9. Create synchronized implementation review documents.

## 7. Validation

- Parse `plan.json` and verify exact agreement with this plan.
- Confirm every human-facing Markdown file has a synchronized counterpart and
  reciprocal language link.
- Search for inconsistent uses of task, operation, correspondence, model-side,
  and causal terminology.
- Verify no statement turns a reference graph into a model mechanism.
- Verify pilot-informed constructs require separate held-out confirmation.
- Verify the changed paths match the approved allowlist.
- Inspect `git diff --check` and repository status.
- Do not run the test suite because no executable code is in scope.

## 8. Open implementation choices

- The notation may use a tuple, typed schema, or prose-plus-schema presentation,
  provided all required semantics are explicit.
- The research document may present the three dependency representations as a
  general interface rather than selecting one globally.
- A future experiment plan will select the exact exploratory/confirmatory split
  and reviewer-independence procedure.
- Future coding tasks must declare their own branch, commit, and push behavior;
  this task does not set a universal Git policy.

## 9. Out of scope

- Implementing or changing task generators.
- Rewriting existing fixture schemas.
- Selecting shared operations or final task pairs.
- Choosing model-side measurement or analysis methods.
- Running tests, models, experiments, downloads, or server commands.
- Creating a Git commit or pushing changes unless separately authorized.

## 10. Review gate

This plan does not authorize documentation implementation. After reviewing the
Chinese, English, or structured plan, the user may approve implementation with:

```text
Plan approved; begin implementation.
```

An equivalent explicit instruction is acceptable. Implementation approval will
cover only the paths, validation, exclusions, and Git behavior stated here.
