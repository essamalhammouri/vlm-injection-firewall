# Threat model

## Scenario

A service lets users upload images (receipts, forms, screenshots, photos) and asks a VLM to
read or summarise them. The VLM's answer influences an action (approve a payment, file a
ticket, answer a customer). An attacker controls the content of an uploaded image.

## Attacker

| Aspect | Assumption |
|---|---|
| Goal | Make the VLM follow an instruction hidden in the image instead of the user's task |
| Access | Can only change image pixels. Cannot change the user's prompt or the model |
| Knowledge, basic attacker | Knows nothing about the firewall |
| Knowledge, adaptive attacker | Knows the firewall design and can query it (Weeks 8-9) |
| Constraint | The text must stay readable to the VLM, otherwise the attack is useless |

## Attack techniques in scope

`tiny`, `faint`, `rotated`, `blended`, `split` and combinations (see `schemas.TRICKS`).
Pixel-level adversarial noise (FGSM/PGD) is in scope only as an attack on **our detector**,
not as a way to inject instructions.

## Out of scope

- Instructions hidden in image metadata (EXIF) or file formats
- Steganography (information the VLM itself cannot see)
- Attacks on the VLM weights or training data
- Text-only prompt injection (handled by a separate project)
- Non-English attacks (the sentence filter keeps English only; see docs/decisions.md D5)

## Success criteria

An attack succeeds if the VLM follows the hidden instruction (criterion: docs/decisions.md D7).
A defence succeeds if it lowers attack success rate **without** flagging clean images or images
with harmless visible text more than the allowed false-positive rate (docs/evaluation_protocol.md).

## Ethics

- Images: public datasets only. Sentences: public datasets only.
- Models: run locally, no third-party service is attacked.
- The repository publishes generation code and results, not a ready-made dataset of images,
  because source image licences differ (docs/data_card.md).
