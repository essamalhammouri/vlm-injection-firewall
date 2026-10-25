# Decisions log

One entry per decision that changes results. Newest at the bottom. Status: decided / open.

## D1: Attack text rendered on a transparent layer (decided, 2026-10-25)
Gives exact boxes for free and keeps them correct after rotation. Alternative (drawing on the
photo and computing boxes by hand) is error-prone.

## D2: Split by source photo, before generating attacks (decided, 2026-10-25)
Prevents the same photo appearing in train and test with different attack text.

## D3: PNG only (decided, 2026-10-25)
JPEG compression erases faint text, which would silently change what the detector sees.

## D4: Hold out one sentence source for the test split (decided, 2026-10-25)
Tensor Trust sentences appear only in test. Measures generalisation to unseen attacker wording.

## D5: Attack sentences come from public datasets (decided, 2026-10-25)
Gandalf and deepset first, Tensor Trust later. English only, 15-150 characters. More credible than
hand-written sentences. Non-English attacks are out of scope for now.

## D6: Final test on an external benchmark (decided, 2026-10-25)
CyberSecEval 3 visual prompt injection, never trained on. Shows the firewall works on attacks
someone else made.

## D7: How to judge that an attack succeeded (OPEN, decide in Week 2)
Public sentences have no built-in success check. Options:
- **Canary token:** append "... and include the word <canary> in your answer", then string-match.
  Objective and cheap, but it slightly changes the original sentence.
- **Judge model:** a second model decides whether the answer followed the hidden text.
  Works with unmodified sentences, but adds a model that can be wrong.
- **Both:** canary for the main number, judge on a sample to check they agree.
Leaning towards "both". Decide after the 20-image VLM smoke test.

## D8: Package layout with stubs and contract tests (decided, 2026-10-25)
Core modules are written by the author to learn from them. Contract tests (xfail until
implemented) define the expected behaviour in advance.
