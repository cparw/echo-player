"""Merge the frame by frame footage audit into shots.json and rewrite the catalog.
Usage: python3 merge_audit.py shots.json audit_results.json catalog.md
Each shot gets "segments" (what is on screen, flags) and "clean": [[from, to], ...] (only windows with no flags).
Shots with no clean window get "banned": true. The old "safe" key is replaced by the longest clean window."""
import json, sys
shots_p, audit_p, cat_p = sys.argv[1:4]
shots = json.load(open(shots_p)); audit = json.load(open(audit_p))
by = {a["shot"]: a for a in audit}
missing = [i for i in range(len(shots)) if i not in by]
for i, sh in enumerate(shots):
    a = by.get(i)
    if not a: continue
    segs = sorted(a["segments"], key=lambda s: s["from"])
    sh["segments"] = segs
    clean = []
    for s in segs:
        badge_only = s["flags"] == ["rating_badge"] and sh.get("crop_box")
        if badge_only: s["clean"], s["flags"] = True, ["none"]; s["content"] += " (badge removed by crop_box)"
        if s["clean"] and s["flags"] == ["none"] and s["to"] - s["from"] >= 0.3:
            # trim 0.1 s at both ends so a cut never lands on a neighbouring frame
            lo, hi = round(s["from"] + 0.1, 2), round(s["to"] - 0.1, 2)
            if clean and lo - clean[-1][1] <= 0.25: clean[-1][1] = hi
            else: clean.append([lo, hi])
    sh["clean"] = clean
    sh.pop("safe", None)
    if clean: sh["safe"] = max(clean, key=lambda w: w[1] - w[0])
    sh["banned"] = not clean
json.dump(shots, open(shots_p, "w"), indent=1)
L = ["# Official GTA VI footage library (Rockstar Games), audited frame by frame",
     "", "Every window below was checked in the exact 9:16 crop the reels use (tiles every 0.4 s). Use clips ONLY inside a CLEAN window:",
     '"clips": [{"shot": N, "offset": seconds_into_shot, "at": spoken_word_index_for_the_cut}]. The mixer keeps each clip inside the clean window that contains its offset and holds the last clean frame if the beat is longer.',
     "Never use flagged windows (weapons, violence, sexual or suggestive, police action, crashes, logos or rating badges).", ""]
L.append("| shot | clean windows (s) | what is on screen in the clean part | good for |")
L.append("|---|---|---|---|")
for i, sh in enumerate(shots):
    if "segments" not in sh: continue
    cl = [s for s in sh["segments"] if s["clean"] and s["flags"] == ["none"]]
    if not cl: continue
    wins = ", ".join(f"{w[0]:.1f} to {w[1]:.1f}" for w in sh["clean"])
    desc = "; ".join(f"{s['content']} ({s['from']:.1f})" for s in cl)
    tags = ", ".join(sorted({t for s in cl for t in s.get("good_for", [])}))
    L.append(f"| {i} | {wins} | {desc} | {tags} |")
L += ["", "## Flagged windows (do not use)", ""]
for i, sh in enumerate(shots):
    bad = [s for s in sh.get("segments", []) if not (s["clean"] and s["flags"] == ["none"])]
    if bad:
        L.append(f"* {i}{' (BANNED, no clean window)' if sh.get('banned') else ''}: " + "; ".join(f"{s['from']:.1f} to {s['to']:.1f} {'/'.join(s['flags'])}: {s['content']}" for s in bad))
open(cat_p, "w").write("\n".join(L) + "\n")
print(f"merged {len(by)} shots; banned {sum(1 for s in shots if s.get('banned'))}; missing from audit: {missing}")
