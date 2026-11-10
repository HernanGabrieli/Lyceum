# Lyceum

Microlearning app: one idea per card from Silicon Valley builders ("Valley", ids `vNN`) and pre-1900 thinkers ("Ancients", ids `aNN`), in EN/IT/ES with Latin titles. Single-file web app, no framework, no build toolchain beyond Python 3.

## Layout
- `site/index.template.html` – the whole UI (CSS + JS). Data goes where `/*__LYCEUM_DATA__*/` sits. Edit this file for UI changes only.
- `content/` – source of truth: `topics.json`, `thinkers.json`, `cards.json`, `duos.json`, `runs.json`, `batches/` (one file per curator run, kept as audit trail).
- `scripts/build.py` – content → `dist/index.html` (also referential checks). `validate_batch.py` and `merge_batch.py` – curator pipeline.
- `dist/index.html` – generated. Never edit by hand; it is the file served by Docker and the one to publish as a claude.ai artifact.
- `.claude/skills/lyceum-curator/` – the curator agent (skill), with its schema and roster.
- `ops/` – scheduled runs (Windows Task Scheduler, cron) and Docker serving.

## Commands
- Build: `python3 scripts/build.py`
- Validate a batch: `python3 scripts/validate_batch.py content/batches/<file>.json`
- Merge a batch (validates, appends, rebuilds): `python3 scripts/merge_batch.py content/batches/<file>.json --note "..."`
- Smoke test the build in a browser: open `dist/index.html` (works from `file://`; progress lives in localStorage).

## Rules
- Content changes go through the scripts; UI changes go through the template; both end in a commit. Keep commits small and named (`curator: batch 2026-11-11-01, 10 cards, 7 verified` / `ui: ...`).
- Card ids are never reused or renumbered, even after deletion.
- `v:true` (red check) means a source was verified in that run and `source_url` is present. Never set it from memory.
- Card text is the curator's own words; no quotations from modern authors; no brands, logos or private persons.
- Languages: EN is the base; IT and ES are full translations; LA is title-only by design (grammar risk). The UI strings live in the `UI` object in the template.
- Visual identity is fixed (AIXCEEDS Night Edition: night blue, silver Palatino/Book Antiqua headlines, blue martini accent, red martini only for the verified check and destructive actions). Do not introduce other colours or fonts.
- Do not add external scripts, fonts or network calls to the template: the same file is published as a claude.ai artifact, whose CSP blocks them.
