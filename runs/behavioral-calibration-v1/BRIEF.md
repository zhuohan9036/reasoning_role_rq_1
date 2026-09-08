# Brief: behavioral-calibration-v1

**Status:** awaiting review
**Research phase:** Phase B behavioral calibration
**Research goals:** G0 calibration; prerequisite for G1–G4

## Desired outcome

Build a reproducible behavioral-evaluation harness that determines whether a
candidate frozen causal language model solves the two pilot task families
reliably enough to justify later mechanistic analysis.

This task evaluates model outputs only. It must not collect activations, assign
model-side computation labels, cluster components, or claim evidence for
functional differentiation.

## Proposed primary condition

- Use the record's final-answer-only prompt.
- Run the frozen model in evaluation mode with greedy decoding.
- Do not expose `task_side_trace` or intermediate task states.
- Do not request visible chain of thought.
- Preserve the exact rendered model input and raw completion for audit.

A visible-scratchpad condition, if later desired, will be a separately planned
experimental condition rather than an undocumented fallback.

## Required outputs

1. Versioned records linking each completion to data, instance, model,
   tokenizer, prompt-format, and generation revisions.
2. A backend-neutral inference interface, deterministic fake backend, and frozen
   Hugging Face causal-LM backend.
3. Strict whole-output parsers for every family and answer encoding.
4. Per-example JSONL with exact input, raw completion, parsing, correctness,
   timing, token counts, and failures.
5. Summary JSON/CSV stratified by family, split, length, distractors,
   presentation order, template, vocabulary, and answer encoding.
6. Run manifests, safe resume, failure accounting, and content hashes.
7. An eligibility report that separates engineering success from empirical
   task/model adequacy.
8. Local tests and `REVIEW.md`; no server run until separately authorized.

## Proposed pilot decision rule

A family is provisionally suitable for the next data-design iteration when:

- trimmed exact-match accuracy is at least 80% overall;
- every evaluated chain-length cell reaches at least 60%; and
- invalid-format or inference-failure rate is at most 5%.

These are engineering calibration thresholds, not inferential evidence. The
current dataset cannot establish a paper claim or a powered inclusion threshold.

## Local acceptance criteria

1. The full path runs on committed fixtures without network or weights using the
   fake backend.
2. Stable scientific outputs replay identically under fixed provenance.
3. Parsers reject malformed, contaminated, and adversarial outputs and never
   extract a correct answer from an invalid explanation.
4. Resume skips completed IDs, rejects incompatible manifests, and never
   duplicates or silently overwrites records.
5. Summaries reconcile exactly with per-example outputs and keep all failures in
   their denominators.
6. Manifests record data hashes, code/config revisions, exact model/tokenizer
   revisions, prompt formatting, decoding, dependencies, and hardware metadata.
7. Stub tests verify frozen parameters and disabled gradients without downloading
   a model.

## Server acceptance criteria

After model, environment, data size, and execution are approved:

1. A tiny real-model run completes and is manually inspected.
2. The pilot completes without missing or duplicated instances.
3. A fixed greedy-decoding subset reproduces or exposes backend nondeterminism.
4. The report includes all required strata and Wilson confidence intervals.
5. Only compact summaries and manifests return to Git.

## Out of scope

- Final model selection without hardware information.
- Local model downloads or any real-model/server run.
- Visible chain of thought or scratchpad evaluation.
- Activations, hooks, attribution, probing, clustering, patching, or ablation.
- Expanding generator semantic support.
- Treating behavioral success as evidence for reasoning roles.

## Review questions

1. Approve final-answer-only, no-visible-scratchpad evaluation?
2. Approve a generic Hugging Face adapter before exact model/server selection?
3. Accept the 80% overall / 60% per-length / 5% failure rule as a provisional
   engineering gate?

Exact model and server details are required before a real-model run, but not
before local harness implementation.
