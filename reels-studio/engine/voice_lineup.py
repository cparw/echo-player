"""Voice lineup: the same Reel 1 opening in six versions of the owner's voice, paced alike, loudness matched."""
import base64, json, os, subprocess
TXT = ("If you were born the day GTA Five came out, you're thirteen now. And you're still four years too young for GTA Six's rating. "
       "That's how long this wait has been. Four thousand, eight hundred and eleven days. But here's the part nobody talks about.")
WORDS = len(TXT.split())
ME = "bqoGL6z7prHxVFnnNfsb"
GUIDE_SET = {"stability": 0.30, "similarity_boost": 0.75, "style": 0.25, "use_speaker_boost": True, "speed": 1.08}
def tts(voice, model, settings, out):
    body = {"text": TXT, "model_id": model, "voice_settings": settings}
    r = subprocess.run(["curl", "-sS", "-f", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
                        "-H", "xi-api-key: dummy", "-H", "Content-Type: application/json", "--data-binary", json.dumps(body), "-o", out],
                       capture_output=True, text=True)
    if r.returncode: raise SystemExit(f"tts {voice} {model}: {r.stderr[:300]}")
def sts(src, out, stab, sim):
    vs = json.dumps({"stability": stab, "similarity_boost": sim, "style": 0, "use_speaker_boost": True})
    r = subprocess.run(["curl", "-sS", "-f", "-X", "POST", f"https://api.elevenlabs.io/v1/speech-to-speech/{ME}?output_format=mp3_44100_128",
                        "-H", "xi-api-key: dummy", "-F", f"audio=@{src}", "-F", "model_id=eleven_multilingual_sts_v2",
                        "-F", f"voice_settings={vs}", "-F", "remove_background_noise=false", "-o", out], capture_output=True, text=True)
    if r.returncode: raise SystemExit(f"sts {src}: {r.stderr[:300]}")
def speech_dur(p):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_threshold=-45dB:stop_duration=0.6,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    t = [l for l in out.splitlines() if "time=" in l][-1].split("time=")[1].split()[0]
    h, m, s = t.split(":"); return int(h) * 3600 + int(m) * 60 + float(s)
def finish(raw, out, target_wpm=184):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", raw], capture_output=True, text=True).stdout)
    wpm = WORDS / d * 60; f = min(1.12, max(0.90, target_wpm / wpm))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", f"silenceremove=start_periods=1:start_threshold=-50dB,atempo={f:.4f},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100",
                    "-c:a", "libmp3lame", "-b:a", "192k", out], check=True)
    return wpm, f
os.makedirs("work", exist_ok=True)
plan = []
tts("nPczCjzI2devNBz1zQrb", "eleven_multilingual_v2", GUIDE_SET, "work/guide_brian.mp3")
sts("work/guide_brian.mp3", "work/v1.mp3", 0.45, 0.95); plan.append(("1_current_brian_delivery", "work/v1.mp3"))
sts("work/guide_brian.mp3", "work/v2.mp3", 0.80, 1.00); plan.append(("2_current_delivery_more_of_you", "work/v2.mp3"))
tts(ME, "eleven_multilingual_v2", {"stability": 0.35, "similarity_boost": 1.0, "style": 0.25, "use_speaker_boost": True, "speed": 1.08}, "work/v3.mp3")
plan.append(("3_your_clone_direct", "work/v3.mp3"))
tts(ME, "eleven_v4", {"stability": 0.5, "similarity_boost": 1.0, "style": 0.2, "use_speaker_boost": True, "speed": 1.08}, "work/v4.mp3")
plan.append(("4_your_clone_newest_model", "work/v4.mp3"))
tts("w7yaXuKi0bjR3rtgNpVp", "eleven_multilingual_v2", GUIDE_SET, "work/guide_teja.mp3")
sts("work/guide_teja.mp3", "work/v5.mp3", 0.45, 0.95); plan.append(("5_indian_american_delivery", "work/v5.mp3"))
tts("1U02n4nD6AdIZ9CjF053", "eleven_multilingual_v2", GUIDE_SET, "work/guide_viraj.mp3")
sts("work/guide_viraj.mp3", "work/v6.mp3", 0.45, 0.95); plan.append(("6_desi_calm_delivery", "work/v6.mp3"))
for name, raw in plan:
    wpm, f = finish(raw, f"{name}.mp3")
    print(f"{name}: raw {wpm:.0f} wpm, tempo x{f:.3f}")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "real_sample.mp3", "-t", "14", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100,afade=t=out:st=13:d=1",
                "-c:a", "libmp3lame", "-b:a", "192k", "0_your_real_recording.mp3"], check=True)
