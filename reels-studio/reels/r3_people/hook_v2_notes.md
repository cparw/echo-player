# R3 People: hook v2

## Final hook
* Spoken (new opening, 11 words): "A King of the Hill star plays one of these eight."
* On screen from frame one (`instant`): A **KING OF THE HILL** STAR PLAYS ONE OF THESE **8.**
* Footnote (no spoiler): "REPORTED: AP interview, Sept 2026. Rockstar hasn't published a cast list."
* Payoff, on screen only, on the Brian Heder beats (spoken words unchanged): a name chip "KING OF THE HILL'S STEPHEN ROOT, REPORTED" over the official Brian Heder image and the next shot, with the footnote "REPORTED: Root told the AP he is in GTA 6 (Sept 2026); outlets identify his role as Brian Heder". Name as text only, no photo of him.
* Cover (`cover_v2.json`): "A King of the Hill star" / "is one of these 8." (orange box), big 8, noticed. mark.

## Ending (owner CTA rule, 13 Nov)
"So which one are you?" stays as recorded, then the new line "Follow noticed dot daily and comment CAST. The character cheat sheet lands straight in your inbox. See you in Leonida." (three beats on screen). "Send this to your Cal." and "Follow for tomorrow. See you in Leonida." are gone. End card: cta "FOLLOW @noticed.daily + COMMENT CAST", episode "The character cheat sheet lands straight in your inbox".

## Splice (done 13 Nov by the main session, which alone calls ElevenLabs)
Old voice = `six/r3_people/voice` (original full take). Opening: n_old_beats_removed = 4 ("Your friend group already has" / "a GTA Six character in it." / "Rockstar wrote eight official profiles." / "You'll recognize someone."), n_new_hook_beats = 1. Ending: 2 old beats out, 1 new line in (3 beats in the script).
```
S=/tmp/claude-0/-home-user-echo-player/53197e09-39b2-53e1-ace7-1aefc4b23039/scratchpad; python3 $S/engine/splice_multi.py $S/six/r3_people/script_hook_v2.json $S/six/r3_people/voice $S/six/r3_people/voice3
```
Opening only, with the older tool: `python3 $S/engine/splice_hook.py <dir holding script_hook_v2.json as script.json> $S/six/r3_people/voice 4 1 <out>` (it cannot do the ending).
Result (`voice3/splice_report.txt`): opening 4 old lines (19 words) to 1 new (11 words), gain +2.0 dB; ending 2 old lines (12 words) to 3 new (20 words), gain +1.8 dB; 239 words, speech 77.35 s. The recorded text matches script_hook_v2.json word for word.

## What changed vs script.json
* Beat 0: new hook (say, show, footnote); clips cut at word 6.
* Brian Heder beat and the Mudslide beat: name chip added; footnotes swapped (REPORTED line on the Brian beat, the official bio line moved to the Mudslide beat).
* Ending: as above; new CTA beats; end card cta and episode.
* Freeze fix (no freeze rule): the first CTA beat gets a second clip (shot 83 at word 4) so shot 43 never holds.

## Fact check
* Stephen Root is in GTA 6: VERIFIED as REPORTED. He told the AP at the BAFTA TV Tea Party (Sept 2026), "Yeah, you're gonna see me in there", and that his character was in the first rollout, recognised by fans from his King of the Hill voice (Push Square, 14 Sept 2026, quoting the AP clip; also Variety AU, Insider Gaming).
* "Brian Heder. Voiced by Stephen Root." with "REPORTED: Stephen Root to the AP": FAILS as worded. In the AP clip Root does not name his character; Push Square, Tweaktown and Tbreak say the Brian Heder link is inferred from his voice and Rockstar's character text, and Rockstar has published no cast list. Closest true version used: "King of the Hill's Stephen Root, reported" on screen, with the footnote above.
* "Plays one of these eight": SUPPORTED. Root says his character was in Rockstar's first rollout; the eight in this reel are the eight official profiles from that rollout, and every outlet places him as Brian Heder, one of them.
* Root is a King of the Hill star: VERIFIED (he voices Bill Dauterive and Buck Strickland, main cast).

## DM for keyword CAST (paste as the auto reply)
Auto reply: here's your GTA 6 character cheat sheet 🎬
All 8 official characters, from Rockstar's own bios:
1. Jason Duval: grew up around grifters, then the Army, then the Keys. Wants an easy life; it keeps getting harder.
2. Lucia Caminos: her father taught her to fight as soon as she could walk. Leonida Penitentiary, then sheer luck got her out.
3. Cal Hampton: Jason's friend. Feels safest at home with a few beers and private browser tabs. Snoops on Coast Guard comms.
4. Brian Heder: runs a boat yard in the Keys with his third wife Lori. Lets others do the dirty work.
5. Boobie Ike: a Vice City legend with real estate and a recording studio, and he acts like it.
6. Dre'Quan Priest: Boobie's partner in Only Raw Records. Always more of a hustler than a gangster.
7. Real Dimez: a duo, friends since high school, viral videos and viral hooks, now signed to Only Raw Records.
8. Raul Bautista: confidence, charm and cunning, always hunting for talent.
The voice: King of the Hill's Stephen Root told the AP in Sept 2026 that he's in GTA 6; outlets identify his role as Brian Heder. Rockstar hasn't published a cast list.
That's all eight. New GTA 6 breakdown every day on @noticed.daily. See you in Leonida.

## QA (render)
* R3_characters_v2.mp4: 1080x1920 30/1 fps | 80.50 s | -14.0 LUFS | TP -1.4 dBTP | 65.3 MB | end card from 77.70 s | freezes outside end card: none | PASS
* Published as reels-studio/media/R3_characters_v2.mp4 with cover reels-studio/media/r3_cover_v2.jpg.
