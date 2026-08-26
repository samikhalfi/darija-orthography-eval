# Findings

Updated as work lands. Empty sections mean not yet run, not nothing to report.

## 0. The three conventions are not symmetric

Status: **found 2026-08-26**, while implementing the normaliser. Not predicted
by the plan.

The README treats Arabic script, Arabizi and French-habit spelling as three
equally valid ways of writing the same utterance. Implementing the
canonicalisation layer showed that is wrong in an important way.

| pair | recoverable | why |
|---|---|---|
| Arabic script ↔ Arabizi | yes | both record the gutturals: ع as ع or `3`, ح as ح or `7` |
| either ↔ French habit | **no** | French habit writes ع as a vowel (`aafak`) and ح as `h` (`chhal`) |

Arabic script and Arabizi are mutually recoverable because both encode the full
consonant inventory. French-habit spelling is **lossy**: it discards phonemes
rather than respelling them, and no normalisation layer can recover information
the writer never recorded.

Demonstrated by the convergence table in `normaliser/canon.py`:

```
word                       arabic  arabizi   french  converge
afak   (ar/arabizi/fr)        3fk      3fk       fk  2 of 3
bezzaf (ar/arabizi/fr)        bzf      bzf      bzf  all 3
ch7al  (ar/arabizi/fr)        c7l      c7l      chl  2 of 3
```

`bezzaf` converges across all three only because it contains no guttural.

**Why this matters for the plan.** The headline question was how much of the
cross-script gap a canonicalisation layer recovers. The answer now has to be
reported per convention pair, because a single average would blend a
recoverable gap with an unrecoverable one and understate the layer while hiding
the real limit. Week 2 reports the pairs separately.

**Open:** what fraction of a real Darija corpus contains a guttural at all. That
number decides how much of the corpus falls into the lossy class, and it is
cheap to measure once `data/eval-set.jsonl` is populated.

## 1. WER spread across orthographic conventions

Status: not started, blocked on the evaluation set. Due week 1.

Tooling is ready: `eval/score.py` reports WER and CER per convention plus the
spread, and its worked example shows the mechanism on a single utterance (the
same hypothesis scoring 0.000 against Arabizi and 1.000 against Arabic script).
A worked example is not a result. The result needs the corpus.

## 2. Effect of canonicalisation on the spread

Status: not started. Due week 2. Must be reported per convention pair, see 0.

## 3. Effect of canonicalisation on retrieval failure@k

Status: not started. Due week 3.

## Limitations

- The unrecoverable classes in 0 are asserted in `canon.py` and are a property
  of the writing system, not of this implementation.
- Degemination and the treatment of و/ي are unvalidated choices. Both are
  ablatable and neither has been ablated. See `notes/decisions.md`.
- The evaluation set does not exist yet, so nothing above except 0 rests on
  data.
