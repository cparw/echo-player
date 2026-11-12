"""Validate a reel script.json for the HARD NUMBERS engine.
Usage: python3 validate.py path/to/script.json [path/to/caption.txt]
Exit code 0 = OK (warnings may print), 1 = errors.
"""
import json, os, re, sys

errs, warns = [], []
p = sys.argv[1]
s = json.load(open(p))
cap = open(sys.argv[2]).read() if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else ""
LAYOUTS = {"words", "number", "bars", "list", "endcard", "countdown", "waffle", "map", "quote"}
BANNED = ["part you never see", "part of gta 6 you never see", "thank you for guarding", "this is unseen", "unseen",
          "countdown to vice city", "guard it", "our arithmetic", "on the record", "denmark"]
DASHES = ["—", "–", "‒", "−"]
_ij = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons.js")
ICONS = set(re.findall(r'"([a-z0-9-]+)": "', open(_ij).read())) if os.path.exists(_ij) else set()

for k in ["voice_id", "model_id", "tag", "theme", "beats"]:
    if k not in s: errs.append(f"missing top level key: {k}")
beats = s.get("beats", [])
SHOTS = json.load(open(s["shots_json"])) if s.get("shots_json") and os.path.exists(s["shots_json"]) else []
if not beats or beats[-1].get("layout") != "endcard":
    errs.append("last beat must be the endcard")
total = 0
for i, b in enumerate(beats):
    lay = b.get("layout", "words")
    if lay not in LAYOUTS: errs.append(f"beat {i}: unknown layout {lay}")
    if lay == "endcard":
        for k in ["brand", "series", "episode", "cta"]:
            if k not in b: errs.append(f"endcard missing {k}")
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
    if b.get("bg") in ("dim", "duo") and not b.get("media") and not b.get("media_request") and not b.get("clips"):
        errs.append(f"beat {i}: bg {b.get('bg')} needs clips, media or media_request")
    if lay == "countdown" and not isinstance(b.get("remaining"), (int, float)):
        errs.append(f"beat {i}: countdown needs 'remaining' (seconds left at the start of the beat)")
    if lay == "waffle":
        if "filled" not in b: errs.append(f"beat {i}: waffle needs 'filled'")
        if b.get("fill_at", 0) >= n: errs.append(f"beat {i}: fill_at out of range")
    if lay == "map":
        for cy in b.get("cities", []):
            for k in ("name", "lon", "lat"):
                if k not in cy: errs.append(f"beat {i}: map city missing {k}")
            if cy.get("at", 0) >= n: errs.append(f"beat {i}: city anchor out of range")
        if b.get("sweep", {}).get("at", 0) >= n: errs.append(f"beat {i}: sweep anchor out of range")
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
            elif not any(w[0] - 0.05 <= off <= w[1] for w in sh["clean"]):
                errs.append(f"beat {i}: shot {c['shot']} offset {off} is outside its clean windows {sh['clean']}")
            else:
                w = next(w for w in sh["clean"] if w[0] - 0.05 <= off <= w[1])
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
