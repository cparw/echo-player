#!/usr/bin/env bash
# One command reel build in the owner's voice:
# validate -> guide performance (licensed ElevenLabs voice, word timestamps) -> Speech to Speech into the owner's clone
# -> pace fix toward the target wpm -> timeline -> graphics (headless Chromium) -> footage, music, mix, loudness.
# Usage: bash make_reel.sh <reel_dir> <out_name> [music.mp3] [target_wpm]
# script.json must carry voice_id (the owner's clone) and the guide_* settings (see STUDIO.md, "Voice").
set -euo pipefail
REEL="$1"; NAME="$2"; MUSIC="${3:-}"; TARGET="${4:-184}"
ENGINE="$(cd "$(dirname "$0")" && pwd)"
OUT="$REEL/$NAME"
mkdir -p "$OUT"
cp "$REEL/script.json" "$OUT/script.json"
python3 "$ENGINE/validate.py" "$OUT/script.json" "$REEL/caption.txt"
python3 "$ENGINE/tts_sts.py" "$OUT/script.json" "$OUT"
F=$(python3 - "$OUT/words.json" "$TARGET" <<'PY'
import json, sys
w = json.load(open(sys.argv[1])); wpm = len(w) / w[-1]["end"] * 60
f = min(1.10, max(0.92, float(sys.argv[2]) / wpm))
print(f"{f:.3f}" if abs(f - 1) > 0.03 else "1.000")
PY
)
echo "pace factor $F"
if [ "$F" != "1.000" ]; then python3 "$ENGINE/tempo.py" "$OUT" "$F"; fi
python3 "$ENGINE/build.py" "$OUT/script.json" "$OUT/words.json" "$OUT"
node "$ENGINE/render.js" "$OUT/timeline.json" "$OUT/graphics.mov"
python3 "$ENGINE/compose.py" "$OUT" "${MUSIC:-none}" "$OUT/$NAME.mp4"
ffprobe -v error -show_entries format=duration -of default=nw=1 "$OUT/$NAME.mp4"
