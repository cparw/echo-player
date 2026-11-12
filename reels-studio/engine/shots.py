"""Detect shots in official clips and write shots.json [{src, start, end, dur}] plus a numbered contact sheet.
Usage: python3 shots.py out_dir clip1.mp4 clip2.mp4 ...
"""
import json, os, re, subprocess, sys
out = sys.argv[1]; clips = sys.argv[2:]
os.makedirs(out, exist_ok=True)
shots = []
for c in clips:
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", c], capture_output=True, text=True).stdout)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", c, "-vf", "scale=270:480,select='gt(scene,0.32)',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True)
    cuts = [0.0] + [float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)] + [dur]
    for a, b in zip(cuts, cuts[1:]):
        if b - a >= 0.9:
            shots.append({"src": os.path.abspath(c), "start": round(a + 0.05, 2), "end": round(b - 0.05, 2), "dur": round(b - a - 0.1, 2)})
json.dump(shots, open(os.path.join(out, "shots.json"), "w"), indent=1)
# thumbnails at shot midpoints
thumbs = []
for i, s in enumerate(shots):
    t = os.path.join(out, f"s{i:03d}.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str((s["start"] + s["end"]) / 2), "-i", s["src"], "-frames:v", "1",
                    "-vf", f"scale=160:284,drawtext=text='{i}':x=4:y=4:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.7", t])
    thumbs.append(t)
cols = 14
for page in range(0, len(thumbs), cols * 4):
    group = thumbs[page:page + cols * 4]
    args = []
    for t in group: args += ["-i", t]
    n = len(group); rows = (n + cols - 1) // cols
    fc = "".join(f"[{i}:v]setsar=1[t{i}];" for i in range(n))
    for i in range(n, rows * cols): fc += f"color=c=gray:s=160x284:d=1[t{i}];"
    fc += "".join(f"[t{i}]" for i in range(rows * cols)) + f"xstack=inputs={rows*cols}:layout=" + "|".join(f"{(i%cols)*160}_{(i//cols)*284}" for i in range(rows * cols))
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + args + ["-filter_complex", fc, "-frames:v", "1", os.path.join(out, f"sheet_{page//(cols*4)}.jpg")], check=True)
print(len(shots), "shots; sheets:", sorted(f for f in os.listdir(out) if f.startswith("sheet_")))
