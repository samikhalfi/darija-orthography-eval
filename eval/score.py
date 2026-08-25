"""WER, CER, and the spread across orthographic conventions.

YOU implement the three functions. They are the metric, which means they are
exactly what a panel will ask you to explain. Nothing here may be pasted.

No jiwer, no torchmetrics, no editdistance package. Levenshtein by hand is
about fifteen lines and you need to be able to draw the DP table on a
whiteboard.

Run: python eval/score.py
It fails until the functions are real. That is the check.
"""


def _edit_distance(a: list, b: list) -> int:
    """Levenshtein distance between two sequences.

    Before writing it, answer: what are the three edits, what does each cell of
    the DP table mean, and why is the table (len(a)+1) x (len(b)+1) rather than
    len(a) x len(b)?
    """
    raise NotImplementedError


def wer(reference: str, hypothesis: str) -> float:
    """Word error rate.

    Edit distance over WORDS, divided by something. Divided by what, exactly,
    and why that rather than the other one? Write the answer in a comment here
    before you write the code, because this is the question that gets asked.
    """
    raise NotImplementedError


def cer(reference: str, hypothesis: str) -> float:
    """Character error rate. Same shape, different unit.

    For this project CER matters more than usual. Say why in one line: what does
    CER see that WER cannot, when the two references are in different scripts?
    """
    raise NotImplementedError


def spread(hypothesis: str, refs: dict) -> dict:
    """Score one hypothesis against every reference convention.

    Returns {"per_ref": {name: wer}, "min": float, "max": float, "spread": float}

    `spread` is max minus min, and it is the number this whole repository
    exists to report. A single WER with no stated convention is not a result.
    """
    raise NotImplementedError


def demo():
    # Identical strings: no errors.
    assert wer("kayn chi haja", "kayn chi haja") == 0.0

    # One substitution out of three words.
    assert abs(wer("kayn chi haja", "kayn chi hana") - 1 / 3) < 1e-9

    # One deletion out of three.
    assert abs(wer("kayn chi haja", "kayn haja") - 1 / 3) < 1e-9

    # One insertion. Note the denominator does NOT change: it is the reference
    # length. If this assertion surprises you, that is the point of it.
    assert abs(wer("kayn chi haja", "kayn chi dyal haja") - 1 / 3) < 1e-9

    # CER is finer grained than WER: one wrong letter is a whole wrong word to
    # WER, but only one wrong character to CER.
    assert cer("bezzaf", "bezzef") < wer("bezzaf", "bezzef")

    # THE POINT OF THE REPOSITORY.
    # Same utterance, same meaning, three conventions a Moroccan would accept.
    # An ASR system emitting the Arabizi form scores near-perfect against the
    # Arabizi reference and catastrophically against the Arabic-script one.
    # The "true" WER of this system is therefore not a number.
    refs = {
        "arabic": "شكرا بزاف",
        "arabizi": "shukran bezzaf",
        "french": "chokran bezzaf",
    }
    s = spread("shukran bezzaf", refs)
    assert s["per_ref"]["arabizi"] == 0.0
    assert s["per_ref"]["arabic"] == 1.0, "no shared words across scripts"
    assert s["spread"] == 1.0, (
        "This is the finding in miniature: the same output is perfect or "
        "worthless depending only on which convention you scored against."
    )

    print("all assertions passed")
    print(f"spread on the worked example: {s['spread']:.3f}")
    for name, v in sorted(s["per_ref"].items()):
        print(f"  {name:<8} WER {v:.3f}")


if __name__ == "__main__":
    demo()
