"""Apply several separate spoken changes (new opening, cut lines, new ending...) to an already voiced reel, one block at a
time with splice_lines.py, so only the changed lines are recorded.
Usage: python3 splice_multi.py <final_voice_spec.json> <old_voice_dir> <out_voice_dir>
"""
import difflib, json, os, shutil, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
final_path, old_dir, out = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
final = json.load(open(final_path))
old_spec = json.load(open(os.path.join(old_dir, "script_at_voice.json")))
O = [b["say"].strip() for b in old_spec["beats"] if b.get("say")]
N = [b["say"].strip() for b in final["beats"] if b.get("say")]
ops = [op for op in difflib.SequenceMatcher(None, O, N, autojunk=False).get_opcodes() if op[0] != "equal"]
assert ops, "nothing changed"
base = {k: v for k, v in final.items() if k != "beats"}
cur, cur_dir, shift = list(O), old_dir, 0
work = out + "_steps"; os.makedirs(work, exist_ok=True)
for n, (tag, i1, i2, j1, j2) in enumerate(ops, 1):
    cur = cur[:i1 + shift] + N[j1:j2] + cur[i2 + shift:]
    shift += (j2 - j1) - (i2 - i1)
    sp = os.path.join(work, f"spec_{n}.json")
    json.dump(dict(base, beats=[{"say": x} for x in cur]), open(sp, "w"), indent=1, ensure_ascii=False)
    step = out if n == len(ops) else os.path.join(work, f"step_{n}")
    print(f"step {n}/{len(ops)}: {tag} old lines {i1 + 1}-{i2} -> {j2 - j1} new", flush=True)
    subprocess.run(["python3", os.path.join(here, "splice_lines.py"), sp, cur_dir, step], check=True)
    cur_dir = step
assert cur == N
json.dump(final, open(os.path.join(out, "script_at_voice.json"), "w"), indent=1, ensure_ascii=False)
print("done:", out)
