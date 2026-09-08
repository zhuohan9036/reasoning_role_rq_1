# Server environment: behavioral-calibration-v1

> 中文版：[SERVER.zh-CN.md](SERVER.zh-CN.md)

**Status:** unresolved; no server execution authorized

## Required before a real-model run

- Exact model and tokenizer IDs with immutable revisions.
- Base versus instruction-tuned checkpoint.
- Plain prompt versus a pinned tokenizer chat template.
- GPU model/count, VRAM, CUDA, driver, and supported PyTorch versions.
- Launcher or scheduler, wall time, CPU, RAM, and storage limits.
- Model-cache, dataset, scratch-output, and compact-result paths.
- Internet access versus pre-staged local-only weights.
- Approved dependency lock or existing server environment.

## Model selection constraints

The pilot model should provide frozen pinned weights, load through inspectable
local code, expose internal tensors for a later separate task, avoid
`trust_remote_code` unless reviewed, fit the approved GPU, and achieve adequate
performance without task-specific training. A later replication model should
differ meaningfully in model family or architecture.

## Local validation

- Python 3.11 with no network or model download.
- Fake backend for outputs, failures, resume, and summaries.
- Lightweight stubs for freeze/no-gradient adapter checks.
- Optional model dependencies isolated from the task-data package.

## Proposed server sequence

Execution remains blocked until explicitly authorized:

1. record environment and verify pinned local model files;
2. run tests and a one-batch model-load check;
3. inspect 8–16 balanced examples manually;
4. freeze the pilot configuration and its hash;
5. run the complete pilot with resume enabled;
6. replay a deterministic subset;
7. produce metrics, intervals, runtime, memory, and failure diagnostics; and
8. return only compact artifacts to Git.

No activation dump is permitted in this task.
