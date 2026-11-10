# Lyceum curator — headless Claude Code run (Windows). Schedule with the schtasks line in ops/README.md.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
New-Item -ItemType Directory -Force -Path "$root\logs" | Out-Null
$stamp = Get-Date -Format "yyyy-MM-dd_HHmm"
$prompt = Get-Content "$root\ops\curator_prompt.txt" -Raw
# Tools are restricted to what the skill needs: files, web verification, the three scripts and git.
claude -p $prompt `
  --permission-mode acceptEdits `
  --allowedTools "Read,Edit,Write,Glob,Grep,WebSearch,WebFetch,Bash(python3 scripts/*),Bash(python scripts/*),Bash(git add *),Bash(git commit *),Bash(git status*),Bash(git log*),Bash(git remote*)" `
  --output-format json | Out-File -Encoding utf8 "$root\logs\curator_$stamp.json"
Write-Host "curator run logged to logs\curator_$stamp.json"
