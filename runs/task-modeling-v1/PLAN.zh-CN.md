# 实施方案：task-modeling-v1

> English: [PLAN.md](PLAN.md)

**状态：** 已实现并通过本地验证
**方案版本：** 1
**代码修改授权：** 是，仅限本地实现
**服务器执行授权：** 否

## 1. 目标

实现 `BRIEF.md` 中描述的任务侧校准基础。最终系统为两个受控 reasoning family 生成
小型、确定性的数据集，并使 task structure、nuisance factor 和 split provenance 可
审计。它不执行模型 inference 或模型侧分析。

## 2. 提议接口

### Canonical instance record

使用带版本、可序列化为 JSON 的 record，并包含以下顶层概念：

- `schema_version`、`instance_id`、`family` 和 `generator_version`；
- 独立于措辞的 canonical problem specification；
- 渲染后面向模型的 `prompt` 和 `target` 字段；
- 具有稳定 node ID 的 directed acyclic dependency graph；
- 明确标记为 task-side provenance 的 deterministic generator trace；
- 任务族内部的临时 candidate-operation label；
- chain length、distractor count、presentation order、vocabulary/template ID 和
  answer encoding 等 nuisance factor；
- split name 和 semantic grouping key。

Canonical record 可以保存中间任务状态以供验证，但默认 renderer 不得在 prompt 中
暴露它们。该选择已于 2026-09-08 获批。

### Task-family adapter

每个 family 实现一个小型公共 protocol：

- 使用明确的 random-number-generator 生成 canonical problem；
- 根据 canonical problem 求解或验证，不读取已存储 target；
- 使用具名 template 和 vocabulary 渲染 prompt；
- 输出 dependency graph 和 task-side trace；
- 返回用于 split 的 semantic identity 与 grouping key。

### 数据集生成入口

单一入口接收 YAML configuration，并输出：

- 每个 split 一个 canonical JSONL 文件；
- 包含 provenance、count、factor distribution 和 hash 的 `manifest.json`；
- 若 constraint 违反则使进程失败的 validation summary。

文档将规定稳定 serialization 规则，以便在支持的 Python 版本中测试 determinism。

## 3. 计划文件

| 路径 | 操作 | 用途 |
|---|---|---|
| `pyproject.toml` | 创建 | Python 3.11 package、dependency 和 test/lint configuration |
| `src/reasoning_role/__init__.py` | 创建 | package/version metadata |
| `src/reasoning_role/tasks/schema.py` | 创建 | canonical record、graph node/edge 与 validation |
| `src/reasoning_role/tasks/base.py` | 创建 | task-family protocol 与公共类型 |
| `src/reasoning_role/tasks/registry.py` | 创建 | 不使用 dynamic import 的显式 family lookup |
| `src/reasoning_role/tasks/function_composition.py` | 创建 | symbolic function-composition generator、solver、renderer |
| `src/reasoning_role/tasks/relational_path.py` | 创建 | relational path generator、solver、renderer |
| `src/reasoning_role/data/split.py` | 创建 | group-aware deterministic split assignment |
| `src/reasoning_role/data/generate.py` | 创建 | balanced generation orchestration 与 validation |
| `src/reasoning_role/data/io.py` | 创建 | canonical JSONL writing、hashing 与 manifest |
| `scripts/generate_dataset.py` | 创建 | 轻量命令行入口 |
| `configs/data/task_calibration_smoke.yaml` | 创建 | 小型本地/CI fixture 配置 |
| `configs/data/task_calibration_v1.yaml` | 创建 | 提议的较大校准配置，不执行 |
| `tests/tasks/test_schema.py` | 创建 | schema 与 dependency-graph invariant |
| `tests/tasks/test_function_composition.py` | 创建 | generation/solver/property test |
| `tests/tasks/test_relational_path.py` | 创建 | generation/solver/property test |
| `tests/data/test_split.py` | 创建 | split reproducibility 与 semantic leakage test |
| `tests/data/test_generate.py` | 创建 | balance、determinism、manifest 与 failure test |
| `tests/test_cli.py` | 创建 | 端到端 smoke generation |
| `tests/fixtures/task_calibration_smoke/` | 创建 | 小型已审核输出与 expected manifest |
| `docs/DATA.md` | 创建 | schema、factor、split semantics 与 provenance |
| `runs/task-modeling-v1/REVIEW.md` | 实现后创建 | change、test、deviation 与 acceptance evidence |

只有在行为和接口保持不变时，实施阶段才可以调整具体文件分组；任何调整都记录在
`REVIEW.md`。

## 4. 配置结构

YAML configuration 包含：

- schema 和 generator version；
- global seed 与 output serialization format；
- task-family list 与 family-specific domain；
- 按 chain length、distractor count、template、vocabulary 和 answer encoding 请求的
  count；
- 具名 split definition 与 group key；
- surface、template 和 length generalization 的 holdout value；
- maximum generation attempt 和 strict balance policy；
- 在运行时提供的 output path，而不是提交机器路径。

Seed 从稳定的 textual namespace 派生，不使用 Python 的 process-random hash function。
Manifest 保存完整解析后的配置。

## 5. Split 与泄漏设计

1. 在 prompt rendering 前构造 canonical semantic identity。
2. 确定性地分配 group，然后渲染 template 和 surface form。
3. 等价 canonical problem 必须位于同一个互斥 split。
4. 对 held-out-surface 和 held-out-template evaluation，区分 semantic core 与 held-out
   factor，使目标维度改变时不产生 semantic leakage。
5. 对 held-out-length，保留配置中的 chain length，并报告不支持的 factor combination，
   不得静默回填。
6. 输出 semantic ID、canonical problem hash、rendered prompt hash，以及 v1 中可用的
   family-specific isomorphism key 的 overlap audit。

## 6. 正确性策略

- 全程使用显式 random-number-generator object。
- 序列化前从 canonical problem 验证每个生成样例，并拒绝无效 graph。
- Target verification 的逻辑必须与读取 stored target 分离。
- 测试 graph acyclicity、reachable target dependency、trace/graph consistency 与
  task-family invariant。
- 使用跨 seed 与 factor combination 的 property-style parameterized test。
- 在两个独立临时目录中各生成一次 smoke fixture，并要求 JSONL 逐字节相同、manifest
  content hash 相等。
- 不可行的 balance/split 请求必须抛出描述性错误。

实施审核必须披露 generation 和 verification 之间会削弱独立性的共享逻辑。

## 7. 批准后的执行顺序

1. 创建 package/configuration scaffold 与 schema type。
2. 实现 family protocol 与 canonical serialization。
3. 实现 symbolic function composition 和独立检查。
4. 实现 relational path composition 和独立检查。
5. 实现 group-aware split、audit、strict balancing 和 manifest。
6. 添加 CLI、smoke configuration 和文档。
7. 添加并运行 unit、property-style、integration 和 deterministic replay test。
8. 只生成小型 fixture。
9. 编写 `REVIEW.md`，记录 file change、command、result、known limitation 和 server step；
   不启动 server job。

## 8. 本地验收检查

- 在 Python 3.11 中完成 package install/import。
- 完整自动化测试通过。
- CLI help 与 invalid-configuration path 行为正确。
- 两次 smoke generation 逐字节一致。
- 重新计算的 target 与所有 stored target 一致。
- 所有必需 identity/hash audit 均无 cross-split overlap。
- Manifest count 与实际 record 和请求的 factor cell 一致。
- 仓库中不存在大型输出或机器专属绝对路径。

## 9. 服务器验证（延后）

获得服务器详情和授权后：

1. 重建固定版本的环境；
2. 运行完整测试；
3. 在 scratch storage 中运行两次较大的 v1 配置；
4. 比较 hash 并验证所有 record；
5. 记录 runtime、RAM、artifact size、environment 和 Git revision；
6. 只把 manifest 和小型 summary 传入 version control。

本任务不需要 GPU test。

## 10. 风险与缓解

- **研究者预设 ontology：** operation label 保持 family-local 和 provisional；
  cross-family mapping 放入可选 hypothesis metadata。
- **Solver circularity：** 从 canonical problem 验证并披露共享逻辑；适用时为小型 fixture
  增加 brute-force 或 alternative check。
- **Split leakage：** rendering 前分组，并审计多个 identity level。
- **意外结构相关：** 生成并报告交叉 factor cell；请求的平衡不可行时失败。
- **虚假的跨平台确定性：** 把 Python 3.11 定义为 v1 目标，对 canonical serialized
  record 而非 filesystem metadata 计算 hash。
- **过早固定任务：** 把两个 family 都标为 calibration pilot，并要求在 pilot 后做出决策，
  再冻结 primary task。

## 11. 批准门禁

用户于 2026-09-08 批准本方案及三个推荐选择。已授权本地实现与测试，但没有授权
服务器执行或任何模型实验。
