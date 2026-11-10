---
name: lyceum-curator
description: Curator agent for Lyceum, the AIXCEEDS microlearning app (Silicon Valley builders and pre-1900 thinkers). Adds a batch of N new cards (default 10) in four languages to content/, verifies sources before setting the red check, merges, rebuilds dist/ and commits. Use when asked to "run the Lyceum curator", "add cards to Lyceum", "lote de tarjetas", "aggiungi tarjetas", or when a scheduled headless run invokes it. Not for changing the UI or the scripts.
---

# Lyceum curator (Claude Code edition)

Source of truth is `content/` in this repo, not the claude.ai artifact. Every run ends with a commit; nothing is "online" until `dist/index.html` is served (Docker) or published from a chat.

Defaults: N = 10 cards per run, 5 Valley (`v` ids) + 5 Ancients (`a` ids); EN base + IT + ES full, LA title only; `v:true` only with a confirmed source.

Read `reference/schema.md` first. Content rules are not negotiable: the curator's own words, no quotations, nothing reproduced from modern authors.

## Run

1. **Inventory.** Read `content/cards.json`, `content/thinkers.json`, `content/duos.json`, `content/runs.json`. Next ids = highest `vNN` + 1 and highest `aNN` + 1 (independent series; ids in `runs.json` count as used even if a card was later deleted). Build the list of existing titles: a new card must not restate an existing idea in other words.
2. **Select.** 5 Valley (founders, investors, modern business theorists, 1950 to today) + 5 Ancients (pre-1900). Pick from `reference/roster.md`; a thinker already in the corpus gets at most 1 new card per run, and only for an idea they do not have yet. Per run: at most 3 cards on one topic, at least 5 topics covered, at least 2 `duo` pairings (Ancients ↔ Valley on one topic; a tension counts, not only an agreement).
3. **Write.** One JSON document per card (schema in `reference/schema.md`). Register: McKinsey/Economist, declarative, no hype. Title = the thesis in one sentence; body = 45–70 English words (fact, mechanism, consequence); `d` = one concrete action, 15–30 words. IT and ES translated in full (title, body, d, source); LA title only, max 12 words, classical Latin; when unsure of the grammar simplify the sentence rather than invent.
4. **Verify.** One WebSearch per card on work + author + year. `v:true` and `source_url` only when a reliable source (publisher, author site, national press, library catalogue, Wikipedia confirmed by a second source) confirms the work exists, the idea is in it and the year is right. Otherwise `v:false` and a `note`. If verification contradicts the attribution, fix or drop the card.
5. **Merge.** Save the batch as `content/batches/<YYYY-MM-DD>-<NN>.json` (array). Run `python3 scripts/validate_batch.py <file>`; zero errors or fix. Then `python3 scripts/merge_batch.py <file> --note "<one line>"` (validates again, appends to content/, rebuilds `dist/index.html`).
6. **Commit.** `git add -A && git commit -m "curator: batch <id>, <n> cards, <k> verified"`. Push only if the repo has a remote configured for it (`git remote -v`); never force-push.
7. **Report** (10 lines max): batch id, ids written, thinkers, topics, duos, verified/total, dropped cards and why. Do not summarise the card content.

## Guard rails
- Never edit `dist/` by hand and never edit an existing card; corrections are new commits that change `content/` through the scripts.
- Never recycle an id. Never set `v:true` from memory.
- If two consecutive runs drop more than 3 cards for duplication or failed verification, write that in the report and in `content/runs.json` (`"warning"`): the cadence is outrunning the pool of thinkers, and the owner should lower it.
- The curator cannot see the owner's H signals (browser-local). If the owner wants them to steer selection, they say so in the run prompt.
