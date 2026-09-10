# Task brief: pilot-a0-target-grounding-v1

> 中文版：[BRIEF.zh-CN.md](BRIEF.zh-CN.md)

**Status:** revised planning artifacts generated; implementation awaiting review
**Brief version:** 2
**Research scope:** no-annotation source inventory and model-first route

## Desired outcome

Prepare a direct, auditable path from native mainstream reasoning tasks to
label-free model-side pattern discovery. The immediate implementation produces a
source inventory only; behavioral runs, activation capture, analysis, transfer,
and interpretation each require later plans.

## Frozen requirements

1. The initial population is English, text-only, objectively scored,
   self-contained multi-step reasoning.
2. Initial source strata are GSM8K, DROP, MuSiQue-Ans v1.0, and BIG-Bench
   `logical_deduction` plus `tracking_shuffled_objects`.
3. Native inference preserves benchmark semantics and does not impose operation
   labels, symbolic state slots, or a forced execution trace.
4. Discovery begins from model-side activation or transition patterns, not a
   researcher-defined operation vocabulary.
5. Within-task recurrence precedes frozen cross-task transfer.
6. MI is one diagnostic of information association, not an operation detector
   or causal test.
7. Native rationales, DAGs, and generator metadata are optional source artifacts,
   not unique algorithms or model-side ground truth.
8. New manual annotation and synthetic task construction are fallback tools only
   after a documented identification failure and separate approval.
9. `Symbol8`, its proposed function pairs, and C1-C4 remain inactive calibration
   ideas.
10. Relevant new research should be surfaced whenever encountered, with a
    periodic literature watch focused on preserving project differentiation.

## Immediate implementation acceptance criteria

- Exact official source locations, immutable revisions or checksums, licenses,
  native ID schemes, and eligible splits are recorded.
- The inventory lists correctness semantics, native metadata, source-provided
  structural artifacts, prompt affordances, perturbation affordances, and known
  leakage/grouping risks for each source.
- The inventory does not create task-operation labels or manually reconstruct
  solution graphs.
- A suitability matrix recommends the smallest initial native behavioral pilot
  and explains what each rejected or deferred source cannot currently support.
- Separate next-task boundaries are specified for behavior, activation capture,
  label-free discovery, cross-task transfer, and interpretation.

## Unresolved choices

- Exact immutable source revisions, licenses, eligible splits, and access mode.
- Initial source task or task pair for behavioral feasibility.
- Model, native prompt regime, decoding, and behavioral gate.
- Activation measurement unit and storage budget.
- Pattern-discovery, MI/predictive, trajectory, and transfer methods.
- Perturbation families and later intervention boundary.

## Out of scope for this planning action

- Benchmark download or source-instance inspection.
- New annotation or task decomposition.
- Source code, tests, configuration, or fixtures.
- Model selection, download, inference, activation capture, or analysis.
- Synthetic task implementation.
- Server execution, commit, or push.

