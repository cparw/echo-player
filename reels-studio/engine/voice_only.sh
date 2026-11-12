#!/usr/bin/env bash
# Voice only: guide TTS -> Speech to Speech into the owner's clone -> pace fix. Leaves narration.mp3 + words.json in <reel_dir>/voice.
# Usage: bash voice_only.sh <reel_dir> [target_wpm]
set -euo pipefail
REEL="$1"; TARGET="${2:-184}"
ENGINE="$(cd "$(dirname "$0")" && pwd)"
OUT="$REEL/voice"; mkdir -p "$OUT"
cp "$REEL/script.json" "$OUT/script_at_voice.json"
python3 "$ENGINE/tts_sts.py" "$REEL/script.json" "$OUT"
F=$(python3 - "$OUT/words.json" "$TARGET" <<'PY'
import json, sys
w = json.load(open(sys.argv[1])); wpm = len(w) / w[-1]["end"] * 60
f = min(1.10, max(0.92, float(sys.argv[2]) / wpm))
print(f"{f:.3f}" if abs(f - 1) > 0.03 else "1.000")
PY
)
echo "pace factor $F"
if [ "$F" != "1.000" ]; then python3 "$ENGINE/tempo.py" "$OUT" "$F"; fi
python3 -c "import json,sys;w=json.load(open(sys.argv[1]));print('final wpm', round(len(w)/w[-1]['end']*60), 'speech', round(w[-1]['end'],2),'s')" "$OUT/words.json"
