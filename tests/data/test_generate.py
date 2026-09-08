from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from reasoning_role.data.generate import generate_dataset, load_config
from reasoning_role.data.io import sha256_file
from reasoning_role.tasks.registry import get_task_family
from reasoning_role.tasks.schema import CanonicalInstance


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SMOKE_CONFIG = REPOSITORY_ROOT / "configs/data/task_calibration_smoke.yaml"


def output_files(path: Path) -> dict[str, bytes]:
    return {
        item.relative_to(path).as_posix(): item.read_bytes()
        for item in path.rglob("*")
        if item.is_file()
    }


class DatasetGenerationTest(unittest.TestCase):
    def test_deterministic_generation_and_manifest(self) -> None:
        config = load_config(SMOKE_CONFIG)
        revision = {"commit": "test-revision", "dirty": False}
        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / "first"
            second = Path(temp_dir) / "second"
            first_manifest = generate_dataset(
                config, first, code_revision=revision
            )
            second_manifest = generate_dataset(
                config, second, code_revision=revision
            )
            self.assertEqual(output_files(first), output_files(second))
            self.assertEqual(first_manifest, second_manifest)
            self.assertEqual(first_manifest["validation"]["records"], 80)
            self.assertEqual(
                first_manifest["validation"]["targets_verified"], 80
            )
            self.assertTrue(
                first_manifest["validation"]["overlap_audit"]["passed"]
            )
            for split_name in config["splits"]:
                counts = first_manifest["counts"][split_name]["by_family"]
                self.assertEqual(counts["function_composition"], 8)
                self.assertEqual(counts["relational_path"], 8)
                cells = first_manifest["counts"][split_name]["joint_factor_cells"]
                self.assertTrue(
                    all(
                        count == 1
                        for family_cells in cells.values()
                        for count in family_cells.values()
                    )
                )

    def test_records_revalidate_and_targets_recompute(self) -> None:
        config = load_config(SMOKE_CONFIG)
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "output"
            generate_dataset(
                config,
                output,
                code_revision={"commit": "test-revision", "dirty": False},
            )
            semantic_ids: set[str] = set()
            record_count = 0
            for split_path in sorted(output.glob("*.jsonl")):
                with split_path.open("r", encoding="utf-8") as handle:
                    for line in handle:
                        record = CanonicalInstance.from_dict(json.loads(line))
                        record.validate()
                        family = get_task_family(record.family)
                        solved = family.solve(record.canonical_problem)
                        final_state = list(
                            record.task_side_trace[-1].output_state.values()
                        )[0]
                        self.assertEqual(solved, final_state)
                        semantic_id = record.group_keys["semantic_id"]
                        self.assertNotIn(semantic_id, semantic_ids)
                        semantic_ids.add(semantic_id)
                        record_count += 1
            self.assertEqual(record_count, 80)

    def test_manifest_file_hashes_match(self) -> None:
        config = load_config(SMOKE_CONFIG)
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "output"
            manifest = generate_dataset(
                config,
                output,
                code_revision={"commit": "test-revision", "dirty": False},
            )
            for filename, entry in manifest["files"].items():
                self.assertEqual(sha256_file(output / filename), entry["sha256"])

    def test_existing_output_is_not_overwritten(self) -> None:
        config = load_config(SMOKE_CONFIG)
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(FileExistsError):
                generate_dataset(config, temp_dir)


if __name__ == "__main__":
    unittest.main()
