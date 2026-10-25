"""Attack our own defence (Week 8-9). See docs/evaluation_protocol.md for the rules."""

from __future__ import annotations

from PIL import Image


def pgd_attack(image: Image.Image, epsilon: float, steps: int) -> Image.Image:
    """White-box PGD against the detector/classifier. FGSM is the steps=1 special case."""
    raise NotImplementedError("Week 8: implement pgd_attack")


def adaptive_attack(image: Image.Image, sentence: str) -> Image.Image:
    """Hide the text so the detector misses it while the VLM can still read it.

    Success needs BOTH: detector evades AND the VLM still follows the instruction.
    """
    raise NotImplementedError("Week 8: implement adaptive_attack")
