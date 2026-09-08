from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from reasoning_role.behavioral.backends.fake import FakeBackend
from reasoning_role.behavioral.runner import load_evaluation_config, run_evaluation
from reasoning_role.data.io import sha256_file


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPOSITORY_ROOT / "configs/eval/behavioral_smoke_fake.yaml"
FIXED_REVISION = {"commit": "test-revision", "dirty": False}


def files(path: Path) -> dict[str, bytes]:
    return {
        item.name: item.read_bytes()
        for item in path.iterdir()
        if item.is_file()
    }


class InterruptingBackend(FakeBackend):
    def __init__(self, config: dict[str, object]) -> None:
        super().__init__(config)
        self.calls = 0

    def generate(self, requests):
        self.calls += 1
        if self.calls == 2:
            raise RuntimeError("intentional interruption")
        return super().generate(requests)


class ReorderedBackend(FakeBackend):
    def generate(self, requests):
        return list(reversed(super().generate(requests)))


class MissingBackend(FakeBackend):
    def generate(self, requests):
        return list(super().generate(requests))[:-1]


class DuplicateBackend(FakeBackend):
    def generate(self, requests):
        results = list(super().generate(requests))
        return [results[0], *results[:-1]]


class RunnerTest(unittest.TestCase):
    def test_complete_run_reconciles_and_hides_task_trace(self) -> None:
        config = load_evaluation_config(CONFIG_PATH)
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "run"
            manifest = run_evaluation(
                config, output, code_revision=FIXED_REVISION
            )
            self.assertEqual(manifest["attempted"], 80)
            self.assertEqual(manifest["completed"], 80)
            records = [
                json.loads(line)
                for line in (output / "records.jsonl").read_text().splitlines()
            ]
            self.assertEqual(len(records), 80)
            self.assertEqual(len({item["instance_id"] for item in records}), 80)
            self.assertTrue(
                all("task_side_trace" not in item["input_text"] for item in records)
            )
            summary = json.loads((output / "summary.json").read_text())
            self.assertEqual(summary["overall"]["attempted"], 80)
            self.assertEqual(summary["attempted_instance_ids"], 80)
            for filename, entry in manifest["files"].items():
                self.assertEqual(sha256_file(output / filename), entry["sha256"])
            csv_lines = (output / "summary.csv").read_text().splitlines()
            self.assertGreater(len(csv_lines), 2)
            self.assertIn("overall,all,80,", csv_lines[1])

    def test_fake_runs_are_byte_identical(self) -> None:
        config = load_evaluation_config(CONFIG_PATH)
        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / "first"
            second = Path(temp_dir) / "second"
            run_evaluation(config, first, code_revision=FIXED_REVISION)
            run_evaluation(config, second, code_revision=FIXED_REVISION)
            self.assertEqual(files(first), files(second))

    def test_interruption_and_resume(self) -> None:
        config = load_evaluation_config(CONFIG_PATH)
        backend_config = dict(config["backend"])
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "run"
            with self.assertRaisesRegex(RuntimeError, "intentional"):
                run_evaluation(
                    config,
                    output,
                    backend=InterruptingBackend(backend_config),
                    code_revision=FIXED_REVISION,
                )
            partial_count = len((output / "records.jsonl").read_text().splitlines())
            self.assertEqual(partial_count, config["generation"]["batch_size"])
            manifest = run_evaluation(
                config,
                output,
                resume=True,
                backend=FakeBackend(backend_config),
                code_revision=FIXED_REVISION,
            )
            self.assertEqual(manifest["completed"], 80)
            self.assertEqual(len((output / "records.jsonl").read_text().splitlines()), 80)

    def test_resume_rejects_config_change(self) -> None:
        config = load_evaluation_config(CONFIG_PATH)
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "run"
            run_evaluation(config, output, code_revision=FIXED_REVISION)
            changed = deepcopy(config)
            changed["seed"] += 1
            with self.assertRaisesRegex(ValueError, "provenance mismatch"):
                run_evaluation(
                    changed,
                    output,
                    resume=True,
                    code_revision=FIXED_REVISION,
                )

    def test_resume_rejects_duplicate_checkpoint_record(self) -> None:
        config = load_evaluation_config(CONFIG_PATH)
        backend_config = dict(config["backend"])
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "run"
            with self.assertRaises(RuntimeError):
                run_evaluation(
                    config,
                    output,
                    backend=InterruptingBackend(backend_config),
                    code_revision=FIXED_REVISION,
                )
            records_path = output / "records.jsonl"
            first_line = records_path.read_text().splitlines()[0]
            with records_path.open("a", encoding="utf-8") as handle:
                handle.write(first_line + "\n")
            with self.assertRaisesRegex(ValueError, "duplicate instance ID"):
                run_evaluation(
                    config,
                    output,
                    resume=True,
                    backend=FakeBackend(backend_config),
                    code_revision=FIXED_REVISION,
                )

    def test_reordered_backend_results_fail(self) -> None:
        config = load_evaluation_config(CONFIG_PATH)
        for backend_type in (ReorderedBackend, MissingBackend, DuplicateBackend):
            with self.subTest(backend_type=backend_type.__name__):
                with tempfile.TemporaryDirectory() as temp_dir:
                    with self.assertRaisesRegex(ValueError, "request order"):
                        run_evaluation(
                            config,
                            Path(temp_dir) / "run",
                            backend=backend_type(dict(config["backend"])),
                            code_revision=FIXED_REVISION,
                        )

    def test_existing_output_needs_resume(self) -> None:
        config = load_evaluation_config(CONFIG_PATH)
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(FileExistsError):
                run_evaluation(config, temp_dir, code_revision=FIXED_REVISION)


if __name__ == "__main__":
    unittest.main()
