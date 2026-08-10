# Darija orthography and what it does to evaluation

Moroccan Darija has no standardised orthography. The same word is written in
Arabic script, in Latin script with numerals (3, 7, 9, 2), and in forms shaped
by French spelling habits, often inside the same sentence as French and Modern
Standard Arabic.

Every metric that compares two strings assumes you already know when two
strings are the same word. For Darija that assumption does not hold, and
nothing downstream of it is safe:

- **Speech.** Word error rate is a string comparison. If the reference
  transcript could reasonably have been spelled three ways, WER is not one
  number, it is a range, and reporting a single value hides which convention
  the score depended on.
- **Retrieval and evidence grounding.** Matching a claim against a source is a
  string comparison too, before it is anything else. Lexical retrieval fails on
  spelling variants that a speaker reads as identical.

Same problem, two hats. This repository measures it and then tries to fix it.

## Questions

1. How much does WER move for the same audio and the same transcription, scored
   against different but equally valid orthographic references?
2. Does a canonicalisation layer shrink that spread, and by how much?
3. Does the same layer change retrieval failure rate on Darija queries?

## Plan

Written 2026-08-10, before any code, so the dates mean something.

| Week | Dates | Deliverable |
|---|---|---|
| 1 | 11 to 17 Aug | Evaluation set built. Zero-shot transcription with open multilingual models. WER and CER scored against 2 to 3 orthographic references. The spread published. |
| 2 | 18 to 24 Aug | Canonicalisation layer: Arabic script, Arabizi with numerals, French insertions, elongation, diacritics. Re-score week 1 through it and report the change. |
| 3 | 25 to 31 Aug | Graded Darija query set. Retrieval with and without canonicalisation. Failure@k with 95% confidence intervals. |
| 4 | 1 to 7 Sep | Write-up. Findings, limitations, and the results that do not support the hypothesis. |
| buffer | 8 to 19 Sep | Slack. Nothing is scheduled here on purpose. |

## Scope, and what is deliberately not here

Parameter-efficient adaptation (LoRA, adapter fusion) is **out of scope for this
repository**. It is the obvious next step and it is not attempted here, because
an adaptation result I cannot fully explain is worth less than an evaluation
result I can. The foundations work that would make it defensible is tracked
separately at [ml-foundations](https://github.com/samikhalfi/ml-foundations).

The evaluation set is small by design. The week 1 finding is about **variance in
the metric**, not about model quality, and metric variance does not need a large
corpus to demonstrate. Sample size and its consequences are stated with the
results rather than glossed.

## Method notes

- Every number is reported with the reference convention it was scored against.
  A WER with no stated orthography is not a result.
- Negative and inconvenient results are published. If canonicalisation does not
  help retrieval, that goes in `FINDINGS.md` in the same font as everything else.
- Confidence intervals accompany comparisons, including the ones that overlap.

## Layout

```
data/         evaluation set, references per orthographic convention
eval/         scoring: WER, CER, retrieval failure@k
normaliser/   the canonicalisation layer
results/      raw run outputs, one directory per run
notes/        reading notes and decisions, dated
FINDINGS.md   what came out, updated as it comes out
```

## Author

Sami Khalfi. Native Darija speaker, which is why the multiple reference
transcriptions in `data/` are hand-written rather than generated.
