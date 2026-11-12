"""Narration in the user's voice with a directed delivery:
guide performance (licensed ElevenLabs voice, with word timestamps) -> Speech to Speech into the user's clone.
Speech to Speech keeps the guide's timing, so the guide's word timestamps stay valid for on screen sync.
Usage: python3 tts_sts.py script.json outdir
script.json keys used: say texts, voice_id (the user's clone), guide_voice_id, guide_speed (default 1.15).
"""
import base64, json, os, subprocess, sys

spec = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
text = " ".join(b["say"].strip() for b in spec["beats"] if b.get("say"))
guide = spec.get("guide_voice_id", "cjVigY5qzO86Huf0OWal")
body = {"text": text, "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": spec.get("guide_stability", 0.42), "similarity_boost": 0.75,
                           "style": spec.get("guide_style", 0.1), "use_speaker_boost": True,
                           "speed": spec.get("guide_speed", 1.15)}}
r = subprocess.run(["curl", "-sS", "-X", "POST",
                    f"https://api.elevenlabs.io/v1/text-to-speech/{guide}/with-timestamps?output_format=mp3_44100_128",
                    "-H", "xi-api-key: dummy", "-H", "Content-Type: application/json", "--data-binary", json.dumps(body)],
                   capture_output=True, text=True, check=True)
d = json.loads(r.stdout)
if "audio_base64" not in d:
    sys.exit("guide TTS error: " + r.stdout[:600])
gpath = os.path.join(out, "guide.mp3")
open(gpath, "wb").write(base64.b64decode(d["audio_base64"]))
al = d.get("alignment") or d.get("normalized_alignment")
words, cur = [], None
for c, s, e in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
    if c.isspace():
        if cur: words.append(cur); cur = None
        continue
    if cur is None: cur = {"w": c, "start": s, "end": e}
    else: cur["w"] += c; cur["end"] = e
if cur: words.append(cur)
json.dump(words, open(os.path.join(out, "words.json"), "w"), indent=1)
npath = os.path.join(out, "narration.mp3")
r = subprocess.run(["curl", "-sS", "-f", "-X", "POST",
                    f"https://api.elevenlabs.io/v1/speech-to-speech/{spec['voice_id']}?output_format=mp3_44100_128",
                    "-H", "xi-api-key: dummy", "-F", f"audio=@{gpath}", "-F", "model_id=eleven_multilingual_sts_v2",
                    "-F", 'voice_settings={"stability":0.45,"similarity_boost":0.95,"style":0,"use_speaker_boost":true}',
                    "-F", "remove_background_noise=false", "-o", npath], capture_output=True, text=True)
if r.returncode != 0:
    sys.exit("speech to speech error: " + r.stderr[:400])
dur = lambda p: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", p],
                                     capture_output=True, text=True).stdout)
gd, nd = dur(gpath), dur(npath)
print(f"words={len(words)} expected={len(text.split())} guide={gd:.2f}s yours={nd:.2f}s drift={nd-gd:+.2f}s wpm={len(words)/words[-1]['end']*60:.0f}")
if abs(nd - gd) > 0.25:
    # keep sync: stretch the converted narration to the guide's exact length
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", npath, "-af", f"atempo={nd/gd:.5f}", npath + ".fix.mp3"], check=True)
    os.replace(npath + ".fix.mp3", npath)
    print("length matched to guide")
