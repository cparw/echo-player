"""Delivery fingerprint: pace, pauses, pitch movement (semitones), loudness dynamics. Timbre independent."""
import sys, json, numpy as np, librosa
def feats(path, words):
    y, sr = librosa.load(path, sr=16000, mono=True)
    y, _ = librosa.effects.trim(y, top_db=35)
    dur = len(y) / sr
    rms = librosa.feature.rms(y=y, frame_length=640, hop_length=160)[0]
    db = 20 * np.log10(rms + 1e-9); thr = np.percentile(db, 95) - 30
    silent = db < thr
    # pauses: runs of silence >= 0.2 s
    runs, n = [], 0
    for s in silent:
        if s: n += 1
        else:
            if n: runs.append(n); n = 0
    pauses = [r * 0.01 for r in runs if r * 0.01 >= 0.2]
    f0, vflag, _ = librosa.pyin(y, fmin=60, fmax=320, sr=sr, frame_length=1024, hop_length=160)
    f0 = f0[vflag & ~np.isnan(f0)]
    st = 12 * np.log2(f0 / np.median(f0))
    return {"wpm": words / dur * 60, "pauses_per_min": len(pauses) / dur * 60, "pause_share": sum(pauses) / dur,
            "f0_median_hz": float(np.median(f0)), "pitch_spread_st": float(np.percentile(st, 90) - np.percentile(st, 10)),
            "pitch_std_st": float(np.std(st)), "loud_std_db": float(np.std(db[~silent]))}
if __name__ == "__main__":
    out = {}
    for arg in sys.argv[1:]:
        path, words = arg.rsplit(":", 1)
        out[path] = feats(path, int(words))
    print(json.dumps(out, indent=1))
