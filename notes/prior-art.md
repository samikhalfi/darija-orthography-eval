# Prior art

Checked 2026-08-17, before any code was written. Week 1 deliverable.

**Headline: the central claim of the first README was not new.** That the lack
of a standard dialectal orthography makes WER inadequate has been stated and
addressed in the literature since at least 2017. The plan below is revised
accordingly, and the revision is the point of doing this check first.

## What is already established

**Ali, Nakov, Bell and Renals, 2017. "WERd: Using Social Text Spelling Variants
for Evaluating Dialectal Speech Recognition."** arXiv:1709.07484.

States the problem almost exactly as this repository originally did: dialect
orthography is not standardized, so there is no clear gold standard, several
outputs can be correct according to different annotators, and standard WER is
therefore inadequate. Their fix borrows TERp from machine translation and admits
spelling variants mined from Twitter without supervision. Evaluated on
**Egyptian Arabic**.

**Orthographic normalization before scoring is standard practice** in Arabic
ASR. Alef, Yaa and Taa variants are folded, diacritics handled, and published
WERs are usually post-normalization. This is a convention, not a research gap.

**Interannotator disagreement on dialectal Arabic orthography is reported around
13%.** So the instability is not only known, it has been quantified.

**The problem shape is currently active in other language families.** SN-WER
(script-normalized WER for multi-script Indic ASR, arXiv:2606.02548, 2026)
attacks the multi-script version of this. Worth reading as a method template
rather than as competition.

## What that leaves

Three gaps survive the check. All are narrower than the original claim and all
are defensible.

**1. Cross-script, not cross-spelling.** WERd admits spelling variants inside
one writing system. The standard Alef/Yaa/Taa normalization also assumes Arabic
script. Moroccan Darija is written pervasively in Latin script with numerals
(3, 7, 9, 2), which is a transliteration rather than a spelling variant. Neither
mechanism covers it. How much error that leaves on the table is not, as far as
this check found, published for Darija.

**2. Moroccan rather than Egyptian.** WERd's evidence is Egyptian. Darija is
further from MSA and more heavily code-switched with French, so the Egyptian
result does not transfer for free.

**3. Native-authored references rather than mined variants.** WERd mines
variants unsupervised from Twitter, which captures frequency but not
correctness. Hand-written references from a native speaker are a different and
stronger ground truth for measuring the spread itself.

## Revised position

Not "WER for Darija is unstable", which is known. Instead:

> The normalization pipeline conventionally applied before computing WER for
> Arabic assumes Arabic script. Moroccan Darija is substantially written in
> Latin script with numerals. This measures what that assumption costs, and
> tests whether a cross-script canonicalisation layer recovers it.

Same three deliverables, same schedule. The framing is narrower, sits inside an
existing literature, and cites the work it extends.

## To read properly, not just abstract

- WERd in full, particularly how variants are admitted during alignment.
- SN-WER, for the multi-script alignment method.
- Whatever normalization the Darija corpora used below applied to their own
  transcripts, since that decision is usually undocumented.

## Corpora found

To verify licence and content before use.

- **MDVC corpus**, ~1000 h from 80 YouTube channels, Wav2Vec2 fine-tune reported
  at 9% WER. Zenodo record 14890886.
- **atlasia/Moroccan-Darija-Wiki-Audio-Dataset**, 551 parallel text and speech
  samples, CC BY-SA 4.0, on Hugging Face. Small, licensed clearly, likely the
  right starting point.
- **DVoice**, open Moroccan dialectal Arabic ASR dataset.
- **nainiayoub/moroccan-darija-datasets**, an index of Darija datasets by source
  and size.
- **Voxlect** (arXiv:2508.01691), a speech foundation model benchmark for
  dialects, for baseline comparison.
