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
import textwrap

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from vlmfw.schemas import Box


def add_text(
    img: Image.Image,
    text: str,
    *,
    size: int = 28,
    alpha: int = 255,
    angle: float = 0.0,
    color: tuple[int, int, int] | None = (0, 0, 0),
    color_offset: int = 0,
    font_path: str | None = None,
    rng: random.Random | None = None,
) -> tuple[Image.Image, Box | None]:
    """Render `text` onto `img` at a random position.

    color=None means: use the typical color of the photo under the text,
    shifted by color_offset (the 'blended' trick).
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

    # 1. break long sentences into lines that fit the photo, write them on a small sheet
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    char_width = max(1.0, probe.textlength(text, font=font) / max(1, len(text)))
    per_line = max(8, int(0.8 * img.width / char_width))
    wrapped = "\n".join(textwrap.wrap(text, width=per_line))
    left, top, right, bottom = probe.multiline_textbbox((0, 0), wrapped, font=font)
    sheet = Image.new("RGBA", (right, bottom), (0, 0, 0, 0))
    draw_color = (0, 0, 0) if color is None else color
    ImageDraw.Draw(sheet).multiline_text((0, 0), wrapped, font=font, fill=(*draw_color, alpha))

    # 2. tilt it, then cut away the empty corners
    sheet = sheet.rotate(angle, expand=True)
    ink = sheet.getbbox()
    if ink is None:
        return img.convert("RGB"), None
    sheet = sheet.crop(ink)

    # 3. choose a random place where the whole sheet fits
    x = rng.randint(0, max(0, img.width - sheet.width))
    y = rng.randint(0, max(0, img.height - sheet.height))

    # 4. blended: every letter pixel takes the photo's own color, shifted by color_offset
    if color is None:
        region = img.convert("RGB").crop((x, y, x + sheet.width, y + sheet.height))
        shifted = np.clip(np.asarray(region).astype(int) + color_offset, 0, 255)
        solid = Image.fromarray(shifted.astype("uint8")).convert("RGBA")
        solid.putalpha(sheet.getchannel("A"))
        sheet = solid

    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    layer.paste(sheet, (x, y))

    box = layer.getbbox()
    out = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    return out, box


DEFAULTS = {"size": 24, "alpha": 255, "angle": 0.0}


def sample_params(tricks: list[str], ranges: dict, rng: random.Random) -> dict:
    """Turn the chosen tricks into keyword arguments for add_text."""
    params = dict(DEFAULTS)
    params["color"] = tuple(rng.randint(0, 255) for _ in range(3))
    for trick in tricks:
        for name, (low, high) in ranges.get(trick, {}).items():
            if name in ("size", "alpha"):
                params[name] = rng.randint(low, high)
            elif name == "angle":
                params[name] = rng.uniform(low, high)
    return params


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
