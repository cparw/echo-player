"""Turn script.json + words.json into timeline.json (graphics) and bgplan.json (background media).
Usage: python3 build.py script.json words.json outdir
Show word markup: *word* = highlighter box, ^word^ = accent colour, ~word~ = teal.
"""
import json, sys, os

spec = json.load(open(sys.argv[1]))
words = json.load(open(sys.argv[2]))
out = sys.argv[3]
fps = spec.get("fps", 30)
LEAD = 0.06

def parse(tok):
    anchor = None
    if "@" in tok and tok.rsplit("@", 1)[1].isdigit():
        tok, a = tok.rsplit("@", 1); anchor = int(a)
    for mark, kind in (("*", "box"), ("^", "color"), ("~", "teal")):
        if len(tok) > 2 and tok.startswith(mark) and tok.endswith(mark):
            return tok[1:-1], kind, anchor
    return tok, None, anchor

# assign spoken words to beats in order
i = 0
spoken = []
for b in spec["beats"]:
    n = len(b.get("say", "").split()) if b.get("say") else 0
    spoken.append(words[i:i + n]); i += n
assert i == len(words), f"word mismatch: used {i} of {len(words)}"

scenes, bg = [], []
voice_end = words[-1]["end"]
for k, (b, sw) in enumerate(zip(spec["beats"], spoken)):
    if b.get("layout") == "endcard":
        continue
    start = 0.0 if k == 0 else max(0.0, sw[0]["start"] - LEAD)
    sc = {k2: v for k2, v in b.items() if k2 not in ("say", "show", "media", "media_offset", "clips", "pan")}
    sc["start"] = round(start, 3)
    lines = []
    if b.get("clips"):
        sc["credit"] = b.get("credit", "FOOTAGE: ROCKSTAR GAMES")
    elif b.get("media"):
        if b["media"].lower().endswith((".jpg", ".jpeg", ".png", ".webp")) or "/official/" in b["media"]:
            sc["credit"] = b.get("credit", "IMAGE: ROCKSTAR GAMES")
        else:
            sc["ai"] = True
    show = b["show"] if "show" in b else [b["say"].split()]
    flat = [w for ln in show for w in ln]
    N, M = len(flat), len(sw)
    j = 0
    for ln in show:
        row = []
        for tok in ln:
            w, kind, anchor = parse(tok)
            idx = anchor if anchor is not None else (0 if N <= 1 else round(j * (M - 1) / (N - 1)))
            t = sw[min(idx, M - 1)]["start"] if M else start
            item = {"w": w, "t": round(t, 3)}
            if kind: item["accent"] = kind
            row.append(item); j += 1
        lines.append(row)
    sc["lines"] = lines
    if b.get("layout") == "number":
        ci = b.get("count_at", 0)
        sc["t0"] = round(sw[min(ci, M - 1)]["start"], 3)
        sc["t1"] = round(sc["t0"] + b.get("count_dur", 1.0), 3)
    if b.get("layout") == "bars":
        sc["t0"] = round(sw[min(b.get("bars_at", 0), M - 1)]["start"], 3)
        for q, bar in enumerate(sc["bars"]):
            bar["t"] = round(sw[min(bar["at"], M - 1)]["start"], 3) if "at" in bar else round(sc["t0"] + q * b.get("bar_gap", 0.28), 3)
    if b.get("layout") == "list":
        for item in sc["items"]:
            item["t"] = round(sw[min(item.get("at", 0), M - 1)]["start"], 3)
            if "strike_at" in item:
                item["ts"] = round(sw[min(item["strike_at"], M - 1)]["start"], 3)
    wt = lambda a: round(sw[min(a, M - 1)]["start"], 3) if M else sc["start"]
    if b.get("layout") == "waffle":
        sc["t0"] = wt(b.get("fill_at", 0))
    if b.get("layout") == "versus":
        for side in ("left", "right"):
            if sc.get(side) and "at" in sc[side]:
                sc[side]["t"] = wt(sc[side]["at"])
    if b.get("layout") == "map":
        for cy in sc.get("cities", []):
            cy["t"] = wt(cy.get("at", 0))
        if sc.get("sweep"):
            sc["sweep"]["t"] = wt(sc["sweep"].get("at", 0))
    clips = None
    if b.get("clips"):
        # cut on the spoken word: a clip with "at" starts LEAD before that word; the first clip starts with the scene
        clips = [dict(c) for c in b["clips"]]
        for q, c in enumerate(clips):
            if q == 0: c["t"] = sc["start"]
            elif "at" in c: c["t"] = round(max(sc["start"], wt(c["at"]) - LEAD), 3)
    scenes.append(sc)
    bg.append({"start": sc["start"], "media": b.get("media"), "media_offset": b.get("media_offset", 0), "pan": b.get("pan", [0.40, 0.60]),
               "clips": clips, "treat": "duo" if b.get("bg") == "duo" else b.get("treat")})

for k in range(len(scenes)):
    scenes[k]["end"] = scenes[k + 1]["start"] if k + 1 < len(scenes) else round(voice_end + 0.35, 3)

end_beat = next((b for b in spec["beats"] if b.get("layout") == "endcard"), None)
duration = scenes[-1]["end"]
if end_beat:
    ec = {k2: v for k2, v in end_beat.items() if k2 not in ("say", "show", "hold")}
    ec.update({"start": duration, "end": round(duration + end_beat.get("hold", 2.0), 3), "noTag": True})
    scenes.append(ec)
    bg.append({"start": ec["start"], "media": None, "media_offset": 0})
    duration = ec["end"]
for k in range(len(bg)):
    bg[k]["end"] = scenes[k]["end"]

tl = {"fps": fps, "duration": round(duration, 3), "tag": spec.get("tag"), "theme": spec["theme"], "scenes": scenes,
      "stills": [round((s["start"] + s["end"]) / 2 + 0.3, 2) for s in scenes]}
os.makedirs(out, exist_ok=True)
json.dump(tl, open(os.path.join(out, "timeline.json"), "w"), indent=1)
json.dump({"duration": tl["duration"], "segments": bg, "shots_json": spec.get("shots_json"), "sfx": [{"t": s["start"], "kind": "hit" if s.get("flash") or s.get("layout") == "number" else "whoosh"} for s in scenes[1:]]},
          open(os.path.join(out, "bgplan.json"), "w"), indent=1)
print(f"scenes={len(scenes)} duration={tl['duration']}s")
