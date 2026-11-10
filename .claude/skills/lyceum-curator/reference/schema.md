# Card document (one element of a batch array)

```json
{
  "id": "v28",                        // v = Valley, a = Ancients; sequential per series, never reused
  "t": "nadella",                     // thinker key [a-z][a-z0-9_]{1,23}
  "era": "2017",                      // year, or "c. 500 BC"; max 24 chars
  "src": "Hit Refresh, 2017",         // work + year, English; max 140
  "h": "The thesis in one sentence.", // max 140
  "b": "45-70 English words: fact, mechanism, consequence.",   // max 700 chars
  "d": "One concrete action, 15-30 words.",                   // max 320
  "tg": ["leadership"],               // 1-3 of: strategy leadership focus risk building power character money
  "v": false,                         // true only after step 4; then source_url is mandatory
  "source_url": "https://...",        // the page that confirmed work + year
  "note": "",                         // what could not be verified
  "thinker": {                        // required when `t` is new; ignored otherwise
    "n": "Satya Nadella", "i": "SN", "r": "CEO, Microsoft", "w": "v", "y": "b. 1967",
    "names": {"it": "", "es": "", "la": ""},
    "roles": {"it": "CEO, Microsoft", "es": "CEO, Microsoft", "la": "Praefectus Microsoft"}
  },
  "tr": {
    "it": ["titolo", "corpo", "usala oggi", "fonte"],
    "es": ["título", "cuerpo", "úsala hoy", "fuente"],
    "la": ["titulus"]
  },
  "duo": {"a": "a30", "v": "v28", "th": "leadership",
          "br": {"en": "...", "it": "...", "es": "...", "la": "..."}},   // optional
  "added": "2026-11-11T08:00:00Z",    // UTC; the app shows "New" for 72 h
  "batch": "2026-11-11-01"
}
```

Content rules: curator's words only; no verbatim sentence from a modern author, at most one short public-domain line from a classic (never a copyrighted translation); no third-party app names, brands or logos; no private persons; facts the reader can check (work, year); every card must be usable by an executive on Monday morning.
