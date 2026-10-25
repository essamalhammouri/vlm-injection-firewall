"""Load and validate the experiment configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path = "configs/default.yaml") -> dict[str, Any]:
    """Read a YAML config and check the values that would silently ruin results if wrong."""
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    ratios = cfg["splits"]
    if abs(sum(ratios.values()) - 1.0) > 1e-9:
        raise ValueError(f"split ratios must sum to 1, got {sum(ratios.values())}")
    if set(ratios) != {"train", "val", "test"}:
        raise ValueError("splits must be exactly: train, val, test")

    attacks = cfg["attacks"]
    if attacks["negative_fraction"] + attacks["harmless_text_fraction"] >= 1:
        raise ValueError("negative + harmless-text fractions must leave room for attacks")
    return cfg
