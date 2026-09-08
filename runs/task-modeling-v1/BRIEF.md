# Brief: task-modeling-v1

**Status:** awaiting review  
**Research goal:** G0, with enabling support for G2–G4

## Desired outcome

Create a small, deterministic, auditable task-calibration package for controlled
multi-step reasoning. It must represent task-side dependency structure without
claiming that the representation describes the Transformer's internal
computation.

The first version should contain two pilot families:

1. symbolic function composition; and
2. relational path composition.

They are chosen because chain length, presentation order, distractors, symbol
vocabulary, templates, and answer encoding can be varied independently. Any
cross-family operation mapping must be optional, explicit, and marked as a
candidate hypothesis.

## Required outputs

1. A versioned canonical record schema for task instances.
2. Deterministic generators and reference solvers for both pilot families.
3. Explicit instance dependency graphs and generator traces.
4. Factorized nuisance metadata and stable semantic instance identifiers.
5. IID, held-out-surface, held-out-template, and held-out-length splits.
6. A command-line data-generation entry point driven by configuration files.
7. Dataset manifests containing configuration, seed, generator version, counts,
   hashes, and split summaries.
8. Small committed fixtures and automated tests.
9. Documentation that distinguishes generator trace from model reasoning.

## Acceptance criteria

1. Repeating generation with the same configuration and seed produces
   byte-identical canonical records and the same manifest hashes.
2. Every target is verified by a reference solver or checker that does not trust
   a stored answer.
3. Semantic instance identities do not overlap between mutually exclusive
   splits, even when prompts differ.
4. Requested factor cells and split constraints either validate or fail loudly;
   generation must not silently create an imbalanced substitute.
5. Small fixtures cover both task families and all split types.
6. Tests cover determinism, answer validity, schema validation, graph integrity,
   split leakage, and CLI smoke behavior.
7. A local CPU smoke run completes under Python 3.11 without model weights or
   network access.
8. The output manifest records enough provenance to reproduce the artifact from
   a clean checkout.

## Out of scope

- Loading or querying a Transformer.
- Chain-of-thought collection.
- Activation, attention, gradient, or component tracing.
- Clustering, probes, functional fingerprints, ablations, or patching.
- A claim that either task family or any labeled operation is universal.
- Large-scale server generation or model experiments.
- Final selection of primary paper tasks.

## Review questions

Before approval, confirm:

1. Are these two pilot task families an acceptable calibration starting point?
2. Should visible intermediate-answer fields be excluded entirely from v1, or
   retained as task-side annotations that are never shown to the model by
   default?
3. Is Python 3.11 the desired local/server baseline?
