from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

from reasoning_role.data.generate import load_config, validate_config
from reasoning_role.data.split import assert_disjoint_semantic_id


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SMOKE_CONFIG = REPOSITORY_ROOT / "configs/data/task_calibration_smoke.yaml"


class SplitConfigurationTest(unittest.TestCase):
    def test_smoke_and_larger_configs_are_valid(self) -> None:
        validate_config(load_config(SMOKE_CONFIG))
        validate_config(
            load_config(REPOSITORY_ROOT / "configs/data/task_calibration_v1.yaml")
        )

    def test_unbalanced_factor_request_fails(self) -> None:
        config = load_config(SMOKE_CONFIG)
        config["splits"]["train"]["count_per_family"] = 7
        with self.assertRaisesRegex(ValueError, "not divisible"):
            validate_config(config)

    def test_template_holdout_must_be_disjoint(self) -> None:
        config = deepcopy(load_config(SMOKE_CONFIG))
        config["splits"]["template_test"]["render"]["function_composition"][
            "templates"
        ] = ["compact"]
        with self.assertRaisesRegex(ValueError, "disjoint templates"):
            validate_config(config)

    def test_duplicate_semantics_across_splits_fail(self) -> None:
        assignments: dict[str, str] = {}
        assert_disjoint_semantic_id("semantic:1", "train", assignments)
        with self.assertRaisesRegex(ValueError, "both"):
            assert_disjoint_semantic_id("semantic:1", "iid_test", assignments)


if __name__ == "__main__":
    unittest.main()
