"""Print each beat with layout, background, clips/media and the spoken words with indices and timings.
Usage: python3 beats.py script.json [words.json]"""
import json, sys, os
s = json.load(open(sys.argv[1]))
w = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None
i = 0
for k, b in enumerate(s["beats"]):
    lay = b.get("layout", "words")
    if lay == "endcard":
        print(k, "ENDCARD", {x: b.get(x) for x in ("brand", "series", "episode", "cta")}); continue
    n = len(b["say"].split())
    vis = [(c["shot"], c.get("offset", 0), c.get("at")) for c in b.get("clips") or []] or os.path.basename(b.get("media") or "") or "-"
    extra = {x: b[x] for x in ("from", "to", "label", "items", "bars", "footnote", "icon", "attrib") if x in b}
    if w:
        sw = w[i:i + n]; i += n
        words = " ".join(f"{x['w']}({j})" for j, x in enumerate(sw))
        print(f"{k} [{lay}/{b.get('bg')}] {sw[0]['start']:.1f}-{sw[-1]['end']:.1f}s ({sw[-1]['end']-sw[0]['start']:.1f}) vis={vis}\n    {words}")
    else:
        print(f"{k} [{lay}/{b.get('bg')}] vis={vis}\n    {b['say']}")
    if extra: print("    ", json.dumps(extra, ensure_ascii=False)[:300])
