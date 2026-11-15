# Lyceum

Microlearning app: one idea per card from three wings — Silicon Valley builders and business theorists ("Valley", ids `vNN`), pre-1900 thinkers ("Ancients", ids `aNN`) and the popularizers of attitude, selling and persuasion ("Masters", ids `mNN`) — in EN/IT/ES with Latin titles. A dialogue (`duos.json`) is 2 or 3 cards from different wings on one topic. Single-file web app, no framework, no build toolchain beyond Python 3.

## Layout
- `site/index.template.html` – the whole UI (CSS + JS). Data goes where `/*__LYCEUM_DATA__*/` sits. Edit this file for UI changes only.
- `site/pwa/` – manifest, icons and service worker; `build.py` copies them into `dist/` and stamps `sw.js` with a hash of the page so every deploy refreshes the cache. The app installs from GitHub Pages (Add to Home Screen) and works offline after the first visit; a service worker never runs from `file://` or inside a claude.ai artifact, and the page does not depend on it.
- `content/` – source of truth: `topics.json`, `thinkers.json`, `cards.json`, `duos.json`, `runs.json`, `batches/` (one file per curator run, kept as audit trail).
- `scripts/build.py` – content → `dist/index.html` (also referential checks). `validate_batch.py` and `merge_batch.py` – curator pipeline.
- `dist/index.html` – generated and git-ignored. Never edit by hand; `scripts/build.py` produces it (locally for Docker and for publishing as a claude.ai artifact; GitHub Actions builds it for Pages).
- `.claude/skills/lyceum-curator/` – the curator agent (skill), with its schema and roster.
- `ops/` – scheduled runs (Windows Task Scheduler, cron) and Docker serving. `.github/workflows/` – Pages deploy on push, cloud curator on cron.

## Commands
- Build: `python3 scripts/build.py`
- Validate a batch: `python3 scripts/validate_batch.py content/batches/<file>.json`
- Merge a batch (validates, appends, rebuilds): `python3 scripts/merge_batch.py content/batches/<file>.json --note "..."`
- Smoke test the build in a browser: open `dist/index.html` (works from `file://`; progress lives in localStorage).

## Rules
- Content changes go through the scripts; UI changes go through the template; both end in a commit. Keep commits small and named (`curator: batch 2026-11-11-01, 10 cards, 7 verified` / `ui: ...`).
- Card ids are never reused or renumbered, even after deletion. A card id starts with its thinker's wing letter (v, a, m); `validate_batch.py --seed` is only for opening a new wing with a single-wing batch.
- Wing discipline: sales trainers, speakers and self-help authors are Masters, never Valley. Topics live in `content/topics.json` (nine, including `persuasion`); adding one means adding its four names there.
- `v:true` (red check) means a source was verified in that run and `source_url` is present. Never set it from memory.
- Card text is the curator's own words; no quotations from modern authors; no brands, logos or private persons.
- Languages: EN is the base; IT and ES are full translations; LA is title-only by design (grammar risk). The UI strings live in the `UI` object in the template.
- Visual identity is fixed (AIXCEEDS Night Edition: night blue, silver Palatino/Book Antiqua headlines, blue martini accent, red martini only for the verified check and destructive actions). Card materials: Valley = night blue, Ancients = shined silver, Masters = blue-martini tinted night. Do not introduce other colours or fonts.
- Do not add external scripts, fonts or network calls to the template: the same file is published as a claude.ai artifact, whose CSP blocks them.
- Reading progress, stashes, H signals and the review schedule (`marks`, `rv`: a kept card returns after 7 and 30 days, two per day, a dwell of 1.6 s completes the stage and counts toward the daily goal) live in `localStorage` under `lyceum_v1`, per browser; nothing is synced.
