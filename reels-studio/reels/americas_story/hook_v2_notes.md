# R7 Project Americas (story): hook v2

## Final hook
* Spoken (new opening): "GTA Six was planned across parts of two continents. Then it shrank." (12 words) then "But Vice City alone is still twice the size of Los Santos."
* On screen from frame one (`instant`, story captions): "GTA 6 was planned across / *parts of two continents.* / Then it shrank." The glowing key phrase is the whole "parts of two continents", so it cannot read as whole continents.
* Beat 2: "2x / VICE CITY VS LOS SANTOS" stamp on a GTA 5 / GTA 6 split.
* Cover (`cover_v2.json`): "GTA 6 was planned across" / "parts of two continents." (orange box) / "Then it shrank.", big "2x" "Vice City vs Los Santos, per Rockstar", noticed. mark.

## Voice (not a splice: R7 had never been voiced)
The whole reel was voiced at once by the main session from `punch/americas_reel/v2/script.json` (a copy of script_hook_v2.json; `americas_reel/script.json` and the old `voice/` are untouched):
```
S=/tmp/claude-0/-home-user-echo-player/53197e09-39b2-53e1-ace7-1aefc4b23039/scratchpad; bash $S/engine/voice_only.sh $S/punch/americas_reel/v2
```
n_old_beats_removed and n_new_hook_beats do not apply (no earlier take). Old beats 0 and 1 became the new beats 0 to 2. Result: 205 words, 180 wpm, speech 68.32 s; reel about 70.7 s. Recorded text matches script_hook_v2.json word for word.

## Changes vs script.json (spoken)
* Do not use list (rulebook, 13 Nov): shot 74 replaced on the 2015 trip beat with shot 41. The first v2 render (commit 4ffbe11) is superseded.
* Opening: old beats 0 and 1 ("GTA Six was first planned across parts of two continents." / "Then Rockstar cut it right back. And what they did with the piece that was left...") become the hook, the Vice City size line and "And how they built what was left is why this game looks so real." (collage kept).
* Old beat 7 ("And what survived is still big. Vice City alone is twice the size of Los Santos.") folded into the opening; its 2x stamp moved there.
* Old last beat "Imagine two continents." dropped (could read as whole continents).
* New ending (owner CTA rule): "Would you have wanted the bigger plan?" then "Follow noticed dot daily and comment AMERICAS. The full Project Americas timeline lands straight in your inbox. See you in Leonida."
* Format: the loop is removed and an engine end card added (noticed., @noticed.daily, cta "FOLLOW @noticed.daily + COMMENT AMERICAS", episode "The full Project Americas timeline lands straight in your inbox"), like the newest story reels.

## Visual fixes from the verified fact rules (all applied in script_hook_v2.json)
* Every mention says "parts of two continents" or "large stretches of North and South America", never whole continents; the lit Americas map only appears under the words "large stretches of".
* Code name card: label "CODE NAME", head "Project Americas", source "Bloomberg reports, Businessweek, 14 Oct 2026". Never "Rockstar confirmed" or "leaked".
* Date card: 2015 / FIRST RESEARCH TRIP / MIAMI, FLORIDA (non breaking spaces force exactly those two lines). Nothing implies development started in 2015.
* The shrink ends on the Florida shaped dot labelled LEONIDA (was FLORIDA). Never "the game is just Miami", never the leaked map.
* "Then it shrank." carries no year, no reason and no DLC hint; the redacted "THE REASON" card stays ("Bloomberg does not say exactly why").
* Never said: that Rob Nelson led the trip (the line says he "lands with senior staff"), four protagonists, three cities, any budget, a development start year.
* GTA 5 vs GTA 6 beat (Vice City twice Los Santos): `compare` split, top GTA V still 500 (Los Santos skyline at sunset), bottom GTA VI shot 91 at 5.4 s (BASE jump over Vice City). Renders once `engine/COMPARE_READY` exists.

## Fact check
* "Planned across parts of two continents" and "Then it shrank": VERIFIED as REPORTED (Bloomberg Businessweek, 14 Oct 2026, via GTA Intel and Notebookcheck: "covering parts of two continents", "cut back to Miami and its surroundings"; Bloomberg gives no date or reason). The proposal "GTA 6 shrank from two continents" was rephrased because it can read as whole continents.
* "Vice City alone is twice the size of Los Santos": VERIFIED, ROCKSTAR SAYS via The New York Times (reprint in The Star, 5 Sept 2026). The proposal's clipped "twice Los Santos" is spoken in full.
* Everything else is unchanged from `factcheck.md` (13 Nov).

## DM for keyword AMERICAS (paste as the auto reply)
Auto reply: here's the full Project Americas timeline, with every source 🗺️
1. 2015: Rockstar North's Rob Nelson and other senior staff fly to Miami on the game's first research trip (Bloomberg Businessweek, 14 Oct 2026).
2. The code name was Project Americas: the first plan covered large stretches of North and South America (Bloomberg).
3. Then it shrank, back to Miami and its surroundings, which became Vice City and the rest of Leonida. Bloomberg doesn't say when or why.
4. For a decade Rockstar staff kept coming back to Miami: "We hang out, get a feeling for the place, listen to the stories" (Rupert Humphries, Rockstar, to Dazed).
5. They rode along with police and visited racetracks and nightclubs (The New York Times), and interviewed respected people from every kind of neighbourhood, hiring some of them (Rob Nelson to the NYT).
6. Dec 2023: Trailer 1 gets 90,421,491 YouTube views in 24 hours, the most viewed game reveal on YouTube (Guinness World Records).
7. What survived is still huge: Vice City alone is twice the size of Los Santos (Rockstar to The New York Times).
8. 19 Nov 2026: launch.
Sources: Bloomberg Businessweek (14 Oct 2026), The New York Times, Dazed, Guinness World Records, Know Your Meme.
New GTA 6 breakdown every day on @noticed.daily. See you in Leonida.

## QA (render)
* R7_project_americas_v2.mp4: 1080x1920 30/1 fps | 70.67 s | -14.0 LUFS | TP -1.3 dBTP | 71.9 MB | end card from 68.67 s | freezes outside end card: none | PASS
* Published as reels-studio/media/R7_project_americas_v2.mp4 with cover reels-studio/media/r7_cover_v2.jpg.
