#!/usr/bin/env bash
# One command reel build: voice (ElevenLabs with timestamps) -> pace fix -> timeline -> graphics -> mix.
# Usage: bash make_reel.sh <reel_dir> <voice_id> <out_name> [music.mp3] [target_wpm]
set -euo pipefail
REEL="$1"; VOICE="$2"; NAME="$3"; MUSIC="${4:-}"; TARGET="${5:-178}"
ENGINE="$(cd "$(dirname "$0")" && pwd)"
OUT="$REEL/$NAME"
mkdir -p "$OUT"
python3 - "$REEL/script.json" "$OUT/script.json" "$VOICE" <<'EOF'
import json, sys
s = json.load(open(sys.argv[1])); s["voice_id"] = sys.argv[3]
json.dump(s, open(sys.argv[2], "w"), indent=1)
EOF
python3 "$ENGINE/tts.py" "$OUT/script.json" "$OUT"
# pace: speed up (never slow down) toward TARGET wpm, capped at 1.10 to keep the voice natural
F=$(python3 - "$OUT/words.json" "$TARGET" <<'EOF'
import json, sys
w = json.load(open(sys.argv[1])); wpm = len(w) / w[-1]["end"] * 60
print(f"{min(1.10, max(1.0, float(sys.argv[2]) / wpm)):.3f}")
EOF
)
echo "tempo factor $F"
if [ "$F" != "1.000" ]; then python3 "$ENGINE/tempo.py" "$OUT" "$F"; fi
python3 "$ENGINE/build.py" "$OUT/script.json" "$OUT/words.json" "$OUT"
node "$ENGINE/render.js" "$OUT/timeline.json" "$OUT/graphics.mov"
python3 "$ENGINE/compose.py" "$OUT" "${MUSIC:-none}" "$OUT/$NAME.mp4"
ffprobe -v error -show_entries format=duration -of default=nw=1 "$OUT/$NAME.mp4"
