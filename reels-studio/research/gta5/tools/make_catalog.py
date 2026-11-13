"""catalog_gta5.md + catalog_gta5.jpg (contact sheet) from official/gta5/shots_gta5.json.
Usage: python3 make_catalog.py <scratchpad dir>"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

S = sys.argv[1]; G = os.path.join(S, "official", "gta5")
lib = json.load(open(os.path.join(G, "shots_gta5.json")))

# ---------- contact sheet: the allowed area (crop_box) of every shot, clips at the middle of their clean window ----------
TW, TH, COLS = 400, 225, 7
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
tiles = []
tmp = os.path.join(G, "audit", "_cat"); os.makedirs(tmp, exist_ok=True)
for s in lib:
    x, y, w, h = s["crop_box"]
    if s["kind"] == "still":
        im = Image.open(s["src"]).convert("RGB").crop((x, y, x + w, y + h))
    else:
        a, b = s["clean"][0]; t = s["start"] + (a + b) / 2; f = os.path.join(tmp, f"{s['id']}.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", s["src"], "-frames:v", "1", "-vf", f"crop={w}:{h}:{x}:{y}", f], check=True)
        im = Image.open(f).convert("RGB")
    im.thumbnail((TW, TH)); tile = Image.new("RGB", (TW, TH), (18, 18, 18)); tile.paste(im, ((TW - im.width) // 2, (TH - im.height) // 2))
    d = ImageDraw.Draw(tile); lab = f"{s['id']} {'S' if s['kind'] == 'still' else 'C'} {s['name'][:24]}"
    d.rectangle([0, 0, TW, 24], fill=(0, 0, 0)); d.text((5, 2), lab, fill=(255, 210, 0), font=font)
    tiles.append(tile)
rows = (len(tiles) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * (TW + 4) + 4, rows * (TH + 4) + 4 + 40), (10, 10, 12))
d = ImageDraw.Draw(sheet)
d.text((8, 10), "Official GTA V library (Rockstar Games), audited 13 Nov 2026. S = 4K still, C = trailer clip. Ids for compare and clips.", fill=(240, 240, 240), font=font)
for i, t in enumerate(tiles):
    sheet.paste(t, (4 + (i % COLS) * (TW + 4), 44 + (i // COLS) * (TH + 4)))
sheet.save(os.path.join(G, "catalog_gta5.jpg"), quality=88)
print("sheet", sheet.size)

# ---------- markdown ----------
L = ["# Official GTA V library (Rockstar Games), audited frame by frame",
     "",
     "Built 13 Nov 2026 for the owner's rule: \"if you want to show GTA 5 comparison with GTA 6, then you should show the GTA 5 pictures also for that properly.\"",
     "Every GTA 5 vs GTA 6 beat shows these official GTA V visuals beside the GTA VI shot with the engine's `compare` key (split screen or A/B cut; see `engine/COMPARE.md`).",
     "Ids start at 500 so they never clash with the GTA VI library (`official/shots/shots.json`). Data: `official/gta5/shots_gta5.json`; contact sheet: `catalog_gta5.jpg`.",
     "",
     "## Sources (official Rockstar only, public pages, no logins, cookies or proxies)",
     "",
     "* The Grand Theft Auto V page, https://www.rockstargames.com/gta-v (4K screenshots and the map art in its page modules).",
     "* Rockstar Newswire posts with official screenshots: Screens from GTA V for PC (27 Mar 2015), New GTA V PC Screens (27 Feb 2015), GTAV PC: New Release Date, First Screens and System Specs (Jan 2015), GTAV and GTA Online Coming March 15 for PS5 and Xbox Series X|S (2022), GTA V and GTA Online Out Now on PS5 and Xbox Series X|S (2022), Free Upgrade for GTA V on PC Now Available / Coming March 4 (2025), GTA V Release Dates and Exclusive Content Details for PS4, Xbox One and PC (Sept 2014). Each shot lists its exact page and file URL.",
     "* Rockstar's own video pages (https://www.rockstargames.com/videos/ID), files Rockstar marks downloadable: Coming March 2022 for PS5 and Xbox Series X|S (r3too449, 2160p), Out Now on PS5 and Xbox Series X|S (1s626s55, 2160p), PS4, Xbox One and PC Announcement Trailer (tr45r42o, 1080p), A Picket Fence and a Dog Named Skip (kc1a9kco, 1080p), 60 Frames Per Second PC Trailer (s6rrr5ao, 1080p60). The videos stay in `official/gta5/vid/` (not committed; audio is never used).",
     "* Not used: the age gated GTA V trailers on Rockstar's site (Trailer 1, Gameplay Video, the Michael, Franklin and Trevor trailers, the PS5 announcement, First Person), YouTube (bot wall), fan uploads and mods.",
     "",
     "## How it was audited",
     "",
     "* Stills: every candidate viewed at 1500 px, then busy areas (crowds, hands, cars, cockpits, signs, corners) zoomed at full 4K. A still is held for any length with a slow push in (`clean` 0 to 10 s).",
     "* Clips: cut detection, then tiles every 0.4 s of the FULL letterbox free frame, so any crop the engine takes (9:8 split half or 9:16 full frame) is covered. Clean windows trim 0.1 s at both ends, like the GTA VI library.",
     "* `crop_box` [x, y, w, h] is the only part of a source that may ever be shown: it removes letterboxes, the GTA V logo on the 2014 screenshots, and flagged corners (a police chase far left in 520, store signs in 539, a movie poster in 509).",
     "* `focus` [fx, fy] is where the subject sits; the engine centres its crop window there unless a script gives `cx` / `cy`.",
     "* `sharp_full`: false means a 1080p letterboxed source (864 px tall); fine in a split half, soft as a full screen A/B shot. Prefer 4K stills or 4K clips for `ab`.",
     "",
     "## Clean visuals by type",
     ""]
groups = [("City skyline and landmarks", lambda s: any(t in s["tags"] for t in ("skyline", "landmark", "houses")) and "protagonists" not in s["tags"]),
          ("Crowds and pedestrians", lambda s: any(t in s["tags"] for t in ("crowds", "pedestrians"))),
          ("Streets, cars and driving", lambda s: any(t in s["tags"] for t in ("streets", "cars", "driving")) and not any(t in s["tags"] for t in ("protagonists", "beach", "countryside"))),
          ("Countryside and wide aerials", lambda s: any(t in s["tags"] for t in ("countryside", "aerial", "map")) and not any(t in s["tags"] for t in ("wildlife", "protagonists", "ocean"))),
          ("Beach and ocean", lambda s: any(t in s["tags"] for t in ("beach", "ocean")) and "wildlife" not in s["tags"]),
          ("Wildlife and animals", lambda s: any(t in s["tags"] for t in ("wildlife", "animals"))),
          ("Protagonists in calm moments", lambda s: "protagonists" in s["tags"])]
seen = set()
for title, f in groups:
    rows = [s for s in lib if f(s) and s["id"] not in seen]
    seen |= {s["id"] for s in rows}
    L.append(f"### {title} ({len(rows)})"); L.append("")
    L.append("| id | kind | what is on screen | clean window (s) | shown area | source |"); L.append("|---|---|---|---|---|---|")
    for s in rows:
        win = ", ".join(f"{a:.2f} to {b:.2f}" for a, b in s["clean"]) if s["kind"] == "clip" else "any length (still)"
        area = f"{s['res'][0]}x{s['res'][1]}" + ("" if s["sharp_full"] else ", soft full screen")
        src = f"[{'page' if s['kind'] == 'still' else 'video'}]({s['page_url']})"
        L.append(f"| {s['id']} | {s['kind']} | {s['desc']}{' (GTA Online)' if s['gta_online'] and 'GTA Online' not in s['desc'] else ''} | {win} | {area} | {src} |")
    L.append("")
left = [s for s in lib if s["id"] not in seen]
if left:
    L.append(f"### Other ({len(left)})"); L.append("")
    for s in left: L.append(f"* {s['id']} {s['kind']}: {s['desc']}")
    L.append("")
L += ["## Flagged inside kept clips (never shown: the engine and validator keep clips inside the clean windows)", ""]
for s in lib:
    bad = [g for g in s["segments"] if not g["clean"]]
    if bad:
        L.append(f"* {s['id']}: " + "; ".join(f"{g['from']:.1f} to {g['to']:.1f} {'/'.join(g['flags'])}: {g['content']}" for g in bad))
L += ["", "## Rejected candidates (not in the library)", "",
      "* GTA V key art (cover collage) and the GTA Online key arts: weapons, police, suggestive panels.",
      "* Wanted level or police: every official shot of it shows police action (chases, flashing cruisers), so none were kept.",
      "* Stills: Trevor in the desert among cacti (holds a pistol, seen only at full size); a Vinewood Boulevard street at sunset (billboard with a nude figure, exhaust flame); Trevor on a crop duster (bullet holes, smoke, logo); all stills with guns, police cars, explosions, menus, spec tables or logos (about 40).",
      "* Trailer shots: logo and rating cards, on screen text, a person jumping from an exploding train, a plane trailing smoke, an airport explosion, police lights, arcade cabinets with gun art (538 keeps only its clean window), a nightclub queue in skimpy outfits, a beach boardwalk in underwear, a jet ski branded with a crude joke name, a protester's xenophobic sign, a mountain lion attack, a strip club, a liquor store sign shot, shirtless posing on the beach, gang scenes and heist shootouts.",
      ""]
open(os.path.join(G, "catalog_gta5.md"), "w").write("\n".join(L) + "\n")
print("catalog", len(lib), "shots,", sum(1 for x in L if x.startswith("| 5")), "table rows")
