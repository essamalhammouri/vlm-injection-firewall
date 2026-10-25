from pathlib import Path

import pytest
import yaml

from vlmfw.config import load_config
from vlmfw.evaluate import attack_success_rate, bootstrap_ci

ROOT = Path(__file__).resolve().parents[1]


def test_default_config_loads():
    cfg = load_config(ROOT / "configs" / "default.yaml")
    assert cfg["seed"] == 1337
    assert abs(sum(cfg["splits"].values()) - 1.0) < 1e-9


def test_bad_split_ratios_rejected(tmp_path):
    cfg = yaml.safe_load((ROOT / "configs" / "default.yaml").read_text())
    cfg["splits"]["train"] = 0.9
    bad = tmp_path / "bad.yaml"
    bad.write_text(yaml.safe_dump(cfg))
    with pytest.raises(ValueError):
        load_config(bad)


def test_attack_success_rate():
    assert attack_success_rate([True, True, False, False]) == 0.5


def test_bootstrap_ci_brackets_the_mean_and_is_reproducible():
    values = [True] * 60 + [False] * 40
    low, high = bootstrap_ci(values, seed=1)
    assert low < 0.6 < high
    assert (low, high) == bootstrap_ci(values, seed=1)


def test_bootstrap_ci_is_narrower_with_more_data():
    small = bootstrap_ci([True] * 6 + [False] * 4, seed=1)
    large = bootstrap_ci([True] * 600 + [False] * 400, seed=1)
    assert (large[1] - large[0]) < (small[1] - small[0])
