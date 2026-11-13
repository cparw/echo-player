# Compare mode: GTA 5 vs GTA 6 beats (engine compare kit)

Owner rule, 13 Nov 2026: "if you want to show GTA 5 comparison with GTA 6, then you should show the GTA 5 pictures also for that properly."
Every GTA 5 vs GTA 6 beat shows official, audited GTA V visuals beside the GTA VI shot, GTA 5 first: a split screen or a fast A/B cut.

Status: READY (installed 13 Nov, 14:23 UTC). Code: `compare_kit.py` plus small hooks in build.py, compose.py, preview.py, validate.py
and stage.html (the versions before it are kept as `*.bak_pre_compare`). Scripts without the `compare` key build and render exactly as
before: timeline.json and bgplan.json byte identical for six/r1_vs and punch/americas_reel, graphics stills of every scene pixel identical,
validator output identical.

## The beat key

```json
"compare": {
  "mode": "split",
  "left":  {"shot": 500, "t": 0},
  "right": [{"shot": 62, "t": 10.6}, {"shot": 104, "t": 0.3, "at": 8}],
  "labels": ["GTA 5", "GTA 6"]
}
```

| field | meaning |
|---|---|
| `mode` | `"split"` (default) or `"ab"` |
| `left` | the GTA 5 side: a GTA V library shot (ids 500 and up) `{"shot": N, "t": seconds into the shot}` (alias `offset`); `t` must sit inside the shot's clean window |
| `right` | the GTA 6 side: a GTA VI shot from `official/shots/shots.json` (below 500), same rules as `clips` |
| a list per side | either side may be a list of shots: items after the first take `"at": k` (spoken word index, like clip anchors) and the side cuts there. Use it whenever one clip is shorter than its time on screen |
| per shot, optional | `cx`, `cy` (0 to 1, framing of the crop window; default: the library's `focus` point, or the middle), `slow` (slow motion factor), `push` (zoom gained over the part) |
| `labels` | default `["GTA 5", "GTA 6"]`; any two short strings (no dash characters, 14 characters max); `false` hides them |
| `at` | `ab` only: spoken word index where it cuts from GTA 5 to GTA 6; default the middle word. Keep it early |
| `flash` | `ab` only: `false` removes the 2 frame white flash on the cut |
| `sfx` | `ab` only: `"whoosh"` (default), `"hit"` or `"none"` on the cut (skipped when the script's `sfx_default` is `"none"`) |
| `label_y` | optional `[top_label_y, bottom_label_y]` in pixels (keep 220 to 1440) |

The beat needs no `clips`: compare supplies the footage for the whole beat (clips given anyway are ignored, with a warning). The credit
FOOTAGE: ROCKSTAR GAMES is added automatically. `compare` cannot sit on the end card or share a beat with `collage`.

### split
Top half (1080x960) = GTA 5, bottom half (1080x960) = GTA 6, a thin off white divider on the seam (y 957 to 963, drawn under the text).
Labels: `GTA 5` (dark pill) at the top left of the top half (y 236, just under the Instagram top bar; y 380 when a fast explainer section
header is on screen) and `GTA 6` (orange pill, the hero) at the lower left of the bottom half (y 1410, above the caption zone). Landscape GTA V
sources keep almost their full width in a 9:8 half; the 4K stills stay sharp.

### ab
GTA 5 full screen (1080x1920) from the start of the beat, then a hard cut on spoken word `at` to GTA 6 full screen. One label at the top left
switches from `GTA 5` to `GTA 6` with a pop, plus a 2 frame flash and a whoosh. Keep the GTA 5 part short (about 1 to 2 s). For `ab` prefer
shots with `sharp_full: true` (the 4K stills and 4K clips): a 1080p source is soft full screen (the validator warns).

### No freezes (RULEBOOK)
Stills always push in (at least 1.6 percent zoom per second). A clip that runs out of clean footage first slows to 1.5x, then holds its
last clean frame with the same slow push, so ffmpeg freezedetect (n=0.003, d=0.5) finds nothing. Better still, give the side a second shot:
the validator estimates the beat at 180 words a minute and warns when a side will hold.

### Works with every layout and caption style
Words, number, bars, list, countdown, waffle, map, quote, versus, titlecard, build and story captions, stamps, paper cards, chips, counters,
dim and the rest render on top as before. Text on the seam reads well; move it with `centerY`, `capsY` or `wordsTop` if a beat needs the
seam clear. The `dim` blur works on the composed split frame too.

## Examples

Split, the GTA 6 half cutting on word 8 (tested; previews in `cmp_test/`):
```json
{
  "say": "Los Santos felt huge in two thousand thirteen. Vice City is twice the size.",
  "instant": true, "font": "anton", "bg": "scrim",
  "show": [["LOS@0", "SANTOS@1", "FELT@2", "HUGE@3"], ["^VICE^@8", "^CITY^@9", "IS@10", "*TWICE*@11"], ["THE@12", "SIZE.@13"]],
  "compare": {"mode": "split", "left": {"shot": 500, "t": 0}, "right": [{"shot": 62, "t": 10.6}, {"shot": 104, "t": 0.3, "at": 8}]}
}
```

A/B cut on word 4, story captions:
```json
{
  "say": "This was Los Santos. And this is Vice City.", "bg": "scrim", "caps_style": "story",
  "caps": [{"text": "This was Los Santos.", "key": ["Los Santos."]}, {"text": "And this is Vice City.", "at": 4, "key": ["Vice City."]}],
  "compare": {"mode": "ab", "left": {"shot": 531, "t": 0.2}, "right": {"shot": 104, "t": 0.3}, "at": 4}
}
```

GTA V shots may also appear in plain `clips` (ids 500 and up, clean windows enforced, stills push in), but the validator errors on a beat
whose footage is only GTA V and warns to use `compare` so viewers see which game is which.

## GTA V library (official Rockstar material only, audited frame by frame)

Files: `official/gta5/shots_gta5.json` (same fields as shots.json plus `id`, `kind`, `desc`, `tags`, `focus`, `res`, `sharp_full`,
`source_url`, `page_url`), `official/gta5/catalog_gta5.md` (clean windows, sources, flags), `official/gta5/catalog_gta5.jpg` (contact sheet).
68 visuals: 29 stills (500 to 528, most of them 4K, held for any length) and 39 official trailer clips (530 to 568, 0.5 to 3.3 s of clean footage each).

| ids | kind | what |
|---|---|---|
| 500 to 509 | stills | Los Santos skyline at sunset, downtown by day over a park, skyline at dusk (stylized), downtown and freeway at dusk, Vinewood sign over the city (day, golden haze, sunset), freeway at night, golf course and skyline, crowd on the Vinewood Boulevard walk of fame |
| 510 to 513 | stills | cars and driving: street race at dusk (a Bravado Banshee), supercar drifting in the rain, quad bike with a coyote in a canyon, quad bike jump at sunset with the skyline |
| 514 to 521 | stills | countryside and wildlife: Mount Chiliad cable car, freight trains by the Alamo Sea (2), countryside highway with a biplane, tree on a rocky point, river and waterfall with rabbits, deer and a mountain lion, stag and doe at sunset, deer in a meadow |
| 522 to 524 | stills | ocean and map: lighthouse and speedboat from above, Del Perro pier at night from the water, Rockstar's gold map art of Los Santos |
| 525 to 528 | stills | protagonists, calm: Trevor flying a helicopter over Sandy Shores, Michael on the phone at night, Franklin with Chop on his doorstep, Michael leaning on a classic sports car |
| 530 to 540 | clips | city: sunset power lines, skyline from the hills, skyscrapers from below, city hall tower, river bridge and skyline, smokestacks at sunset, Maze Bank tower from above, Richman Hotel sign, penthouse view at sunset (GTA Online), neighborhood with skyline, Vinewood Hills at sunset |
| 541 to 545 | clips | streets and driving: freeway interchange traffic, freeway signs, lowriders downtown (GTA Online), coastal highway drive, Franklin in a convertible at sunset |
| 546 to 548 | clips | crowds and pedestrians: Vespucci boardwalk crowd with a mime, mime close up, Sandy Shores street with cyclists, a dog and a biplane |
| 549 to 554 | clips | countryside and aerial: plane over Blaine County, Mount Chiliad at sunset, freight train in a forest, lumber mill, quarry, Paleto Bay aerial at sunset |
| 555 to 558 | clips | beach and ocean: beach from above (Cayo Perico, GTA Online), Vespucci Beach and pier, quad bike on the beach at sunset, underwater swimmer silhouette |
| 559 to 563 | clips | wildlife: stag on a hillside at sunset, deer in a forest, hammerhead sharks, orca, a dog |
| 564 to 568 | clips | protagonists, calm: Michael, Franklin and Trevor in a kitchen, Michael at his tennis court, Michael doing yoga, yoga by the pool, Lester, Trevor and Michael in a car |

Not in the library on purpose: anything with weapons, police, chases, crashes, fire, nudity or suggestive content, logos or rating cards, the
GTA V key art (it has weapons), the wanted level (every official shot of it shows police action), and the age gated trailers on Rockstar's site.
