# Implementation plan: behavioral-calibration-v1

**Status:** implemented and locally verified
**Plan version:** 1
**Code changes authorized:** yes, local harness only
**Server execution authorized:** no

## 1. Objective and scientific contract

Implement a model-output-only evaluation harness for task-calibration records.
The primary v1 condition uses final-answer-only prompts and greedy decoding;
`task_side_trace` is never passed to a backend. Every attempted example remains
in the denominator, including parse and inference failures. Behavioral accuracy
is an eligibility diagnostic, not functional-organization evidence.

## 2. Records and metrics

Each record will preserve dataset and instance identity, model/tokenizer
revisions, prompt mode and exact final input, decoding settings, raw completion,
tokens, latency, structured errors, expected answer, parsed answer, nuisance
factors, and provenance references.

- `raw_exact`: raw completion equals expected answer.
- `trimmed_exact`: equality after outer-whitespace removal; primary metric.
- `format_valid`: the entire trimmed output matches its encoding.
- `parsed_exact`: encoding-aware equality only when fully format-valid.
- Failure, empty-output, and extra-text rates.

Parsers must never search an explanation for a correct substring. Summaries use
all attempted examples and include 95% Wilson intervals.

## 3. Interfaces

The backend protocol provides `prepare`, `format_input`, `generate`, and `close`.
Results preserve request IDs and return either a completion or structured
failure. The runner validates identity rather than assuming response order.

The fake backend supports deterministic correct, malformed, wrong, and failure
modes. The Hugging Face adapter requires exact revisions; supports explicit
local-only, dtype, device, batch, and prompt-mode controls; defaults to
`trust_remote_code: false`; freezes parameters; disables gradients; separates
prompt and completion tokens correctly; and rejects sampling in v1. Torch and
Transformers imports remain lazy.

## 4. Planned files

| Path | Action | Purpose |
|---|---|---|
| `pyproject.toml` | modify | isolated `model` dependencies and evaluation CLI |
| `src/reasoning_role/behavioral/schema.py` | create | requests, results, metrics, manifests |
| `src/reasoning_role/behavioral/parsing.py` | create | whole-output parsers |
| `src/reasoning_role/behavioral/backends/base.py` | create | backend protocol |
| `src/reasoning_role/behavioral/backends/fake.py` | create | deterministic local backend |
| `src/reasoning_role/behavioral/backends/huggingface.py` | create | frozen causal-LM adapter |
| `src/reasoning_role/behavioral/runner.py` | create | batching, resume, reconciliation, writing |
| `src/reasoning_role/behavioral/summary.py` | create | strata, intervals, eligibility |
| `src/reasoning_role/behavioral/provenance.py` | create | data/model/software/hardware metadata |
| `scripts/evaluate_behavior.py` | create | checkout-local CLI |
| `configs/eval/behavioral_smoke_fake.yaml` | create | local complete smoke run |
| `configs/eval/behavioral_server.template.yaml` | create | explicit unresolved server fields |
| `tests/behavioral/` | create | parser, backend, runner, summary, adapter tests |
| `tests/fixtures/behavioral_smoke/` | create | compact deterministic artifact |
| `docs/EVALUATION.md` | create | protocol and interpretation limits |
| `runs/behavioral-calibration-v1/REVIEW.md` | create after build | acceptance and handoff |

## 5. Configuration and provenance

Resolved YAML will specify evaluation versions; dataset files and hashes;
split/family filters; backend; exact model/tokenizer revisions; plain/chat prompt
mode; batch and decoding settings; seed; output/resume policy; summary strata;
and eligibility thresholds. Machine paths stay in ignored local configuration or
CLI arguments.

The manifest records code, config, dataset, model, tokenizer, prompt-template,
software, and available hardware provenance. The exact post-formatting input is
retained and hashed.

## 6. Safe resume

1. Resolve and hash configuration/data before model loading.
2. Reject existing run directories with incompatible provenance.
3. On resume, require exact data, model, tokenizer, prompt, and decoding hashes.
4. Reject duplicated, missing, reordered, or conflicting result IDs.
5. Use atomic batch checkpoints or a tested append journal.
6. Reconcile expected, completed, failed, and missing IDs before summaries.
7. Hash final per-example files and summaries in the manifest.

## 7. Local tests

- Adversarial whole-output parser cases, including explanations, embedded or
  multiple answers, Unicode lookalikes, whitespace, brackets, and signed vectors.
- An 80-record fake run spanning correct, invalid, wrong, and failed cases.
- Repeatability, interruption/resume, and provenance-mismatch tests.
- Missing/duplicate/reordered backend-result rejection.
- Independent summary recomputation and denominator checks.
- Stubbed Hugging Face freeze, no-gradient, chat-format, and token-boundary tests.
- Full Python 3.11 suite with neither network nor optional model downloads.

## 8. Deferred server validation

After exact revisions, environment, and permission are supplied: record the
environment; check one batch; manually inspect 8–16 examples; freeze config and
data hashes; run the pilot; replay a subset; and report stratified accuracy,
Wilson intervals, failures, runtime, and peak memory. No activations are saved.

## 9. Outcome branches

- Both families pass: plan semantic-support expansion and dataset freeze.
- One passes: retain it provisionally and redesign/replace the other.
- Neither passes: reconsider checkpoint, scale, prompt condition, or tasks.
- Scratchpad seems necessary: plan it separately as a manipulation/confound.
- Format errors dominate: report them; never inflate accuracy by substring
  extraction.

## 10. Risks

The plan counters mechanism overclaiming, chat-template confounds, parser
inflation, nondeterminism, silent missing examples, insufficient sample size, and
the current relational family's small short-chain semantic support.

## 11. Approval gate

All three `BRIEF.md` questions were approved on 2026-09-08. Local harness code
and fake tests are authorized. Downloads, real models, activations, and server
execution remain unauthorized.
