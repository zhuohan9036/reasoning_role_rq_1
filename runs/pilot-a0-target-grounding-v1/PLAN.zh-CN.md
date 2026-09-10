# 实施方案：pilot-a0-target-grounding-v1

> English: [PLAN.md](PLAN.md)

**状态：** 等待审核
**方案版本：** 2
**规划产物已授权：** 是
**实施已授权：** 否
**Git 行为：** 所有规划修改保持未提交

## 1. 目标

在不新增 annotation 的前提下，盘点已接受 native task source，并为第一次 behavioral pilot
提供可供决策的建议。不得检查模型 activation、定义 task operation 或实施 synthetic task。

## 2. 阻塞实施的审核选择

实施前冻结：

1. 每个已接受 source 的官方 repository 或 distribution channel；
2. 准确 immutable revision 或 file checksum，以及经过核实的 license；
3. eligible source split 与为后续 return test 保留的 split；
4. source access mode，以及是否授权有边界的 download；
5. inventory 只能检查 dataset schema 与 aggregate metadata，还是也可检查一小批明确声明的
   instance。

本方案不需要 annotation 人员、reconstruction sample size 或 reliability threshold，因为
新的 manual annotation 不在范围内。

## 3. 步骤 1：冻结 source registry

为 GSM8K、DROP、MuSiQue-Ans v1.0 与两个已接受 BIG-Bench task 创建机器可读 registry。
记录 source URL、revision/checksum、license、native ID scheme、official split、
redistribution constraint 与 citation。

## 4. 步骤 2：盘点原生任务信息

对每个 source，只记录其文件、文档、evaluator 或 generator 已经提供的信息：

- input、answer 与 correctness interface；
- rationale、calculation annotation、constituent-question DAG、supporting fact、template、
  size、difficulty 或 generator field；
- passage、constituent question、scenario 或 template 等不能跨 study partition 的自然
  grouping unit；
- benchmark-faithful prompt option 与 output parsing requirement；
- 能否在不指定 operation label 时产生 source-preserving 与 answer-changing perturbation；
- 已知 shortcut、contamination 与 provenance limitation。

不得推断缺失 solution graph，也不得指定 candidate operation label。

## 5. 步骤 3：建立 suitability matrix

按照与模型无关的标准评估每个 source：

- objective behavioral scoring；
- native multi-step evidence 或 task-construction rationale；
- 清楚的 source-instance 与 grouping identity；
- 与 free-form native inference 的兼容性；
- held-out instance 与 source-preserving perturbation 能力；
- 预期 alignment 与 activation-storage cost；
- 对 within-task recurrence 和后续 cross-task transfer 的作用；
- domain、lexical、answer-format 与 task-origin confound。

Matrix 推荐初始 task 或 task pair，但不选择模型，也不运行 behavior。

## 6. 步骤 4：保留 source role

在尚未抽取 instance 的情况下指定：

- 可用于 prompt/adapter development 的 source material；
- 可用于 behavioral discovery 的 source material；
- 为 within-task confirmation 保留的独立 source partition；
- 为 cross-task transfer 保留的独立 family 或 partition。

“Held out”表示没有用于定义本研究的 pattern 或 interpretation；它不表示 pretrained model
从未见过这些公开数据。

## 7. 步骤 5：规定后续任务边界

为以下工作准备简洁 action boundary，而不是 executable plan：

1. native behavioral feasibility；
2. activation-trajectory capture；
3. label-free within-task discovery 与 untouched confirmation；
4. 冻结的 cross-task transfer；
5. 通过 native metadata 与 perturbation 进行 functional interpretation；
6. 只有具名 identification failure 之后才可考虑的 fallback annotation、synthetic
   calibration 或 intervention。

每个后续任务继续分别要求 code、download、model execution、activation capture、server 与
Git publication 授权。

## 8. 拟议实施文件

| 路径 | 动作 | 用途 |
|---|---|---|
| `docs/PILOT_A0_SOURCE_INVENTORY.md` 和 `.zh-CN.md` | 创建 | 人类可读 source 与 suitability audit |
| `configs/data/pilot_a0_sources.yaml` | 创建 | 机器可读 source registry 与 reserved split role |
| `results/pilot-a0-target-grounding-v1/source_inventory.json` | 创建 | 紧凑 derived source metadata；不包含 benchmark text |
| `docs/DECISIONS.md` 和 `.zh-CN.md` | 修改 | 记录已审核 source revision 与 first-pilot 建议 |
| `docs/PROGRESS.md` 和 `.zh-CN.md` | 修改 | 记录 inventory 完成，不产生模型证据 |
| `runs/pilot-a0-target-grounding-v1/REVIEW.md` 和 `.zh-CN.md` | 创建 | 实施、验证、遗漏与下一门禁交接 |

不计划修改 `src/`、`scripts/`、test、dataset、prompt 或 model file。

## 9. 验证

- 解析 YAML 与 JSON 产物。
- 验证每个 source 具有 immutable provenance field、license status、native identity、
  grouping rule 与 reserved split role。
- 验证 source claim 可追溯到官方文档或 schema。
- 验证产物不包含 benchmark text、task-operation label、manual decomposition、model output
  或 activation。
- 验证双语链接与语义同步。
- 验证 changed path 匹配获批 allowlist，并运行 `git diff --check`。

## 10. 范围外事项

- 新 manual annotation、adjudication 或 reliability study。
- Benchmark-derived 或 from-scratch task decomposition。
- Synthetic task language implementation。
- Source code、test 或 executable data adapter。
- Model/tokenizer 选择、下载、inference 或 activation capture。
- MI estimation、probing、clustering、trajectory segmentation 或 transfer。
- Server execution、commit 或 push。

## 11. 审核门禁

人类审核应先解决第 2 节的五项 source-access 选择，之后才能授权实施。批准本 source-
inventory task 不会授权任何模型或 activation 工作。

