"""Fast visual check without rendering video: graphics stills composited over the matching footage frame, tiled into one sheet.
Usage: python3 preview.py <dir with timeline.json and bgplan.json> sheet.jpg [t1 t2 ...]   (default: one still per scene)
Mirrors compose.py framing (rotation, letterbox crop, cx, duotone); ignores slow motion and pans, so it is approximate."""
import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
od, sheet = sys.argv[1], sys.argv[2]
tl = json.load(open(os.path.join(od, "timeline.json"))); plan = json.load(open(os.path.join(od, "bgplan.json")))
times = [float(x) for x in sys.argv[3:]] or [round(s["start"] + min(1.6, (s["end"] - s["start"]) * 0.8), 2) for s in tl["scenes"]]
pv = os.path.join(od, "_pv"); os.makedirs(pv, exist_ok=True)
subprocess.run(["node", os.path.join(here, "stills.js"), os.path.join(od, "timeline.json"), pv] + [f"{t:.2f}" for t in times], check=True)
SHOTS = json.load(open(plan["shots_json"])) if plan.get("shots_json") else []
ROTATED = ("7696925363795938573", "7502175479718284586")
LETTERBOX = {"7696925363795938573": (960, 60), "7502175479718284586": (864, 108)}
DUO = ("hue=s=0,eq=contrast=1.12,gblur=sigma=1.4,"
       "curves=r='0/0.03 0.5/0.21 1/0.66':g='0/0.03 0.5/0.11 1/0.37':b='0/0.08 0.5/0.25 1/0.54'")
tiles = []
for t in times:
    seg = next((s for s in plan["segments"] if s["start"] <= t < s["end"]), plan["segments"][-1])
    grade = DUO if seg.get("treat") == "duo" else "eq=saturation=1.06:contrast=1.03"
    bgp = os.path.join(pv, f"b_{t:.2f}.png"); out = os.path.join(pv, f"c_{t:.2f}.jpg")
    if seg.get("clips"):
        cl = seg["clips"]; c = cl[0]
        for x in cl[1:]:
            if "t" in x and x["t"] <= t: c = x
        sh = SHOTS[c["shot"]]; wins = sh.get("clean") or [sh.get("safe", [0, sh["end"] - sh["start"]])]
        o0 = c.get("offset", 0); lo, hi = next((w for w in wins if w[0] - 0.05 <= o0 <= w[1]), min(wins, key=lambda w: min(abs(o0 - w[0]), abs(o0 - w[1]))))
        off = min(max(c.get("offset", 0), lo), max(lo, hi - 0.6)); src = sh["src"]
        start = c.get("t", seg["start"]); ss = sh["start"] + off + min(max(0, t - start), max(0, hi - off - 0.05))
        if any(r in src for r in ROTATED) if c.get("rot") is None else c["rot"]:
            H, Y = next((v for k, v in LETTERBOX.items() if k in src), (1080, 0)); W = int(round(H * 9 / 16 / 2) * 2)
            geo = f"transpose=2,crop=1920:{H}:0:{Y},crop={W}:{H}:x='(iw-ow)*{c.get('cx', 0.5)}':y=0,scale=1080:1920:flags=lanczos"
        else:
            geo = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        cmd = ["-ss", f"{ss:.3f}", "-i", src, "-frames:v", "1", "-vf", f"{geo},{grade}"]
    elif seg.get("media") and seg["media"].lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        a = seg.get("pan", [0.4, 0.6])[0]
        cmd = ["-i", seg["media"], "-frames:v", "1", "-vf", f"scale=-2:2400,crop=1350:2400:x='(iw-ow)*{a}':y='(ih-oh)/2',scale=1080:1920,{grade}"]
    elif seg.get("media"):
        cmd = ["-ss", str(seg.get("media_offset", 0) + max(0, t - seg["start"])), "-i", seg["media"], "-frames:v", "1",
               "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{grade}"]
    else:
        cmd = ["-f", "lavfi", "-i", "color=c=0x08080B:s=1080x1920", "-frames:v", "1"]
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + cmd + [bgp], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", bgp, "-i", os.path.join(pv, f"g_{t:.2f}.png"), "-filter_complex",
                    "[0][1]overlay=0:0,scale=270:480", "-frames:v", "1", out], check=True)
    tiles.append(os.path.abspath(out))
cols = 6 if len(tiles) > 10 else 5
lst = os.path.join(pv, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in tiles))
rows = (len(tiles) + cols - 1) // cols
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-vf", f"tile={cols}x{rows}:padding=4", "-frames:v", "1", sheet], check=True)
print("sheet", sheet, "|", len(tiles), "stills at", ", ".join(f"{t:.1f}" for t in times))
