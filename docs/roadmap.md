# Roadmap

Roughly 10 hours per week, starting 2026-10-25. Must-haves: Weeks 1-7.

| Week | Dates | Goal | Done when |
|---|---|---|---|
| 1 | Oct 25 - Nov 1 | Setup, sentences, first trick | 20 attacked images, boxes verified by eye; `filter_sentences` and `add_text` tests pass |
| 2 | Nov 2 - 8 | All tricks, VLM smoke test, full dataset | Dataset built; VLM obeys some attacks; D7 decided |
| 3 | Nov 9 - 15 | VLM baseline, start YOLO | One ASR number with CI |
| 4 | Nov 16 - 22 | Finish detector | mAP and a list of failures |
| 5 | Nov 23 - 29 | ResNet multi-label classifier | Per-trick F1 |
| 6 | Nov 30 - Dec 6 | ViT comparison, Grad-CAM | ResNet vs ViT table, heatmaps |
| 7 | Dec 7 - 13 | OCR + inpainting, re-test VLM | **Before/after ASR (headline result)** |
| 8 | Dec 14 - 20 | FGSM/PGD and adaptive attack | Detection rate under attack |
| 9 | Dec 21 - 27 | Adversarial training, external benchmark | Hardened model, external ASR |
| 10 | Dec 28 - Jan 3 | FastAPI + Docker, README, demo video | A stranger can run it |

## Check-ins

1. End of Week 2: if the VLM ignores every attack, strengthen the attacks or change the VLM first.
2. End of Week 4: a low mAP is usually a data problem. Read the failures before changing models.
3. End of Week 7: the before/after ASR number must exist. Start applying with the project on the CV.

## Working rules

- Commit after every finished step. One small commit beats one big lost afternoon.
- Move the xfail marker out of a test file when you implement the function it covers.
- Look at generated images by eye before trusting any metric.
