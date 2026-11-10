#!/usr/bin/env python3
"""Merge a validated batch into content/ (cards, thinkers, duos, runs) and rebuild dist/.
usage: python3 scripts/merge_batch.py content/batches/<batch>.json [--verified N] [--note "..."]
Refuses to run if validate_batch.py fails. Never edits an existing card.
"""
import json, os, subprocess, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def p(n): return os.path.join(ROOT, "content", n)
def load(n): return json.load(open(p(n), encoding="utf-8"))
def dump(n, obj): json.dump(obj, open(p(n), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    bp = sys.argv[1]
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "validate_batch.py"), bp])
    if r.returncode != 0: print("batch rejected; nothing merged"); sys.exit(1)
    batch = json.load(open(bp, encoding="utf-8"))
    thinkers, cards, duos, runs = load("thinkers.json"), load("cards.json"), load("duos.json"), load("runs.json")
    batch_id = batch[0].get("batch") if batch else None
    sources = {}
    for c in batch:
        th = c.pop("thinker", None)
        if th and c["t"] not in thinkers:
            thinkers[c["t"]] = {"n": th["n"], "i": th["i"], "r": th["r"], "w": th["w"], "y": th["y"],
                                "names": {k: v for k, v in th.get("names", {}).items() if v}, "roles": th.get("roles", {})}
        d = c.pop("duo", None)
        if d: duos.append({"a": d["a"], "v": d["v"], "th": d["th"], "br": d["br"]})
        if c.get("source_url"): sources[c["id"]] = c["source_url"]
        c.setdefault("v", False)
        cards.append(c)
    verified = int(sys.argv[sys.argv.index("--verified")+1]) if "--verified" in sys.argv else sum(1 for c in batch if c.get("v"))
    note = sys.argv[sys.argv.index("--note")+1] if "--note" in sys.argv else ""
    runs.append({"at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "batch": batch_id, "by": "lyceum-curator",
                 "ids": [c["id"] for c in batch], "verified": verified, "sources": sources, "note": note})
    dump("thinkers.json", thinkers); dump("cards.json", cards); dump("duos.json", duos); dump("runs.json", runs)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build.py")])
    if r.returncode != 0: print("build failed after merge: fix content/ before committing"); sys.exit(1)
    print(f"merged batch {batch_id}: {len(batch)} cards, {verified} verified; total {len(cards)} cards")

if __name__ == "__main__":
    main()
