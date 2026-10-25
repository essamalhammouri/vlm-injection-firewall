"""Metrics. Every reported number must come with a confidence interval."""

from __future__ import annotations

import numpy as np


def attack_success_rate(followed: list[bool]) -> float:
    """Fraction of attacked images where the VLM obeyed the hidden instruction."""
    if not followed:
        raise ValueError("no results to average")
    return float(np.mean(followed))


def bootstrap_ci(
    values: list[float] | list[bool],
    n_boot: int = 2000,
    alpha: float = 0.05,
    seed: int = 1337,
) -> tuple[float, float]:
    """Percentile bootstrap confidence interval for the mean."""
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        raise ValueError("no values")
    rng = np.random.default_rng(seed)
    means = rng.choice(arr, size=(n_boot, arr.size), replace=True).mean(axis=1)
    low, high = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return float(low), float(high)
