from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import unittest

from reasoning_role.behavioral.provenance import load_dataset_records


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FIXTURE = REPOSITORY_ROOT / "tests/fixtures/task_calibration_smoke"


class ProvenanceTest(unittest.TestCase):
    def test_fixture_selection_and_hash(self) -> None:
        records, identity = load_dataset_records(
            {
                "manifest": str(FIXTURE / "manifest.json"),
                "splits": ["train"],
                "families": ["function_composition"],
            }
        )
        self.assertEqual(len(records), 8)
        self.assertEqual({item.split for item in records}, {"train"})
        self.assertEqual({item.family for item in records}, {"function_composition"})
        self.assertEqual(len(identity["selection_sha256"]), 64)

    def test_tampered_dataset_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            copied = Path(temp_dir) / "fixture"
            shutil.copytree(FIXTURE, copied)
            train = copied / "train.jsonl"
            train.write_text(train.read_text() + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                load_dataset_records({"manifest": str(copied / "manifest.json")})


if __name__ == "__main__":
    unittest.main()
