# Task brief: pilot-a-design-v1

> 中文版：[BRIEF.zh-CN.md](BRIEF.zh-CN.md)

**Status:** paused before implementation; superseded by target-grounding review
**Research scope:** Pilot A task design and implementation handoff

## Desired outcome

Turn the then-proposed Pilot A scientific design into an auditable implementation
contract without treating the existing task generators as authoritative. The
implementation will create a new controlled task language, matched task cells,
negative controls, disjoint discovery/confirmation data, and local validation.

This brief is retained as planning history. Pilot A0 subsequently identified
that the design lacked an explicit bridge to the intended target-task
population. No implementation is authorized; see
`runs/pilot-a0-target-grounding-v1/PLAN.md`.

## Frozen requirements

1. Pilot A is for pattern discovery and measurement validation only.
2. The claim ceiling is limited to the named model, task distribution, and
   response regime.
3. The task language is provisional and makes no completeness claim.
4. The core design crosses serial versus fork-join topology with externally
   supplied versus computed control.
5. Structural node families and functional subtypes are separate. Primary
   comparisons are `shift/reflect`, `add_merge/subtract_merge`,
   `parity/upper_half`, and `select_if/select_unless` within matched signatures.
   Direct-read remains a negative control.
6. Surface, value, position, length, and answer variables are balanced or
   explicitly controlled.
7. Discovery and untouched confirmation use disjoint semantic identities.
8. Qwen is excluded. The working default is a frozen Mistral 7B instruct model;
   exact immutable revisions are required before execution.
9. Existing task generators are non-authoritative calibration artifacts and may
   be reused, replaced, or bypassed only according to the accepted design.

## Acceptance criteria for later code implementation

- A deterministic reference solver validates every instance and event trace.
- All requested task cells and paired renderings satisfy declared balance.
- Discovery, confirmation, and control pools are semantically disjoint.
- Operator display names do not reveal computation identity.
- Functional subtype is not deterministically recoverable from signature,
  graph degree, event index, prompt region, output token, or task cell.
- Every core program has exactly six answer-relevant nodes.
- R1 emits six values in fixed delimiter slots and measures the residual stream
  at the delimiter immediately before each value.
- Simple shortcut heuristics are implemented and reported.
- The existing calibration fixtures continue to pass unless an approved plan
  explicitly replaces them.
- No model, tokenizer, or server is contacted by local tests.

## Out of scope for the current planning action

- Source-code, test, configuration, or fixture changes.
- Model download or execution.
- Activation capture or analysis.
- Server execution.
- Commit or push.
