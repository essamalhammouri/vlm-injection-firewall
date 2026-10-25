# Data card

## Clean images

| Source | Use | Licence note |
|---|---|---|
| COCO val2017 | main clean photos | Images come from Flickr under mixed licences; check before redistributing |
| SROIE / FUNSD (optional, later) | receipts and forms, a more realistic target | check each dataset's terms |

Policy: **do not commit or redistribute images.** The repo contains scripts that download and
regenerate everything.

## Attack sentences

| Source | Size | Licence | Role |
|---|---|---|---|
| Lakera `gandalf_ignore_instructions` | 1,000 real player attacks | MIT | train / val / test |
| `deepset/prompt-injections` | under 1,000 rows, injections and benign | Apache-2.0 | train / val / test; benign rows become harmless visible text |
| Tensor Trust | 100,000+ human attacks | verify at tensortrust.ai/paper before use | **held out: test split only** |
| HackAPrompt (optional) | 100K+ submissions, uncurated, gated | MIT, access conditions apply | only if more volume is needed |

Filtering rules (`sentences.filter_sentences`): English, 15-150 characters, case-insensitive
deduplication, offensive content removed, 50 random rows reviewed by eye.

Every generated image keeps `sentence_source` in its record so results can be reported per source.

## Generated dataset

| Property | Value |
|---|---|
| Format | PNG images, YOLO `.txt` labels, one JSON record per image |
| Splits | 70 / 15 / 15 by source photo |
| Class balance | 60% attacked, 30% clean, 10% harmless visible text (config) |
| Labels | exact by construction (text placed by our own script) |

## Known limitations

- Attacks are synthetic renderings, not captured from real incidents. No public dataset has
  boxed hidden text, so this is the standard approach. Mitigation: external benchmark in Week 9.
- Attack sentences were written for chatbots. Some lose meaning when read from an image.
- COCO photos are everyday scenes; documents and screenshots are a different domain.
