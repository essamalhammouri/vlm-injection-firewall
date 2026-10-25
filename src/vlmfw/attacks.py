"""Attack generator (Week 1-2). YOU write this module: it is the core of the dataset.

Design (see docs/architecture.md):
  - Draw the text on a separate transparent layer, never directly on the photo.
  - The tight bounding box of the non-transparent pixels IS the label. It stays
    correct after rotation, so no box is ever computed by hand.
  - Everything random comes from a `random.Random` passed in, so a dataset can
    be regenerated exactly from the config seed.
"""

from __future__ import annotations

import random

from PIL import Image

from vlmfw.schemas import Box


def add_text(
    img: Image.Image,
    text: str,
    *,
    size: int = 28,
    alpha: int = 255,
    angle: float = 0.0,
    color: tuple[int, int, int] = (0, 0, 0),
    font_path: str | None = None,
    rng: random.Random | None = None,
) -> tuple[Image.Image, Box | None]:
    """Render `text` onto `img` at a random position.

    Returns the attacked RGB image and the tight pixel box around the text,
    or None if nothing visible was drawn.
    Contract (enforced by tests/test_attacks.py):
      * output has the same size as the input
      * every pixel that differs from the input lies inside the returned box
      * the box lies fully inside the image
    """
    raise NotImplementedError("Week 1: implement add_text")


def render_attack(
    img: Image.Image,
    sentence: str,
    tricks: list[str],
    rng: random.Random,
) -> tuple[Image.Image, list[Box]]:
    """Apply one or more tricks (see schemas.TRICKS) and return all text boxes.

    'split' produces several boxes; every other trick produces one.
    """
    raise NotImplementedError("Week 2: implement render_attack")
