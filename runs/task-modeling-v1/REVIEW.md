# Review: task-modeling-v1

**Status:** passed local acceptance checks
**Reviewed:** 2026-09-08
**Implementation commit:** `d574c3e`

## Outcome

The approved task-side calibration foundation is implemented. It produces
deterministic, balanced, auditable records for symbolic function composition and
relational path composition. It does not load a model or make a model-side
claim.

## Delivered

- Versioned canonical record, dependency-graph, and hidden task-side trace
  schemas.
- Two deterministic task families with family-local candidate operations.
- Reference solvers that recompute answers from canonical problems.
- Compact and prose templates, separate surface vocabularies, and two answer
  encodings per family.
- Strict factor-cell expansion and configuration validation.
- IID, surface, template, and length holdout semantics.
- Global semantic-identity exclusion plus canonical-problem and prompt-hash
  overlap audits.
- Stable JSONL serialization, provenance manifests, joint factor-cell counts,
  file hashes, and non-overwriting output behavior.
- Checkout-local and installed command-line entry points.
- Smoke and deferred larger configurations, data documentation, 23 automated
  tests, and an 80-record committed fixture.

## Acceptance evidence

| Check | Result |
|---|---|
| Python baseline | Passed on Python 3.11.16 |
| Editable package install | Passed without network/build isolation |
| Automated tests | 23/23 passed |
| Compilation check | Passed for `src/`, `scripts/`, and `tests/` |
| Smoke records | 80 total; 16 per split; 8 per family per split |
| Deterministic replay | Byte-identical JSONL and full outputs under fixed provenance |
| Target verification | 80/80 recomputed from canonical problems |
| Graph validation | 80/80 DAG and trace-consistency checks passed |
| Factor balance | Every requested smoke joint factor cell has count 1 |
| Split leakage | Zero semantic, canonical-problem, and prompt-hash overlaps |
| Manifest integrity | All recorded artifact SHA-256 hashes verified |
| Hidden annotations | Default renderers never read or expose task-side traces |
| Server/model execution | Not run, as required |

Primary local command:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

The committed smoke artifact is under
`tests/fixtures/task_calibration_smoke/`; its manifest records the exact clean
implementation revision used to generate it.

## Plan deviations and implementation choices

- The property-style coverage uses deterministic parameter sweeps in the
  standard-library `unittest` suite rather than adding Hypothesis. Pytest remains
  an optional development dependency, and the tests are compatible with both
  runners.
- The larger `task_calibration_v1.yaml` configuration was validated but not run,
  consistent with the server-execution gate.
- A repository-local Conda environment was created only for local Python 3.11
  verification and is ignored by Git.

## Independence and limitations

- Function-composition verification recomputes the result from canonical
  mappings and the query, but necessarily consumes the same mapping
  representation emitted by the generator.
- Relational verification performs graph search and ignores stored relevance
  flags and targets, providing a more independent check.
- Semantic IDs remove template, vocabulary, answer encoding, and presentation
  order. The function family does not yet canonicalize all problems under every
  possible renaming of abstract domain symbols. A future leakage audit should
  decide whether that stronger isomorphism equivalence is scientifically
  required.
- Short relational chains have a small semantic support. The deferred larger
  configuration therefore uses one record per crossed factor cell and must be
  audited before any scale increase.
- These tests establish engineering correctness of the generator, not the
  adequacy of the tasks for eliciting multi-step reasoning from a chosen model.

## Deferred server validation

No server action was performed. After `SERVER.md` is completed and execution is
explicitly authorized:

1. recreate the committed environment;
2. rerun the complete test suite;
3. generate `task_calibration_v1.yaml` twice into scratch storage;
4. compare hashes and revalidate every record; and
5. record runtime, peak RAM, storage size, environment, and Git revision.

## Research handoff

The next discussion should calibrate whether both task families elicit reliable
multi-step behavior in candidate frozen models and resolve O-001, O-002, O-004,
and O-008 before planning any activation-capture implementation.
