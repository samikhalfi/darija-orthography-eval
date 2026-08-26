# Design decisions

Every non-obvious choice in `eval/score.py` and `normaliser/canon.py`, why it
was made, and what it costs. Written because a decision without a stated cost
is not a decision, it is a default.

Read this before discussing the repository with anyone. The questions below are
the ones the code invites.

## Scoring

**Levenshtein by hand, not jiwer or editdistance.**
The metric is the object of study here. A library hides its denominator and its
normalisation behind a default, and the whole claim concerns exactly those. Two
rows instead of the full DP table, because nothing here recovers the alignment.
*Cost:* none worth naming. *Upgrade:* if alignment is ever needed for error
analysis, restore the full grid and backtrack.

**WER divides by the reference length.**
Not the hypothesis, not the max of the two. That is what makes WER a rate of
error against the truth rather than a similarity. Direct consequence: WER can
exceed 1.0, and `assert wer("safi", "safi safi safi safi") == 3.0` pins that
down so it cannot be mistaken for a bug later.

**CER is carried alongside WER, not as decoration.**
Across scripts WER saturates. Every word is wrong, the score pins at 1.0, and it
stops distinguishing a near-miss transliteration from unrelated text. CER still
moves, because two spellings of a word share characters where two scripts share
no words. In the worked example WER calls the Arabic and French references
equally wrong (1.0 and 0.5) while CER separates them cleanly (1.44 and 0.14).
Any result reported here carries both.

**Empty reference returns inf rather than dividing by zero.**
An empty reference has no defined rate. Silently returning 0.0 would let a
broken data row read as a perfect score.

## Canonicalisation

**The canonical form is neither script. It is a consonant skeleton.**
The central decision. Arabic script omits short vowels; Arabizi writes them. The
only form both can reach is the one without them, which is also how the Arabic
abjad already works. Mapping into Arabic script instead would require guessing
vowels from Latin, and mapping into Latin would require inventing them from
Arabic.
*Cost:* minimal pairs distinguished only by short vowels collapse together. Not
yet quantified. *Upgrade path:* keep the skeleton as the match key and carry the
vowelled surface form alongside for tie-breaking.

**Emphatics merged with their plain counterparts** (ص→s, ض→d, ط→t, ظ→d).
Arabizi does not distinguish them at all. Keeping them apart would guarantee a
mismatch on every emphatic word, which would measure the transliteration
convention rather than the orthography.
*Cost:* a real phonemic distinction in Arabic is destroyed. Acceptable because
the target is cross-script matching, not phonological analysis.

**Degemination: runs of a repeated symbol collapse to one.**
Arabic script usually omits shadda; Arabizi doubles the letter. A doubled
consonant is therefore a writing habit rather than a signal about the word.
*Cost:* phonemic gemination is lost. This is the decision I would challenge
first, since gemination is contrastive in Arabic.

**و and ي stay as consonants (w, y) rather than being dropped as long vowels.**
They are genuinely both, and the script does not say which. Dropping them would
erase real consonants; keeping them leaves a spurious symbol wherever they are
vocalic.
*Cost:* unquantified, and it should be measured. This is the largest known
source of residual mismatch.

**ش maps to `c`, not `s` or `sh`.**
It has to stay distinct from س, and a single symbol keeps the skeleton
one-symbol-per-phoneme so edit distance over it stays interpretable.

**Longest-match left-to-right scan, digraphs before single letters.**
Otherwise "sh" is read as s followed by h. Arabic characters are single-key so
the same scanner covers both scripts without a script-detection step, which
avoids having to classify mixed-script input at all.

## Known unrecoverable, and why they are not bugs

Asserted in `canon.py` so they cannot quietly disappear. These are cases where
the source spelling destroyed information before the normaliser ever saw it.

| case | example | why |
|---|---|---|
| guttural dropped | `aafak` vs عافاك | French habit writes ع as a vowel. No layer recovers a phoneme the writer did not record. |
| ح written as h | `chhal` vs شحال | Same failure, different consonant. Merges with ه. |
| tanwin | `shukran` vs شكرا | Latin writes the final n; Arabic script carries it on the alef. |

The consequence is that the three conventions are **not symmetric**. Arabic
script and Arabizi are mutually recoverable. French-habit spelling is lossy
against both. That asymmetry is a finding in its own right and is recorded in
FINDINGS.md.

## Open questions

- How much residual mismatch comes from و/ي specifically? Measurable by ablating
  that one rule.
- Does degemination help or hurt overall? Same ablation shape.
- What fraction of a real corpus falls into the unrecoverable classes above?
  That number decides whether the layer is useful or merely tidy.
