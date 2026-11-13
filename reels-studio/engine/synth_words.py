"""Synthetic word timings (no voice credits) in the words.json form build.py reads: [{w, start, end}].
Usage: python3 synth_words.py script.json out_words.json [wpm=210] [sentence_gap=0.18]
Total time = words / wpm minutes; each sentence end adds a gap; the rest is shared by letter count."""
import json, re, sys
spec = json.load(open(sys.argv[1])); wpm = float(sys.argv[3]) if len(sys.argv) > 3 else 210; gap = float(sys.argv[4]) if len(sys.argv) > 4 else 0.18
toks = [w for b in spec["beats"] if b.get("say") for w in b["say"].split()]
ends = [bool(re.search(r"[.!?]$", w)) for w in toks]
n_gaps = sum(ends[:-1])
total = len(toks) / wpm * 60
letters = [max(1, len(re.sub(r"[^A-Za-z0-9]", "", w))) for w in toks]
per = (total - n_gaps * gap) / sum(letters)
t, out = 0.0, []
for w, L, e in zip(toks, letters, ends):
    out.append({"w": w, "start": round(t, 3), "end": round(t + L * per, 3)}); t += L * per
    if e: t += gap
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(f"{len(toks)} words, {out[-1]['end']:.2f} s, {len(toks) / out[-1]['end'] * 60:.0f} wpm overall")
