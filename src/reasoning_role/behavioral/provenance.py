"""Dataset, source-tree, software, and hardware provenance."""

from __future__ import annotations

import hashlib
from importlib import metadata
import json
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

from reasoning_role.data.io import detect_code_revision, sha256_file
from reasoning_role.tasks.schema import CanonicalInstance, canonical_json


def load_dataset_records(
    dataset_config: Mapping[str, Any]
) -> tuple[list[CanonicalInstance], dict[str, Any]]:
    manifest_path = Path(str(dataset_config["manifest"]))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    selected_splits = dataset_config.get("splits")
    split_filter = set(str(value) for value in selected_splits) if selected_splits else None
    selected_families = dataset_config.get("families")
    family_filter = (
        set(str(value) for value in selected_families)
        if selected_families
        else None
    )

    records: list[CanonicalInstance] = []
    selected_files: dict[str, str] = {}
    for filename, entry in sorted(manifest["files"].items()):
        if not filename.endswith(".jsonl"):
            continue
        split_name = filename.removesuffix(".jsonl")
        if split_filter is not None and split_name not in split_filter:
            continue
        path = manifest_path.parent / filename
        actual_hash = sha256_file(path)
        expected_hash = str(entry["sha256"])
        if actual_hash != expected_hash:
            raise ValueError(f"dataset hash mismatch for {filename!r}")
        selected_files[filename] = actual_hash
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                record = CanonicalInstance.from_dict(json.loads(line))
                record.validate()
                if record.split != split_name:
                    raise ValueError(
                        f"record split mismatch in {filename}:{line_number}"
                    )
                if family_filter is None or record.family in family_filter:
                    records.append(record)

    if not selected_files:
        raise ValueError("dataset selection contains no JSONL split files")
    if not records:
        raise ValueError("dataset selection contains no records")
    instance_ids = [record.instance_id for record in records]
    if len(instance_ids) != len(set(instance_ids)):
        raise ValueError("dataset selection contains duplicate instance IDs")
    records.sort(key=lambda item: (item.split, item.instance_id))
    selected_identity = {
        "manifest_sha256": sha256_file(manifest_path),
        "source_config_sha256": manifest.get("config_sha256"),
        "source_code_revision": manifest.get("code_revision"),
        "selected_files": selected_files,
        "split_filter": sorted(split_filter) if split_filter is not None else None,
        "family_filter": sorted(family_filter) if family_filter is not None else None,
        "record_count": len(records),
    }
    selected_identity["selection_sha256"] = hashlib.sha256(
        canonical_json(selected_identity).encode("utf-8")
    ).hexdigest()
    return records, selected_identity


def code_provenance(
    repository_root: Path,
    override: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    revision = dict(override) if override is not None else detect_code_revision()
    source_files = sorted(
        [*repository_root.glob("src/**/*.py"), *repository_root.glob("scripts/*.py")]
    )
    digest = hashlib.sha256()
    for path in source_files:
        digest.update(path.relative_to(repository_root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return {**revision, "source_tree_sha256": digest.hexdigest()}


def environment_provenance(packages: Sequence[str]) -> dict[str, Any]:
    versions: dict[str, str | None] = {}
    for package in packages:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = None
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "system": platform.system(),
        "machine": platform.machine(),
        "packages": versions,
    }
