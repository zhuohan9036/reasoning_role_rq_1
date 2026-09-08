# Behavioral calibration protocol

> 中文版：[EVALUATION.zh-CN.md](EVALUATION.zh-CN.md)

## Interpretation boundary

Behavioral calibration asks whether a frozen model answers the pilot tasks
reliably enough to justify a later mechanistic study. Accuracy, formatting, or
failure rates do not establish internal computation patterns, functional
differentiation, or reasoning roles.

This stage does not collect activations. The task-side dependency graph and
`task_side_trace` are never sent to the inference backend.

## Primary v1 condition

- Existing final-answer-only task prompt.
- No visible scratchpad or chain-of-thought request.
- Frozen model in evaluation mode with gradients disabled.
- Greedy decoding only.
- Exact final post-template input and raw completion retained.
- All attempted examples, including failures, retained in metric denominators.

Any visible-scratchpad condition requires a separate plan because it changes the
observable token sequence and may change the model's internal computation.

## Metrics

`trimmed_exact` is primary and removes outer whitespace only. `raw_exact`
preserves byte-for-text behavior. `format_valid` requires the entire trimmed
completion to match the expected encoding. `parsed_exact` compares values only
after that whole-output check succeeds.

The parser never searches an explanation for an embedded answer. For example,
`The answer is (1,0).` is invalid even when `(1,0)` is correct. This prevents
post-processing from hiding prompt-following or output-control failures.

Every summary includes counts, rates, and a 95% Wilson interval for trimmed exact
match. Summaries are stratified by task and nuisance factors, including family,
split, length, distractors, presentation order, template, vocabulary, and answer
encoding.

## Provisional eligibility gate

For pilot engineering decisions only, a family passes when:

- overall trimmed exact match is at least 80%;
- each observed chain-length cell is at least 60%; and
- invalid-format or inference-failure rate is at most 5%.

This threshold is not powered for a paper claim. It only determines the next
branch: expand/freeze data, redesign one family, reconsider the model/prompt, or
plan a scratchpad manipulation.

## Fake backend

The fake backend validates the harness without representing model behavior. Its
correct, valid-but-wrong, invalid-extra-text, and structured failure outcomes are
assigned deterministically from source instance IDs.
Fake results may be committed as engineering fixtures but must never appear in
an empirical results table.

## Hugging Face backend

The real backend requires explicit model and tokenizer revisions. It defaults to
local files and `trust_remote_code: false`, records plain versus chat-template
formatting, sets evaluation mode, freezes parameters, and runs generation inside
an inference-only context.

Model dependencies are optional:

```bash
python -m pip install -e '.[model]'
```

Do not install or download these dependencies for this task unless separately
authorized and matched to the target server environment.

## Local fake run

From the repository root:

```bash
python scripts/evaluate_behavior.py \
  --config configs/eval/behavioral_smoke_fake.yaml \
  --output /new/output/directory
```

The output directory must be new. To resume an interrupted compatible run, add
`--resume`. Resume rejects changes to source code, configuration, data selection,
or backend identity.

Outputs are `records.jsonl`, `summary.json`, `summary.csv`, `run_state.json`, and
`run_manifest.json`. Manifests contain hashes and provenance but not model
weights. Machine-specific paths are intentionally excluded from committed
scientific artifacts.

## Server gate

Before any real-model run, complete
`runs/behavioral-calibration-v1/SERVER.md`, select exact model/tokenizer revisions,
review chat formatting, pin the model software environment, and receive explicit
download and execution authorization. No activation capture is permitted in this
task.
