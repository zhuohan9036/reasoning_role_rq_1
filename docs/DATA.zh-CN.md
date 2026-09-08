# 任务校准数据契约

> English: [DATA.md](DATA.md)

## 解释边界

该数据集描述的是外部规定的任务计算。dependency graph 和 `task_side_trace` 字段记录
生成器如何构造并检查答案。它们不是对 Transformer 内部算法、chain of thought 或
reasoning role 的观察。

Candidate operation 名称只是任务族内部的便利标签：

- `function_composition.apply_function`；
- `relational_path.compose_relation`。

这些 operation 之间是否存在 correspondence 属于后续假设，因此有意不放入必需的
dataset schema。

## Canonical record

每一行 JSONL 都是一个带 schema 版本的 record，包含：

- 稳定的 instance、family、schema 和 generator identifier；
- 独立于自然语言表达的 canonical problem；
- 面向模型的 `prompt` 和 `target` 字段；
- 任务所需的 task-side dependency graph；
- `task_side_trace` 中隐藏的任务侧中间状态；
- 临时性的 candidate-operation 名称；
- nuisance factor 和 split membership；
- 用于 leakage audit 的 semantic、canonical-problem 和 prompt hash。

默认 renderer 只使用 canonical problem、选定 template、选定 vocabulary 和输出说明
来构造 prompt，从不读取或渲染 `task_side_trace`。

## Pilot task family

### Symbolic function composition

一个问题规定若干有限域 function、一个起始 symbol，以及需要依次应用的 function
子集。问题中可以包含 distractor function，但它们不属于 query。Reference solver
读取 query 和 function mapping，不信任已存储的 target。

### Relational path composition

一个问题规定 entity 之间有向的空间关系，并要求求出 source 到 target 的二维净位移。
Distractor relation 构成不连通 component。Reference solver 搜索 relation graph 并累加
edge vector；它忽略已存储的 relevance flag 和 target。

两个 task family 都只是校准工具。它们的存在不代表 candidate operation 是 minimal、
universal、跨任务共享，或确实被模型内部使用。

## 受控因素

v1 generator 交叉组合以下因素：

- chain length；
- distractor count；
- canonical 或 shuffled presentation order；
- prompt template；
- surface vocabulary；
- answer encoding。

同时记录 function-domain size 等任务族特有因素。每个 split 的请求数量必须能被完整
factor-cell 数整除。若平衡要求不可行，generator 会失败，而不是静默修改请求。

## Split 语义

- `train`：参考 factor domain。
- `iid_test`：使用相同 factor 与 rendering domain，但生成新的 semantic problem。
- `surface_test`：vocabulary ID 与训练集不相交，其他受控 domain 保持一致。
- `template_test`：template ID 与训练集不相交，其他受控 domain 保持一致。
- `length_test`：chain length 与训练集不相交，其他受控 domain 保持一致。

语义等价的问题绝不允许出现在两个 split 中。Audit 还会检查 canonical-problem hash
和 rendered-prompt hash。Semantic identity 在渲染前计算，并排除 presentation order、
vocabulary、template 和 answer encoding。

## 数据生成

在已经安装的开发环境中：

```bash
reasoning-role-generate \
  --config configs/data/task_calibration_smoke.yaml \
  --output /new/output/directory
```

在没有安装 package 的 checkout 中：

```bash
python scripts/generate_dataset.py \
  --config configs/data/task_calibration_smoke.yaml \
  --output /new/output/directory
```

输出目录不得已经存在，以防止意外覆盖 artifact。

## Artifact 内容

生成过程会为每个 split 创建一个 JSONL 文件，并创建
`validation_summary.json` 和 `manifest.json`。Manifest 记录：

- 完整解析后的配置及其 SHA-256 hash；
- global seed、schema、generator 和 package version；
- 可用时记录 Git revision 与工作区 dirty 状态；
- Python 和 PyYAML 版本；
- 按 task family 统计的 record count 与 factor distribution；
- 每个 split 和 validation 文件的内容 hash。

大型生成数据集保存在 Git 之外。只有 smoke fixture、小型 manifest 或 summary 应提交
到 Git。

## 确定性边界

Seed 由带明确文本 namespace 的 SHA-256 派生。Generator 不使用 Python 的进程随机
hash。Record 采用排序后的紧凑 JSON、UTF-8 编码和 Unix 换行。

在 configuration、seed、code revision、dependency version 和支持的 Python baseline
相同时，必须能够逐字节复现。即使 record 内容不变，code 或 environment revision 的
变化仍必须在 manifest 中可见。
