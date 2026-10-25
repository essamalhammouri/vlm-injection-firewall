"""Target vision-language model and the attack-success measurement (Week 2-3)."""

from __future__ import annotations

from typing import Protocol

from PIL import Image


class VLM(Protocol):
    """Anything that answers a question about an image. Keeps models swappable."""

    def ask(self, image: Image.Image, question: str) -> str: ...


def injection_followed(response: str, canary: str) -> bool:
    """True if the model obeyed the hidden instruction.

    OPEN DESIGN DECISION (docs/decisions.md, D7): public sentences have no built-in
    success check. Current proposal: append a canary instruction to the sentence
    ("... and include the word <canary> in your answer") and test for the canary.
    """
    raise NotImplementedError("Week 2: decide the success criterion, then implement")
