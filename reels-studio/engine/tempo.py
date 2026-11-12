"""Speed up narration without pitch change and rescale word timings. Usage: python3 tempo.py outdir 1.08"""
import json, os, subprocess, sys
od, f = sys.argv[1], float(sys.argv[2])
src = os.path.join(od, "narration_raw.mp3")
if not os.path.exists(src):
    os.rename(os.path.join(od, "narration.mp3"), src)
    os.rename(os.path.join(od, "words.json"), os.path.join(od, "words_raw.json"))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", f"atempo={f}", "-c:a", "libmp3lame", "-b:a", "192k", os.path.join(od, "narration.mp3")], check=True)
w = json.load(open(os.path.join(od, "words_raw.json")))
for x in w:
    x["start"] = round(x["start"] / f, 3); x["end"] = round(x["end"] / f, 3)
json.dump(w, open(os.path.join(od, "words.json"), "w"), indent=1)
print(f"tempo {f}: speech {w[-1]['end']:.2f}s, wpm {len(w)/w[-1]['end']*60:.0f}")
