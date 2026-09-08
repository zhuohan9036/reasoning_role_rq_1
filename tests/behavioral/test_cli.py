from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPOSITORY_ROOT / "scripts/evaluate_behavior.py"
CONFIG = REPOSITORY_ROOT / "configs/eval/behavioral_smoke_fake.yaml"


class BehavioralCommandLineTest(unittest.TestCase):
    def test_help(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--resume", result.stdout)

    def test_fake_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "run"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--config",
                    str(CONFIG),
                    "--output",
                    str(output),
                ],
                cwd=REPOSITORY_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            status = json.loads(result.stdout)
            self.assertEqual(status["attempted"], 80)
            self.assertEqual(status["completed"], 80)
            self.assertTrue((output / "run_manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
