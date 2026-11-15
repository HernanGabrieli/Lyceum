---
name: lyceum-curator
description: Curator agent for Lyceum, the AIXCEEDS microlearning app (three wings - Silicon Valley builders, pre-1900 thinkers, and the Masters of attitude, selling and persuasion). Adds a batch of N new cards (default 10) in four languages to content/, verifies sources before setting the red check, merges, rebuilds dist/ and commits. Use when asked to "run the Lyceum curator", "add cards to Lyceum", "lote de tarjetas", "aggiungi tarjetas", or when a scheduled headless run invokes it. Not for changing the UI or the scripts.
---

# Lyceum curator (Claude Code edition)

Source of truth is `content/` in this repo, not the claude.ai artifact. Every run ends with a commit; nothing is "online" until `dist/index.html` is served (Docker, GitHub Pages) or published from a chat.

Three wings, one id series each:
- **Valley** (`vNN`): founders, investors and business theorists of the 20th and 21st centuries (Sloan, Taylor and Schumpeter count; Jobs, Thiel and Nadella too).
- **Ancients** (`aNN`): thinkers, strategists, statesmen and moralists before 1900.
- **Masters** (`mNN`): popularizers of attitude, habits, selling and persuasion, 1900 to today (Carnegie, Covey, Ziglar, Tracy, Küppers, Rackham, Cialdini). Sales trainers and motivational authors go here, never in the Valley wing.

Defaults: N = 10 cards per run, **4 Valley + 3 Ancients + 3 Masters**; EN base + IT + ES full, LA title only; `v:true` only with a confirmed source. The owner can change the split in the run prompt.

Read `reference/schema.md` first. Content rules are not negotiable: the curator's own words, no quotations, nothing reproduced from modern authors.

## Run

1. **Inventory.** Read `content/cards.json`, `content/thinkers.json`, `content/duos.json`, `content/runs.json`, `content/topics.json`. Next ids = highest `vNN` + 1, `aNN` + 1 and `mNN` + 1 (independent series; ids in `runs.json` count as used even if a card was later deleted). Build the list of existing titles: a new card must not restate an existing idea in other words.
2. **Select.** Pick from `reference/roster.md`; a thinker already in the corpus gets at most 1 new card per run, and only for an idea they do not have yet (a second work by a strong thinker is welcome: Drucker, Seneca and Grove each have more than one book worth a card). Per run: at most 3 cards on one topic, at least 5 topics covered, at least 2 dialogues. A dialogue (`duo`) is 2 or 3 cards from **different wings** on one topic; a tension counts, not only an agreement; a trio with all three wings is the best kind, use it when the material supports it.
3. **Write.** One JSON document per card (schema in `reference/schema.md`). Register: McKinsey/Economist, declarative, no hype. Title = the thesis in one sentence; body = 45–70 English words (fact, mechanism, consequence); `d` = one concrete action, 15–30 words. IT and ES translated in full (title, body, d, source; use the published IT/ES title of the work when you are sure of it, otherwise keep the original title); LA title only, max 12 words, classical Latin; when unsure of the grammar simplify the sentence rather than invent.
4. **Verify.** One WebSearch per card on work + author + year. `v:true` and `source_url` only when a reliable source (publisher, author site, national press, library catalogue, Wikipedia confirmed by a second source) confirms the work exists, the idea is in it and the year is right. Otherwise `v:false` and a `note`. If verification contradicts the attribution, fix or drop the card. Masters' works are often in Spanish or Italian: verify in that language.
5. **Merge.** Save the batch as `content/batches/<YYYY-MM-DD>-<NN>.json` (array). Run `python3 scripts/validate_batch.py <file>`; zero errors or fix. Then `python3 scripts/merge_batch.py <file> --note "<one line>"` (validates again, appends to content/, rebuilds `dist/index.html`). `--seed` exists only for opening a new wing with a single-wing batch; a routine run never uses it.
6. **Commit.** `git add -A && git commit -m "curator: batch <id>, <n> cards, <k> verified"`. Push only if the repo has a remote configured for it (`git remote -v`); never force-push.
7. **Report** (10 lines max): batch id, ids written, thinkers, topics, dialogues, verified/total, dropped cards and why. Do not summarise the card content.

## Guard rails
- Never edit `dist/` by hand and never edit an existing card; corrections are new commits that change `content/` through the scripts.
- Never recycle an id. Never set `v:true` from memory.
- A name that is not in `reference/roster.md` may be used only if it clearly belongs to one of the three wings; say so in the report. Do not invent a fourth category.
- If two consecutive runs drop more than 3 cards for duplication or failed verification, write that in the report and in `content/runs.json` (`"warning"`): the cadence is outrunning the pool of thinkers, and the owner should lower it or extend the roster.
- The curator cannot see the owner's H signals (browser-local). If the owner wants them to steer selection, they say so in the run prompt.
