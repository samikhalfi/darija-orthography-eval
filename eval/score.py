"""WER, CER, and the spread across orthographic conventions.

Levenshtein is written by hand rather than pulled from jiwer or editdistance:
the metric is the object of study here, so it has to be inspectable and its
denominator has to be an explicit choice rather than a library default.

Run: python eval/score.py
"""


def _edit_distance(a: list, b: list) -> int:
    """Levenshtein distance between two sequences.

    Three edits, each costing 1: substitute, delete from `a`, insert from `b`.
    The table is (len(a)+1) x (len(b)+1) because row 0 and column 0 hold the
    cost of matching against the empty prefix, which is the length itself.

    ponytail: two rows instead of the full table. The full grid is only needed
    to recover the alignment, and nothing here does.
    """
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(
                prev[j] + 1,                      # delete x
                cur[j - 1] + 1,                   # insert y
                prev[j - 1] + (x != y),           # substitute, free if equal
            ))
        prev = cur
    return prev[-1]


def wer(reference: str, hypothesis: str) -> float:
    """Word error rate: edit distance over words, divided by REFERENCE length.

    The denominator is the reference, not the hypothesis and not the max of the
    two. That is what makes WER a rate of error against the truth rather than a
    similarity score, and it is why WER can exceed 1.0: a hypothesis longer than
    the reference can accumulate more insertions than there are reference words.

    An empty reference has no defined rate. Returns 0.0 when both are empty and
    float('inf') when only the reference is, rather than dividing by zero.
    """
    ref, hyp = reference.split(), hypothesis.split()
    if not ref:
        return 0.0 if not hyp else float("inf")
    return _edit_distance(ref, hyp) / len(ref)


def cer(reference: str, hypothesis: str) -> float:
    """Character error rate. Same shape, characters instead of words.

    CER matters more than usual here. Across scripts WER saturates: every word
    is wrong, so the score pins at 1.0 and stops distinguishing a near-miss
    transliteration from unrelated text. CER still moves, because two spellings
    of the same word share characters where two scripts do not share words.

    Whitespace is kept as a character so word boundaries still count.
    """
    if not reference:
        return 0.0 if not hypothesis else float("inf")
    return _edit_distance(list(reference), list(hypothesis)) / len(reference)


def spread(hypothesis: str, refs: dict, metric=wer) -> dict:
    """Score one hypothesis against every reference convention.

    The `spread` key is max minus min, and it is the number this repository
    exists to report: a single WER with no stated convention is not a result,
    because this is how far it could have moved by choosing another one.
    """
    per_ref = {name: metric(ref, hypothesis) for name, ref in refs.items()}
    values = list(per_ref.values())
    return {
        "per_ref": per_ref,
        "min": min(values),
        "max": max(values),
        "spread": max(values) - min(values),
        "best_convention": min(per_ref, key=per_ref.get),
    }


def demo():
    assert wer("kayn chi haja", "kayn chi haja") == 0.0
    assert abs(wer("kayn chi haja", "kayn chi hana") - 1 / 3) < 1e-9   # substitution
    assert abs(wer("kayn chi haja", "kayn haja") - 1 / 3) < 1e-9       # deletion
    assert abs(wer("kayn chi haja", "kayn chi dyal haja") - 1 / 3) < 1e-9  # insertion

    # WER can exceed 1.0. This is the direct consequence of dividing by the
    # reference: three spurious insertions against a one-word reference.
    assert wer("safi", "safi safi safi safi") == 3.0

    # CER is finer grained: one wrong letter is a whole wrong word to WER.
    assert cer("bezzaf", "bezzef") < wer("bezzaf", "bezzef")
    assert abs(cer("bezzaf", "bezzef") - 1 / 6) < 1e-9
    assert wer("bezzaf", "bezzef") == 1.0

    # THE POINT OF THE REPOSITORY.
    # One utterance, three conventions a Moroccan would accept, one ASR output.
    refs = {
        "arabic": "شكرا بزاف",
        "arabizi": "shukran bezzaf",
        "french": "chokran bezzaf",
    }
    s = spread("shukran bezzaf", refs)
    assert s["per_ref"]["arabizi"] == 0.0
    assert s["per_ref"]["arabic"] == 1.0, "no shared words across scripts"
    assert s["spread"] == 1.0, (
        "The same output is perfect or worthless depending only on which "
        "convention it was scored against."
    )
    assert s["best_convention"] == "arabizi"

    # And the reason CER is carried alongside: it separates the two references
    # that WER cannot tell apart.
    c = spread("shukran bezzaf", refs, metric=cer)
    assert c["per_ref"]["french"] < c["per_ref"]["arabic"], (
        "WER calls both references equally wrong. CER sees that the French "
        "spelling is a near miss and the Arabic script is a different alphabet."
    )

    print("all assertions passed")
    print()
    print("worked example, hypothesis = 'shukran bezzaf'")
    print(f"{'convention':<10} {'WER':>6} {'CER':>6}")
    for name in sorted(refs):
        print(f"{name:<10} {s['per_ref'][name]:>6.3f} {c['per_ref'][name]:>6.3f}")
    print(f"{'spread':<10} {s['spread']:>6.3f} {c['spread']:>6.3f}")


if __name__ == "__main__":
    demo()
