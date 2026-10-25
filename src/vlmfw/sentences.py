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
    raise NotImplementedError("Week 1: implement filter_sentences")
