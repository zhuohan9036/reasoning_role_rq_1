# Task Brief: research-specification-v1

> 中文：[BRIEF.zh-CN.md](BRIEF.zh-CN.md)

**Status:** implemented locally; awaiting human review
**Research scope:** RQ1 task-side formalism and planning-to-Codex governance

## Desired outcome

Produce a reviewable documentation revision that makes the task-side objects in
RQ1 structurally explicit without treating them as the model's internal
algorithm. The revision must also define a clear handoff from a planning
conversation to a Codex implementation task, with documents as the durable
interface.

## Required content

1. Disambiguate workflow task, reasoning task family, task instance, reference
   task-side structure, candidate operation, and model-side pattern.
2. Define a minimal versioned task-family specification and canonical instance
   specification.
3. Define the semantics and evidential limits of a reference dependency graph.
4. Allow a single reference graph, a family of valid graphs, or shared partial
   order constraints when multiple solution procedures are valid.
5. Separate minimum pre-pilot task modeling from pilot-informed exploratory
   refinement.
6. Treat candidate operations and task-side cross-task correspondences as
   hypotheses, not empirical model results.
7. Require pilot-informed definitions to be frozen before evaluation on
   untouched instances, task conditions, or models.
8. Define the planning-conversation, Codex-plan, human-review,
   Codex-implementation, and review-report handoff.
9. Propagate the resulting rules into repository instructions, decisions, and
   progress records in synchronized English and Chinese.

## Acceptance criteria

1. The research specification states what each task-side object contains and
   how the objects relate.
2. Prompt rendering is explicitly separated from canonical task identity.
3. Reference task-side structure is not described as a uniquely necessary
   model algorithm.
4. Exploratory refinement is permitted but cannot be confirmed on the evidence
   that defined it.
5. Task-side correspondence hypotheses and model-side empirical correspondence
   are distinct terms.
6. Future Codex implementation cannot begin from an informal conversation
   alone; it requires an approved, versioned plan contract.
7. All human-facing Markdown changes remain bilingual and semantically aligned.
8. The implementation review can verify every changed path against this brief.

## Out of scope

- Selecting the final pilot task families.
- Choosing a model, tokenizer, activation measurement, clustering method, or
  statistical model.
- Re-labeling existing fixtures or changing data schemas in this task.
- Changing source code, tests, configurations, or generated artifacts.
- Model download, model execution, server execution, or activation capture.
- Claiming that candidate operations or cross-task correspondences have already
  been empirically established.

## Frozen discussion consensus

The current `docs/RESEARCH.md` is not accepted as a fully frozen specification.
Its core question, scope boundaries, competing explanations, and reporting
rules are accepted. Its goals and evidence stages remain a working roadmap. The
task-side conceptual hierarchy and Stage A require a structured formalism before
the full research specification can be accepted.

The operational handoff will be: planning conversation freezes requirements;
Codex generates a reviewable plan after explicit authorization; the user
reviews that plan; Codex implements only after a separate approval; and a
bilingual review records delivery, validation, deviations, and the next gate.
