# Review: behavioral-calibration-v1

> 中文版：[REVIEW.zh-CN.md](REVIEW.zh-CN.md)

**Status:** passed local acceptance checks
**Reviewed:** 2026-09-08
**Implementation commits:** `4797581`, `17fda49`
**Committed fixture source:** clean revision `17fda49`

## Outcome

The approved model-output-only behavioral calibration harness is implemented.
It evaluates final answers with strict whole-output scoring, preserves failed
attempts in every denominator, and records reproducibility metadata. It neither
loads a real model in this review nor collects activations or provides evidence
about functional differentiation.

## Delivered

- Versioned request, backend-result, and per-example evaluation records.
- A backend-neutral interface with a deterministic fake backend.
- A generic Hugging Face causal-LM adapter with lazy optional imports, exact
  model/tokenizer revisions, explicit prompt mode, evaluation mode, frozen
  parameters, greedy generation, and inference-only execution.
- Strict whole-output parsers for symbol and vector answer encodings.
- Atomic batch checkpoints, compatible-run resume, provenance comparison, and
  duplicate/missing/reordered result rejection.
- JSON and CSV summaries over all attempts, requested nuisance strata, family by
  chain length, 95% Wilson intervals, and explicit provisional gate decisions.
- Source-data, configuration, code, backend, environment, input, and output
  hashes or identities.
- Offline configuration, unresolved server template, protocol documentation,
  automated tests, and a committed 80-record fake-run fixture.

## Acceptance evidence

| Check | Result |
|---|---|
| Python baseline | Passed on Python 3.11.16 |
| Editable package and CLI | Passed without downloading optional model packages |
| Automated tests | 51/51 passed |
| Compilation and diff checks | Passed |
| Offline fake evaluation | 80 attempted; 80 completed; zero missing or duplicate IDs |
| Stable replay | Records, run state, summary JSON, and summary CSV reproduce byte-for-byte under fixed provenance |
| Strict scoring | Explanations, embedded answers, extra text, malformed vectors, and Unicode lookalikes are rejected |
| Failure accounting | 6 structured failures retained among all 80 attempted examples |
| Summary reconciliation | 60 trimmed-exact, 66 format-valid, 14 invalid-or-failed; all denominators equal 80 |
| Resume safety | Interruption recovers; config changes and duplicate checkpoints fail visibly |
| Frozen-model contract | Stub tests verify exact revisions, chat-template identity, evaluation mode, frozen parameters, greedy decoding, and disabled gradients |
| Manifest integrity | All four recorded output hashes verified |
| Real model/server/activations | Not run, as required |

Primary local command:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

The committed engineering artifact is under
`tests/fixtures/behavioral_smoke/`. Its manifest binds the run to the task-data
hashes, configuration, backend identity, source-tree hash, and clean code
revision.

## Interpretation of the fake result

The fake backend deliberately emits a mixture of correct, wrong, invalid, and
failed outputs. Its overall 75% trimmed exact-match and 17.5%
invalid-or-inference-failure rate therefore do not pass the provisional gate.
This is expected test input, not a result about any Transformer and not evidence
for or against the paper's hypotheses. The fixture exists only to prove that
metrics and negative outcome branches are implemented correctly.

## Plan deviations and implementation choices

- No real `torch`, `transformers`, or `accelerate` packages were installed. The
  Hugging Face path was checked with controlled stubs so this task stayed within
  the no-download/no-real-model approval boundary.
- Model dependencies use compatible lower bounds rather than a locked server
  environment because the server and target checkpoint are still unresolved.
- The server configuration remains a visibly non-runnable template with
  replacement markers.
- The committed fake fixture was generated only after the implementation had a
  clean Git revision, so its recorded code identity is meaningful.

## Limitations and deferred validation

- The Hugging Face adapter has not yet been exercised against an installed
  Transformers version, a real tokenizer/chat template, a real checkpoint, or
  GPU placement. Those compatibility checks belong to the authorized server
  pilot.
- Exact model, tokenizer, and immutable revisions; base versus instruction
  checkpoint; prompt template; CUDA/GPU environment; and dependency lock remain
  open.
- The current 80-record task fixture is an engineering sample, not a powered
  behavioral dataset. Its short-chain semantic support limitations still apply.
- Passing a later behavioral gate would justify further task/data design only;
  it would not establish model-internal computation patterns or reasoning roles.

## Server handoff gate

Before a real-model run, resolve the open model and environment decisions,
complete `SERVER.md`, pin the software environment, inspect the exact prompt
template, and explicitly authorize downloads and execution. The first server
step should be a tiny manual-inspection batch, followed by the complete
behavioral pilot and a deterministic-subset replay. Activation capture remains
outside this task.

## Handoff

This implementation task is complete locally. No next implementation task is
authorized by this review. Update the working norms before further planning.
