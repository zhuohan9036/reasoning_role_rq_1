# Implementation plan: task-modeling-v1

**Status:** awaiting_review  
**Plan version:** 1  
**Code changes authorized:** no

## 1. Objective

Implement the task-side calibration foundation described in `BRIEF.md`. The
result will generate small, deterministic datasets for two controlled reasoning
families and will make task structure, nuisance factors, and split provenance
auditable. It will not perform model inference or model-side analysis.

## 2. Proposed interfaces

### Canonical instance record

Use a versioned JSON-serializable record with these top-level concepts:

- `schema_version`, `instance_id`, `family`, and `generator_version`;
- a canonical problem specification independent of wording;
- `prompt` and `target` as rendered model-facing fields;
- a directed acyclic dependency graph with stable node IDs;
- a deterministic generator trace, explicitly labeled task-side provenance;
- provisional candidate-operation labels local to the task family;
- nuisance factors such as chain length, distractor count, presentation order,
  vocabulary/template IDs, and answer encoding;
- split name and semantic grouping keys.

Intermediate task states may exist in the canonical record for validation, but
the default renderer must not expose them in the prompt. This is a provisional
implementation choice pending the second review question in `BRIEF.md`.

### Task-family adapter

Each family will implement a small common protocol:

- generate a canonical problem from an explicit random-number generator;
- solve or verify from the canonical problem rather than from the stored target;
- render a prompt using a named template and vocabulary;
- emit the dependency graph and task-side trace;
- return semantic identity and grouping keys used for splitting.

### Dataset generation entry point

A single entry point will accept a YAML configuration and output:

- one canonical JSONL file per split;
- `manifest.json` with provenance, counts, factor distributions, and hashes; and
- a validation summary that fails the process when constraints are violated.

Stable serialization rules will be documented so determinism is testable across
runs on the supported Python version.

## 3. Planned files

| Path | Action | Purpose |
|---|---|---|
| `pyproject.toml` | create | Python 3.11 package, dependencies, and test/lint configuration |
| `src/reasoning_role/__init__.py` | create | package/version metadata |
| `src/reasoning_role/tasks/schema.py` | create | canonical records, graph nodes/edges, validation |
| `src/reasoning_role/tasks/base.py` | create | task-family protocol and shared types |
| `src/reasoning_role/tasks/registry.py` | create | explicit family lookup without dynamic imports |
| `src/reasoning_role/tasks/function_composition.py` | create | symbolic function-composition generator, solver, renderer |
| `src/reasoning_role/tasks/relational_path.py` | create | relational path generator, solver, renderer |
| `src/reasoning_role/data/split.py` | create | group-aware deterministic split assignment |
| `src/reasoning_role/data/generate.py` | create | balanced generation orchestration and validation |
| `src/reasoning_role/data/io.py` | create | canonical JSONL writing, hashing, and manifests |
| `scripts/generate_dataset.py` | create | thin command-line entry point |
| `configs/data/task_calibration_smoke.yaml` | create | tiny local/CI fixture configuration |
| `configs/data/task_calibration_v1.yaml` | create | proposed larger calibration configuration, not executed |
| `tests/tasks/test_schema.py` | create | schema and dependency-graph invariants |
| `tests/tasks/test_function_composition.py` | create | generation/solver/property tests |
| `tests/tasks/test_relational_path.py` | create | generation/solver/property tests |
| `tests/data/test_split.py` | create | split reproducibility and semantic leakage tests |
| `tests/data/test_generate.py` | create | balance, determinism, manifest, and failure tests |
| `tests/test_cli.py` | create | end-to-end smoke generation |
| `tests/fixtures/task_calibration_smoke/` | create | small reviewed outputs and expected manifest |
| `docs/DATA.md` | create | schema, factors, split semantics, and provenance |
| `runs/task-modeling-v1/REVIEW.md` | create after implementation | changes, tests, deviations, and acceptance evidence |

Exact file grouping may change during implementation only when behavior and
interfaces remain unchanged; any change will be recorded in `REVIEW.md`.

## 4. Configuration structure

The YAML configuration will contain:

- schema and generator versions;
- global seed and output serialization format;
- task-family list and family-specific domains;
- requested counts by chain length, distractor count, template, vocabulary, and
  answer encoding;
- named split definitions and group keys;
- holdout values for surface, template, and length generalization;
- maximum generation attempts and strict balance policy;
- output path supplied at runtime rather than a committed machine path.

Seeds will be derived from stable textual namespaces, not Python's process-random
hash function. The manifest will save the fully resolved configuration.

## 5. Split and leakage design

1. Construct canonical semantic identities before prompt rendering.
2. Assign groups deterministically, then render templates and surface forms.
3. Keep equivalent canonical problems in one mutually exclusive split.
4. For held-out-surface and held-out-template evaluations, distinguish the
   semantic core from the held-out factor so the intended axis changes without
   semantic leakage.
5. For held-out-length, reserve configured chain lengths and report unsupported
   factor combinations rather than backfilling them silently.
6. Emit overlap audits for semantic ID, canonical problem hash, rendered prompt
   hash, and any family-specific isomorphism key available in v1.

## 6. Correctness strategy

- Use explicit random-number-generator objects throughout.
- Verify every generated example from its canonical problem and reject invalid
  graphs before serialization.
- Keep target verification logically separate from reading the stored target.
- Test graph acyclicity, reachable target dependencies, trace/graph consistency,
  and task-family invariants.
- Use property-style parameterized tests across seeds and factor combinations.
- Generate the smoke fixture twice in separate temporary directories and require
  byte-identical JSONL plus equal manifest content hashes.
- Make infeasible balance/split requests raise descriptive errors.

The implementation review must disclose any logic shared between generation and
verification that weakens independence.

## 7. Execution sequence after approval

1. Create package/configuration scaffold and schema types.
2. Implement family protocol and canonical serialization.
3. Implement symbolic function composition plus independent checks.
4. Implement relational path composition plus independent checks.
5. Implement group-aware splits, audits, strict balancing, and manifests.
6. Add CLI, smoke configuration, and documentation.
7. Add and run unit, property-style, integration, and deterministic replay tests.
8. Generate only the small fixture.
9. Write `REVIEW.md` with file changes, commands, results, known limitations, and
   server steps. Do not start a server job.

## 8. Local acceptance checks

- Package installation/import on Python 3.11.
- Full automated test suite passes.
- CLI help and invalid-configuration paths behave correctly.
- Two smoke generations are byte-identical.
- Recomputed targets match every stored target.
- No cross-split overlap is reported by any required identity/hash audit.
- Manifest counts match actual records and requested factor cells.
- Repository contains no large outputs or machine-specific absolute paths.

## 9. Server validation (deferred)

After server details and authorization are provided:

1. Recreate the pinned environment.
2. run the full tests;
3. generate the larger v1 configuration into scratch storage twice;
4. compare hashes and validate all records;
5. record runtime, RAM, artifact size, environment, and Git revision; and
6. transfer only the manifest and compact summary into version control.

No GPU test is required for this task.

## 10. Risks and mitigations

- **Researcher-imposed ontology:** keep operation labels family-local and
  provisional; place cross-family mappings in optional hypothesis metadata.
- **Solver circularity:** verify from canonical problems and disclose shared
  logic; add brute-force or alternative checks for small fixtures where useful.
- **Split leakage:** group before rendering and audit multiple identity levels.
- **Accidental structural correlation:** generate and report crossed factor cells;
  fail on infeasible requested balance.
- **False cross-platform determinism:** define Python 3.11 as the v1 target and
  hash canonical serialized records, not filesystem metadata.
- **Premature task commitment:** label both families as calibration pilots and
  require a post-pilot decision before freezing primary tasks.

## 11. Approval gate

Implementation may begin only after the user approves this plan and resolves or
accepts the three review questions in `BRIEF.md`. Approval does not authorize
server execution or any model experiment.
