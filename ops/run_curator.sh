#!/usr/bin/env bash
# Lyceum curator — headless Claude Code run (Linux/macOS). Cron line in ops/README.md.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"; mkdir -p logs
STAMP="$(date +%Y-%m-%d_%H%M)"
claude -p "$(cat ops/curator_prompt.txt)" \
  --permission-mode acceptEdits \
  --allowedTools "Read,Edit,Write,Glob,Grep,WebSearch,WebFetch,Bash(python3 scripts/*),Bash(git add *),Bash(git commit *),Bash(git status*),Bash(git log*),Bash(git remote*)" \
  --output-format json > "logs/curator_$STAMP.json"
echo "curator run logged to logs/curator_$STAMP.json"
