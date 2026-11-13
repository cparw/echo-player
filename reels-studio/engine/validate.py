"""Validate a reel script.json for the HARD NUMBERS engine.
Usage: python3 validate.py path/to/script.json [path/to/caption.txt]
Exit code 0 = OK (warnings may print), 1 = errors.
"""
import json, os, re, sys

errs, warns = [], []
p = sys.argv[1]
s = json.load(open(p))
cap = open(sys.argv[2]).read() if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else ""
LAYOUTS = {"words", "number", "bars", "list", "endcard", "countdown", "waffle", "map", "quote", "versus", "titlecard"}
BANNED = ["part you never see", "part of gta 6 you never see", "thank you for guarding", "this is unseen", "unseen",
          "countdown to vice city", "guard it", "our arithmetic", "on the record", "denmark"]
DASHES = ["—", "–", "‒", "−"]
ALLD = DASHES + ["-"]
GUNLIKE = ("crosshair", "sword", "swords", "bomb", "target", "skull", "knife")
_ij = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons.js")
ICONS = set(re.findall(r'"([a-z0-9-]+)": "', open(_ij).read())) if os.path.exists(_ij) else set()

for k in ["voice_id", "model_id", "tag", "theme", "beats"]:
    if k not in s: errs.append(f"missing top level key: {k}")
beats = s.get("beats", [])
SHOTS = json.load(open(s["shots_json"])) if s.get("shots_json") and os.path.exists(s["shots_json"]) else []
_G5 = {}
def gta5_lib():
    """compare kit: the GTA V library (official/gta5/shots_gta5.json, ids 500 and up), read on first use"""
    if not _G5:
        gp = s.get("shots_gta5_json") or (os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(s["shots_json"]))), "gta5", "shots_gta5.json") if s.get("shots_json") else None)
        _G5.update({x["id"]: x for x in json.load(open(gp))} if gp and os.path.exists(gp) else {})
    return _G5
if s.get("loop"):
    # fast explainer loop: no end card; the last line runs back into the first
    if any(b.get("layout") == "endcard" for b in beats): warns.append("loop is set but the script has an endcard (loop reels end without one)")
elif not beats or beats[-1].get("layout") != "endcard":
    errs.append("last beat must be the endcard")
total = 0
for i, b in enumerate(beats):
    lay = b.get("layout", "words")
    if lay not in LAYOUTS: errs.append(f"beat {i}: unknown layout {lay}")
    if lay == "endcard":
        for k in ["brand", "series", "episode", "cta"]:
            if k not in b: errs.append(f"endcard missing {k}")
        if not (b.get("clips") or b.get("media")): errs.append("endcard needs footage behind it (clips or media): no void frames")
        # optional brand keys (noticed., 13 Nov): handle = second line under the brand, wordmark = brand set as the wordmark
        if "handle" in b and (not isinstance(b["handle"], str) or not b["handle"].startswith("@") or any(d in b["handle"] for d in ALLD)):
            errs.append(f"endcard handle must look like @name with no dash characters: {b['handle']!r}")
        if "wordmark" in b and not isinstance(b["wordmark"], bool): errs.append("endcard wordmark must be true or false")
        if b.get("compare"): errs.append("endcard cannot use compare (compare kit)")
        continue
    say = b.get("say", "")
    if not say: errs.append(f"beat {i}: empty say"); continue
    n = len(say.split()); total += n
    if re.search(r"\d", say): warns.append(f"beat {i}: digits in 'say' ({say[:50]}...). Spell numbers out for the voice.")
    if any(c in say for c in "()%$#&/+"): warns.append(f"beat {i}: symbols in 'say'; write them as words")
    if "-" in say or any(d in say for d in DASHES): errs.append(f"beat {i}: dash character in 'say'")
    for ln in b.get("show", []):
        for tok in ln:
            if "@" in tok and tok.rsplit("@", 1)[1].isdigit():
                a = int(tok.rsplit("@", 1)[1])
                if a >= n: errs.append(f"beat {i}: anchor @{a} out of range (beat has {n} spoken words) in '{tok}'")
            if any(d in tok for d in DASHES): errs.append(f"beat {i}: dash in show token '{tok}'")
    for key in ("count_at", "bars_at"):
        if key in b and b[key] >= n: errs.append(f"beat {i}: {key}={b[key]} out of range ({n} words)")
    if lay == "number":
        for k in ["from", "to", "label"]:
            if k not in b: errs.append(f"beat {i}: number layout missing {k}")
    if lay == "bars":
        for bar in b.get("bars", []):
            if bar.get("at", 0) >= n: errs.append(f"beat {i}: bar anchor out of range")
    if lay == "list":
        for it in b.get("items", []):
            for key in ("at", "strike_at"):
                if key in it and it[key] >= n: errs.append(f"beat {i}: list {key} out of range")
    if b.get("bg") == "black" or not (b.get("clips") or b.get("media") or b.get("compare")):
        errs.append(f"beat {i}: every frame must show GTA 6 footage (RULEBOOK 1.1): give it clips or an official still")
    if b.get("bg") in ("duo",):
        warns.append(f"beat {i}: bg duo tints the footage; RULEBOOK 1.2 prefers full colour (bg scrim)")
    if len(b.get("clips") or []) == 1 and n >= 9:
        warns.append(f"beat {i}: {n} words on one shot; cut every 1.5 to 2.5 s with a second clip anchored on a word")
    if b.get("bg") in ("dim", "duo") and not b.get("media") and not b.get("media_request") and not b.get("clips"):
        errs.append(f"beat {i}: bg {b.get('bg')} needs clips, media or media_request")
    if lay == "countdown" and not isinstance(b.get("remaining"), (int, float)):
        errs.append(f"beat {i}: countdown needs 'remaining' (seconds left at the start of the beat)")
    if lay == "waffle":
        if "filled" not in b: errs.append(f"beat {i}: waffle needs 'filled'")
        if b.get("fill_at", 0) >= n: errs.append(f"beat {i}: fill_at out of range")
    if lay == "versus":
        for side in ("left", "right"):
            sd = b.get(side)
            if not sd or "label" not in sd or "value" not in sd: errs.append(f"beat {i}: versus needs {side} with label and value")
            elif sd.get("at", 0) >= n: errs.append(f"beat {i}: versus {side} anchor out of range")
            for txt in (sd or {}).values():
                if isinstance(txt, str) and any(d in txt for d in DASHES + ["-"]): errs.append(f"beat {i}: dash in versus text '{txt}'")
    if lay == "map":
        for cy in b.get("cities", []):
            for k in ("name", "lon", "lat"):
                if k not in cy: errs.append(f"beat {i}: map city missing {k}")
            if cy.get("at", 0) >= n: errs.append(f"beat {i}: city anchor out of range")
        if b.get("sweep", {}).get("at", 0) >= n: errs.append(f"beat {i}: sweep anchor out of range")
    # ---- fast explainer keys ----
    if lay == "titlecard":
        if not isinstance(b.get("title"), list) or not 1 <= len(b["title"]) <= 2: errs.append(f"beat {i}: titlecard needs 'title' as a list of 1 or 2 lines")
        if not b.get("topic"): warns.append(f"beat {i}: titlecard has no 'topic' tag")
        for txt in list(b.get("title") or []) + [b.get("topic") or ""]:
            if any(d in txt for d in ALLD): errs.append(f"beat {i}: dash in titlecard text '{txt}'")
    if b.get("caps") is not None:
        if not isinstance(b["caps"], list): errs.append(f"beat {i}: caps must be a list")
        for cp in b["caps"] if isinstance(b["caps"], list) else []:
            txt = cp.get("text", "")
            if not txt.strip(): errs.append(f"beat {i}: caption with empty text"); continue
            if len(txt.split(" / ")) > 3: errs.append(f"beat {i}: caption '{txt}' has more than 3 lines")
            if len(txt.replace(" / ", " ").split()) > 8 and b.get("caps_style", s.get("caps_style")) != "story": warns.append(f"beat {i}: caption '{txt}' is long (key phrases, about 6 words)")
            if any(d in txt.replace(" / ", " ") for d in ALLD): errs.append(f"beat {i}: dash in caption '{txt}'")
            if not isinstance(cp.get("at", 0), int) or cp.get("at", 0) >= n: errs.append(f"beat {i}: caption '{txt}' anchor at={cp.get('at')} out of range ({n} words)")
            words_up = {w.strip(".,!?").upper() for w in txt.replace(" / ", " ").split()}
            for kk in ("key", "danger"):
                for ph in cp.get(kk, []):
                    for w in ph.split():
                        if w.strip(".,!?").upper() not in words_up: errs.append(f"beat {i}: {kk} word '{w}' is not in caption '{txt}'")
        ats = [cp.get("at", 0) for cp in b["caps"] if isinstance(cp, dict)]
        if ats != sorted(ats): errs.append(f"beat {i}: captions must be in spoken order")
    # ---- story style keys ----
    cst = b.get("caps_style", s.get("caps_style"))
    if cst not in (None, "build", "story"): errs.append(f"beat {i}: caps_style must be build or story")
    if cst == "story" and isinstance(b.get("caps"), list):
        for cp in b["caps"]:
            nw = len(cp.get("text", "").replace(" / ", " ").split())
            if not b.get("instant") and cp.get("at", 0) + nw > n: warns.append(f"beat {i}: story caption '{cp.get('text')}' has more words than are left to speak")
    for key in ("stamp", "dim"):
        o = b.get(key)
        if o:
            txt = o.get("big" if key == "stamp" else "text")
            if not txt: errs.append(f"beat {i}: {key} needs {'big' if key == 'stamp' else 'text'}")
            for v in (o.get("big"), o.get("small"), o.get("text")):
                if isinstance(v, str) and any(d in v for d in ALLD): errs.append(f"beat {i}: dash in {key} text '{v}'")
            for k2 in ("at", "until"):
                if k2 in o and o[k2] >= n: errs.append(f"beat {i}: {key} {k2} out of range ({n} words)")
    for c in b.get("paper") or []:
        if not (c.get("head") or c.get("redact") or c.get("quote")): errs.append(f"beat {i}: paper card needs head, quote or redact")
        if c.get("quote") and any(d in c["quote"] for d in ALLD): errs.append(f"beat {i}: dash in paper quote")
        if c.get("mark") and c["mark"] not in c.get("head", ""): errs.append(f"beat {i}: paper mark '{c['mark']}' is not in the headline")
        if not c.get("source"): warns.append(f"beat {i}: paper card without a source line")
        for v in (c.get("label"), c.get("head"), c.get("source")):
            if isinstance(v, str) and any(d in v for d in ALLD): errs.append(f"beat {i}: dash in paper text '{v}'")
        for k2 in ("at", "mark_at"):
            if k2 in c and c[k2] >= n: errs.append(f"beat {i}: paper {k2} out of range ({n} words)")
    if lay == "map":
        for k2 in ("region", "collapse"):
            if b.get(k2, {}).get("at", 0) >= n: errs.append(f"beat {i}: map {k2} anchor out of range")
    if b.get("section"):
        sec = b["section"]
        if not isinstance(sec.get("n"), int) or not sec.get("title"): errs.append(f"beat {i}: section needs n (int) and title")
        if any(d in str(sec.get("title", "")) for d in ALLD): errs.append(f"beat {i}: dash in section title")
        if sec.get("icon") and sec["icon"] not in ICONS: warns.append(f"beat {i}: unknown section icon {sec['icon']}")
        if sec.get("icon") and any(g in sec["icon"] for g in GUNLIKE): errs.append(f"beat {i}: section icon {sec['icon']} reads as a weapon")
    if b.get("hud"):
        hud = b["hud"]; ht = hud.get("type")
        if ht not in ("stars", "clues"): errs.append(f"beat {i}: hud type must be stars or clues")
        if ht == "stars":
            tot = hud.get("total", 6)
            if not isinstance(tot, int) or not 1 <= tot <= 8: errs.append(f"beat {i}: stars total must be 1 to 8")
            for a in hud.get("fill_at", []):
                if a >= n: errs.append(f"beat {i}: stars fill_at {a} out of range ({n} words)")
            if len(hud.get("fill_at", [])) > tot: errs.append(f"beat {i}: more fill_at entries than stars")
            for h in hud.get("hot", []):
                if not 1 <= h <= tot: errs.append(f"beat {i}: hot star {h} outside 1..{tot}")
        if ht == "clues":
            for it in hud.get("items") or []:
                if any(d in it.get("label", "") for d in ALLD): errs.append(f"beat {i}: dash in clue label")
                ic = it.get("icon", "")
                if ic and ic not in ICONS: warns.append(f"beat {i}: unknown clue icon {ic}")
                if any(g in ic for g in GUNLIKE): errs.append(f"beat {i}: clue icon {ic} reads as a weapon (use alert-triangle)")
                for kk in ("red_at", "clear_at"):
                    if kk in it and it[kk] >= n: errs.append(f"beat {i}: clue {kk} out of range")
    if b.get("icon") and b["icon"] not in ICONS: warns.append(f"beat {i}: unknown icon {b['icon']} (have: {', '.join(sorted(ICONS))})")
    for c in b.get("clips", []) or []:
        if isinstance(c, dict) and c.get("at", 0) >= n: errs.append(f"beat {i}: clip anchor at={c['at']} out of range")
    for c in b.get("clips", []) or []:
        if not isinstance(c, dict) or "shot" not in c:
            errs.append(f"beat {i}: each clip needs a 'shot' number")
        elif SHOTS and c["shot"] < len(SHOTS) and SHOTS[c["shot"]].get("clean") is not None:
            sh, off = SHOTS[c["shot"]], c.get("offset", 0)
            if c.get("card") and c["shot"] == 72:
                pass  # Rockstar's official date and rating card, used on purpose
            elif not sh["clean"]:
                errs.append(f"beat {i}: shot {c['shot']} has no clean window (audit flagged it)")
            elif not any(w[0] - 0.15 <= off <= w[1] for w in sh["clean"]):
                errs.append(f"beat {i}: shot {c['shot']} offset {off} is outside its clean windows {sh['clean']}")
            else:
                w = next(w for w in sh["clean"] if w[0] - 0.15 <= off <= w[1])
                if w[1] - off < 1.0: warns.append(f"beat {i}: shot {c['shot']} offset {off} leaves only {w[1]-off:.1f} s of clean footage (it will slow down or hold)")
        elif c["shot"] in (0, 7, 19, 23, 25, 26, 53, 61, 63, 66, 67, 70, 73, 75) and not (c["shot"] == 26 and 7.2 <= c.get("offset", 0) <= 7.6):
            errs.append(f"beat {i}: shot {c['shot']} is on the banned list (logo, title card or violence)")
    if b.get("media") and not os.path.exists(b["media"]) and not b.get("media_request"):
        warns.append(f"beat {i}: media file not found yet: {b['media']}")
    # ---- compare kit (GTA 5 vs GTA 6, owner rule 13 Nov; COMPARE.md): GTA V ids (500 and up) only inside their clean windows ----
    def side_ok(where, c):
        if not isinstance(c, dict) or not isinstance(c.get("shot"), int):
            errs.append(f"beat {i}: {where} needs a 'shot' number"); return
        sid, off = c["shot"], c.get("t", c.get("offset", 0))
        if sid >= 500:
            sh = gta5_lib().get(sid)
            if not sh: errs.append(f"beat {i}: {where}: GTA V shot {sid} is not in shots_gta5.json"); return
            if not sh.get("clean"): errs.append(f"beat {i}: {where}: GTA V shot {sid} has no clean window"); return
            w = next((w for w in sh["clean"] if w[0] - 0.15 <= off <= w[1]), None)
            if w is None: errs.append(f"beat {i}: {where}: GTA V shot {sid} t={off} is outside its clean windows {sh['clean']}")
            elif sh.get("kind") == "clip" and w[1] - off < 0.6: warns.append(f"beat {i}: {where}: GTA V shot {sid} t={off} leaves only {w[1] - off:.1f} s of clean footage (it will slow down or hold)")
        elif SHOTS and sid < len(SHOTS) and SHOTS[sid].get("clean") is not None:
            sh = SHOTS[sid]
            if not sh["clean"]: errs.append(f"beat {i}: {where}: shot {sid} has no clean window (audit flagged it)")
            elif not any(w[0] - 0.15 <= off <= w[1] for w in sh["clean"]): errs.append(f"beat {i}: {where}: shot {sid} t={off} is outside its clean windows {sh['clean']}")
        elif SHOTS and sid >= len(SHOTS):
            errs.append(f"beat {i}: {where}: shot {sid} does not exist")
        elif sid in (0, 7, 19, 23, 25, 26, 53, 61, 63, 66, 67, 70, 73, 75):
            errs.append(f"beat {i}: {where}: shot {sid} is on the banned list (logo, title card or violence)")
    cpx = b.get("compare")
    if cpx is not None:
        if not isinstance(cpx, dict): errs.append(f"beat {i}: compare must be an object (see engine/COMPARE.md)")
        else:
            cmode = cpx.get("mode", "split")
            if cmode not in ("split", "ab"): errs.append(f"beat {i}: compare mode must be split or ab")
            sides = {}
            for nm in ("left", "right"):  # a side is one shot or a list of shots cut on spoken words ("at" on every item after the first)
                v = cpx.get(nm); its = v if isinstance(v, list) else [v]
                if isinstance(v, list) and not v: errs.append(f"beat {i}: compare {nm} is an empty list")
                for q, c in enumerate(its):
                    side_ok(f"compare {nm}" + (f" item {q}" if isinstance(v, list) else ""), c)
                    if isinstance(v, list) and q and isinstance(c, dict):
                        if "at" not in c: warns.append(f"beat {i}: compare {nm} item {q} has no 'at' (the side is split evenly)")
                        elif not isinstance(c["at"], int) or not 1 <= c["at"] < n: errs.append(f"beat {i}: compare {nm} item {q} at={c['at']} out of range ({n} words)")
                sides[nm] = [c.get("shot") for c in its if isinstance(c, dict)]
            lsid = (sides.get("left") or [None])[0]
            if any(isinstance(x, int) and x >= 500 for x in sides.get("right", [])): errs.append(f"beat {i}: compare right must be GTA VI shots (below 500) so GTA 6 stays on screen")
            if any(isinstance(x, int) and x < 500 for x in sides.get("left", [])): warns.append(f"beat {i}: compare left has a shot that is not in the GTA V library (ids 500 and up); the owner wants official GTA V visuals beside GTA VI")
            labs = cpx.get("labels", ["GTA 5", "GTA 6"])
            if labs is not False:
                if not (isinstance(labs, list) and len(labs) == 2 and all(isinstance(x, str) for x in labs)): errs.append(f"beat {i}: compare labels must be two strings (or false)")
                else:
                    for x in labs:
                        if any(d in x for d in ALLD): errs.append(f"beat {i}: dash in compare label '{x}'")
                        if len(x) > 14: warns.append(f"beat {i}: compare label '{x}' is long (labels are small pills, 14 characters max)")
            if cmode == "ab":
                cat = cpx.get("at", max(1, n // 2))
                if not isinstance(cat, int) or not 1 <= cat < n: errs.append(f"beat {i}: compare at={cat} must be a spoken word index from 1 to {n - 1}")
                elif cat > max(3, n * 0.6): warns.append(f"beat {i}: the GTA 5 part runs {cat} of {n} words; keep the A/B cut early so GTA 6 stays on screen (RULEBOOK 1.1)")
                ls = gta5_lib().get(lsid) if isinstance(lsid, int) else None
                if ls and not ls.get("sharp_full", True): warns.append(f"beat {i}: GTA V shot {lsid} is {ls['res'][0]}x{ls['res'][1]}; full screen in ab mode it looks soft, prefer a 4K still or clip (sharp_full)")
            elif "at" in cpx: warns.append(f"beat {i}: compare 'at' only applies to ab mode")
            lyy = cpx.get("label_y")
            if lyy is not None and not (isinstance(lyy, list) and len(lyy) == 2 and all(isinstance(v, (int, float)) for v in lyy)): errs.append(f"beat {i}: compare label_y must be [top_y, bottom_y]")
            elif lyy and (min(lyy) < 220 or max(lyy) > 1440): warns.append(f"beat {i}: compare label_y {lyy} puts a label under an Instagram UI zone (keep 220 to 1440)")
            def span_warn(nm, v, a0, a1):  # a side running out of clean footage holds (with a slow push): suggest another shot
                its = v if isinstance(v, list) else [v]
                bounds = [a0] + [c.get("at", a0) if isinstance(c, dict) else a0 for c in its[1:]] + [a1]
                for q, c in enumerate(its):
                    if not isinstance(c, dict) or not isinstance(c.get("shot"), int): continue
                    sh = gta5_lib().get(c["shot"]) if c["shot"] >= 500 else (SHOTS[c["shot"]] if SHOTS and c["shot"] < len(SHOTS) else None)
                    if not sh or sh.get("kind") == "still" or not sh.get("clean"): continue
                    off = c.get("t", c.get("offset", 0)); w = next((w for w in sh["clean"] if w[0] - 0.15 <= off <= w[1]), None)
                    if not w: continue
                    need = max(0, bounds[q + 1] - bounds[q]) / max(n, 1) * (n / 3.0)  # seconds on screen, beat estimated at 180 words a minute
                    have = (w[1] - max(off, w[0])) * 1.5
                    if need > have + 0.3: warns.append(f"beat {i}: compare {nm} shot {c['shot']} has about {have:.1f} s of clean footage (slowed) for about {need:.1f} s on screen; it will hold on a slow push. Add a second shot to the {nm} list (cut on a word with at) to keep it moving")
            cut_w = cpx.get("at", max(1, n // 2)) if cmode == "ab" else None
            if isinstance(cut_w, int) or cut_w is None:
                span_warn("left", cpx.get("left"), 0, cut_w if cmode == "ab" else n); span_warn("right", cpx.get("right"), cut_w if cmode == "ab" else 0, n)
            if b.get("clips"): warns.append(f"beat {i}: clips are ignored while compare is on (compare supplies the footage)")
            if b.get("collage"): errs.append(f"beat {i}: compare and collage cannot share a beat")
    g5 = [c for c in b.get("clips") or [] if isinstance(c, dict) and isinstance(c.get("shot"), int) and c["shot"] >= 500]
    if g5 and cpx is None:
        for c in g5: side_ok("clip", c)
        if len(g5) == len(b.get("clips") or []): errs.append(f"beat {i}: every clip is GTA V; every frame must show GTA 6 (RULEBOOK 1.1): use compare (split or ab) or add a GTA VI clip")
        else: warns.append(f"beat {i}: GTA V shots in plain clips carry no label; prefer compare so viewers see which game is which")
    if b.get("footnote") and any(d in b["footnote"] for d in DASHES): errs.append(f"beat {i}: dash in footnote")
text_all = " ".join(b.get("say", "") for b in beats).lower() + " " + cap.lower()
for ph in BANNED:
    if ph in text_all: errs.append(f"banned reference creator phrase found: '{ph}'")
if cap and any(d in cap for d in DASHES + ["-"]):
    warns.append("caption contains a dash or hyphen character (user rule: none in prose; URLs excepted)")
if cap and cap.count("#") > 5: errs.append("caption has more than 5 hashtags")
est = total / 180 * 60
print(f"spoken words: {total} | est. duration at 180 wpm: {est:.1f}s (+ endcard)")
if total < 175: warns.append("under 175 words: may finish below 61 s (TikTok Creator Rewards needs over 1 minute)")
if total > 260: warns.append("over 260 words: likely above 90 s")
for w in warns: print("WARN:", w)
for e in errs: print("ERROR:", e)
print("RESULT:", "OK" if not errs else f"{len(errs)} error(s)")
sys.exit(1 if errs else 0)
