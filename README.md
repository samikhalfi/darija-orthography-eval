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

## Claim

Revised 2026-08-17 after the prior-art check in `notes/prior-art.md`. The first
version of this claim was that WER for Darija is unstable without a stated
orthographic convention. That is true and it is **not new**: Ali et al. stated it
in 2017 and proposed WERd to address it, and normalising before scoring is
standard practice in Arabic ASR. The narrower claim that survives is this one.

> The normalisation conventionally applied before computing WER for Arabic
> assumes Arabic script. It folds Alef, Yaa and Taa variants and handles
> diacritics. Moroccan Darija is substantially written in Latin script with
> numerals (3, 7, 9, 2), which is a transliteration rather than a spelling
> variant, and no amount of Alef folding reaches it.

So: how much error does that assumption leave on the table for Darija, and does
a cross-script canonicalisation layer recover it? The same question applies to
lexical retrieval, where it costs recall rather than comparability.

**What would falsify this:** if the cross-script spread turns out to be small
relative to the differences between the systems being compared, or if existing
Arabic-script normalisation already absorbs most of it, the claim is
uninteresting. That outcome gets published here in the same font as any other.

## Questions

1. After the standard Arabic-script normalisation has already been applied, how
   much does WER still move for the same hypothesis scored against an
   Arabic-script reference versus a Latin-script-with-numerals one?
2. Does a cross-script canonicalisation layer recover that gap, and how much of
   it?
3. Does the same layer change lexical retrieval failure@k on Darija queries, or
   is the effect specific to transcription scoring?

## Prior art

Done, before any code. See `notes/prior-art.md`. Short version: the original
framing was already covered by the literature, the check caught it in week 1
rather than at the write-up, and the claim above is the narrower one that
survived. Work this repository extends rather than competes with:

- Ali, Nakov, Bell and Renals (2017), *WERd*, arXiv:1709.07484
- SN-WER, script-normalised WER for multi-script Indic ASR, arXiv:2606.02548

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
