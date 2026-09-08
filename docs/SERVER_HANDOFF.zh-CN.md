# 服务器结果交接契约

> English: [SERVER_HANDOFF.md](SERVER_HANDOFF.md)

## 目的与边界

本契约使负责本地规划与审核的任务能够检查服务器实验结果，同时避免把大型文件提交到
Git。Git remote 传递的是已经提交的仓库状态，并不会暴露服务器上未提交的文件。

大型原始 artifact 保留在服务器。一个能够自我描述的小型 handoff bundle 被复制到
本地仓库中被忽略的 `artifacts/` 目录。Assistant 首先只读检查该 bundle。创建 tracked
result report 或提升小型证据需要另一次明确的文档动作授权。

## 三层存储

```text
# 第 1 层：完整服务器输出；绝不提交
/scratch/<project>/<run-id>/
├── run_manifest.json
├── summary.json
├── summary.csv
├── artifact_index.json
├── checksums.sha256
├── diagnostics.jsonl
├── log_tail.txt
├── activations/
├── checkpoints/
└── full_logs/

# 第 2 层：本机小型交接包；被 Git 忽略
artifacts/server-results/<run-id>/
├── run_manifest.json
├── summary.json
├── summary.csv
├── artifact_index.json
├── checksums.sha256
├── diagnostics.jsonl
└── log_tail.txt

# 第 3 层：经审核的小型证据；获批后可进入 Git
results/<run-id>/
├── manifest.json
├── summary.json
├── summary.csv
├── REPORT.md
└── REPORT.zh-CN.md
```

第 2 层不得包含 secret，也不是 backup。只读结果审核期间不会自动创建第 3 层。

## 必需的小型交接文件

### `run_manifest.json`

在适用情况下，run manifest 必须包含：

- schema version、run ID、task ID 和 parent plan ID/version；
- exact Git commit 与要求的 clean-worktree state；
- 完整解析后的 configuration 及其 hash，或稳定路径与 hash；
- dataset manifest 和 selected-file hash；
- exact model/tokenizer ID 和 immutable revision；
- prompt/template identity 和 generation setting；
- 经过清理的 command 或 entry point 与 argument；
- Python、package、CUDA、driver、GPU、host alias 和 scheduler metadata；
- start/end time、run status、resume count 和 stopping reason；
- expected、attempted、completed、failed、duplicated 和 missing record count；
- 每个小型 output 的 hash；
- 证据允许的最弱科学解释。

Manifest 中不得出现 credential、access token、private key、environment secret 或敏感
host detail。

### `summary.json` 与 `summary.csv`

这些文件包含预先规定的 aggregate metric、denominator、uncertainty、stratum、failure
count 和 eligibility decision。除非获批方案明确规定不同 estimand，每个 failed attempt
都必须保留在已声明 denominator 中。

### `artifact_index.json`

Artifact index 表示保留在服务器的大型文件。推荐的最低 schema：

```json
{
  "schema_version": "1.0",
  "run_id": "<run-id>",
  "server_alias": "<non-secret-alias>",
  "output_root": "/scratch/<project>/<run-id>",
  "artifacts": [
    {
      "artifact_id": "<stable-id>",
      "kind": "activation",
      "path": "activations/<relative-path>",
      "format": "<format>",
      "schema_version": "<version>",
      "size_bytes": 0,
      "sha256": "<sha256>",
      "producer_commit": "<git-commit>",
      "producer_config_sha256": "<sha256>",
      "retention": "server_only"
    }
  ]
}
```

优先使用相对于 `output_root` 的路径。若必须使用绝对路径，应保留在这个本机 ignored
handoff 中，不写入 tracked report。

### `diagnostics.jsonl`

Diagnostic 应保持小型，并按事先声明的规则选取，例如包含全部 failure，再加上使用固定
seed 对 success 进行 stratified sampling。不得在看到预期结果后静默选择 convenience
sample。

### `log_tail.txt`

只包含诊断 completion、warning 和 failure 所需的有界片段。移除 secret，避免传输没有
上限的完整日志。

### `checksums.sha256`

该文件覆盖除自身外的每个已传输小型文件。应在服务器生成，并在传输后验证。如果服务
器平台使用其他 checksum 命令，在 manifest 中记录精确的等价方法。

## 推荐传输方式

从本地仓库根目录只复制 allowlist 中的小文件：

```bash
mkdir -p artifacts/server-results/<run-id>

rsync -av --prune-empty-dirs \
  --include='*/' \
  --include='run_manifest.json' \
  --include='summary.json' \
  --include='summary.csv' \
  --include='artifact_index.json' \
  --include='checksums.sha256' \
  --include='diagnostics.jsonl' \
  --include='log_tail.txt' \
  --exclude='*' \
  <user>@<server>:/scratch/<project>/<run-id>/ \
  artifacts/server-results/<run-id>/
```

若无法使用 `rsync`，可以使用 SFTP、经过批准的 mounted directory 或上传小型 archive。
不得复制 target 会展开到意外大型或敏感目录的 symlink。

复制完成后，用户对本地 Codex task 说：

```text
只读审核服务器运行 <run-id>。
本地交接路径：artifacts/server-results/<run-id>/
大文件仍保留在服务器，并由 artifact_index.json 索引。
```

该请求只授权只读检查和讨论，不授权仓库写入、报告生成、remote access 或额外服务器
命令。

## 本地审核顺序

Assistant 应当：

1. 解析精确本地 handoff path，并确认 Git 忽略该路径；
2. 列出 file、size 和意外 entry，不打开大型 artifact；
3. 验证 `checksums.sha256` 和 `run_manifest.json` 中的 hash；
4. 对照获批方案核对 run/config/data/model/code identity；
5. 对账 expected、attempted、completed、failed、duplicate 和 missing count；
6. 在可能时重新计算小型 summary invariant；
7. 检查事先声明的 diagnostic sample 和 bounded log；
8. 区分 empirical result 与 pipeline/fake-backend check；
9. 报告 anomaly、证据不足和证据能支持的最弱解释；
10. 说明是否确实需要额外的小型数据切片。

若小型证据不足，应请求最小且具有决定性的补充，例如 fixed-seed stratified sample、
选定 tensor statistic、有边界的 layer/component slice 或 derived aggregate。默认不请求
或复制完整 activation store。

## 提升为 tracked result

只读讨论结束后，assistant 在创建 `results/<run-id>/` 前必须先提供文档动作预告。预告
写明要提升的精确小型文件、报告路径、validation、redaction 和 Git 行为。

只有得到明确批准后，assistant 才可以创建：

- `results/<run-id>/manifest.json`：经过清理的小型 provenance；
- 获批的 summary JSON/CSV 或小型 figure data；
- `REPORT.md` 与 `REPORT.zh-CN.md`：同步记录 result、uncertainty、limitation、
  alternative explanation 和 research handoff；
- 适用时为 tracked compact evidence 创建 checksum。

报告必须通过 stable ID 和 checksum 指向大型 artifact，不能假装未提交的服务器路径是
持久公共证据。

## 保留与可复现性

- 在项目的 retention policy 将大型 artifact 移动到获批持久存储前，服务器仍是其
  权威位置。
- `artifacts/server-results/` 是可以丢弃的本地 review cache，不能替代服务器 backup。
- 结果审核期间绝不删除、覆盖或重新组织服务器 artifact。
- 如果 rerun 改变 code、configuration、data、model 或 prompt，应获得新 run ID；除非
  获批 protocol 明确定义它属于兼容 resume。
- 不能仅仅因为小型 bundle 成功复制，就声称结果可复现；provenance、determinism
  expectation 和 replay check 仍是相互独立的证据。
