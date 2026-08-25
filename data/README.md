# Evaluation set format

One utterance per line in `eval-set.jsonl`. Every line carries the same audio
and the same words, written under each orthographic convention.

```json
{
  "id": "atlasia-0001",
  "audio": "audio/atlasia-0001.wav",
  "source": "atlasia/Moroccan-Darija-Wiki-Audio-Dataset",
  "refs": {
    "arabic": "شكرا بزاف",
    "arabizi": "shukran bezzaf",
    "french": "chokran bezzaf"
  },
  "notes": "sh/ch is the French-influence axis"
}
```

## The three conventions

| key | what it is |
|---|---|
| `arabic` | Arabic script, written the way it appears in Darija social text |
| `arabizi` | Latin script with numerals: 3 for ع, 7 for ح, 9 for ق, 2 for hamza |
| `french` | Latin script following French spelling habits: `ch` for /ʃ/, `ou` for /u/, silent letters |

`arabizi` and `french` are kept apart on purpose. They are both Latin script but
they disagree, and collapsing them early would hide half of what is being
measured.

## Rules for writing references

- Write what a Moroccan would actually type, not a transliteration standard.
- No version is the "correct" one. If one convention genuinely has no natural
  form for an utterance, leave the key out rather than inventing one.
- Do not look at the model output first. Write the references, then transcribe.
- Note anything ambiguous in `notes`. Those notes are data, not commentary.

## Size

100 to 200 utterances. The finding is about variance in the metric, not model
quality, so a large corpus buys nothing here. Sample size and its consequences
get stated with the results.

## Audio

`data/audio/` is gitignored. Keep a `fetch.py` or a documented command so the
set is reproducible without committing audio.
