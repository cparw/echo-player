"""Compare kit: GTA 5 vs GTA 6 beats (owner rule, 13 Nov 2026: "if you want to show GTA 5 comparison with GTA 6, then you should show
the GTA 5 pictures also for that properly"). Schema and examples: engine/COMPARE.md.

Beat key (optional; beats without it build and render exactly as before):
  "compare": {"mode": "split" | "ab", "left": {"shot": 500, "t": 0}, "right": {"shot": 62, "t": 10.3}, "labels": ["GTA 5", "GTA 6"], "at": k}
  split: left (GTA V) on the top half, right (GTA VI) on the bottom half, each 1080x960; stage.html draws the divider and labels.
  A side may be a list of shots, items after the first cut on spoken word "at" (like clips), so a long beat keeps moving.
  ab:    left full screen, then a hard cut to right on spoken word k; the label switches on the cut.
GTA V library: official/gta5/shots_gta5.json, ids 500 and up, {"id", "kind": "clip" | "still", "src", "start", "end", "crop_box": [x, y, w, h]
(the only part of the source that may be shown), "focus": [fx, fy], "clean": [[from, to]], ...}. Stills are held with a slow push in.
Used by build.py (timeline and bgplan keys), compose.py (renders the background), preview.py (stills) and validate.py (checks)."""
import json, os, subprocess

GTA5_MIN = 500
FPS = 30
ROTATED = ("7696925363795938573", "7502175479718284586")
LETTERBOX = {"7696925363795938573": (960, 60), "7502175479718284586": (864, 108)}
VIVID = "eq=saturation=1.10:contrast=1.05"
ENC = ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-r", str(FPS)]


# ---------- shot table: shots.json (GTA VI, index = id) plus the GTA V library (ids 500 and up) ----------
def default_gta5_path(shots_json):
    """official/shots/shots.json -> official/gta5/shots_gta5.json"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(shots_json))), "gta5", "shots_gta5.json") if shots_json else None


class ShotTable(list):
    def __init__(self, base, extra):
        super().__init__(base)
        self.gta5 = {s["id"]: s for s in extra}

    def __getitem__(self, i):
        if isinstance(i, int) and i >= GTA5_MIN:
            if i not in self.gta5:
                raise SystemExit(f"GTA V shot {i} is not in shots_gta5.json")
            return self.gta5[i]
        return super().__getitem__(i)

    def has(self, i):
        return i in self.gta5 if i >= GTA5_MIN else 0 <= i < len(self)


def load_table(shots_json, gta5_json=None, base=None):
    if base is None:
        base = json.load(open(shots_json)) if shots_json else []
    p = gta5_json or default_gta5_path(shots_json)
    return ShotTable(base, json.load(open(p)) if p and os.path.exists(p) else [])


def uses_kit(segments):
    """True when a bgplan needs the kit (a compare segment or a GTA V shot in plain clips)"""
    return any(s.get("compare") or any(isinstance(c, dict) and c.get("shot", 0) >= GTA5_MIN for c in s.get("clips") or []) for s in segments)


def clean_window(sh, offset):
    """The audited clean window that contains offset (else the nearest one), same rule as compose.py."""
    wins = sh.get("clean")
    if wins is None:
        return sh.get("safe", [0, sh["end"] - sh["start"]])
    if not wins:
        raise SystemExit(f"shot is banned (no clean window): {sh['src']} {sh['start']}")
    for w in wins:
        if w[0] - 0.15 <= offset <= w[1]:
            return w
    return min(wins, key=lambda w: min(abs(offset - w[0]), abs(offset - w[1])))


def items(v):
    """a side is one shot {"shot", "offset", ...} or a list of them (cut on spoken words like clips)"""
    return v if isinstance(v, list) else [v]


def spans(v, t0, dur):
    """[(shot, start in the span, length)] for one side over a span of dur seconds starting at reel time t0. List items after the first cut
    at their "cut" time (build.py: LEAD before spoken word "at"), else the span is shared evenly. Snapped to whole frames."""
    it = items(v); n = len(it); N = max(n, round(dur * FPS))
    if n == 1:
        return [(it[0], 0.0, dur)]
    if all("cut" in x for x in it[1:]):
        fr = [0] + [round((x["cut"] - t0) * FPS) for x in it[1:]] + [N]
    else:
        fr = [round(N * k / n) for k in range(n + 1)]
    for k in range(1, n):
        fr[k] = min(max(fr[k], fr[k - 1] + 1), N - (n - k))
    return [(x, fr[k] / FPS, (fr[k + 1] - fr[k]) / FPS) for k, x in enumerate(it)]


# ---------- framing ----------
_SIZE = {}


def src_size(sh):
    if sh.get("w") and sh.get("h"):
        return sh["w"], sh["h"]
    if sh["src"] not in _SIZE:
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", sh["src"]],
                           capture_output=True, text=True).stdout.strip().split(",")
        _SIZE[sh["src"]] = (int(r[0]), int(r[1]))
    return _SIZE[sh["src"]]


def region(sh):
    """(pre filters, width, height) of the part of the source that may be shown: the GTA VI TikTok trailers are stored rotated with a
    cinema letterbox; crop_box removes Rockstar's rating badge (GTA VI) or a letterbox, logo or flagged corner (GTA V)."""
    src = sh["src"]
    if any(r in src for r in ROTATED):
        H, Y = next((v for k, v in LETTERBOX.items() if k in src), (1080, 0))
        return [f"transpose=2,crop=1920:{H}:0:{Y}"], 1920, H
    if sh.get("crop_box"):
        x, y, w, h = sh["crop_box"]
        return [f"crop={w}:{h}:{x}:{y}"], w, h
    w, h = src_size(sh)
    return [], w, h


def window(sh, W, H, cx=None, cy=None):
    """filters that cut the largest W:H window out of the allowed region. cx / cy (0..1) place it like compose.py's cx;
    without them the window is centred on the shot's focus point (GTA V library) or on the middle."""
    pre, aw, ah = region(sh)
    if aw * H > ah * W:
        wh, ww = ah, ah * W / H
    else:
        ww, wh = aw, aw * H / W
    ww, wh = int(ww) // 2 * 2, int(wh) // 2 * 2
    fx, fy = (sh.get("focus") or [0.5, 0.5])[:2]
    x = (aw - ww) * cx if cx is not None else min(max(fx * aw - ww / 2, 0), aw - ww)
    y = (ah - wh) * cy if cy is not None else min(max(fy * ah - wh / 2, 0), ah - wh)
    return pre + [f"crop={ww}:{wh}:{int(round(x))}:{int(round(y))}"], ww, wh


def full_geo_gta6(sh, c):
    """The engine's own full frame 9:16 framing of a GTA VI shot (as in preview.py), for previews of the A/B cut."""
    src = sh["src"]
    if any(r in src for r in ROTATED) if c.get("rot") is None else c["rot"]:
        H, Y = next((v for k, v in LETTERBOX.items() if k in src), (1080, 0)); W = int(round(H * 9 / 16 / 2) * 2)
        return f"transpose=2,crop=1920:{H}:0:{Y},crop={W}:{H}:x='(iw-ow)*{c.get('cx', 0.5)}':y=0,scale=1080:1920:flags=lanczos"
    if sh.get("crop_box"):
        x, y, w, h = sh["crop_box"]
        return f"crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos"
    return "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"


def still_zoom(W, H, push, dur, at=None):
    """slow push in on a still (or on a clip that has to hold its last clean frame). Animated (at is None): zoom grows by `push` over dur, computed at twice the size so it moves smoothly.
    Single frame (at = seconds): the zoom at that moment."""
    if at is not None:
        z = 1 + push * min(1.0, max(0.0, at) / max(dur, 0.1))
        return [f"scale={int(W * z) // 2 * 2}:{int(H * z) // 2 * 2}:flags=lanczos", f"crop={W}:{H}"]
    W2, H2, z = W * 2, H * 2, f"(1+{push:.4f}*t/{max(dur, 0.1):.3f})"
    return [f"scale={W2}:{H2}:flags=lanczos", f"scale=w='trunc({W2}*{z}/2)*2':h='trunc({H2}*{z}/2)*2':eval=frame:flags=bicubic",
            f"crop={W2}:{H2}:(iw-{W2})/2:(ih-{H2})/2", f"scale={W}:{H}:flags=lanczos"]


def auto_push(dur):
    """push in that keeps a picture moving (RULEBOOK: no frozen picture over 0.5 s): at least 1.6 percent zoom per second, tested with
    ffmpeg freezedetect n=0.003 d=0.5"""
    return round(max(0.05, 0.016 * dur), 4)


def clip_timing(sh, c, dur):
    """(offset, available clean seconds, slow factor, holds): the same rule as compose.py's clip_part"""
    lo, hi = clean_window(sh, c.get("offset", 0))
    off = min(max(c.get("offset", 0), lo), max(lo, hi - 0.6))
    avail = max(0.3, hi - off)
    slow = c.get("slow") or min(1.5, max(1.0, dur / avail))
    return off, avail, slow, dur > avail * slow + 0.05


# ---------- rendering (compose.py) ----------
def render_part(sh, c, dur, outp, W, H, run, grade=VIVID, post=""):
    """One shot into a W x H video of dur seconds: a clip stays inside its clean window (slowed up to 1.5x, then held on its last clean
    frame with a slow push so it never freezes), a still gets a slow push in. post: extra filters (for example compose.py's dim blur)."""
    chain, ww, wh = window(sh, W, H, c.get("cx"), c.get("cy"))
    if sh.get("kind") == "still":
        vf = ",".join(chain + still_zoom(W, H, c.get("push") or auto_push(dur), dur) + [f"fps={FPS}", grade, "setsar=1"]) + post + ",format=yuv420p"
        run(["-loop", "1", "-framerate", str(FPS), "-t", f"{dur + 0.5:.3f}", "-i", sh["src"], "-vf", vf, "-frames:v", str(max(1, round(dur * FPS))),
             "-t", f"{dur:.3f}"] + ENC + [outp])
        return
    off, avail, slow, holds = clip_timing(sh, c, dur)
    push = c.get("push") or (auto_push(dur) if holds else None)  # a held last frame keeps moving
    scale = [f"scale={W}:{H}:flags=lanczos"] + (["unsharp=5:5:0.5:5:5:0.0"] if W / ww > 1.15 else [])
    vf = (f"trim=duration={avail:.3f},setpts=PTS-STARTPTS,setpts={slow:.3f}*PTS," + ",".join(chain + scale) +
          f",fps={FPS},tpad=stop_mode=clone:stop_duration={max(3.0, dur + 1):.2f}," + (",".join(still_zoom(W, H, push, dur)) + "," if push else "") +
          f"{grade},setsar=1" + post + ",format=yuv420p")
    run(["-ss", f"{sh['start'] + off:.3f}", "-i", sh["src"], "-vf", vf, "-t", f"{dur:.3f}"] + ENC + [outp])


def compare_segment(s, dur, outp, SHOTS, od, i, run, clip_part, grade, blur_graph):
    """A compare background segment (1080x1920): split = left over right, 1080x960 each; ab = left, then a cut to right at s["compare"]["ts"].
    A full frame GTA VI side uses the same 9:16 window as compose.py's clip_part (clip_part is accepted for compatibility, not called)."""
    cp = s["compare"]; mode = cp.get("mode", "split"); tr = s.get("treat"); g = grade({"treat": tr})
    part = lambda k: os.path.join(od, f"seg_{i:02d}_{k}.mp4")

    def one(c, d, p, W, H):  # every side goes through render_part: same window as clip_part, and a held frame keeps a slow push (no freezes)
        render_part(SHOTS[c["shot"]], c, d, p, W, H, run, g)

    def side(v, d, p, W, H, t0):  # one shot, or a list cut on spoken words (parts joined without re encoding, like plain clips)
        sp = spans(v, t0, d)
        if len(sp) == 1:
            return one(sp[0][0], d, p, W, H)
        parts = []
        for q, (c, _, dd) in enumerate(sp):
            pp = p[:-4] + f"_{q}.mp4"; one(c, dd, pp, W, H); parts.append(pp)
        lst = p[:-4] + ".txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in parts))
        run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", p])

    if mode == "ab":
        n = max(2, round(dur * FPS)); k = min(max(1, round((cp["ts"] - s["start"]) * FPS)), n - 1)
        side(cp["left"], k / FPS, part("a"), 1080, 1920, s["start"]); side(cp["right"], dur - k / FPS, part("b"), 1080, 1920, s["start"] + k / FPS)
        ins, fc = ["-i", part("a"), "-i", part("b")], "[0:v][1:v]concat=n=2:v=1:a=0"
    else:
        side(cp["left"], dur, part("top"), 1080, 960, s["start"]); side(cp["right"], dur, part("bot"), 1080, 960, s["start"])
        ins, fc = ["-i", part("top"), "-i", part("bot")], "[0:v][1:v]vstack=inputs=2"
    if s.get("blur"):  # story dim line / collage over a compare beat: blur the composed frame, same curve as plain clips
        b0, b1 = s["blur"][0] - s["start"], s["blur"][1] - s["start"]
        if b1 > 0 and b0 < dur:
            fc += blur_graph(b0, b1, s.get("blur_full", False))
    run(ins + ["-filter_complex", fc + ",setsar=1,format=yuv420p", "-t", f"{dur:.3f}"] + ENC + [outp])


# ---------- previews (preview.py) ----------
def _side_frame(SHOTS, v, t_in, W, H, grade, dur, full_gta6=False, t0=0.0):
    """ffmpeg input args and filter chain for one frame of one side (a shot or a list), t_in seconds into its span (slow motion ignored)"""
    c = v
    if isinstance(v, list):
        c, a, dur = next(((x, a, d) for x, a, d in reversed(spans(v, t0, dur)) if t_in >= a - 1e-6), (v[0], 0.0, dur))
        t_in -= a
    sh = SHOTS[c["shot"]]
    if sh.get("kind") == "still":
        chain, _, _ = window(sh, W, H, c.get("cx"), c.get("cy"))
        return ["-i", sh["src"]], ",".join(chain + still_zoom(W, H, c.get("push") or auto_push(dur), dur, at=t_in) + [grade])
    lo, hi = clean_window(sh, c.get("offset", 0)); off = min(max(c.get("offset", 0), lo), max(lo, hi - 0.6))
    ss = sh["start"] + off + min(max(0, t_in), max(0, hi - off - 0.05))
    if full_gta6 and c["shot"] < GTA5_MIN:
        f = full_geo_gta6(sh, c)
    else:
        chain, _, _ = window(sh, W, H, c.get("cx"), c.get("cy")); f = ",".join(chain + [f"scale={W}:{H}:flags=lanczos"])
    return ["-ss", f"{ss:.3f}", "-i", sh["src"]], f + "," + grade


def _blur_preview(seg, t):
    if not (seg.get("blur") and seg["blur"][0] <= t <= seg["blur"][1]):
        return ""
    k = min(1, (t - seg["blur"][0]) / 0.2 if not seg.get("blur_full") else 1, (seg["blur"][1] - t) / 0.25)
    return (f",split=2[o][b];[b]gblur=sigma=22,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*{k:.3f}*" +
            ("1" if seg.get("blur_full") else "clip(1.25-hypot((X-W/2)/(W*0.62),(Y-H*0.43)/(H*0.30)),0,1)") + "'[m];[o][m]overlay=format=auto")


def preview_cmd(seg, t, SHOTS, grade):
    """ffmpeg arguments (inputs and filters, no output) for the background frame of a compare segment, or of a plain clips segment that
    uses GTA V shots, at reel time t. Mirrors compare_segment / render_part framing (slow motion ignored)."""
    dur = seg["end"] - seg["start"]
    if seg.get("compare"):
        cp = seg["compare"]
        if cp.get("mode") == "ab":
            right = t >= cp["ts"]
            c = cp["right"] if right else cp["left"]
            d = (seg["end"] - cp["ts"]) if right else (cp["ts"] - seg["start"])
            ins, f = _side_frame(SHOTS, c, t - (cp["ts"] if right else seg["start"]), 1080, 1920, grade, d, True, cp["ts"] if right else seg["start"])
            return ins + ["-filter_complex", "[0:v]" + f + _blur_preview(seg, t), "-frames:v", "1"]
        i1, f1 = _side_frame(SHOTS, cp["left"], t - seg["start"], 1080, 960, grade, dur, False, seg["start"])
        i2, f2 = _side_frame(SHOTS, cp["right"], t - seg["start"], 1080, 960, grade, dur, False, seg["start"])
        return i1 + i2 + ["-filter_complex", f"[0:v]{f1}[a];[1:v]{f2}[b];[a][b]vstack=inputs=2" + _blur_preview(seg, t), "-frames:v", "1"]
    cl = seg["clips"]; c = cl[0]
    for x in cl[1:]:
        if "t" in x and x["t"] <= t:
            c = x
    start = c.get("t", seg["start"]); nxt = [x["t"] for x in cl if "t" in x and x["t"] > start]
    ins, f = _side_frame(SHOTS, c, t - start, 1080, 1920, grade, (min(nxt) if nxt else seg["end"]) - start, full_gta6=True)
    return ins + ["-filter_complex", "[0:v]" + f + _blur_preview(seg, t), "-frames:v", "1"]
