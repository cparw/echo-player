# R5 Places: hook v2

## Final hook
* Spoken (new opening, 15 words, two beats): "Florida's highest point? Three hundred forty five feet." / "Why does GTA Six have a mountain?"
* On screen: beat 1 from frame one (`instant`): FLORIDA'S HIGHEST POINT? **345 FEET.** over Rockstar's Mount Kalaga still (steep red canyon, slow pan); beat 2: WHY DOES GTA 6 HAVE A **MOUNTAIN?** over the Mount Kalaga ridge at sunset.
* Footnotes: "USGS: Britton Hill, Florida's highest natural point, 345 ft" and "Rockstar: Mount Kalaga National Park, one of six Leonida regions".
* Cover (`cover_v2.json`): Mount Kalaga background, "Florida's peak?" / "345 feet." (orange box) / "Why a mountain?", big 6 "regions, six real Floridas", noticed. mark.

## Ending (owner CTA rule, 13 Nov)
"Be honest. Which region are you? Vice City," / "or Port Gellhorn?" / "Follow for tomorrow. See you in Leonida." are replaced by "Which region are you?" then "Follow noticed dot daily and comment TRIP. The six stop road trip lands straight in your inbox. See you in Leonida." End card: cta "FOLLOW @noticed.daily + COMMENT TRIP", episode "The six stop road trip lands straight in your inbox", hold 2.0 s (was 2.8) to stay under 90 s.

## Splice (done 13 Nov by the main session)
Old voice = `six/r5_places/voice` (original full take, which had no hook). Opening: n_old_beats_removed = 0, n_new_hook_beats = 2 (prepended, as on 12 Nov). Plus the sugarcane line cut (below) and the ending.
```
S=/tmp/claude-0/-home-user-echo-player/53197e09-39b2-53e1-ace7-1aefc4b23039/scratchpad; python3 $S/engine/splice_multi.py $S/six/r5_places/voice_spec_final.json $S/six/r5_places/voice $S/six/r5_places/voice3
```
Opening only, with the older tool: `splice_hook.py <dir with the spec as script.json> $S/six/r5_places/voice 0 2 <out>`.
Result: 249 words, speech 84.52 s; reel 86.9 s with the end card. Recorded text matches script_hook_v2.json word for word.

## What changed vs script.json
* Beats 0 and 1: new hook, first shot and cover on Mount Kalaga.
* "Real Florida leads America in sugarcane." CUT with its visuals (USDA ERS: Louisiana leads; removed from the voice by the main session). The black snow line stays.
* Freeze fixes (no freeze rule): the 345 count beat pans 0.62 to 0.95 (was 1.0 to 0.995, nearly still); "River of Grass" pans 0.0 to 0.16 (was 0.04 to 0.0) and stays left of the helicopter part of that still; the first CTA beat gets a second clip.
* Ending and end card as above.

## Asked for but left out (and why)
* Midpoint rehook "GTA 5 got Mount Chiliad. Real California peaks near 14,500 feet. Florida? 345." Not used: R5 was already 88.5 s and the cap is 90 s; this line adds about 5 s, and it is a middle line. If wanted later, swap it for an existing middle line and give it a GTA V split (Mount Chiliad: GTA V library still 514 or clip 550).

## Fact check
* Florida's highest point is 345 ft (Britton Hill, Walton County): VERIFIED, USGS "Highest and Lowest Elevations" table; also the lowest state high point in the US.
* GTA 6 has a mountain region: VERIFIED as Rockstar's own region name, Mount Kalaga National Park, on rockstargames.com/VI (Only in Leonida); its official stills show steep hills and ridges.
* Rehook facts (checked even though the line is not used): Mount Whitney 14,505 ft (NPS Sequoia and Kings Canyon page, NAVD88; USGS table 14,494 ft on the older datum), so "near 14,500 feet" holds. Mount Chiliad is GTA V's mountain (Rockstar's GTA V site and Newswire).
* Sugarcane claim: removed (see above).

## DM for keyword TRIP (paste as the auto reply)
Auto reply: here's your six stop real Florida road trip 🚗
One real place for each GTA 6 region (the links are our reading; Rockstar never says they're on purpose):
1. Vice City: Miami. PortMiami's registered slogan is "The Cruise Capital of the World".
2. Leonida Keys: the Florida Keys, beside North America's only coral barrier reef (NOAA).
3. Grassrivers: Everglades National Park. "River of Grass" comes from Marjory Stoneman Douglas's 1947 book, and it's the only place where alligators and crocodiles live side by side (NPS).
4. Port Gellhorn: the Gulf coast trademarked as the Forgotten Coast (first used in 1992 by the Apalachicola Bay Chamber).
5. Ambrosia: the sugar towns on Lake Okeechobee's south shore. Growers burn cane before harvest and locals call the ash black snow (AP, 2019).
6. Mount Kalaga: Britton Hill in Walton County, near the Alabama line: Florida's highest natural point, 345 feet (USGS).
That's the full route. New GTA 6 breakdown every day on @noticed.daily. See you in Leonida.
