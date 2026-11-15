# Card document (one element of a batch array)

```json
{
  "id": "m11",                        // v = Valley, a = Ancients, m = Masters; sequential per series, never reused
  "t": "goleman",                     // thinker key [a-z][a-z0-9_]{1,23}; the id's first letter must equal the thinker's wing
  "era": "1995",                      // year, or "c. 500 BC"; max 24 chars
  "src": "Emotional Intelligence, 1995", // work + year, English; max 140
  "h": "The thesis in one sentence.", // max 140
  "b": "45-70 English words: fact, mechanism, consequence.",   // max 700 chars
  "d": "One concrete action, 15-30 words.",                   // max 320
  "tg": ["leadership"],               // 1-3 of the ids in content/topics.json (strategy leadership focus risk building power character money persuasion)
  "v": false,                         // true only after verification; then source_url is mandatory
  "source_url": "https://...",        // the page that confirmed work + year
  "note": "",                         // what could not be verified, or where the second source is
  "thinker": {                        // required when `t` is new; ignored otherwise
    "n": "Daniel Goleman", "i": "DG", "r": "Psychologist and science journalist", "w": "m", "y": "b. 1946",
    "names": {"it": "", "es": "", "la": ""},   // only when the name changes by language
    "roles": {"it": "Psicologo e giornalista scientifico", "es": "Psicólogo y periodista científico", "la": "Psychologus et scriptor"}
  },
  "tr": {
    "it": ["titolo", "corpo", "usala oggi", "fonte"],
    "es": ["título", "cuerpo", "úsala hoy", "fuente"],
    "la": ["titulus"]
  },
  "duo": {"ids": ["a12", "v07", "m11"], "th": "leadership",   // optional: 2 or 3 existing or in-batch cards from at least two different wings
          "br": {"en": "...", "it": "...", "es": "...", "la": "..."}},
  "added": "2026-11-16T08:00:00Z",    // UTC; the app shows "New" for 72 h
  "batch": "2026-11-16-01"
}
```

Stored shape after merge: `content/duos.json` holds `{"ids": [...], "th", "br"}`; the old `{a, v}` pairs were migrated on 2026-11-15 and the scripts still read them.

Content rules: curator's words only; no verbatim sentence from a modern author, at most one short public-domain line from a classic (never a copyrighted translation); no third-party app names, brands or logos (an author's own company or institution in the role line is fine); no private persons; facts the reader can check (work, year); every card must be usable by an executive on Monday morning. Wing discipline: sales trainers, speakers and self-help authors are Masters, never Valley, even when they write about business.
