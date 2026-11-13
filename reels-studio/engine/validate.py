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
    if b.get("bg") == "black" or not (b.get("clips") or b.get("media")):
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
        if not c.get("head"): errs.append(f"beat {i}: paper card needs head")
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
