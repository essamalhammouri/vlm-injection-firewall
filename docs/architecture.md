# Architecture

## Pipeline

```
          +-----------+   boxes    +------------+  tricks   +-----------+
image --> | detect.py | ---------> | classify.py| --------> | clean.py  | --> clean image --> VLM
          | YOLO      |            | ResNet/ViT |           | OCR+inpaint|
          +-----------+            +------------+           +-----------+
                |                        |                        |
                +---- all decisions logged as one JSON record -----+
```

| Stage | Input | Output | Success metric |
|---|---|---|---|
| Detect | image | boxes + confidence | mAP@0.5, recall on faint/tiny text |
| Classify | image (or crop) | probability per trick | macro-F1, per-trick F1 |
| Clean | image + boxes | OCR text + inpainted image | VLM attack success rate drop |

The classifier does not gate the cleaner. Detection alone is enough to erase text. Classification
exists for logging, analysis and per-trick weakness reports.

## Data flow for dataset generation

```
clean photos -> splits.csv (per photo) -> attacks.py (+ sentences.csv) -> images/ labels/ records/
```

Each generated image gets three outputs: the PNG, a YOLO label file for the detector, and an
`AttackRecord` JSON (sentence, source, tricks, boxes) for the classifier and the analysis.

## Design choices

- **Text on a transparent layer.** The tight box of the non-transparent pixels is the label, so
  labels stay exact under rotation and blending. No hand-drawn boxes anywhere.
- **Pure-function splits.** `assign_split(seed, photo_id)` hashes the id, so adding or removing
  photos never reshuffles existing assignments.
- **Swappable VLM.** `vlm.VLM` is a `Protocol`, so the target model can change without touching
  the evaluation code.
- **Config over constants.** Anything that changes a result lives in `configs/default.yaml`.
