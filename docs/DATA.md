# Task-calibration data contract

## Interpretation boundary

The dataset describes externally specified task computation. Its dependency
graphs and `task_side_trace` fields record how the generator constructs and
checks an answer. They are not observations of a Transformer's internal
algorithm, chain of thought, or reasoning roles.

Candidate operation names are family-local conveniences:

- `function_composition.apply_function`;
- `relational_path.compose_relation`.

Any proposed correspondence between these operations is a later hypothesis and
is intentionally absent from the required dataset schema.

## Canonical record

Each JSONL line is a schema-versioned record containing:

- stable instance, family, schema, and generator identifiers;
- a canonical problem independent of natural-language phrasing;
- model-facing `prompt` and `target` fields;
- the required task-side dependency graph;
- hidden intermediate task-side states under `task_side_trace`;
- provisional candidate-operation names;
- nuisance factors and split membership; and
- semantic, canonical-problem, and prompt hashes used for leakage audits.

Default renderers construct prompts only from the canonical problem, selected
template, selected vocabulary, and output instructions. They never read or
render `task_side_trace`.

## Pilot families

### Symbolic function composition

A problem specifies several finite-domain functions, a start symbol, and an
ordered subset of functions to apply. Distractor functions are present but not
part of the query. The reference solver reads the query and function mappings;
it does not trust a stored target.

### Relational path composition

A problem specifies directed spatial relations between entities and asks for
the net two-dimensional displacement between a source and target. Distractor
relations form disconnected components. The reference solver searches the
relation graph and accumulates edge vectors; it ignores stored relevance flags
and the stored target.

Both families are calibration instruments. Their presence does not establish
that the candidate operations are minimal, universal, shared across tasks, or
used internally by a model.

## Controlled factors

The v1 generator crosses:

- chain length;
- distractor count;
- canonical or shuffled presentation order;
- prompt template;
- surface vocabulary; and
- answer encoding.

Family-specific factors such as function-domain size are also recorded. A
requested split count must be divisible by its complete factor-cell count. The
generator fails rather than silently changing an infeasible balance request.

## Split semantics

- `train`: reference factor domains.
- `iid_test`: the same factor and rendering domains, with new semantic problems.
- `surface_test`: vocabulary IDs disjoint from training while other controlled
  domains match.
- `template_test`: template IDs disjoint from training while other controlled
  domains match.
- `length_test`: chain lengths disjoint from training while other controlled
  domains match.

Equivalent semantic problems are never allowed in two splits. Audits also check
canonical-problem and rendered-prompt hashes. Semantic identity is computed
before rendering and excludes presentation order, vocabulary, template, and
answer encoding.

## Generation

From an installed development environment:

```bash
reasoning-role-generate \
  --config configs/data/task_calibration_smoke.yaml \
  --output /new/output/directory
```

From a checkout without installation:

```bash
python scripts/generate_dataset.py \
  --config configs/data/task_calibration_smoke.yaml \
  --output /new/output/directory
```

The output directory must not already exist. This prevents accidental artifact
overwrites.

## Artifact contents

Generation creates one JSONL file per split, `validation_summary.json`, and
`manifest.json`. The manifest records:

- the fully resolved configuration and its SHA-256 hash;
- global seed, schema, generator, and package versions;
- Git revision and dirty-worktree state when available;
- Python and PyYAML versions;
- record counts and factor distributions by family; and
- content hashes for every split and validation file.

Large generated datasets remain outside Git. Only the smoke fixture and compact
manifests or summaries should be committed.

## Determinism boundary

Seeds are derived with SHA-256 from explicit textual namespaces. The generator
does not use Python's randomized process hash. Records use sorted, compact JSON
with UTF-8 and Unix newlines.

Byte-identical replay is required for the same configuration, seed, code
revision, dependency versions, and supported Python baseline. A changed code or
environment revision should remain visible in the manifest even if record
content is unchanged.
