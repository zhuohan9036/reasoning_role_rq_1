# 实施方案：behavioral-calibration-v1

> English: [PLAN.md](PLAN.md)

**状态：** 已实现并通过本地验证
**方案版本：** 1
**代码修改授权：** 是，仅限本地框架
**服务器执行授权：** 否

## 1. 目标与科学契约

为 task-calibration record 实现只评估模型输出的框架。v1 主条件采用
final-answer-only prompt 和 greedy decoding；`task_side_trace` 永远不传给 backend。
包括 parse failure 和 inference failure 在内，每个尝试 example 都保留在 denominator
中。Behavioral accuracy 是 eligibility diagnostic，不是 functional-organization 证据。

## 2. Record 与 metric

每个 record 保存 dataset 和 instance identity、model/tokenizer revision、prompt mode
和 exact final input、decoding setting、raw completion、token、latency、structured
error、expected answer、parsed answer、nuisance factor 和 provenance reference。

- `raw_exact`：raw completion 与 expected answer 相等。
- `trimmed_exact`：去除两端空白后相等；主要 metric。
- `format_valid`：去除两端空白后的完整输出符合其 encoding。
- `parsed_exact`：只有输出格式完全有效时，才进行 encoding-aware equality。
- Failure、empty-output 和 extra-text rate。

Parser 绝不在 explanation 中搜索正确 substring。Summary 使用所有 attempted example，
并包含 95% Wilson interval。

## 3. 接口

Backend protocol 提供 `prepare`、`format_input`、`generate` 和 `close`。Result 保留
request ID，并返回 completion 或 structured failure。Runner 验证 identity，而不是
假定 response order。

Fake backend 支持 deterministic correct、malformed、wrong 和 failure mode。Hugging
Face adapter 要求 exact revision；支持显式 local-only、dtype、device、batch 和 prompt
mode 控制；默认 `trust_remote_code: false`；冻结 parameter；关闭 gradient；正确区分
prompt token 与 completion token；并拒绝 v1 中的 sampling。Torch 和 Transformers 均
采用 lazy import。

## 4. 计划文件

| 路径 | 操作 | 用途 |
|---|---|---|
| `pyproject.toml` | 修改 | 隔离的 `model` dependency 与 evaluation CLI |
| `src/reasoning_role/behavioral/schema.py` | 创建 | request、result、metric、manifest |
| `src/reasoning_role/behavioral/parsing.py` | 创建 | whole-output parser |
| `src/reasoning_role/behavioral/backends/base.py` | 创建 | backend protocol |
| `src/reasoning_role/behavioral/backends/fake.py` | 创建 | deterministic local backend |
| `src/reasoning_role/behavioral/backends/huggingface.py` | 创建 | frozen causal-LM adapter |
| `src/reasoning_role/behavioral/runner.py` | 创建 | batching、resume、reconciliation、writing |
| `src/reasoning_role/behavioral/summary.py` | 创建 | stratum、interval、eligibility |
| `src/reasoning_role/behavioral/provenance.py` | 创建 | data/model/software/hardware metadata |
| `scripts/evaluate_behavior.py` | 创建 | checkout-local CLI |
| `configs/eval/behavioral_smoke_fake.yaml` | 创建 | 完整本地 evaluation |
| `configs/eval/behavioral_server.template.yaml` | 创建 | 显式标注未解决 server field |
| `tests/behavioral/` | 创建 | behavioral harness test |
| `tests/fixtures/behavioral_smoke/` | 创建 | 小型 deterministic artifact |
| `docs/EVALUATION.md` | 创建 | protocol 与 interpretation limit |
| `runs/behavioral-calibration-v1/REVIEW.md` | build 后创建 | acceptance 与 handoff |

## 5. 配置与 provenance

解析后的 YAML 指定 evaluation version；dataset file 与 hash；split/family filter；
backend；exact model/tokenizer revision；plain/chat prompt mode；batch 和 decoding setting；
seed；output/resume policy；summary stratum；eligibility threshold。机器路径只放在忽略的
local configuration 或 CLI argument 中。

Manifest 记录 code、config、dataset、model、tokenizer、prompt template、software 与
可用 hardware provenance。保留并计算 template 处理后 exact input 的 hash。

## 6. 安全恢复

1. 加载模型前解析 configuration/data 并计算 hash。
2. 拒绝 provenance 不兼容的现有 run directory。
3. Resume 时要求 data、model、tokenizer、prompt 和 decoding hash 完全相同。
4. 拒绝 duplicated、missing、reordered 或 conflicting result ID。
5. 使用 atomic batch checkpoint 或经过测试的 append journal。
6. 生成 summary 前，对 expected、completed、failed 和 missing ID 进行对账。
7. 在 manifest 中记录最终 per-example file 和 summary 的 hash。

## 7. 本地测试

- 对 whole-output parser 进行 adversarial case 测试，包括 explanation、embedded 或
  multiple answer、Unicode lookalike、whitespace、bracket 和 signed vector。
- 执行包含 correct、invalid、wrong 和 failed case 的 80-record fake run。
- Repeatability、interruption/resume 和 provenance-mismatch test。
- 拒绝 missing/duplicate/reordered backend result。
- 独立重算 summary 与 denominator check。
- Stubbed Hugging Face freeze、no-gradient、chat-format 和 token-boundary test。
- 不使用网络或可选模型下载，在 Python 3.11 上运行完整 suite。

## 8. 延后的服务器验证

提供 exact revision、environment 和 permission 后：记录环境；检查一个 batch；人工检查
8–16 个 example；冻结 config 和 data hash；运行 pilot；重放 subset；报告 stratified
accuracy、Wilson interval、failure、runtime 和 peak memory。不保存 activation。

## 9. 结果分支

- 两个 family 都通过：规划 semantic-support expansion 和 dataset freeze。
- 一个通过：暂时保留该 family，重新设计或替换另一个。
- 都未通过：重新考虑 checkpoint、scale、prompt condition 或 task。
- 似乎需要 scratchpad：把它作为 manipulation/confound 单独规划。
- Format error 占主导：如实报告；绝不通过 substring extraction 人为提高 accuracy。

## 10. 风险

本方案处理以下风险：机制性过度解释、chat-template confound、parser inflation、
nondeterminism、静默缺失 example、sample size 不足，以及当前 relational family 在短链条
上的 semantic support 较小。

## 11. 批准门禁

`BRIEF.md` 中三个问题已于 2026-09-08 全部获批。已授权本地框架代码与 fake test；
仍未授权下载、真实模型、activation 或服务器执行。
