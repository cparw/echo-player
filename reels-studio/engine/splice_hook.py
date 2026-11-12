"""Replace only the opening lines of an already voiced reel: record the new hook in the owner's voice, stitch it onto the
existing narration, and rebuild word timings. Saves voice credits versus re-recording the whole reel.
Usage: python3 splice_hook.py <reel_dir> <old_voice_dir> <n_old_beats_removed> <n_new_hook_beats> <out_voice_dir>
<reel_dir>/script.json must already start with the new hook beats, followed by the kept old beats (unchanged say text).
"""
import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
reel, old_dir, n_removed, n_new, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
os.makedirs(out, exist_ok=True)
spec = json.load(open(os.path.join(reel, "script.json")))
old_spec = json.load(open(os.path.join(old_dir, "script_at_voice.json")))
old_words = json.load(open(os.path.join(old_dir, "words.json")))
raw_words = json.load(open(os.path.join(old_dir, "words_raw.json"))) if os.path.exists(os.path.join(old_dir, "words_raw.json")) else old_words
factor = raw_words[-1]["end"] / old_words[-1]["end"]
said = lambda b: b.get("say") or ""
k = sum(len(said(b).split()) for b in old_spec["beats"][:n_removed])
kept_text = [said(b) for b in old_spec["beats"][n_removed:] if said(b)]
new_kept = [said(b) for b in spec["beats"][n_new:] if said(b)]
assert kept_text == new_kept, "kept beats changed their spoken text; re-record instead"
# 1) record the hook only
hook_dir = os.path.join(out, "_hook"); os.makedirs(hook_dir, exist_ok=True)
hspec = dict(spec); hspec["beats"] = spec["beats"][:n_new]
json.dump(hspec, open(os.path.join(hook_dir, "script.json"), "w"), indent=1)
subprocess.run(["python3", os.path.join(here, "tts_sts.py"), os.path.join(hook_dir, "script.json"), hook_dir], check=True)
hw = json.load(open(os.path.join(hook_dir, "words.json")))
for x in hw: x["start"] = round(x["start"] / factor, 3); x["end"] = round(x["end"] / factor, 3)
hook_end = hw[-1]["end"] + 0.12
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(hook_dir, "narration.mp3"), "-af", f"atempo={factor:.4f}",
                "-t", f"{hook_end:.3f}", os.path.join(hook_dir, "hook_tempo.wav")], check=True)
# 2) keep the old narration from just before its first kept word
t_cut = max(0.0, old_words[k]["start"] - 0.08) if k > 0 else 0.0
gap = 0.22
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(hook_dir, "hook_tempo.wav"),
                "-f", "lavfi", "-t", f"{gap}", "-i", "anullsrc=r=44100:cl=mono",
                "-ss", f"{t_cut:.3f}", "-i", os.path.join(old_dir, "narration.mp3"),
                "-filter_complex", "[0:a]aresample=44100,aformat=channel_layouts=mono[a];[1:a]aformat=channel_layouts=mono[b];"
                "[2:a]aresample=44100,aformat=channel_layouts=mono[c];[a][b][c]concat=n=3:v=0:a=1[o]",
                "-map", "[o]", "-c:a", "libmp3lame", "-b:a", "192k", os.path.join(out, "narration.mp3")], check=True)
shift = hook_end + gap - t_cut
words = hw + [{"w": x["w"], "start": round(x["start"] + shift, 3), "end": round(x["end"] + shift, 3)} for x in old_words[k:]]
json.dump(words, open(os.path.join(out, "words.json"), "w"), indent=1)
json.dump(spec, open(os.path.join(out, "script.json"), "w"), indent=1, ensure_ascii=False)
expected = sum(len(said(b).split()) for b in spec["beats"])
print(f"hook words {len(hw)}, kept words {len(old_words) - k}, total {len(words)} (script expects {expected}); hook {hook_end:.2f}s, cut old at {t_cut:.2f}s")
assert len(words) == expected
