"""Data records shared by every stage, plus the YOLO label conversion."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field

Box = tuple[int, int, int, int]  # (x_min, y_min, x_max, y_max) in pixels

TRICKS = ("tiny", "faint", "rotated", "blended", "split")


@dataclass
class AttackRecord:
    """The answer key for one generated image. One JSON file per image."""

    image: str  # attacked PNG file name
    source_id: str  # the clean photo it was made from
    split: str  # train | val | test
    sentence: str | None  # None for clean images
    sentence_source: str | None  # gandalf | deepset | tensortrust | ...
    tricks: list[str] = field(default_factory=list)
    boxes: list[Box] = field(default_factory=list)  # one per text fragment
    harmless_text: bool = False  # visible, non-attack text present

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, text: str) -> AttackRecord:
        data = json.loads(text)
        data["boxes"] = [tuple(b) for b in data["boxes"]]
        return cls(**data)


def box_to_yolo(box: Box, width: int, height: int) -> tuple[float, float, float, float]:
    """Pixel box -> YOLO format (x_center, y_center, w, h), all divided by image size."""
    x0, y0, x1, y1 = box
    return (
        (x0 + x1) / 2 / width,
        (y0 + y1) / 2 / height,
        (x1 - x0) / width,
        (y1 - y0) / height,
    )
