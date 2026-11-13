"""Shorten long pauses in a narration and shift the word timings to match (fast explainer format).
Usage: python3 tighten_pauses.py <voice dir with narration.mp3 + words.json> [max_pause=0.35] [lead=0.10]
Every gap between words longer than max_pause is cut down to max_pause (the middle of the silence is removed, with
10 ms fades at each join); leading silence is cut to `lead`. Keeps narration_pretighten.mp3 / words_pretighten.json."""
import json, os, shutil, subprocess, sys
od = sys.argv[1]; mx = float(sys.argv[2]) if len(sys.argv) > 2 else 0.35; lead = float(sys.argv[3]) if len(sys.argv) > 3 else 0.10
na, wj = os.path.join(od, "narration.mp3"), os.path.join(od, "words.json")
shutil.copy(na, os.path.join(od, "narration_pretighten.mp3")); shutil.copy(wj, os.path.join(od, "words_pretighten.json"))
w = json.load(open(wj))
cuts = []  # (from, to) seconds to remove
if w[0]["start"] > lead: cuts.append((0.0, w[0]["start"] - lead))
for a, b in zip(w, w[1:]):
    g = b["start"] - a["end"]
    if g > mx: cuts.append((a["end"] + mx / 2, b["start"] - mx / 2))
keep, t = [], 0.0
for c0, c1 in cuts:
    if c0 > t: keep.append((t, c0))
    t = c1
keep.append((t, None))
parts, labels = [], []
for i, (k0, k1) in enumerate(keep):
    tr = f"atrim=start={k0:.4f}" + (f":end={k1:.4f}" if k1 is not None else "")
    fade = "" if len(keep) == 1 else f",afade=t=in:d=0.01" + (f",areverse,afade=t=in:d=0.01,areverse" if k1 is not None else "")
    parts.append(f"[0:a]{tr},asetpts=PTS-STARTPTS{fade}[p{i}]"); labels.append(f"[p{i}]")
fc = ";".join(parts) + f";{''.join(labels)}concat=n={len(keep)}:v=0:a=1[a]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(od, "narration_pretighten.mp3"), "-filter_complex", fc, "-map", "[a]",
                "-c:a", "libmp3lame", "-b:a", "192k", na], check=True)
def shift(x):
    return x - sum(min(c1, x) - c0 for c0, c1 in cuts if x > c0)
for x in w:
    x["start"] = round(shift(x["start"]), 3); x["end"] = round(shift(x["end"]), 3)
json.dump(w, open(wj, "w"), indent=1)
print(f"tighten: {len(cuts)} cuts, removed {sum(c1 - c0 for c0, c1 in cuts):.2f} s, speech now {w[-1]['end']:.2f} s, {len(w) / w[-1]['end'] * 60:.0f} wpm")
