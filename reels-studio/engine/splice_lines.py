"""Re-record only the spoken lines that changed in an already voiced reel (opening, middle or ending), in the owner's voice,
and stitch them into the existing narration with matched pace and loudness. A block of lines can also be cut (no new audio).
Saves credits versus re-recording the reel.
Usage: python3 splice_lines.py <new_voice_spec.json> <old_voice_dir> <out_voice_dir>
<new_voice_spec.json>: voice settings plus beats with "say" (only beats with say are used). The changed lines must form one
contiguous block; lines before and after it must be word for word identical to <old_voice_dir>/script_at_voice.json.
For several separate changes use splice_multi.py.
"""
import json, os, re, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
spec_path, old_dir, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
spec = json.load(open(spec_path))
old_spec = json.load(open(os.path.join(old_dir, "script_at_voice.json")))
old_words = json.load(open(os.path.join(old_dir, "words.json")))
rawp = os.path.join(old_dir, "words_raw.json")
raw_words = json.load(open(rawp)) if os.path.exists(rawp) else old_words
F = raw_words[-1]["end"] / old_words[-1]["end"]
old = [b["say"].strip() for b in old_spec["beats"] if b.get("say")]
new = [b["say"].strip() for b in spec["beats"] if b.get("say")]
nw = lambda xs: sum(len(x.split()) for x in xs)
assert len(old_words) == nw(old), f"old words.json has {len(old_words)} words, old script {nw(old)}"
a = 0
while a < min(len(old), len(new)) and old[a] == new[a]: a += 1
s = 0
while s < min(len(old), len(new)) - a and old[-1 - s] == new[-1 - s]: s += 1
old_mid, new_mid = old[a:len(old) - s], new[a:len(new) - s]
assert old_mid or new_mid, "nothing changed"
k0, k1 = nw(old[:a]), nw(old[:len(old) - s])
src = os.path.join(old_dir, "narration.mp3")

def run(cmd): subprocess.run(cmd, check=True)
def lufs(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    v = re.findall(r"I:\s+(-?\d+(?:\.\d+)?) LUFS", r.stderr)
    return float(v[-1]) if v else None

# 1) record only the new lines, at the reel's pace and loudness
mw, mid_dur, gain = [], 0.0, 0.0
if new_mid:
    mid_dir = os.path.join(out, "_mid"); os.makedirs(mid_dir, exist_ok=True)
    mspec = {k: v for k, v in spec.items() if k != "beats"}; mspec["beats"] = [{"say": x} for x in new_mid]
    json.dump(mspec, open(os.path.join(mid_dir, "script.json"), "w"), indent=1, ensure_ascii=False)
    run(["python3", os.path.join(here, "tts_sts.py"), os.path.join(mid_dir, "script.json"), mid_dir])
    mw = json.load(open(os.path.join(mid_dir, "words.json")))
    for x in mw: x["start"] = round(x["start"] / F, 3); x["end"] = round(x["end"] / F, 3)
    mid_dur = mw[-1]["end"] + 0.12
    mid_wav = os.path.join(mid_dir, "mid_tempo.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(mid_dir, "narration.mp3"), "-af", f"atempo={F:.4f},aresample=44100",
         "-ac", "1", "-t", f"{mid_dur:.3f}", mid_wav])
    lo, lm = lufs(src), lufs(mid_wav)
    gain = max(-6.0, min(6.0, lo - lm)) if lo is not None and lm is not None else 0.0
# 2) cut points in the old narration
gap = 0.30
t0 = 0.0
if a > 0:
    t0 = old_words[k0 - 1]["end"] + 0.10
    if k0 < len(old_words): t0 = min(t0, old_words[k0]["start"] - 0.02)
t1 = max(old_words[k1]["start"] - 0.08, t0) if s > 0 else None
segs = []  # (ffmpeg input args, filter for that input)
if a > 0: segs.append((["-t", f"{t0:.3f}", "-i", src], f"aresample=44100,aformat=channel_layouts=mono,afade=t=out:st={max(0, t0 - 0.015):.3f}:d=0.015"))
if new_mid: segs.append((["-i", mid_wav], f"aformat=channel_layouts=mono,volume={gain:.2f}dB,afade=t=in:d=0.015"))
if s > 0: segs.append((["-ss", f"{t1:.3f}", "-i", src], "aresample=44100,aformat=channel_layouts=mono,afade=t=in:d=0.015"))
args, filt, labels, n = [], [], [], 0
for k, (inp, f) in enumerate(segs):
    if k > 0:
        args += ["-f", "lavfi", "-t", f"{gap}", "-i", "anullsrc=r=44100:cl=mono"]; filt.append(f"[{n}:a]aformat=channel_layouts=mono[p{n}]"); labels.append(f"[p{n}]"); n += 1
    args += inp; filt.append(f"[{n}:a]{f}[p{n}]"); labels.append(f"[p{n}]"); n += 1
fc = ";".join(filt) + ";" + "".join(labels) + f"concat=n={n}:v=0:a=1[o]"
run(["ffmpeg", "-y", "-v", "error", *args, "-filter_complex", fc, "-map", "[o]", "-c:a", "libmp3lame", "-b:a", "192k", os.path.join(out, "narration.mp3")])
# 3) word timings
cur = t0 if a > 0 else 0.0
words = [dict(x) for x in old_words[:k0]]
if new_mid:
    if a > 0: cur += gap
    words += [{"w": x["w"], "start": round(x["start"] + cur, 3), "end": round(x["end"] + cur, 3)} for x in mw]
    cur += mid_dur
if s > 0:
    if a > 0 or new_mid: cur += gap
    sh = cur - t1
    words += [{"w": x["w"], "start": round(x["start"] + sh, 3), "end": round(x["end"] + sh, 3)} for x in old_words[k1:]]
assert len(words) == nw(new), f"{len(words)} words vs script {nw(new)}"
json.dump(words, open(os.path.join(out, "words.json"), "w"), indent=1)
json.dump([{"w": x["w"], "start": round(x["start"] * F, 3), "end": round(x["end"] * F, 3)} for x in words],
          open(os.path.join(out, "words_raw.json"), "w"), indent=1)
json.dump(spec, open(os.path.join(out, "script_at_voice.json"), "w"), indent=1, ensure_ascii=False)
msg = (f"kept {a} lines before and {s} after; replaced {len(old_mid)} old lines ({k1 - k0} words) with {len(new_mid)} new "
       f"({nw(new_mid)} words); pace factor {F:.3f}; gain {gain:+.2f} dB; speech {words[-1]['end']:.2f} s")
open(os.path.join(out, "splice_report.txt"), "w").write(msg + "\n"); print(msg)
