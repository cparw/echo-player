"""Bring a reel script and caption in line with the current brand rules (works on the CURRENT files, idempotent).
Usage: python3 harmonize.py reelNN [reelMM ...]
"""
import json, os, sys
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ref = json.load(open(os.path.join(S, "reel01/v3/script.json")))
SIGN = "Follow for tomorrow. See you in Leonida."
SIGN_SHOW = [["Follow@0", "for@1", "tomorrow.@2"], ["See@3", "you@4", "in@5"], ["*Leonida.*@6"]]
OLD_SIGNS = ("That's the number. Follow, and I'll see you tomorrow.",)
for d in sys.argv[1:]:
    p = os.path.join(S, d, "script.json")
    s = json.load(open(p))
    for k in ("voice_id", "model_id", "guide_voice_id", "guide_speed", "guide_stability", "guide_style"):
        s[k] = ref[k]
    beats = s["beats"]
    last = max(i for i, b in enumerate(beats) if b.get("say"))
    b = beats[last]
    if b["say"].strip() in OLD_SIGNS or "see you in leonida" not in b["say"].lower():
        if b["say"].strip() in OLD_SIGNS:
            b["say"], b["show"] = SIGN, SIGN_SHOW
        else:  # keep their closing line, add ours as its own beat
            nb = {"say": SIGN, "show": SIGN_SHOW, "layout": "words", "font": "anton", "bg": "dim", "clips": [{"shot": 74, "offset": 14.5}]}
            beats.insert(last + 1, nb); last += 1
    for c in beats[last].get("clips") or []:
        if c.get("shot") == 22: c.update(shot=74, offset=14.5)
    if not beats[last].get("clips") and not beats[last].get("media"):
        beats[last].update(clips=[{"shot": 74, "offset": 14.5}], bg="dim")
    ec = beats[-1]
    if ec.get("layout") == "endcard":
        tag = s.get("tag", "").split("·")[-1].strip().lower()
        series = {"tomorrow": "1 day out", "launch day": "Launch day", "day 2": "Day 2"}.get(tag, tag) or ec.get("series", "")
        ep = ec.get("episode", "").split(": ", 1)[-1]
        ec.update(brand="GTA 6", series=series[:1].upper() + series[1:], episode=ep, cta="Follow for tomorrow")
    json.dump(s, open(p, "w"), indent=1, ensure_ascii=False)
    cp = os.path.join(S, d, "caption.txt")
    if os.path.exists(cp):
        c = open(cp).read()
        c = c.replace("One number a day. Follow so you don't miss tomorrow's.", "Follow for tomorrow. See you in Leonida.")
        c = c.replace("That's the number. Follow, and I'll see you tomorrow.", "Follow for tomorrow. See you in Leonida.")
        open(cp, "w").write(c)
    print(d, "|", beats[last]["say"], "|", ec.get("series"), "|", ec.get("episode"))
