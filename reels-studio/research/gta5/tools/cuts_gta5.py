"""Cut detection for landscape GTA V trailers + one labelled thumbnail per shot (full 16:9 frame).
Usage: python3 cuts_gta5.py out_dir clip1.mp4 clip2.mp4 ...   -> out_dir/cuts.json, out_dir/overview_N.jpg"""
import json, os, re, subprocess, sys
out = sys.argv[1]; clips = sys.argv[2:]; os.makedirs(out, exist_ok=True)
shots = []
for c in clips:
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", c], capture_output=True, text=True).stdout)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", c, "-vf", "scale=320:180,select='gt(scene,0.24)',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True)
    cuts = [0.0] + [float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)] + [dur]
    vid = os.path.basename(c).split(".")[0]
    for a, b in zip(cuts, cuts[1:]):
        if b - a >= 0.7:
            shots.append({"vid": vid, "src": os.path.abspath(c), "start": round(a + 0.05, 2), "end": round(b - 0.05, 2), "dur": round(b - a - 0.1, 2)})
json.dump(shots, open(os.path.join(out, "cuts.json"), "w"), indent=1)
thumbs = []
for i, s in enumerate(shots):
    t = os.path.join(out, f"_t{i:03d}.jpg")
    lab = f"{i} {s['vid']} {s['start']:.1f}+{s['dur']:.1f}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str((s["start"] + s["end"]) / 2), "-i", s["src"], "-frames:v", "1",
                    "-vf", f"scale=384:216,drawbox=x=0:y=0:w=384:h=26:color=black@0.75:t=fill,drawtext=text='{lab}':x=4:y=4:fontsize=17:fontcolor=yellow", t], check=True)
    thumbs.append(t)
per = 30
for p in range(0, len(thumbs), per):
    grp = thumbs[p:p + per]; lst = os.path.join(out, "_l.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in grp))
    rows = (len(grp) + 4) // 5
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-vf", f"tile=5x{rows}:padding=3", "-frames:v", "1",
                    os.path.join(out, f"overview_{p // per}.jpg")], check=True)
for t in thumbs: os.remove(t)
print(len(shots), "shots")
