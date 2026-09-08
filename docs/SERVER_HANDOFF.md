# Server-result handoff contract

> 中文版：[SERVER_HANDOFF.zh-CN.md](SERVER_HANDOFF.zh-CN.md)

## Purpose and boundary

This contract lets the local planning/review task inspect server experiment
results without committing large files to Git. A Git remote transfers committed
repository state; it does not expose uncommitted files on a server.

Large raw artifacts remain on the server. A small, self-describing handoff
bundle is copied into the local repository's ignored `artifacts/` tree. The
assistant first inspects that bundle read-only. Creating a tracked result report
or promoting compact evidence requires a separate, explicit documentation
action.

## Three storage layers

```text
# Layer 1: complete server output; never committed
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

# Layer 2: compact local handoff; ignored by Git
artifacts/server-results/<run-id>/
├── run_manifest.json
├── summary.json
├── summary.csv
├── artifact_index.json
├── checksums.sha256
├── diagnostics.jsonl
└── log_tail.txt

# Layer 3: reviewed compact evidence; eligible for Git after approval
results/<run-id>/
├── manifest.json
├── summary.json
├── summary.csv
├── REPORT.md
└── REPORT.zh-CN.md
```

Layer 2 must never contain secrets and is not a backup. Layer 3 is not created
automatically during read-only result review.

## Required compact handoff files

### `run_manifest.json`

The run manifest must contain, where applicable:

- schema version, run ID, task ID, and parent plan ID/version;
- exact Git commit and required clean-worktree state;
- resolved configuration plus its hash, or a stable path and hash;
- dataset manifest and selected-file hashes;
- exact model and tokenizer IDs and immutable revisions;
- prompt/template identity and generation settings;
- sanitized command or entry point and arguments;
- Python, package, CUDA, driver, GPU, host-alias, and scheduler metadata;
- start/end time, run status, resume count, and stopping reason;
- expected, attempted, completed, failed, duplicated, and missing record counts;
- hashes for each compact output; and
- the weakest permitted scientific interpretation.

Credentials, access tokens, private keys, environment secrets, and sensitive
host details must not appear in the manifest.

### `summary.json` and `summary.csv`

These contain the pre-specified aggregate metrics, denominators, uncertainty,
strata, failure counts, and eligibility decisions. Every failed attempt remains
in the declared denominator unless the approved plan explicitly specifies a
different estimand.

### `artifact_index.json`

The artifact index represents large files that remain on the server. Recommended
minimum schema:

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

Prefer paths relative to `output_root`. If an absolute path is necessary, keep
it in this local ignored handoff rather than a tracked report.

### `diagnostics.jsonl`

Diagnostics should be compact and selected by a declared rule—for example all
failures plus a fixed-seed stratified sample of successes. It must not be a
silent convenience sample chosen after inspecting the desired result.

### `log_tail.txt`

Include only the bounded section needed to diagnose completion, warnings, and
failures. Remove secrets and avoid transferring an unbounded full log.

### `checksums.sha256`

This file covers every transferred compact file except itself. Generate it on
the server and verify it after transfer. If the server platform uses another
checksum command, record the exact equivalent in the manifest.

## Recommended transfer

From the local repository root, copy only the compact allowlist:

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

SFTP, an approved mounted directory, or a compact uploaded archive is acceptable
when `rsync` is unavailable. Do not copy a symlink whose target expands to an
unintended large or sensitive tree.

After copying, the user tells the local Codex task:

```text
Review server run <run-id> read-only.
Local handoff path: artifacts/server-results/<run-id>/
Large files remain on the server and are indexed by artifact_index.json.
```

This request authorizes read-only inspection and discussion, not repository
writes, report generation, remote access, or additional server commands.

## Local review sequence

The assistant should:

1. resolve the exact local handoff path and confirm Git ignores it;
2. list files, sizes, and unexpected entries without opening large artifacts;
3. verify `checksums.sha256` and hashes in `run_manifest.json`;
4. reconcile run/config/data/model/code identities with the approved plan;
5. reconcile expected, attempted, completed, failed, duplicate, and missing
   counts;
6. recompute compact summary invariants where possible;
7. inspect the pre-declared diagnostic sample and bounded log;
8. distinguish empirical results from pipeline or fake-backend checks;
9. report anomalies, insufficient evidence, and the weakest justified
   interpretation; and
10. state whether an additional small slice is genuinely required.

If compact evidence is insufficient, request the smallest decisive addition,
such as a fixed-seed stratified sample, selected tensor statistics, a bounded
layer/component slice, or a derived aggregate. Do not request or copy the entire
activation store by default.

## Promotion to tracked results

After read-only discussion, the assistant must present a documentation action
preview before creating `results/<run-id>/`. The preview names the exact compact
files to promote, report paths, validation, redaction, and Git behavior.

Only after explicit approval may the assistant create:

- `results/<run-id>/manifest.json`: sanitized compact provenance;
- approved summary JSON/CSV or small figure data;
- `REPORT.md` and `REPORT.zh-CN.md`: synchronized result, uncertainty,
  limitations, alternative explanations, and research handoff; and
- checksums for tracked compact evidence where useful.

The report must point to large artifacts through stable IDs and checksums, not
pretend that uncommitted server paths are durable public evidence.

## Retention and reproducibility

- The server remains the authoritative location for large artifacts until the
  project's retention policy moves them to approved durable storage.
- `artifacts/server-results/` is a disposable local review cache and not a
  substitute for server backup.
- Never delete, overwrite, or reorganize server artifacts during result review.
- Any rerun with changed code, configuration, data, model, or prompt receives a
  new run ID unless the approved protocol explicitly defines a compatible
  resume.
- A result cannot be called reproducible merely because the compact bundle was
  copied successfully; provenance, determinism expectations, and replay checks
  remain separate evidence.
