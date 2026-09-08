# Server environment: task-modeling-v1

> 中文版：[SERVER.zh-CN.md](SERVER.zh-CN.md)

**Status:** incomplete; no server execution authorized

## Known constraints

- Operating system: Ubuntu.
- Preferred Python baseline: 3.11, pending confirmation.
- Formal model training and large mechanistic runs will occur only on the
  server.
- This task's required acceptance run is CPU-only and should work locally.

## Unknown environment fields

- Host/access method.
- Scheduler or job launcher.
- GPU model and count.
- NVIDIA driver and CUDA versions.
- Available CPU, RAM, and local scratch storage.
- Shared dataset, model-cache, and result paths.
- Internet/registry access policy.
- Environment manager and approved dependency-install process.
- Job time limits and preemption behavior.
- Artifact transfer and backup policy.

## Validation split

### Required locally before task acceptance

- Install package in a clean Python 3.11 environment.
- Run formatting/static checks selected during implementation.
- Run the full unit and integration test suite.
- Generate the committed-scale smoke dataset twice and compare hashes.

### Deferred server validation

- Recreate the environment from committed metadata.
- Generate a larger calibration dataset into server scratch storage.
- Verify manifests and hashes after artifact transfer.
- Measure runtime, peak RAM, and storage footprint.
- Confirm that no absolute local paths appear in artifacts.

GPU/CUDA validation is intentionally deferred because this task does not use a
model. Server commands must be written after O-009 is resolved and must not be
run without explicit authorization.
