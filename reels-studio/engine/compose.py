"""Background track + graphics overlay + audio mix -> final 1080x1920 H.264 reel.
Usage: python3 compose.py outdir [music.mp3|none] [final.mp4]
Expects outdir/bgplan.json, outdir/graphics.mov, outdir/narration.mp3.
Audio recipe (production research): voice HPF 90 Hz + 3:1 comp, bed about -20 LUFS ducked by sidechain
(threshold 0.03, ratio 8), synthesized hits/whooshes, two pass loudnorm to -14 LUFS, TP -1.
"""
import json, os, re, subprocess, sys

od = sys.argv[1]
music = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "none" else None
final = sys.argv[3] if len(sys.argv) > 3 else os.path.join(od, "final.mp4")
plan = json.load(open(os.path.join(od, "bgplan.json")))
here = os.path.dirname(os.path.abspath(__file__))
FPS = 30
D = plan["duration"]

def run(args, capture=False):
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-v", "info" if capture else "error"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg failed: " + r.stderr[-2500:])
    return r.stderr

def clip_len(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", p],
                                capture_output=True, text=True).stdout.strip())

# official trailer shots: [{shot, offset?, cx?}] resolved from shots.json; Rockstar TikTok trailers are stored rotated 90 deg
SHOTS = json.load(open(plan["shots_json"])) if plan.get("shots_json") else []
ROTATED = ("7696925363795938573", "7502175479718284586")
LETTERBOX = {"7696925363795938573": (960, 60), "7502175479718284586": (864, 108)}  # active height, top offset after transpose (cropdetect)

# Our sunset duotone for footage behind data cards: grey, soft focus, shadows to deep indigo, highlights to dusty rose
# (dark enough that the orange accent and off white text still pop on top)
DUO = ("hue=s=0,eq=contrast=1.12,gblur=sigma=1.4,"
       "curves=r='0/0.03 0.5/0.21 1/0.66':g='0/0.03 0.5/0.11 1/0.37':b='0/0.08 0.5/0.25 1/0.54'")

VIVID = "eq=saturation=1.10:contrast=1.05"

def grade(s):
    t = s.get("treat")
    if t == "duo": return DUO
    if t == "blur": return "gblur=sigma=10,eq=saturation=1.15:brightness=-0.04"
    return VIVID

def clean_window(sh, offset):
    """The audited clean window that contains offset (else the nearest one); falls back to the old safe window."""
    wins = sh.get("clean")
    if wins is None:
        return sh.get("safe", [0, sh["end"] - sh["start"]])
    if not wins:
        sys.exit(f"shot is banned (no clean window): {sh['src']} {sh['start']}")
    for w in wins:
        if w[0] - 0.15 <= offset <= w[1]: return w
    return min(wins, key=lambda w: min(abs(offset - w[0]), abs(offset - w[1])))

def clip_part(c, dur, outp, treat=None):
    sh = SHOTS[c["shot"]]
    lo, hi = clean_window(sh, c.get("offset", 0))
    off = min(max(c.get("offset", 0), lo), max(lo, hi - 0.6))
    c = dict(c, offset=off)
    src = sh["src"]; avail = max(0.3, hi - off)
    slow = c.get("slow") or min(1.5, max(1.0, dur / avail))  # a clip may ask for slow motion to hold a moment (e.g. the cat on the ATM)
    rot = any(r in src for r in ROTATED) if c.get("rot") is None else c["rot"]
    cx = c.get("cx", 0.5)
    if rot:
        # trailers are letterboxed cinema widescreen inside the rotated frame: crop the active picture first
        H, Y = next((v for k, v in LETTERBOX.items() if k in src), (1080, 0))
        W = int(round(H * 9 / 16 / 2) * 2)
        geo = (f"transpose=2,crop=1920:{H}:0:{Y},crop={W}:{H}:x='(iw-ow)*{cx}':y=0,"
               "scale=1080:1920:flags=lanczos,unsharp=5:5:0.55:5:5:0.0")
    elif sh.get("crop_box"):
        x, y, w, h = sh["crop_box"]  # zoom past Rockstar's corner rating badge
        geo = f"crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos,unsharp=5:5:0.5:5:5:0.0"
    else:
        geo = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    vf = f"trim=duration={avail:.3f},setpts=PTS-STARTPTS,setpts={slow:.3f}*PTS,{geo},fps=30,tpad=stop_mode=clone:stop_duration=3,{grade({'treat': treat})},setsar=1,format=yuv420p"
    run(["-ss", str(sh["start"] + c.get("offset", 0)), "-i", src, "-vf", vf, "-t", str(dur), "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-r", "30", outp])

# 1) background segments (official footage, stills, AI b-roll, or brand black)
segs = []
for i, s in enumerate(plan["segments"]):
    dur = round(s["end"] - s["start"], 3)
    p = os.path.join(od, f"seg_{i:02d}.mp4")
    if s.get("clips"):
        n = len(s["clips"]); parts = []
        if all("t" in c for c in s["clips"][1:]) and n > 1:
            # cuts on spoken words (times from build.py), snapped to whole frames
            cuts = [s["start"]] + [c["t"] for c in s["clips"][1:]] + [s["end"]]
            fr = [round((x - s["start"]) * FPS) for x in cuts]
            durs = [max(1, fr[j + 1] - fr[j]) / FPS for j in range(n)]
        else:
            durs = [round(dur / n, 3) if j < n - 1 else round(dur - round(dur / n, 3) * (n - 1), 3) for j in range(n)]
        for j, c in enumerate(s["clips"]):
            pp = os.path.join(od, f"seg_{i:02d}_{j}.mp4"); clip_part(c, durs[j], pp, s.get("treat")); parts.append(pp)
        pl = os.path.join(od, f"seg_{i:02d}.txt"); open(pl, "w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in parts))
        run(["-f", "concat", "-safe", "0", "-i", pl, "-c", "copy", p])
    elif s.get("media") and s["media"].lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        a, b2 = s.get("pan", [0.40, 0.60])
        frames = int(round(dur * FPS))
        vf = (f"scale=-2:2400,crop=1350:2400:x='(iw-ow)*({a}+({b2}-{a})*min(1,t/{max(dur,0.1)}))':y='(ih-oh)/2',"
              f"scale=1080:1920,{grade(s)},setsar=1,format=yuv420p")
        run(["-loop", "1", "-framerate", "30", "-t", str(dur), "-i", s["media"], "-vf", vf, "-frames:v", str(frames),
             "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-r", "30", p])
    elif s.get("media"):
        avail = clip_len(s["media"]) - s.get("media_offset", 0)
        slow = min(1.45, max(1.0, dur / max(avail, 0.5)))  # stretch slightly instead of looping when possible
        vf = (f"setpts={slow:.3f}*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,"
              f"zoompan=z='min(1.0+0.0010*on,1.14)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
              f"{grade(s) if s.get('treat') == 'duo' else 'eq=saturation=1.08:contrast=1.04'},setsar=1,format=yuv420p")
        run(["-stream_loop", "-1", "-ss", str(s.get("media_offset", 0)), "-i", s["media"], "-t", str(dur * 1.0 + 0.2), "-vf", vf,
             "-t", str(dur), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-r", "30", p])
    else:
        run(["-f", "lavfi", "-i", f"color=c=0x08080B:s=1080x1920:r=30:d={dur}", "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "14", "-pix_fmt", "yuv420p", p])
    segs.append(p)
lst = os.path.join(od, "segs.txt")
open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in segs))
bgv = os.path.join(od, "bg.mp4")
run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", bgv])

# 2) sound design assets (synthesized, royalty free)
hit = os.path.join(here, "sfx_hit.wav"); whoosh = os.path.join(here, "sfx_whoosh.wav")
if not os.path.exists(hit):
    run(["-f", "lavfi", "-i", "aevalsrc='0.8*sin(2*PI*(70*t-38*t*t))*exp(-5.5*t)':s=48000:d=0.7",
         "-f", "lavfi", "-i", "anoisesrc=d=0.12:c=pink:a=0.25:r=48000",
         "-filter_complex", "[1]lowpass=f=2500,afade=t=out:d=0.12[n];[0][n]amix=inputs=2:normalize=0,aformat=channel_layouts=stereo", hit])
    run(["-f", "lavfi", "-i", "anoisesrc=d=0.45:c=pink:a=0.35:r=48000", "-af",
         "highpass=f=500,lowpass=f=7000,afade=t=in:d=0.32:curve=exp,afade=t=out:st=0.32:d=0.13,aformat=channel_layouts=stereo", whoosh])

# 3) audio mix -> mix.wav
inputs = ["-i", os.path.join(od, "narration.mp3")]
fc = ["[0:a]aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=90,acompressor=threshold=0.125:ratio=3:attack=10:release=120:makeup=1.5,asplit=2[vo][vk]"]
mix = ["[vo]"]; idx = 1
if music:
    inputs += ["-stream_loop", "-1", "-i", music]
    fc.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{D},volume=0.5,afade=t=in:d=0.6,afade=t=out:st={max(0, D - 1.8)}:d=1.8[mu]")
    fc.append("[mu][vk]sidechaincompress=threshold=0.03:ratio=8:attack=15:release=400[md]")
    mix.append("[md]"); idx += 1
else:
    fc.append("[vk]anullsink")
for q, s in enumerate(plan.get("sfx", [])):
    src = hit if s["kind"] == "hit" else whoosh
    inputs += ["-i", src]
    delay = max(0, int((s["t"] - (0.04 if s["kind"] == "hit" else 0.36)) * 1000))
    vol = 0.5 if s["kind"] == "hit" else 0.22
    fc.append(f"[{idx}:a]adelay={delay}|{delay},volume={vol}[s{q}]")
    mix.append(f"[s{q}]"); idx += 1
fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0,apad,atrim=0:{D}[a]")
mixwav = os.path.join(od, "mix.wav")
run(inputs + ["-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s24le", "-ar", "48000", mixwav])

# 4) two pass loudness: measure, then apply linearly in the final encode
err = run(["-i", mixwav, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"], capture=True)
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S).group(0))
ln = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")

# 5) final: overlay graphics with grain, encode once
run(["-i", bgv, "-i", os.path.join(od, "graphics.mov"), "-i", mixwav, "-filter_complex",
     f"[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v];[2:a]{ln}[a]",
     "-map", "[v]", "-map", "[a]", "-t", str(D), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", "12M", "-bufsize", "24M", "-profile:v", "high",
     "-level:v", "4.2", "-g", "60", "-bf", "2", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
     "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", final])
print("wrote", final, "| pass1 input_i", m["input_i"])
