# Research plan: stable functional differentiation in multi-step reasoning

> 中文版：[RESEARCH.zh-CN.md](RESEARCH.zh-CN.md)

**Status:** reviewed research specification; task-side formalism v1 accepted;
experiment-level choices remain open
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

## 3. Structured task-side objects

The repository term **workflow task**, such as `task-modeling-v1`, names a
bounded planning or implementation action. It is not a reasoning task. The
scientific analysis distinguishes the following versioned external objects.

### Task family specification

A task family specifies:

- an instance space and generation or sampling distribution;
- input, query, output, and correctness semantics;
- a reference-solution interface;
- a rendering family that maps canonical instances to prompts;
- controlled factors and nuisance variables;
- semantic identity and split rules;
- a declared form of reference dependency structure;
- a version identifier and provenance.

Examples include symbolic function composition and relational path composition.
A task family is an external research object, not a claim that the model
represents the same variables or follows the reference solver.

For tasks sampled from an existing benchmark, the project must additionally
record the target-population definition, benchmark release and native instance
identity, task origin, sampling stratum, and an explicit distinction between
historical task construction and this project's later analytical
reconstruction. A task dimension is not justified solely because it supports a
clean synthetic generator.

### Canonical task instance

A canonical instance contains a family and schema version, canonical problem and
query, target under the task's correctness semantics, controlled and nuisance
variables, semantic identity, reference dependency structure and provenance,
and zero or more provisional task-side annotations. One or more prompts may be
rendered from the instance, but rendering is not part of canonical task identity
unless the task specification explicitly says otherwise.

### Reference dependency structure

Because a task may admit more than one valid algorithm, a task family may use:

1. a graph for one declared reference solver;
2. a set or family of valid solution graphs; or
3. partial-order constraints shared by an explicitly scoped class of valid
   solutions.

The specification must state what nodes, edges, intermediate states, and
execution semantics mean. A reference graph records generator or solver
provenance; it is not the model's computation graph or a uniquely necessary
algorithm without independent evidence.

### Candidate operations and correspondence

A candidate operation is a provisional task-side equivalence claim over nodes
or transitions. Its identity criteria, granularity, scope, motivation, and
version must be stated. It may be motivated by theory, task semantics, or
exploratory evidence, but it is not a model-side finding.

A task-side cross-task correspondence is a hypothesis that two task-side
operations share a relevant computational property. A model-side empirical
correspondence is a separate result requiring independently measured patterns,
structural controls, held-out evaluation, uncertainty, and an appropriate
negative-control comparison.

### Staged commitment

Before an exploratory pilot, a task must have a thin specification sufficient
to determine instances, answers, provenance, rendering, and major structural
covariates. Fine-grained operation labels and cross-task mappings may remain
unset.

Exploratory model evidence may motivate a revised task decomposition or role
vocabulary. Every such revision must record the motivating evidence, receive a
new version, and be frozen before confirmatory evaluation. Evidence used to
define or select a construct cannot also serve as its independent confirmation;
confirmation must use untouched instances, held-out structural conditions, a
new task pair, an additional frozen model, or another prospectively declared
partition.

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

### G0 — Establish auditable task sources and native semantics

Record exact task provenance, native identity, inputs, answers, correctness
semantics, source-provided structural artifacts, and major observable covariates.
Do not require a new operation vocabulary or manual solution decomposition
before exploratory model-side discovery.

Success means that instances, prompts, outputs, and source metadata are
reproducible and auditable. Any later task-side decomposition remains
provisional and separately justified.

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

Freeze independently discovered model-side patterns and test whether they
transfer between task families without being redefined from the target task's
outcome. Compare against layer, position, lexical, answer-format, difficulty,
and task-identity explanations. Functional interpretation follows successful
transfer rather than being required to define it.

### G5 — Replicate the central finding

Repeat the smallest decisive set of G1–G4 tests on an additional frozen
pretrained model or architecture. Prioritize the existence of differentiation,
the function-versus-step distinction, and the strongest generalization result.

## 6. Planned evidence structure

### Phase A0 — Native-source inventory without new annotation

The revised protocol is specified in [PILOT_A0.md](PILOT_A0.md). Freeze exact
provenance, native correctness semantics, source-provided metadata and
structures, grouping risks, perturbation affordances, and reserved split roles
for GSM8K, DROP, MuSiQue-Ans v1.0, and the selected BIG-Bench tasks. Do not create
operation labels or manually reconstruct solution graphs.

`Symbol8`, the proposed matched function pairs, C1-C4, and new manual annotation
are inactive fallback instruments rather than prerequisites.

### Phase A1 — Native behavioral feasibility

- Select a frozen mechanistically accessible model and benchmark-faithful free-
  form response regime.
- Establish behavior by source task and native covariates before activation
  analysis.
- Keep all attempts in behavioral denominators and distinguish correct from
  incorrect inference trajectories.
- Do not define the target population by which tasks the selected model solves.

### Phase B — Activation-trajectory instrumentation

- Capture reproducible token-by-layer residual states and declared residual
  updates during native inference.
- Treat generated reasoning as behavior and possible alignment evidence, not as
  latent-computation ground truth.
- Freeze measurement units, storage policy, alignment, and quality controls
  before confirmatory use.

### Phase C — Label-free within-task pattern discovery

- Discover activation or transition patterns without task-operation labels.
- Test held-out within-task recurrence across instances and valid surface
  variation.
- Compare against shuffled, layer-only, position-only, lexical, answer,
  difficulty, output-length, correctness, and task-identity baselines.
- Use MI only as one estimator-sensitive information diagnostic, triangulated
  with held-out prediction, trajectory, similarity, and permutation analyses.

### Phase D — Frozen cross-task reuse and functional interpretation

- Freeze pattern definitions before applying them to a held-out task.
- Report A-to-B and B-to-A transfer separately without target-task redefinition.
- Use native metadata, source-preserving and answer-changing perturbations, and
  correct/incorrect comparisons to interpret successful transfer.
- Retain neutral `candidate computation pattern` language when semantic function
  remains uncertain.

### Phase E — Replication and causal boundary

- Replicate the smallest decisive within-task and cross-task findings on a
  second frozen model.
- Introduce targeted annotation or synthetic calibration only after a named
  identification failure and a separate plan.
- Treat patching, ablation, and stronger causal claims as separately designed
  evidence beyond observational pattern recurrence.

## 7. Baselines and null models

At minimum, primary analyses should compare against:

- layer/depth-only prediction;
- token-position-only prediction;
- reasoning-step/chain-depth-only prediction;
- task-family and prompt-template prediction;
- difficulty and correctness controls;
- randomly permuted discovered-pattern assignments or evaluation variables
  within appropriate matched strata;
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

Pilot A0 must first freeze source provenance and access. The remaining decisions
are:

1. Exact repositories, immutable revisions or checksums, licenses, eligible
   splits, and return-test reservations for the accepted source strata.
2. Whether the source inventory may inspect schemas and aggregate metadata only
   or a small declared set of instances.
3. First native task or task pair for behavioral feasibility.
4. Exact immutable primary model and tokenizer revisions; Qwen is excluded.
5. Native prompt regime, decoding, behavioral gate, and correctness parsing.
6. Activation measurement unit, capture scope, alignment, and storage budget.
7. Pattern-discovery, MI/predictive, trajectory, uncertainty, multiplicity, and
   transfer methods.
8. Perturbation families and the boundary of later intervention evidence.

## 10. Literature watch and differentiation policy

Whenever directly relevant new work is encountered, record or report its
primary source, date, central result, overlap with this project, methodological
difference, and concrete implication for novelty or design. A periodic watch
supplements this continuous obligation and should notify only on materially
relevant developments, not on routine search noise.

These decisions must be resolved in `DECISIONS.md` before they constrain code or
primary experiments.
