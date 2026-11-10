# Lyceum — microlearning prototype (AIXCEEDS)

Five minutes a day with the minds that built business. Single-file web app + a curator agent that adds cards on a schedule.

## Quick start
```bash
python3 scripts/build.py          # -> dist/index.html
open dist/index.html              # or double-click; nothing to install
```

## Serve it (Docker, e.g. on the Tailscale PC)
```bash
docker compose up -d              # nginx on http://localhost:8087 serving ./dist read-only
```
Rebuilding `dist/` is enough; nginx serves the new file immediately.

## Run the curator by hand (Claude Code, from the repo root)
```bash
claude "Run the lyceum-curator skill: one batch of 10 cards, 5 Valley + 5 Ancients. Verify every source. End with the report."
```

## Run it every 12 hours (headless)
- Windows (this PC): `ops/run_curator.ps1` + the `schtasks` line in `ops/README.md`.
- Linux/macOS: `ops/run_curator.sh` + the cron line in `ops/README.md`.
- GitHub Actions (optional, uses an API key, not the subscription): `.github/workflows/curate.yml`.

## Publish to claude.ai
`dist/index.html` is self-contained: in a chat with the Artifact tool, publish it with `url` of the existing artifact. The artifact's own database (`cards` collection) is no longer used; this repo is the source of truth.
