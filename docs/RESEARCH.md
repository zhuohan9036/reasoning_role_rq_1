# Research plan: stable functional differentiation in multi-step reasoning

**Status:** initial research specification, awaiting review  
**RQ:** RQ1  
**Last updated:** 2026-09-08

## 1. Central question

When a frozen pretrained Transformer performs multi-step reasoning, does its
internal computation exhibit stable functional differentiation: repeatedly
identifiable computation patterns that systematically track what computation is
being performed, rather than merely where or when it occurs?

The study must not assume that such differentiation exists. It should determine
whether the evidence is best explained by functional organization, generic
network structure, task-specific regularity, or no robust differentiation.

## 2. Scope and non-goals

### In scope

- Characterize repeatable model-side computation patterns during successful
  multi-step reasoning.
- Test whether any differentiation remains after accounting for layer depth,
  token position, reasoning step, prompt format, task difficulty, and fixed
  component identity.
- Measure stability across instances, controlled input variations, task
  families, and at least one additional frozen pretrained model or architecture.
- Compare independently specified task-side computational structure with
  independently measured model-side structure.

### Not established by RQ1 alone

- That a discovered pattern is a causal mechanism required for reasoning.
- That task-side operations are the model's actual or atomic primitives.
- That a cluster, probe direction, attention head, MLP, layer, or token position
  is itself a reasoning role.
- That task-specific training reveals naturally occurring organization in a
  pretrained model.

Causal interventions may be used as targeted diagnostics, but strong causal
claims belong to a later research question unless supported by a dedicated
intervention design.

## 3. Conceptual levels

The analysis keeps three task-side levels separate:

1. **Task family:** a distribution such as symbolic function composition or
   relational path composition.
2. **Instance-level dependency structure:** the computation graph or algorithmic
   dependencies sufficient to solve one generated instance.
3. **Candidate local operation:** a provisional description of one step in that
   task-side graph.

These task-side objects are external specifications. Model-side measurements
must be constructed without assigning these labels as internal truth. Only a
validated correspondence can motivate a stronger functional interpretation.

## 4. Competing empirical explanations

The project treats the following as genuine competitors rather than as stages in
a predetermined hierarchy.

### E0: structural or temporal organization only

Apparent patterns are explained by layer, token position, reasoning-step
progression, sequence length, or other generic processing structure. After
matching or controlling for these variables, little function-related signal
remains.

### E1: task-specific functional differentiation

Function-related patterns remain beyond structural confounds but do not
generalize meaningfully across task families.

### E2: reusable cross-task functional organization

Some model-side patterns track computations that recur across task families and
generalize to held-out surface forms, instances, and tasks better than matched
structural baselines.

### E3: stable function with mobile implementation

Functional patterns are reproducible, but the exact heads, MLPs, layers, or
other physical components carrying them vary across examples, model instances,
or architectures.

Mixtures and negative results are allowed. For example, only a subset of
operations or tasks may show differentiation.

## 5. Research goals and decision criteria

### G0 — Build explicit task-side computational models

Represent instance dependency graphs, deterministic solutions, candidate local
operations, and nuisance variables for controlled multi-step tasks.

Success means that task instances are reproducible and auditable, candidate
labels are explicitly provisional, and task structure can be manipulated
independently of surface form and key structural confounds.

### G1 — Establish whether repeatable model-side patterns exist

Measure internal computation at a unit that is not defined solely by fixed
component identity. Compare within- and between-condition reproducibility using
held-out instances.

Evidence for G1 requires out-of-sample stability beyond shuffled-label and
structure-only null models. Exploratory clustering alone is insufficient.

### G2 — Separate computational function from structural confounds

Use matched contrasts and statistical variance partitioning or an equivalent
design to compare function-related explanations against layer, position,
reasoning step, prompt form, and difficulty.

The strongest initial test is cross-classification: train or align on one set of
positions/steps/layers and evaluate function-related structure on held-out
positions/steps/layers, while also testing the reverse prediction.

### G3 — Quantify stability

Evaluate stability across examples, paraphrases or symbolic renamings, problem
lengths, random seeds, sampling conditions where applicable, and model
instances. Report confidence intervals and sensitivity to analysis choices.

### G4 — Distinguish task-specific from reusable computation

Test whether independently discovered model-side patterns transfer between task
families that share a hypothesized computation but differ in tokens, semantics,
and presentation. Include equally structured negative-control pairs that do not
share the hypothesized function.

### G5 — Replicate the central finding

Repeat the smallest decisive set of G1–G4 tests on an additional frozen
pretrained model or architecture. Prioritize the existence of differentiation,
the function-versus-step distinction, and the strongest generalization result.

## 6. Planned evidence structure

### Phase A — Task calibration

- Define a versioned canonical instance schema and deterministic reference
  solvers.
- Begin with two controlled task families whose dependency structures can be
  manipulated independently of wording: symbolic function composition and
  relational path composition.
- Factorize chain length, graph or rule position, distractor count, presentation
  order, symbol vocabulary, answer encoding, and prompt template.
- Store the exact generator trace as task-side provenance. Do not treat it as a
  model chain of thought.
- Create IID, held-out-surface, held-out-template, and held-out-length splits
  using semantic instance identities.

The two initial families are calibration instruments, not a final claim that
they define universal reasoning primitives. They may be replaced if pilot
behavior or identifiability is inadequate.

### Phase B — Behavioral and instrumentation baseline

- Select frozen, mechanistically accessible primary and replication models.
- Establish accuracy by task, length, template, and nuisance factor.
- Define which correct examples enter mechanistic analyses before inspecting
  functional results.
- Implement reproducible trace capture with explicit token alignment and model,
  tokenizer, prompt, and software versions.

### Phase C — Model-side pattern discovery

- Pre-register the unit of analysis and candidate measurements before primary
  confirmatory runs.
- Discover patterns on a training partition without task-operation labels where
  possible, or clearly separate supervised correspondence tests from discovery.
- Evaluate out-of-sample cluster/pattern stability and compare against shuffled,
  layer-only, position-only, and step-only baselines.

The representation, fingerprint, dimensionality reduction, and clustering
method remain open until the instrumentation pilot establishes what can be
measured reliably.

### Phase D — Functional correspondence and confound tests

- Test association with candidate task operations only after model-side
  structure has been defined.
- Use balanced matched cells and held-out-axis cross-classification.
- Compare incremental explanatory value of candidate function over structural
  covariates, with uncertainty and multiple-comparison control.
- Include prompt and label permutations plus non-reasoning controls where
  feasible.

### Phase E — Stability, transfer, and replication

- Measure stability across task instances and controlled surface changes.
- Evaluate within-task and cross-task generalization separately.
- Test whether functional similarity survives changes in physical component
  identity.
- Replicate only the central structural, confound-control, and transfer results
  on the second model.

## 7. Baselines and null models

At minimum, primary analyses should compare against:

- layer/depth-only prediction;
- token-position-only prediction;
- reasoning-step/chain-depth-only prediction;
- task-family and prompt-template prediction;
- difficulty and correctness controls;
- randomly permuted candidate-operation labels within appropriate matched
  strata;
- randomly initialized, resampled, or dimension-matched representations where
  appropriate to the selected metric;
- model-side patterns learned on one partition and scored on a strictly held-out
  partition.

Exact statistical models and metrics remain open decisions. Selection must be
driven by the scientific contrasts, not by whichever method yields the clearest
clusters.

## 8. Reporting policy

Each reported result must identify:

- whether it is exploratory or confirmatory;
- the task distribution and split;
- model and tokenizer revision;
- inclusion/exclusion rules and behavioral accuracy;
- measurement unit and alignment procedure;
- confounds controlled or matched;
- seeds, uncertainty, and sensitivity analyses;
- whether the result is within-task, cross-task, or cross-model;
- the weakest justified interpretation.

Use "computation pattern" or "candidate role" until the evidence supports a
stronger term. Null and task-specific findings are first-class outcomes.

## 9. Major open decisions before model experiments

1. Primary and replication model families, sizes, and exact revisions.
2. Whether models answer directly, produce visible intermediate tokens, or are
   evaluated under both regimes.
3. Model-side unit of analysis: residual-stream events, component outputs,
   activation changes, causal-response fingerprints, or another construct.
4. Token-to-task event alignment without using privileged model-side labels.
5. Discovery method and pre-specified stability metric.
6. Statistical design for incremental function signal and dependence between
   observations.
7. Minimum behavioral accuracy and sampling policy for mechanistic analysis.
8. Which task families provide credible shared-function and negative-control
   comparisons after pilot calibration.

These decisions must be resolved in `DECISIONS.md` before they constrain code or
primary experiments.
