"""Narration in the owner's voice with a directed delivery.
Guide performance (a licensed ElevenLabs voice, with word timestamps) -> Speech to Speech into the owner's clone.
Speech to Speech keeps the guide's timing, so the guide's word timestamps stay valid for on screen sync.
A guide of "self" means the owner's clone reads the script directly (no Speech to Speech).
Usage: python3 tts_sts.py script.json outdir
script.json keys: say texts, voice_id (the owner's clone) and either voice_preset (see PRESETS, the owner's lineup
numbers from 12 Nov 2026) or the individual keys guide_voice_id, guide_model, guide_speed, guide_stability,
guide_style, guide_similarity, sts_stability, sts_similarity, pitch_semitones.
"""
import base64, json, os, subprocess, sys

BRIAN, TEJA, VIRAJ = "nPczCjzI2devNBz1zQrb", "w7yaXuKi0bjR3rtgNpVp", "1U02n4nD6AdIZ9CjF053"
DIRECTED = {"guide_model": "eleven_multilingual_v2", "guide_speed": 1.08, "guide_stability": 0.30, "guide_style": 0.25, "guide_similarity": 0.75}
PRESETS = {
    "1": dict(DIRECTED, guide_voice_id=BRIAN, sts_stability=0.45, sts_similarity=0.95),
    "2": dict(DIRECTED, guide_voice_id=BRIAN, sts_stability=0.80, sts_similarity=1.0),
    "3": dict(guide_voice_id="self", guide_model="eleven_multilingual_v2", guide_speed=1.08, guide_stability=0.35, guide_style=0.25, guide_similarity=1.0),
    "4": dict(guide_voice_id="self", guide_model="eleven_v4", guide_speed=1.08, guide_stability=0.5, guide_style=0.2, guide_similarity=1.0),
    "5": dict(DIRECTED, guide_voice_id=TEJA, sts_stability=0.45, sts_similarity=0.95),
    "6": dict(DIRECTED, guide_voice_id=VIRAJ, sts_stability=0.45, sts_similarity=0.95),
    "7": dict(DIRECTED, guide_voice_id=BRIAN, sts_stability=0.80, sts_similarity=1.0, pitch_semitones=-2.0),
}

spec = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
cfg = dict(DIRECTED, guide_voice_id=BRIAN, sts_stability=0.45, sts_similarity=0.95)
if spec.get("voice_preset"):
    cfg.update(PRESETS[str(spec["voice_preset"])])
cfg.update({k: spec[k] for k in ("guide_voice_id", "guide_model", "guide_speed", "guide_stability", "guide_style",
                                 "guide_similarity", "sts_stability", "sts_similarity", "pitch_semitones") if k in spec and not spec.get("voice_preset")})
text = " ".join(b["say"].strip() for b in spec["beats"] if b.get("say"))
self_read = cfg["guide_voice_id"] == "self"
gvoice = spec["voice_id"] if self_read else cfg["guide_voice_id"]
body = {"text": text, "model_id": cfg["guide_model"],
        "voice_settings": {"stability": cfg["guide_stability"], "similarity_boost": cfg["guide_similarity"],
                           "style": cfg["guide_style"], "use_speaker_boost": True, "speed": cfg["guide_speed"]}}
r = subprocess.run(["curl", "-sS", "-X", "POST",
                    f"https://api.elevenlabs.io/v1/text-to-speech/{gvoice}/with-timestamps?output_format=mp3_44100_128",
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
dur = lambda p: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", p],
                                     capture_output=True, text=True).stdout)
if self_read:
    subprocess.run(["cp", gpath, npath], check=True)
else:
    vs = json.dumps({"stability": cfg["sts_stability"], "similarity_boost": cfg["sts_similarity"], "style": 0, "use_speaker_boost": True})
    r = subprocess.run(["curl", "-sS", "-f", "-X", "POST",
                        f"https://api.elevenlabs.io/v1/speech-to-speech/{spec['voice_id']}?output_format=mp3_44100_128",
                        "-H", "xi-api-key: dummy", "-F", f"audio=@{gpath}", "-F", "model_id=eleven_multilingual_sts_v2",
                        "-F", f"voice_settings={vs}", "-F", "remove_background_noise=false", "-o", npath], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("speech to speech error: " + r.stderr[:400])
    gd, nd = dur(gpath), dur(npath)
    if abs(nd - gd) > 0.25:
        # keep sync: stretch the converted narration to the guide's exact length
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", npath, "-af", f"atempo={nd/gd:.5f}", npath + ".fix.mp3"], check=True)
        os.replace(npath + ".fix.mp3", npath)
        print("length matched to guide")
if cfg.get("pitch_semitones"):
    # move the voice to the owner's natural pitch; formants kept so it still sounds like him, timing unchanged
    f = 2 ** (cfg["pitch_semitones"] / 12)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", npath, "-af", f"rubberband=pitch={f:.4f}:formant=preserved:pitchq=quality",
                    "-c:a", "libmp3lame", "-b:a", "192k", npath + ".p.mp3"], check=True)
    os.replace(npath + ".p.mp3", npath)
print(f"preset={spec.get('voice_preset', 'custom')} guide={'self' if self_read else cfg['guide_voice_id']} words={len(words)} "
      f"expected={len(text.split())} guide={dur(gpath):.2f}s yours={dur(npath):.2f}s wpm={len(words)/words[-1]['end']*60:.0f}")
