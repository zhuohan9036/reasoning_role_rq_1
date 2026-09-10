# Pilot A0 protocol: native-task inventory and model-first discovery bridge

> 中文版：[PILOT_A0.zh-CN.md](PILOT_A0.zh-CN.md)

**Status:** revised protocol; awaiting human review
**Protocol version:** 0.2
**Last updated:** 2026-09-10

## 1. Purpose

Pilot A0 prepares a direct path from current mainstream reasoning tasks to
model-side discovery. It does not begin by inventing an operation vocabulary,
manually decomposing a benchmark, or implementing a synthetic task language.

The primary sequence is:

> native task -> successful native inference -> internal computation trajectory
> -> recurring within-task pattern -> frozen cross-task transfer test -> cautious
> functional interpretation

This route asks what computation patterns the model actually forms while
solving tasks, rather than asking whether the model matches a researcher-defined
list of operations. Task-side and model-side structure remain distinct.

## 2. Accepted target scope

The initial target population is English, text-only reasoning with objectively
checkable answers, task-relevant premises contained in the input or task rules,
and more than one mutually dependent computational step.

The accepted initial source strata are:

- human-authored mathematical word problems, initially represented by GSM8K;
- discrete reasoning over supplied text, initially represented by DROP;
- connected multi-hop question answering with native provenance, initially
  represented by MuSiQue-Ans v1.0;
- abstract deduction and state tracking, initially represented by BIG-Bench
  `logical_deduction` and `tracking_shuffled_objects`.

These strata diversify task origin and observable computation demands. They do
not constitute a complete ontology or a probability sample of all reasoning.
External retrieval, open-ended subjective generation, multimodal perception,
code execution, and formal theorem proving are outside this first population.

Exact repositories, immutable revisions, licenses, eligible splits, and source
access remain to be frozen before source inspection.

## 3. No-new-annotation rule

New manual task decomposition is not part of the default method. Pilot A0 first
uses only information native to each source:

- questions, inputs, answers, and official correctness rules;
- benchmark-native IDs, splits, difficulty or size fields;
- source-provided rationales, calculation traces, constituent questions, DAGs,
  supporting facts, templates, or generator metadata when available;
- reproducible prompt and inference provenance.

Native rationales and graphs are source artifacts, not unique necessary
algorithms and not descriptions of the model's internal computation.

Manual annotation may be proposed only after a documented failure analysis
shows that a specific scientific distinction cannot be tested with native
metadata, model-side patterns, controlled input variation, or existing source
artifacts. Such annotation requires a new bounded plan and explicit approval.

## 4. Native inference

A native inference uses the benchmark's original task semantics and a
benchmark-faithful prompt. The model may generate free-form reasoning and a
final answer, but the protocol does not impose researcher-defined operation
names, symbolic state slots, or a forced execution trace.

Every attempt records the prompt, decoding configuration, full response, parsed
answer, correctness, model and tokenizer revisions, and source-instance
identity. All attempts remain in behavioral denominators.

Generated reasoning text is a behavioral artifact. It may support token
alignment or interpretation hypotheses, but it is not accepted as a faithful
record of latent computation.

## 5. Model-side measurement objects

The first discovery stage may examine, at declared token and layer resolutions:

- residual-stream states;
- residual updates across attention and MLP sublayers;
- local state transitions across layers or generated-token windows;
- attention or MLP outputs when a later plan justifies their added cost;
- responses to source-preserving or answer-changing input perturbations.

A measurement unit must be frozen before its confirmatory use. Initial neutral
terms are `activation pattern`, `transition pattern`, and `candidate computation
pattern`. A cluster is not automatically an operation or reasoning role.

## 6. Label-free within-task discovery

Pattern discovery does not use task-operation labels. It may use task family,
correctness, native instance metadata, token/layer coordinates, and declared
perturbation identity as controls or evaluation variables.

A candidate within-task computation pattern must:

1. recur across held-out correct instances rather than one prompt template;
2. survive controls for layer, absolute token position, output length, lexical
   overlap, answer identity, difficulty, and task-instance identity;
3. remain stable under at least one source-preserving surface variation when
   such variation is valid;
4. outperform shuffled, structure-only, and metadata-only baselines;
5. have its definition frozen before untouched evaluation.

Incorrect inferences are retained as a separate diagnostic. They cannot be
silently removed from behavior reports or pooled with correct trajectories.

## 7. Information-theoretic and predictive diagnostics

Mutual information and related measures may test whether a model-side pattern
contains information about a future output, answer, task identity, input
variable, perturbation, or correctness after declared controls.

Mutual information is not an operation detector. In particular:

- information about the answer may reflect answer representation rather than
  computation;
- information about task identity may reflect lexical or domain differences;
- observational dependence does not show that the information is used;
- high-dimensional continuous MI estimates can be estimator-sensitive.

Accordingly, MI must be triangulated with held-out prediction, representation
or transition similarity, trajectory segmentation, permutation baselines, and
sensitivity analysis. The exact estimator, dimensionality treatment, and null
distribution require a later reviewed analysis plan.

## 8. Cross-task reuse test

A within-task pattern becomes a cross-task candidate only through transfer:

1. discover and freeze the pattern definition using one source task or a
   predeclared discovery set;
2. apply it to a held-out task without redefining the pattern from that task's
   outcome;
3. test recurrence, transition similarity, predictive information, and
   perturbation response against layer, position, lexical, difficulty, and task-
   identity baselines;
4. report asymmetric transfer when A-to-B differs from B-to-A;
5. restrict the result to the tested tasks and model.

Shared task labels or similar answer formats do not establish reuse. Conversely,
a transferable model-side pattern may be reported before it has a confident
semantic operation name.

## 9. Functional interpretation

Interpretation follows discovery rather than defining it. Evidence may come
from:

- when and where the pattern appears in the model's generated trajectory;
- native benchmark metadata and source-provided structures;
- controlled input perturbations and resulting internal/output changes;
- comparison with correct and incorrect inferences;
- later targeted patching, ablation, or controlled microtasks under separate
  plans.

An interpretation remains a `candidate computation` until evidence separates
it from answer encoding, task identity, position, generic generation dynamics,
and other structural explanations. Strong causal claims remain outside RQ1
unless separately designed interventions support them.

## 10. Status of task language v0.2 and annotation

`Symbol8`, its proposed function pairs, and cells C1-C4 remain inactive
calibration-sandbox ideas. They are not the source of model-side discovery and
are not authorized for implementation.

Both synthetic task construction and new manual annotation are fallback tools.
Either may be reconsidered only when a named unresolved identification problem
cannot be addressed through native tasks, native source artifacts, held-out
transfer, or controlled perturbations. Convenience alone is insufficient.

## 11. Evidence ladder

Pilot evidence is interpreted in the following order:

1. **measurement validity:** trajectories and metadata are captured and aligned
   reproducibly;
2. **within-task recurrence:** a frozen pattern survives held-out instances and
   declared confound controls;
3. **cross-task reuse:** the frozen pattern transfers to an independently held-
   out task;
4. **functional interpretation:** converging native and perturbational evidence
   supports a bounded account of what the pattern tracks;
5. **causal role:** requires a separate intervention design and is not implied
   by the preceding levels.

Failure at a later level does not erase an earlier result; it lowers the claim
ceiling.

## 12. Immediate outputs and next gates

The immediate Pilot A0 implementation should produce a no-annotation source
inventory recording exact provenance, native fields, correctness semantics,
available structural artifacts, perturbation affordances, and suitability for
native inference and model-side discovery.

Separate future plans must then authorize:

1. behavioral feasibility on selected native tasks;
2. activation capture for successful native inference;
3. label-free within-task discovery and confirmation;
4. cross-task transfer;
5. targeted interpretation or fallback instrumentation.

No model, benchmark, code, download, or server action is authorized by this
protocol alone.
