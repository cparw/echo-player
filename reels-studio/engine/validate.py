"""Validate a reel script.json for the HARD NUMBERS engine.
Usage: python3 validate.py path/to/script.json [path/to/caption.txt]
Exit code 0 = OK (warnings may print), 1 = errors.
"""
import json, os, re, sys

errs, warns = [], []
p = sys.argv[1]
s = json.load(open(p))
cap = open(sys.argv[2]).read() if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else ""
LAYOUTS = {"words", "number", "bars", "list", "endcard"}
BANNED = ["part you never see", "part of gta 6 you never see", "thank you for guarding", "this is unseen", "unseen",
          "countdown to vice city", "guard it", "our arithmetic", "on the record", "denmark"]
DASHES = ["—", "–", "‒", "−"]

for k in ["voice_id", "model_id", "tag", "theme", "beats"]:
    if k not in s: errs.append(f"missing top level key: {k}")
beats = s.get("beats", [])
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
    if b.get("bg") == "dim" and not b.get("media") and not b.get("media_request"):
        errs.append(f"beat {i}: bg dim needs media or media_request")
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
