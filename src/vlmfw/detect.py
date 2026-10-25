"""Stage 1: locate hidden text with an object detector (Week 3-4)."""

from __future__ import annotations

from PIL import Image

from vlmfw.schemas import Box


def train_detector(cfg: dict) -> None:
    """Fine-tune a YOLO model on data/processed/attacks. Metric: mAP@0.5 on the val split."""
    raise NotImplementedError("Week 3: implement train_detector")


def detect(image: Image.Image) -> list[tuple[Box, float]]:
    """Return (box, confidence) for each suspected hidden-text region."""
    raise NotImplementedError("Week 4: implement detect")
