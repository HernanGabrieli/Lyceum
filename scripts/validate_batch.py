#!/usr/bin/env python3
"""Validate a curator batch (JSON array of card documents, see .claude/skills/lyceum-curator/SKILL.md)
against the current content/ before merging.
usage: python3 scripts/validate_batch.py content/batches/<batch>.json [--seed]
Exit 0 = valid; 1 = errors, one per line.
--seed: a lane-launch batch (one wing only, topic cap 6) — only for opening a new wing.
Wings: v = Valley, a = Ancients, m = Masters. A card id starts with its thinker's wing letter.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WINGS = ("v", "a", "m")
ID_RE, T_RE = re.compile(r"^[avm]\d{2,3}$"), re.compile(r"^[a-z][a-z0-9_]{1,23}$")
LIMITS = {"h": 140, "b": 700, "d": 320, "src": 140, "era": 24}
def load(n): return json.load(open(os.path.join(ROOT, "content", n), encoding="utf-8"))
def norm(s): return [w for w in re.sub(r"[^a-z0-9 ]", " ", s.lower()).split() if len(w) > 3]
def duo_ids(d): return list(d.get("ids") or [d.get("a"), d.get("v")])

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    batch = json.load(open(sys.argv[1], encoding="utf-8"))
    seed = "--seed" in sys.argv
    topics, thinkers, cards, duos = load("topics.json"), load("thinkers.json"), load("cards.json"), load("duos.json")
    TOP = set(topics["ids"]); known_ids = {c["id"] for c in cards}; titles = {c["h"] for c in cards}
    runs = load("runs.json"); used_ids = known_ids | {i for r in runs for i in r.get("ids", [])}
    wing_of = {c["id"]: c["id"][0] for c in cards}          # wing is the id's first letter
    existing_duos = {frozenset(duo_ids(d)) for d in duos}
    errs, bids, per_t, per_top = [], set(), {}, {}
    for c in batch:
        if isinstance(c, dict) and ID_RE.match(str(c.get("id", ""))): wing_of[c["id"]] = c["id"][0]
    for i, c in enumerate(batch):
        tag = f"[{i}] {c.get('id','?')}"
        for k in ("id", "t", "era", "src", "h", "b", "d", "tg", "added", "batch", "tr"):
            if k not in c: errs.append(f"{tag}: missing {k}")
        cid = str(c.get("id", ""))
        if not ID_RE.match(cid): errs.append(f"{tag}: bad id (vNN, aNN or mNN)")
        if cid in used_ids: errs.append(f"{tag}: id already used (ids are never recycled)")
        if cid in bids: errs.append(f"{tag}: id repeated in batch")
        bids.add(cid)
        for k, mx in LIMITS.items():
            v = c.get(k, "")
            if not isinstance(v, str) or not v or len(v) > mx: errs.append(f"{tag}: {k} empty or longer than {mx}")
        wb = len(str(c.get("b", "")).split())
        if wb and not 35 <= wb <= 85: errs.append(f"{tag}: body has {wb} words (target 45-70)")
        tg = c.get("tg", [])
        if not isinstance(tg, list) or not 1 <= len(tg) <= 3 or not set(tg) <= TOP: errs.append(f"{tag}: bad tg {tg}")
        for t in (tg if isinstance(tg, list) else []): per_top[t] = per_top.get(t, 0) + 1
        t = str(c.get("t", "")); wing = cid[:1]
        if not T_RE.match(t): errs.append(f"{tag}: bad thinker key")
        if t in thinkers:
            if thinkers[t]["w"] != wing: errs.append(f"{tag}: id series {wing} vs thinker wing {thinkers[t]['w']}")
        else:
            th = c.get("thinker")
            if not th: errs.append(f"{tag}: new thinker {t} needs a thinker object")
            else:
                for k in ("n", "i", "r", "w", "y"):
                    if not th.get(k): errs.append(f"{tag}: thinker.{k} missing")
                if th.get("w") not in WINGS: errs.append(f"{tag}: thinker.w must be v, a or m")
                elif th["w"] != wing: errs.append(f"{tag}: id series {wing} vs thinker.w {th['w']}")
                if len(str(th.get("i", ""))) > 3: errs.append(f"{tag}: initials longer than 3")
                for l in ("it", "es"):
                    if not th.get("roles", {}).get(l): errs.append(f"{tag}: thinker.roles.{l} missing")
                thinkers[t] = {"w": th.get("w")}
        per_t[t] = per_t.get(t, 0) + 1
        words = set(norm(c.get("h", "")))
        for kt in titles:
            kw = set(norm(kt))
            if words and kw and len(words & kw) / len(words) >= 0.7: errs.append(f"{tag}: title looks like a duplicate of '{kt}'")
        tr = c.get("tr", {})
        for l in ("it", "es"):
            a = tr.get(l)
            if not isinstance(a, list) or len(a) != 4 or not all(isinstance(x, str) and x for x in a): errs.append(f"{tag}: tr.{l} must be [h,b,d,src]")
        la = tr.get("la")
        if not isinstance(la, list) or not la or not la[0]: errs.append(f"{tag}: tr.la must be [title]")
        elif len(la[0].split()) > 14: errs.append(f"{tag}: Latin title longer than 14 words")
        if c.get("v") is True and not c.get("source_url"): errs.append(f"{tag}: v:true requires source_url")
        if "duo" in c:
            d = c["duo"]
            if not isinstance(d, dict) or d.get("th") not in TOP: errs.append(f"{tag}: duo.th invalid")
            else:
                di = duo_ids(d); pool = used_ids | bids | {x.get("id") for x in batch if isinstance(x, dict)}
                if not 2 <= len(di) <= 3 or len(set(di)) != len(di): errs.append(f"{tag}: duo.ids must list 2-3 distinct cards")
                for x in di:
                    if x not in pool: errs.append(f"{tag}: duo references unknown card {x}")
                if len({wing_of.get(x) for x in di if x in wing_of}) < 2: errs.append(f"{tag}: a dialogue needs at least two different wings")
                if frozenset(di) in existing_duos: errs.append(f"{tag}: duo already exists")
                for l in ("en", "it", "es"):
                    if not d.get("br", {}).get(l): errs.append(f"{tag}: duo.br.{l} missing")
        if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", str(c.get("added", ""))): errs.append(f"{tag}: added must be ISO 8601 UTC")
    for t, n in per_t.items():
        if n > 2: errs.append(f"batch: {n} cards for thinker {t} (max 2)")
    for t, n in per_top.items():
        if n > (6 if seed else 4): errs.append(f"batch: {n} cards tagged {t} (max {6 if seed else 4})")
    nd = sum(1 for c in batch if "duo" in c)
    wings = {w: sum(1 for c in batch if str(c.get("id", "")).startswith(w)) for w in WINGS}
    if len(batch) >= 8:
        if nd < 2: errs.append(f"batch: only {nd} dialogue(s), expected at least 2")
        if not seed and sum(1 for w in wings.values() if w) < 2: errs.append(f"batch: cards come from a single wing {wings}")
        if not seed and max(wings.values()) > len(batch) // 2: errs.append(f"batch: one wing holds more than half the batch {wings}")
    if errs: print("\n".join(errs)); print(f"\n{len(errs)} error(s)"); sys.exit(1)
    print(f"OK: {len(batch)} cards, {nd} dialogues, wings {wings}, topics {per_top}")

if __name__ == "__main__":
    main()
