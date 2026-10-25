"""Stage 3: read the hidden text (OCR) and erase it (inpainting) (Week 7)."""

from __future__ import annotations

from PIL import Image

from vlmfw.schemas import Box


def read_text(image: Image.Image, box: Box) -> str:
    """OCR the region inside `box`. Used for logging what the attacker tried to say."""
    raise NotImplementedError("Week 7: implement read_text")


def erase(image: Image.Image, boxes: list[Box]) -> Image.Image:
    """Inpaint the boxes so the area looks natural again (OpenCV inpainting)."""
    raise NotImplementedError("Week 7: implement erase")
