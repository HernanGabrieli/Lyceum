# Scheduling the curator

Claude Code has no scheduler of its own: the OS (or CI) calls `claude -p` on a timer. Headless runs load `.claude/` (skills, settings, CLAUDE.md) from the repo root, so the skill is available without installing it anywhere else. Reference: https://code.claude.com/docs/en/headless

## Windows Task Scheduler (every 12 h, 08:00 and 20:00)
Run once in an elevated PowerShell, after `claude --version` works in that user's session:
```
schtasks /Create /TN "Lyceum curator" /SC HOURLY /MO 12 /ST 08:00 /TR "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:\path\to\lyceum\ops\run_curator.ps1\""
```
Check: `schtasks /Query /TN "Lyceum curator" /V`. Logs land in `logs\curator_<stamp>.json`.

## cron (Linux/macOS)
```
0 8,20 * * * cd /path/to/lyceum && ./ops/run_curator.sh >> logs/cron.log 2>&1
```

## GitHub Actions (optional)
`.github/workflows/curate.yml` runs the same prompt on a cron with `ANTHROPIC_API_KEY` as a repository secret (API billing, not the Claude subscription), commits the batch and rebuilds `dist/`. Pair it with GitHub Pages serving `dist/` if the Docker PC should not be the host.

## Recommended cadence
The owner asked for every 12 h (20 cards/day). The curator warns in `runs.json` when the pool of thinkers runs dry (more than 3 cards dropped in two consecutive runs); when that happens, change `/MO 12` to `/SC DAILY`.
