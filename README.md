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

## GitHub
```bash
# from the repo root on the PC, after creating an empty private repo on github.com (no README, no .gitignore)
git remote add origin https://github.com/<user>/lyceum.git
git push -u origin main
# or, with the GitHub CLI:  gh repo create lyceum --private --source=. --remote=origin --push
```
Then in the repository settings: Pages → Build and deployment → Source: **GitHub Actions**. Every push to `main` that touches `content/`, `site/` or `scripts/` rebuilds `dist/` and deploys it to `https://<user>.github.io/lyceum/`. `dist/` is not committed; it is built by the workflow (and locally by `scripts/build.py` for Docker or for publishing to claude.ai).

Cloud curator (optional): add the repository secret `ANTHROPIC_API_KEY`; `.github/workflows/curate.yml` then runs the curator on its cron, pushes the commit and redeploys Pages. It bills the API, not the Claude subscription.

## Publish to claude.ai
Run `python3 scripts/build.py` first. `dist/index.html` is self-contained: in a chat with the Artifact tool, publish it with `url` of the existing artifact. The artifact's own database (`cards` collection) is no longer used; this repo is the source of truth.
