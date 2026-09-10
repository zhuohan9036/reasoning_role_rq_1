# Implementation plan: pilot-a0-target-grounding-v1

> 中文版：[PLAN.zh-CN.md](PLAN.zh-CN.md)

**Status:** awaiting review
**Plan version:** 2
**Planning artifacts authorized:** yes
**Implementation authorized:** no
**Git behavior:** leave all planning changes uncommitted

## 1. Objective

Produce a no-new-annotation inventory of the accepted native task sources and a
decision-ready recommendation for the first behavioral pilot. Do not inspect
model activations, define task operations, or implement a synthetic task.

## 2. Blocking review choices

Before implementation, freeze:

1. the official repository or distribution channel for each accepted source;
2. the exact immutable revision or file checksum and verified license;
3. eligible source splits and the split reserved for later return tests;
4. source access mode and whether a bounded download is authorized;
5. whether the inventory may inspect dataset schemas and aggregate metadata only,
   or a small declared set of instances as well.

No annotation staffing, reconstruction sample size, or reliability threshold is
required because new manual annotation is outside this plan.

## 3. Step 1: freeze the source registry

Create a machine-readable registry for GSM8K, DROP, MuSiQue-Ans v1.0, and the two
accepted BIG-Bench tasks. Record source URL, revision or checksum, license,
native ID scheme, official splits, redistribution constraints, and citation.

## 4. Step 2: inventory native task information

For each source, record only information already provided by its files,
documentation, evaluator, or generator:

- input, answer, and correctness interfaces;
- rationale, calculation annotation, constituent-question DAG, supporting fact,
  template, size, difficulty, or generator fields;
- natural grouping units such as passage, constituent question, scenario, or
  template that must not cross study partitions;
- benchmark-faithful prompt options and output parsing requirements;
- whether source-preserving and answer-changing perturbations can be generated
  without assigning operation labels;
- known shortcut, contamination, and provenance limitations.

Do not infer missing solution graphs or assign candidate operation labels.

## 5. Step 3: build the suitability matrix

Evaluate each source against model-independent criteria:

- objective behavioral scoring;
- native multi-step evidence or task construction rationale;
- clean source-instance and grouping identity;
- compatibility with free-form native inference;
- capacity for held-out instances and source-preserving perturbations;
- expected alignment and activation-storage cost;
- usefulness for within-task recurrence and later cross-task transfer;
- domain, lexical, answer-format, and task-origin confounds.

The matrix recommends an initial task or task pair but does not select a model or
run behavior.

## 6. Step 4: reserve source roles

Assign, without sampling instances yet:

- source material eligible for prompt/adapter development;
- source material eligible for behavioral discovery;
- a separate source partition reserved for within-task confirmation;
- a separate family or partition reserved for cross-task transfer.

“Held out” means not used to define this study's pattern or interpretation. It
does not imply that a pretrained model has never encountered the public data.

## 7. Step 5: specify follow-on task boundaries

Prepare concise action boundaries—not executable plans—for:

1. native behavioral feasibility;
2. activation-trajectory capture;
3. label-free within-task discovery and untouched confirmation;
4. frozen cross-task transfer;
5. functional interpretation through native metadata and perturbations;
6. fallback annotation, synthetic calibration, or intervention only if a named
   identification failure later justifies one.

Each follow-on task retains separate authorization for code, downloads, model
execution, activation capture, server use, and Git publication.

## 8. Proposed implementation files

| Path | Action | Purpose |
|---|---|---|
| `docs/PILOT_A0_SOURCE_INVENTORY.md` and `.zh-CN.md` | create | Human-readable source and suitability audit |
| `configs/data/pilot_a0_sources.yaml` | create | Machine-readable source registry and reserved split roles |
| `results/pilot-a0-target-grounding-v1/source_inventory.json` | create | Compact derived source metadata; no benchmark text |
| `docs/DECISIONS.md` and `.zh-CN.md` | modify | Record reviewed source revisions and first-pilot recommendation |
| `docs/PROGRESS.md` and `.zh-CN.md` | modify | Record inventory completion without model evidence |
| `runs/pilot-a0-target-grounding-v1/REVIEW.md` and `.zh-CN.md` | create | Implementation, validation, omissions, and next gates |

No `src/`, `scripts/`, test, dataset, prompt, or model file is planned.

## 9. Validation

- Parse YAML and JSON outputs.
- Verify every source has an immutable provenance field, license status, native
  identity, grouping rule, and reserved split role.
- Verify source claims are traceable to official documentation or schemas.
- Verify no benchmark text, task-operation label, manual decomposition, model
  output, or activation appears in the outputs.
- Verify bilingual links and semantic synchronization.
- Verify changed paths match the approved allowlist and run `git diff --check`.

## 10. Out of scope

- New manual annotation, adjudication, or reliability studies.
- Benchmark-derived or from-scratch task decomposition.
- Synthetic task language implementation.
- Source code, tests, or executable data adapters.
- Model/tokenizer selection, download, inference, or activation capture.
- MI estimation, probing, clustering, trajectory segmentation, or transfer.
- Server execution, commit, or push.

## 11. Review gate

Human review should first resolve the five source-access choices in Section 2.
Only then can implementation be authorized. Approval of this source-inventory
task will not authorize any model or activation work.

