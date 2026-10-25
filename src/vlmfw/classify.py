"""Stage 2: name the trick(s) with a multi-label classifier (Week 5-6)."""

from __future__ import annotations

from PIL import Image


def train_classifier(cfg: dict, backbone: str = "resnet50") -> None:
    """Fine-tune a pretrained backbone (resnet50 | convnext_tiny | vit_b_16), BCE loss."""
    raise NotImplementedError("Week 5: implement train_classifier")


def classify(image: Image.Image) -> dict[str, float]:
    """Return a probability per trick in schemas.TRICKS."""
    raise NotImplementedError("Week 5: implement classify")
