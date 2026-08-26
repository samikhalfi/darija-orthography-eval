"""Normalisation, in two layers.

Layer 1, `normalise_arabic`, is the BASELINE: the Alef/Yaa/Taa folding that
Arabic ASR papers apply before reporting WER. Prior art, implemented here so
the comparison against layer 2 is honest rather than rhetorical.

Layer 2, `to_canonical`, is the contribution: a consonant skeleton that Arabic
script and Arabizi both map onto.

Design decisions and what they cost are recorded in notes/decisions.md. The
short version: the canonical form is neither script. It is an abjad-style
consonant skeleton, because Arabic script already omits short vowels and
Arabizi writes them, so the only form both can reach is the one without them.

Run: python normaliser/canon.py
"""

ALEF_VARIANTS = "آأإٱ"
ALEF = "ا"
YAA_ALT, YAA = "ى", "ي"
TAA_MARBUTA, HAA = "ة", "ه"
TATWEEL = "ـ"
DIACRITICS = "ًٌٍَُِّْٰ"

# Arabic script to canonical. Emphatics are merged with their plain
# counterparts (ص->s, ض->d, ط->t, ظ->d) because Arabizi does not
# distinguish them at all, so keeping them apart would guarantee a mismatch.
ARABIC_MAP = {
    "ا": "", "ب": "b", "ت": "t", "ث": "t", "ج": "j",
    "ح": "7", "خ": "x", "د": "d", "ذ": "d", "ر": "r",
    "ز": "z", "س": "s", "ش": "c", "ص": "s", "ض": "d",
    "ط": "t", "ظ": "d", "ع": "3", "غ": "g", "ف": "f",
    "ق": "9", "ك": "k", "ل": "l", "م": "m", "ن": "n",
    "ه": "h", "و": "w", "ي": "y", "ء": "2",
    "گ": "g", "پ": "p", "ڤ": "v",
}

# Latin, longest match first. Digraphs must be tried before their letters or
# "sh" is read as s followed by h.
LATIN_MAP = {
    "sh": "c", "ch": "c", "kh": "x", "gh": "g", "th": "t", "dj": "j",
    "ou": "", "ai": "", "ei": "", "ee": "",
    "3": "3", "7": "7", "9": "9", "2": "2", "5": "x", "8": "g",
    "b": "b", "t": "t", "j": "j", "d": "d", "r": "r", "z": "z", "s": "s",
    "c": "c", "f": "f", "q": "9", "k": "k", "g": "g", "l": "l", "m": "m",
    "n": "n", "h": "h", "w": "w", "y": "y", "v": "v", "p": "p", "x": "x",
    "a": "", "e": "", "i": "", "o": "", "u": "",
    "é": "", "è": "", "ê": "", "à": "", "ô": "", "û": "",
}
_LATIN_KEYS = sorted(LATIN_MAP, key=len, reverse=True)


def normalise_arabic(s: str) -> str:
    """The standard Arabic-script baseline. Deliberately the weak layer."""
    out = []
    for ch in s:
        if ch in DIACRITICS or ch == TATWEEL:
            continue
        if ch in ALEF_VARIANTS:
            ch = ALEF
        elif ch == YAA_ALT:
            ch = YAA
        elif ch == TAA_MARBUTA:
            ch = HAA
        out.append(ch)
    return "".join(out)


def _canon_word(w: str) -> str:
    out, i = [], 0
    while i < len(w):
        ch = w[i]
        if ch in ARABIC_MAP:
            out.append(ARABIC_MAP[ch])
            i += 1
            continue
        for key in _LATIN_KEYS:
            if w.startswith(key, i):
                out.append(LATIN_MAP[key])
                i += len(key)
                break
        else:
            i += 1  # punctuation, digits we do not map, anything else
    # Degeminate. Arabic script usually omits shadda while Arabizi doubles the
    # letter, so a doubled consonant is a writing habit rather than a signal.
    skeleton = []
    for c in "".join(out):
        if not skeleton or skeleton[-1] != c:
            skeleton.append(c)
    return "".join(skeleton)


def to_canonical(s: str) -> str:
    """Map Arabic script or Arabizi onto one consonant skeleton."""
    s = normalise_arabic(s.lower())
    return " ".join(f for f in (_canon_word(w) for w in s.split()) if f)


def demo():
    afak_ar, bezzaf_ar, ch7al_ar = "عافاك", "بزاف", "شحال"

    # Layer 1 does what the literature says it does, and no more.
    assert normalise_arabic("أحمد") == "احمد"
    assert normalise_arabic("مدرسة").endswith(HAA)
    assert TATWEEL not in normalise_arabic("مــدرسة")

    # THE NEGATIVE RESULT, ENCODED AS A TEST. Alef folding cannot reach a
    # transliteration. If this ever fails, the README claim is falsified.
    assert normalise_arabic(afak_ar) != normalise_arabic("3afak")

    # Layer 2: Arabic script and Arabizi converge.
    assert to_canonical(afak_ar) == to_canonical("3afak") == "3fk"
    assert to_canonical(bezzaf_ar) == to_canonical("bezzaf") == to_canonical("bzaf") == "bzf"
    assert to_canonical(ch7al_ar) == to_canonical("sh7al") == to_canonical("ch7al") == "c7l"

    # Idempotent, or scoring becomes order-dependent.
    assert to_canonical(to_canonical("3afak")) == to_canonical("3afak")

    # Multi-word.
    assert to_canonical("شكرا " + bezzaf_ar) == "ckr bzf"

    # KNOWN UNRECOVERABLE, asserted so they cannot be forgotten. These are not
    # bugs, they are information the source spelling destroyed. Measured as an
    # error class in FINDINGS.md rather than patched away.
    assert to_canonical("aafak") != to_canonical(afak_ar), (
        "French-habit spelling drops the guttural entirely: no layer can "
        "recover a phoneme the writer did not record."
    )
    assert to_canonical("chhal") != to_canonical(ch7al_ar), "same, for ح written as h"
    assert to_canonical("shukran") != to_canonical("شكرا"), (
        "tanwin: Latin writes the final n, Arabic script carries it on the alef"
    )

    print("all assertions passed")
    print()
    rows = [
        ("afak   (ar/arabizi/fr)", afak_ar, "3afak", "aafak"),
        ("bezzaf (ar/arabizi/fr)", bezzaf_ar, "bezzaf", "bzaf"),
        ("ch7al  (ar/arabizi/fr)", ch7al_ar, "sh7al", "chhal"),
    ]
    print(f"{'word':<24} {'arabic':>8} {'arabizi':>8} {'french':>8}  converge")
    for label, a, b, c in rows:
        ca, cb, cc = to_canonical(a), to_canonical(b), to_canonical(c)
        mark = "all 3" if ca == cb == cc else ("2 of 3" if ca == cb else "no")
        print(f"{label:<24} {ca:>8} {cb:>8} {cc:>8}  {mark}")


if __name__ == "__main__":
    demo()
