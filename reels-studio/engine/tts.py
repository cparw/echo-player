"""Narration with word timings via ElevenLabs /with-timestamps.
Usage: python3 tts.py script.json outdir
Writes outdir/narration.mp3 and outdir/words.json ([{w, start, end}]).
"""
import base64, json, os, subprocess, sys

spec = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
text = " ".join(b["say"].strip() for b in spec["beats"] if b.get("say"))
body = {"text": text, "model_id": spec.get("model_id", "eleven_multilingual_v2"),
        "voice_settings": spec.get("voice_settings", {"stability": 0.45, "similarity_boost": 0.85, "style": 0.2, "use_speaker_boost": True})}
if spec.get("seed") is not None:
    body["seed"] = spec["seed"]
url = f"https://api.elevenlabs.io/v1/text-to-speech/{spec['voice_id']}/with-timestamps?output_format=mp3_44100_128"
r = subprocess.run(["curl", "-sS", "-X", "POST", url, "-H", "xi-api-key: dummy", "-H", "Content-Type: application/json",
                    "--data-binary", json.dumps(body)], capture_output=True, text=True, check=True)
d = json.loads(r.stdout)
if "audio_base64" not in d:
    sys.exit("TTS error: " + r.stdout[:800])
open(os.path.join(out, "narration.mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
al = d.get("alignment") or d.get("normalized_alignment")
chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
words, cur = [], None
for c, s, e in zip(chars, st, en):
    if c.isspace():
        if cur: words.append(cur); cur = None
        continue
    if cur is None: cur = {"w": c, "start": s, "end": e}
    else: cur["w"] += c; cur["end"] = e
if cur: words.append(cur)
json.dump(words, open(os.path.join(out, "words.json"), "w"), indent=1)
expected = len(text.split())
print(f"chars={len(text)} words={len(words)} expected={expected} duration={words[-1]['end']:.2f}s wpm={len(words)/max(words[-1]['end'],1)*60:.0f}")
if len(words) != expected:
    print("WARNING: word count mismatch; check alignment")
