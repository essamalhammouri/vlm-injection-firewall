"""Build the full attacked dataset from clean photos + sentences (Week 2)."""

from __future__ import annotations

from typing import Any


def build_dataset(cfg: dict[str, Any]) -> None:
    """Generate images, YOLO label files and per-image JSON records.

    Output layout (data/processed/attacks/):
        images/{train,val,test}/<id>.png
        labels/{train,val,test}/<id>.txt      # YOLO: class xc yc w h (normalised)
        records/{train,val,test}/<id>.json    # schemas.AttackRecord

    Rules:
      * read the split table first; never re-split
      * sentences from cfg['sentences']['held_out_sources'] go to the test split only
      * respect negative_fraction and harmless_text_fraction
      * always save PNG, never JPEG (compression erases faint text)
    """
    raise NotImplementedError("Week 2: implement build_dataset")
