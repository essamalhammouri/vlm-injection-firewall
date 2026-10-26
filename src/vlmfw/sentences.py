"""Collect and filter real-world attack sentences from public datasets (Week 1)."""

from __future__ import annotations

import pandas as pd

# Columns of data/interim/sentences.csv
COLUMNS = ["sentence", "source", "label"]  # label: 1 = injection, 0 = benign


def filter_sentences(df: pd.DataFrame, min_chars: int, max_chars: int) -> pd.DataFrame:
    """Keep short, English, unique, non-offensive sentences that work as image text.

    Contract (enforced by tests/test_sentences.py):
      * length within [min_chars, max_chars] after stripping whitespace
      * exact duplicates removed (case-insensitive), keeping the first
      * the `source` and `label` columns are preserved
    Then skim ~50 random rows by eye before trusting the result.
    """
    out = df.copy()
    out["sentence"] = (
        out["sentence"]
        .str.replace(r"\\n", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    key = out["sentence"].str.lower()
    out = out[~key.duplicated()]
    out = out[out["sentence"].str.len().between(min_chars, max_chars)]
    return out
