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
section_cur = None  # fast explainer: the current section header stays up until the next one
CAP_GAP = 0.11      # build captions: seconds between words
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
    if (b.get("caps") is not None or b.get("layout") == "titlecard") and "show" not in b:
        sc["lines"] = []  # these beats carry their own text (caption builds, title card), not the full spoken line
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
    # ---- fast explainer keys (new; absent in older scripts, so they render exactly as before) ----
    cstyle = b.get("caps_style", spec.get("caps_style"))
    if cstyle and b.get("caps") is not None: sc["caps_style"] = cstyle
    if b.get("caps") is not None and cstyle == "story":
        # story captions: sentence case, each word lands on its own spoken word (all at once on an instant hook)
        caps = []
        for cp in b["caps"]:
            keyw = {x.strip(".,!?:").lower() for ph in cp.get("key", []) for x in ph.split()}
            a0 = cp.get("at", 0); q = 0; rows = []
            t0 = sc["start"] if (a0 == 0 or b.get("instant")) else wt(a0)
            for ln in cp["text"].split(" / "):
                row = []
                for w in ln.split():
                    tw = t0 if b.get("instant") else (sc["start"] if a0 + q == 0 else wt(a0 + q))
                    item = {"w": w, "t": round(tw, 3)}
                    if w.strip(".,!?:").lower() in keyw: item["kind"] = "key"
                    row.append(item); q += 1
                rows.append(row)
            caps.append({"t0": t0, "lines": rows})
        sc["caps"] = caps
    elif b.get("caps") is not None:
        caps = []
        for cp in b["caps"]:
            keyw = {x.strip(".,!?").upper() for ph in cp.get("key", []) for x in ph.split()}
            dang = {x.strip(".,!?").upper() for ph in cp.get("danger", []) for x in ph.split()}
            t0 = sc["start"] if cp.get("at", 0) == 0 else wt(cp["at"]); q = 0; rows = []  # word 0 captions land with the cut
            for ln in cp["text"].split(" / "):
                row = []
                for w in ln.split():
                    u = w.strip(".,!?").upper()
                    item = {"w": w.upper(), "t": round(t0 + q * cp.get("gap", CAP_GAP), 3)}
                    if u in dang: item["kind"] = "danger"
                    elif u in keyw: item["kind"] = "key"
                    row.append(item); q += 1
                rows.append(row)
            caps.append({"t0": t0, "lines": rows})
        sc["caps"] = caps
    if b.get("section"):
        section_cur = dict(b["section"], t=sc["start"])
        sc["section"] = section_cur; sc["section_new"] = True
    elif section_cur is not None and b.get("layout") != "titlecard":
        sc["section"] = section_cur
    # ---- story style keys ----
    at_t = lambda a: sc["start"] if not a else wt(a)
    if b.get("stamp"):
        st = dict(b["stamp"]); st["t"] = at_t(st.get("at", 0))
        if "until" in st: st["tu"] = wt(st["until"]) - LEAD
        sc["stamp"] = st
    if b.get("dim"):
        dm = dict(b["dim"]); dm["t"] = at_t(dm.get("at", 0))
        if "until" in dm: dm["tu"] = wt(dm["until"]) - LEAD
        sc["dim"] = dm
    if b.get("paper"):
        cards = [dict(c) for c in b["paper"]]
        for c in cards:
            c["t"] = at_t(c.get("at", 0))
            if "mark_at" in c: c["tm"] = wt(c["mark_at"])
        sc["paper"] = cards
    if b.get("layout") == "map":
        for k in ("region", "collapse"):
            if sc.get(k): sc[k] = dict(sc[k], t=wt(sc[k].get("at", 0)))
    if b.get("hud"):
        hud = dict(b["hud"])
        if hud.get("type") == "stars":
            hud["fill_t"] = [wt(a) for a in hud.get("fill_at", [])]
        elif hud.get("type") == "clues":
            items = [dict(x) for x in hud.get("items") or [{"label": l, "icon": i} for l, i in
                     (("CAMERA", "cctv"), ("PARTNER", "users"), ("CLOTHES", "shirt"), ("FACE", "scan-face"), ("WEAPON", "alert-triangle"), ("CAR", "car"))]]
            for x in items:
                if "red_at" in x: x["tr"] = wt(x["red_at"])
                if "clear_at" in x: x["tc"] = wt(x["clear_at"])
            hud["items"] = items
        sc["hud"] = hud
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
    push = b.get("push", 0.07 if b.get("layout") == "titlecard" else None)  # slow push in (zoom gained over the beat)
    if push: bg[-1]["push"] = push
    if sc.get("dim"):  # story dim line: compose and preview blur the footage locally while it is up
        bg[-1]["blur"] = [sc["dim"]["t"], sc["dim"].get("tu")]

for k in range(len(scenes)):
    scenes[k]["end"] = scenes[k + 1]["start"] if k + 1 < len(scenes) else round(voice_end + 0.35, 3)

end_beat = next((b for b in spec["beats"] if b.get("layout") == "endcard"), None)
duration = scenes[-1]["end"]
if end_beat:
    ec = {k2: v for k2, v in end_beat.items() if k2 not in ("say", "show", "hold")}
    ec.update({"start": duration, "end": round(duration + end_beat.get("hold", 2.0), 3), "noTag": True})
    ec.pop("clips", None); ec.pop("media", None)
    if end_beat.get("clips") or end_beat.get("media"): ec["overFootage"] = True
    scenes.append(ec)
    bg.append({"start": ec["start"], "media": end_beat.get("media"), "media_offset": 0, "pan": end_beat.get("pan", [0.45, 0.55]),
               "clips": [dict(c) for c in end_beat.get("clips") or []] or None, "treat": "blur" if (end_beat.get("clips") or end_beat.get("media")) else None})
    duration = ec["end"]
for k in range(len(bg)):
    bg[k]["end"] = scenes[k]["end"]

tl = {"fps": fps, "duration": round(duration, 3), "tag": spec.get("tag"), "theme": spec["theme"], "scenes": scenes,
      "stills": [round((s["start"] + s["end"]) / 2 + 0.3, 2) for s in scenes]}
if spec.get("loop"): tl["loop"] = True
if spec.get("grain"): tl["grain"] = spec["grain"]
for k in range(len(bg)):
    if bg[k].get("blur") and bg[k]["blur"][1] is None: bg[k]["blur"][1] = bg[k]["end"]
os.makedirs(out, exist_ok=True)
json.dump(tl, open(os.path.join(out, "timeline.json"), "w"), indent=1)
json.dump({"duration": tl["duration"], "segments": bg, "shots_json": spec.get("shots_json"), "sfx": [{"t": s["start"], "kind": "hit" if s.get("flash") or s.get("section_new") or s.get("layout") == "number" else "whoosh"} for s in scenes[1:]]},
          open(os.path.join(out, "bgplan.json"), "w"), indent=1)
print(f"scenes={len(scenes)} duration={tl['duration']}s")
