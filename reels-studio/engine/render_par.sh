#!/usr/bin/env bash
# Parallel graphics render: split the timeline into N frame-aligned chunks, render them at once, join losslessly.
# Usage: bash render_par.sh timeline.json out.mov [chunks]
set -euo pipefail
TL="$1"; OUT="$2"; N="${3:-3}"
ENGINE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(dirname "$OUT")/_chunks"; rm -rf "$TMP"; mkdir -p "$TMP"
read FPS FRAMES < <(python3 -c "import json,sys;t=json.load(open(sys.argv[1]));f=t.get('fps',30);print(f, round(t['duration']*f))" "$TL")
pids=()
for ((i=0;i<N;i++)); do
  f0=$(( FRAMES * i / N )); f1=$(( FRAMES * (i+1) / N ))
  s0=$(python3 -c "print($f0/$FPS)"); s1=$(python3 -c "print($f1/$FPS)")
  node "$ENGINE/render.js" "$TL" "$TMP/part_$i.mov" "$s0" "$s1" > "$TMP/part_$i.log" 2>&1 &
  pids+=($!)
done
for p in "${pids[@]}"; do wait "$p"; done
: > "$TMP/list.txt"; for ((i=0;i<N;i++)); do echo "file '$TMP/part_$i.mov'" >> "$TMP/list.txt"; done
ffmpeg -y -v error -f concat -safe 0 -i "$TMP/list.txt" -c copy "$OUT"
echo "done $FRAMES frames in $N chunks -> $OUT"
