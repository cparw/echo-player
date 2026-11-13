"""Frame by frame audit tiles for GTA V trailer shots: the FULL active picture (letterbox removed), every STEP s, time burned in.
Every crop the engine can take (9:8 split half or 9:16 full) lies inside this frame, so a clean tile is clean for both.
Usage: python3 audit_tiles_gta5.py cuts.json out_dir ids(comma list) [step=0.4] [per_sheet=24]"""
import json, os, subprocess, sys
cuts = json.load(open(sys.argv[1])); out = sys.argv[2]; ids = [int(x) for x in sys.argv[3].split(",")]
step = float(sys.argv[4]) if len(sys.argv) > 4 else 0.4; per = int(sys.argv[5]) if len(sys.argv) > 5 else 24
os.makedirs(out, exist_ok=True)
ACTIVE = {"r3too449": (0, 216, 3840, 1728), "ks18e7s9": (0, 216, 3840, 1728), "1s626s55": (0, 0, 3840, 2160),
          "tr45r42o": (0, 108, 1920, 864), "kc1a9kco": (0, 108, 1920, 864), "s6rrr5ao": (0, 110, 1920, 860), "s7kr6392": (0, 0, 1920, 1080)}
tiles = []
for n in ids:
    s = cuts[n]; x, y, w, h = ACTIVE[s["vid"]]; L = s["end"] - s["start"]
    k = max(1, int(L / step + 0.999))
    for i in range(k):
        t = round(min(L - 0.04, i * step), 2)
        f = os.path.join(out, f"_a{n:03d}_{i:02d}.jpg")
        lab = f"{n} @{t:.1f}s"
        th = int(round(480 * h / w / 2) * 2)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{s['start'] + t:.3f}", "-i", s["src"], "-frames:v", "1", "-vf",
                        f"crop={w}:{h}:{x}:{y},scale=480:{th},pad=480:272:0:(272-ih)/2:black,drawbox=x=0:y=0:w=110:h=24:color=black@0.75:t=fill,drawtext=text='{lab}':x=4:y=4:fontsize=17:fontcolor=yellow", f], check=True)
        tiles.append(f)
    tiles += [None] * ((-len(tiles)) % 4)  # each shot starts on a new row
sheets = []
for p in range(0, len(tiles), per):
    grp = [t for t in tiles[p:p + per]]
    lst = os.path.join(out, "_l.txt"); body = ""
    for t in grp:
        if t is None:
            t = os.path.join(out, "_blank.jpg")
            if not os.path.exists(t): subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=0x202020:s=480x272", "-frames:v", "1", t], check=True)
        body += f"file '{os.path.abspath(t)}'\n"
    open(lst, "w").write(body)
    rows = (len(grp) + 3) // 4; name = os.path.join(out, f"audit_{p // per:02d}.jpg")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-vf", f"tile=4x{rows}:padding=3", "-frames:v", "1", name], check=True)
    sheets.append(name)
for t in tiles:
    if t: os.remove(t)
print(len([t for t in tiles if t]), "frames ->", len(sheets), "sheets")
