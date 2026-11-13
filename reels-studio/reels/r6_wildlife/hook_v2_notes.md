# R6 Wildlife: hook v2

## Final hook
* Spoken (new opening, 18 words, two beats): "GTA Six has more kinds of birds than GTA Five had animals." / "Even Florida's invaders made the cut."
* On screen from frame one (`instant`): GTA 6 HAS MORE KINDS OF **BIRDS** THAN GTA 5 HAD **ANIMALS.** on a GTA 5 / GTA 6 split; beat 2 over Rockstar's Leonida Keys still of an iguana crossing (slow pan).
* Footnotes: "REPORTED: 60+ bird types in GTA VI (Game Informer, Sept 2026). GTA V: 28 animal species (GTABase count)" and "REPORTED: Game Informer, Sept 2026: non native animals such as monkeys and armadillos".
* Cover (`cover_v2.json`): "GTA 6 has more" / "kinds of birds" (orange box) / "than GTA 5 had animals.", big "60+" "bird types in GTA 6, reported", Mount Kalaga deer still behind, noticed. mark.

## Ending (owner CTA rule, 13 Nov)
"So which animal are you finding first? Tell me in the comments." + "Follow for tomorrow. See you in Leonida." are replaced by "So which animal are you finding first?" then "Follow noticed dot daily and comment WILD. The trailer spotting list lands straight in your inbox. See you in Leonida." End card: cta "FOLLOW @noticed.daily + COMMENT WILD", episode "The trailer spotting list lands straight in your inbox".

## Splice (done 13 Nov by the main session)
Old voice = `six/r6_wildlife/voice` (current full take). Opening: n_old_beats_removed = 1 (the iguana hook "Real Florida warns people about falling iguanas. GTA Six put the iguanas in."), n_new_hook_beats = 2. Ending: 2 old beats out, 4 new beats in.
```
S=/tmp/claude-0/-home-user-echo-player/53197e09-39b2-53e1-ace7-1aefc4b23039/scratchpad; python3 $S/engine/splice_multi.py $S/six/r6_wildlife/script_hook_v2.json $S/six/r6_wildlife/voice $S/six/r6_wildlife/voice3
```
Opening only, with the older tool: `splice_hook.py <dir with the spec as script.json> $S/six/r6_wildlife/voice 1 2 <out>`.
Result: 213 words, speech 73.38 s. Recorded text matches script_hook_v2.json word for word.

## What changed vs script.json
* Beats 0 and 1: new hook and bridge. The old iguana hook is gone; the falling iguana payoff at the end still works as the last real Florida detail.
* Hook `compare` (GTA 5 vs GTA 6 beat): split, top GTA V still 519 (river and waterfall with rabbits, a deer and a mountain lion), bottom GTA VI shot 82 (airboat on a swamp river, birds overhead; 2.8 s clean, so no freeze). Clips kept only as the fallback.
* Freeze fixes (no freeze rule; the live R6 froze 8.4 to 11.1 s): the iguana line now cuts shot 5 (slow 2.0), shot 27 at word 8, shot 1 at word 12; the closing "See you in Leonida." uses shot 91 instead of a 0.3 s window of shot 5.
* Ending and end card as above.

## Fact check
* GTA VI bird count: VERIFIED as REPORTED. Game Informer's cover feature "Grand Theft Auto VI: Welcome to Leonida" (29 Sept 2026) gives over 170 animal species, per Rockstar, including more than 60 bird types and 30+ land mammals; relayed by Kotaku, VGC (sharks, whales, jellyfish), Dexerto, Insider Gaming and Beebom. Note: one later Kotaku piece says 150+; Rockstar's figure and most outlets say 170+.
* GTA V animal count: 28 species in story mode (GTABase, "28 Animal Species ... 13 of which are exclusive to the Next Gen edition"; Red Bull Gaming, "around 28 animal species"); 40 even counting every GTA Online addition (GTA Wiki). Rockstar never published a GTA V count.
* Claim "GTA 6 has more kinds of birds than GTA 5 had animals": HOLDS (60+ against 28, or 40 with Online). Labels: REPORTED for GTA VI, a fan count for GTA V, comparison is OUR MATH.
* "Even Florida's invaders made the cut": SUPPORTED. Game Informer reports non native animals such as monkeys and armadillos; Rockstar's own Leonida Keys still shows a green iguana; Florida's FWC lists green iguanas as invasive (already in the reel).

## DM for keyword WILD (paste as the auto reply)
Auto reply: here's your GTA 6 trailer spotting list 🦩
Where to look in Rockstar's own trailers and screenshots:
1. Launch Trailer: a green iguana crossing a sunny road.
2. Launch Trailer: the Welcome to The Keys sign has a heron and a shark painted on it.
3. Trailer 2: a cat sitting on an ATM.
4. Trailer 2: someone's pet snake, just hanging out.
5. Extended Look: two seagulls squabbling on a sidewalk by a mural.
6. Rockstar's Ultimate Edition screenshot: dolphins right off the boat.
7. Rockstar's Leonida Keys screenshot: an iguana crossing in front of a mobility scooter.
The numbers (reported, Rockstar to Game Informer, Sept 2026): over 170 species, 60+ bird types, 30+ land mammals, plus sharks, whales and jellyfish. Some are Rare, Discoverable or Legendary.
Real Florida bonus: rhesus macaques have lived wild at Silver Springs since the 1930s (UF/IFAS), and green iguanas are listed as invasive (FWC).
Happy spotting. New GTA 6 breakdown every day on @noticed.daily. See you in Leonida.
