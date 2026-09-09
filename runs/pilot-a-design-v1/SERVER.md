# Server environment: pilot-a-design-v1

> 中文版：[SERVER.zh-CN.md](SERVER.zh-CN.md)

**Status:** unresolved; no download, model, activation, or server execution authorized

## Not required for local task implementation

The canonical task language, generator, solver, balance audits, splits, paired
renderings, shortcut checks, and local fixture require no GPU, model weights, or
network access.

## Required before behavior execution

- Full immutable commit SHAs for the selected Mistral model and tokenizer.
- Confirmation of instruction-tuned versus base checkpoint.
- GPU model/count, VRAM, CUDA, driver, PyTorch, and Transformers versions.
- Scheduler or launcher, wall-time, RAM, and storage limits.
- Model cache and generated-data paths.
- Internet access or verified pre-staged local weights.
- Verified single-token `Symbol8` rendering bank.
- Frozen behavior configuration and dataset manifest hashes.

## Model policy

- Qwen is excluded from Pilot A.
- Working default: `mistralai/Mistral-7B-Instruct-v0.3` at an immutable revision.
- Preferred alternative: a comparable Llama instruct checkpoint if access,
  license terms, and hardware permit.
- Parameters remain frozen and gradients disabled.
- Model selection is revisited before the paper's primary evidence; the pilot
  checkpoint is not automatically promoted.

## Separate future server runs

1. Behavior-only feasibility run; no activations.
2. R1 residual-stream capture, only after behavior review and separate approval.
3. Untouched confirmation capture, only after discovery definitions are frozen.
4. Optional R2 or semantic-domain replication, each under a new run run contract.

Every run requires its own exact command, resource estimate, stopping condition,
output policy, and authorization. Large outputs remain outside Git.

