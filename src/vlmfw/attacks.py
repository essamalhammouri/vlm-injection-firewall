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

from PIL import Image, ImageDraw, ImageFont

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
    rng = rng or random.Random()
    if font_path is None:
        font = ImageFont.load_default(size=size)
    else:
        font = ImageFont.truetype(font_path, size)

    # 1. write the text on a small see-through sheet, just big enough for it
    left, top, right, bottom = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox(
        (0, 0), text, font=font
    )
    sheet = Image.new("RGBA", (right, bottom), (0, 0, 0, 0))
    ImageDraw.Draw(sheet).text((0, 0), text, font=font, fill=(*color, alpha))

    # 2. tilt it, then cut away the empty corners
    sheet = sheet.rotate(angle, expand=True)
    ink = sheet.getbbox()
    if ink is None:
        return img.convert("RGB"), None
    sheet = sheet.crop(ink)

    # 3. choose a random place where the whole sheet fits, and paste it
    x = rng.randint(0, max(0, img.width - sheet.width))
    y = rng.randint(0, max(0, img.height - sheet.height))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    layer.paste(sheet, (x, y))

    box = layer.getbbox()
    out = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    return out, box


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
