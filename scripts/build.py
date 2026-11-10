#!/usr/bin/env python3
"""Build dist/index.html from site/index.template.html + content/*.json.
Fails on referential errors (unknown thinker, unknown topic, duo pointing to a missing card).
usage: python3 scripts/build.py [--out dist/index.html]
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n): return json.load(open(os.path.join(ROOT, "content", n), encoding="utf-8"))
def js(v): return json.dumps(v, ensure_ascii=False, separators=(",", ":"))

def main():
    out = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else os.path.join(ROOT, "dist", "index.html")
    topics, thinkers, cards, duos = load("topics.json"), load("thinkers.json"), load("cards.json"), load("duos.json")
    errs = []
    ids = {c["id"] for c in cards}
    if len(ids) != len(cards): errs.append("duplicate card ids")
    for c in cards:
        if c["t"] not in thinkers: errs.append(f"{c['id']}: unknown thinker {c['t']}")
        for t in c["tg"]:
            if t not in topics["ids"]: errs.append(f"{c['id']}: unknown topic {t}")
        if c["t"] in thinkers and thinkers[c["t"]]["w"] != c["id"][0]: errs.append(f"{c['id']}: id series does not match thinker wing")
    for d in duos:
        if d["a"] not in ids or d["v"] not in ids: errs.append(f"duo {d['a']}-{d['v']}: missing card")
        if d["th"] not in topics["ids"]: errs.append(f"duo {d['a']}-{d['v']}: unknown topic")
    if errs:
        print("\n".join(errs)); sys.exit(1)
    TOPICS = [[k, topics["names"]["en"][k]] for k in topics["ids"]]
    THINKERS = {k: {x: t[x] for x in ("n", "i", "r", "w", "y")} for k, t in thinkers.items()}
    TNAME = {l: {k: t["names"][l] for k, t in thinkers.items() if t.get("names", {}).get(l)} for l in ("it", "es", "la")}
    TROLE = {l: {k: t["roles"][l] for k, t in thinkers.items() if t.get("roles", {}).get(l)} for l in ("it", "es", "la")}
    CARDS = [{k: c[k] for k in ("id", "t", "era", "src", "h", "b", "d", "tg", "v", "added") if k in c} for c in cards]
    L = {l: {c["id"]: c["tr"][l] for c in cards if c.get("tr", {}).get(l)} for l in ("it", "es", "la")}
    DUOS = [{"a": d["a"], "v": d["v"], "th": d["th"], "br": d["br"]} for d in duos]
    block = (f"const TOPICS={js(TOPICS)};const TOPN={js(topics['names'])};const THINKERS={js(THINKERS)};"
             f"const TNAME={js(TNAME)};const TROLE={js(TROLE)};const CARDS={js(CARDS)};const L={js(L)};const DUOS={js(DUOS)};")
    tpl = open(os.path.join(ROOT, "site", "index.template.html"), encoding="utf-8").read()
    if "/*__LYCEUM_DATA__*/" not in tpl: print("template placeholder missing"); sys.exit(1)
    html = tpl.replace("/*__LYCEUM_DATA__*/", block)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    print(f"built {out}: {len(cards)} cards, {len(thinkers)} thinkers, {len(duos)} duos, {sum(1 for c in cards if c['v'])} verified")

if __name__ == "__main__":
    main()
