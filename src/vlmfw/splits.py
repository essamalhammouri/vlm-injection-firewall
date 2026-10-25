"""Leak-free train/val/test splitting.

Rule: split by SOURCE PHOTO, before any attack is generated. If two attacked
versions of the same photo land in different splits, test results are inflated.

The split is a pure function of (seed, photo id), so it never changes when files
are added, removed or processed in a different order.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def assign_split(source_id: str, ratios: dict[str, float], seed: int) -> str:
    """Deterministically map a photo id to 'train', 'val' or 'test'."""
    digest = hashlib.sha256(f"{seed}:{source_id}".encode()).digest()
    u = int.from_bytes(digest[:8], "big") / 2**64  # uniform in [0, 1)
    cumulative = 0.0
    for name, share in ratios.items():
        cumulative += share
        if u < cumulative:
            return name
    return list(ratios)[-1]  # guards against float rounding at the very end


def make_split_table(image_dir: str | Path, ratios: dict[str, float], seed: int) -> pd.DataFrame:
    """List every photo in image_dir with its split. One row per source photo."""
    files = sorted(p for p in Path(image_dir).iterdir() if p.suffix.lower() in IMAGE_SUFFIXES)
    rows = [
        {"source_id": p.stem, "filename": p.name, "split": assign_split(p.stem, ratios, seed)}
        for p in files
    ]
    return pd.DataFrame(rows, columns=["source_id", "filename", "split"])
