"""Normalisation, in two layers.

Layer 1, `normalise_arabic`, is the BASELINE: the Alef/Yaa/Taa folding that
Arabic ASR papers apply before reporting WER. It is prior art, not a
contribution. You implement it so the comparison is honest.

Layer 2, `to_canonical`, is the contribution: one form that Arabic script,
Arabizi and French-influenced spellings all map onto.

YOU write both. They are the claim of this repository expressed as code, so
they are the first thing a panel will open.

Run: python normaliser/canon.py
"""

# Arabic-script variants the standard pipeline folds. Kept as data rather than
# buried in the function so the baseline is auditable.
ALEF_VARIANTS = "آأإٱ"   # آ أ إ ٱ  -> ا
ALEF = "ا"
YAA_ALT = "ى"                              # ى -> ي
YAA = "ي"
TAA_MARBUTA = "ة"                          # ة -> ه
HAA = "ه"
TATWEEL = "ـ"                              # ـ  removed
DIACRITICS = "ًٌٍَُِّْ"

# The Arabizi numeral substitutions. This is the axis the standard pipeline
# cannot see, because these are not spelling variants, they are a different
# script.
NUMERAL_MAP = {
    "3": "ع",   # ع
    "7": "ح",   # ح
    "9": "ق",   # ق
    "2": "ء",   # ء
    "5": "خ",   # خ
    "8": "غ",   # غ
}


def normalise_arabic(s: str) -> str:
    """The standard Arabic-script baseline. Prior art, implemented for comparison.

    Fold the Alef variants, ى to ي, ة to ه, strip tatweel and diacritics.
    Nothing clever. This is deliberately the WEAK layer.
    """
    raise NotImplementedError


def to_canonical(s: str) -> str:
    """Map any of the three conventions onto one form.

    Design decisions you have to make and then defend:

    1. What is the canonical target? Arabic script, a Latin transliteration, or
       an abstract phoneme-ish form that is neither? There is no free lunch.
       Whatever you pick, write down what it loses.
    2. How do you detect which convention an input is in, or do you avoid
       needing to?
    3. `ch` is /ʃ/ in French habit but c-then-h in some Arabizi. `ou` is /u/ in
       French habit but o-then-u elsewhere. These are genuinely ambiguous. What
       do you do, and what is the error rate of that choice?

    ponytail: start with the smallest mapping that makes the assertions below
    pass. Do not build a phonological engine on day one.
    """
    raise NotImplementedError


def demo():
    shukran_ar = "شكرا"      # شكرا
    afak_ar = "عافاك"  # عافاك

    # Layer 1 does what it says.
    assert normalise_arabic("أحمد") == "احمد"
    assert normalise_arabic("مدرسة").endswith(HAA)
    assert TATWEEL not in normalise_arabic("مــدرسة")

    # THE NEGATIVE RESULT, ENCODED AS A TEST.
    # The standard pipeline cannot unify across scripts. If this assertion ever
    # fails, the premise of this repository is wrong and FINDINGS.md says so.
    assert normalise_arabic(shukran_ar) != normalise_arabic("shukran"), (
        "Alef folding does not reach a transliteration. This failing would "
        "falsify the claim in the README."
    )

    # Layer 2 is the contribution: all three conventions land together.
    assert to_canonical(shukran_ar) == to_canonical("shukran") == to_canonical("chokran")
    assert to_canonical(afak_ar) == to_canonical("3afak") == to_canonical("aafak")

    # Idempotent. Normalising twice must not move it again, or scoring becomes
    # order-dependent.
    assert to_canonical(to_canonical("3afak")) == to_canonical("3afak")

    print("all assertions passed")
    print(f"  baseline keeps them apart: {normalise_arabic(shukran_ar)!r} vs {normalise_arabic('shukran')!r}")
    print(f"  canonical brings together: {to_canonical(shukran_ar)!r}")


if __name__ == "__main__":
    demo()
