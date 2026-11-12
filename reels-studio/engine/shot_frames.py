"""Audit sheets: frames of each shot exactly as the reel shows them (9:16 crop, rotation and letterbox fixed), timestamp burned in.
Usage: python3 shot_frames.py <shots.json> <outdir> <shot ids, e.g. 0-19 or 5,9,22> [step_seconds=0.4] [cx=0.5]
Writes <outdir>/shot_NN.jpg (one row of frames per shot, label = seconds into the shot)."""
import json, os, subprocess, sys
shots = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
spec = sys.argv[3]; step = float(sys.argv[4]) if len(sys.argv) > 4 else 0.4; cx = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
ids = []
for part in spec.split(","):
    if "-" in part: a, b = map(int, part.split("-")); ids += list(range(a, b + 1))
    else: ids.append(int(part))
ROTATED = ("7696925363795938573", "7502175479718284586")
LETTERBOX = {"7696925363795938573": (960, 60), "7502175479718284586": (864, 108)}
for n in ids:
    if n >= len(shots): continue
    sh = shots[n]; src = sh["src"]; L = sh["end"] - sh["start"]
    if any(r in src for r in ROTATED):
        H, Y = next((v for k, v in LETTERBOX.items() if k in src), (1080, 0)); W = int(round(H * 9 / 16 / 2) * 2)
        geo = f"transpose=2,crop=1920:{H}:0:{Y},crop={W}:{H}:x='(iw-ow)*{cx}':y=0,scale=216:384"
    else:
        geo = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale=216:384"
    k = max(1, int(L / step + 0.999)); k = min(k, 30)
    times = [round(min(L - 0.05, i * step), 2) for i in range(k)]
    frames = []
    for i, t in enumerate(times):
        f = os.path.join(out, f"_f{n}_{i:02d}.jpg")
        lab = f"{n} @{t:.1f}s"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{sh['start'] + t:.3f}", "-i", src, "-frames:v", "1", "-vf",
                        f"{geo},drawbox=x=0:y=0:w=216:h=30:color=black@0.7:t=fill,drawtext=text='{lab}':x=6:y=6:fontsize=20:fontcolor=white", f], check=True)
        frames.append(f)
    cols = min(len(frames), 10); rows = (len(frames) + cols - 1) // cols
    lst = os.path.join(out, f"_l{n}.txt"); open(lst, "w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in frames))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-vf", f"tile={cols}x{rows}:padding=3", "-frames:v", "1",
                    os.path.join(out, f"shot_{n:02d}.jpg")], check=True)
    for x in frames: os.remove(x)
    os.remove(lst)
    print(f"shot {n}: {L:.1f}s, {len(frames)} frames -> shot_{n:02d}.jpg")
