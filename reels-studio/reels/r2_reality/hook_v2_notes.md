# R2 Reality check: hook v2

## Final hook
* Spoken (new opening, 13 words): "GTA Six is eighty dollars. GTA Five cost eighty six in today's money."
* On screen from frame one (`instant`): GTA 6 IS **$80.** / GTA 5 COST **$86** / IN TODAY'S MONEY.
* Footnote: "Our math: $59.99 in Sept 2013 is $86.47 in Oct 2026 (BLS CPI). In plain dollars GTA VI costs $20 more."
* Cover (`cover_v2.json`): "GTA 6 is $80." / "GTA 5 cost $86" (orange box) / "in today's money.", big "$80 vs $86", noticed. mark.

## Ending (owner CTA rule, 13 Nov; recorded by the main session, see NEW_ENDING.json)
"Comment CHECK and I'll send you my full launch checklist." and "Follow for tomorrow. See you in Leonida." are gone. The question "Standard or Ultimate? Tell me which one." stays, then "Follow noticed dot daily and comment CHECK. My full launch checklist lands straight in your inbox. See you in Leonida." (three beats on screen). End card: cta "FOLLOW @noticed.daily + COMMENT CHECK", episode "The launch checklist lands straight in your inbox".
This replaces the hook team's proposed end line ("Comment CHECK and I'll DM you my full launch checklist. Follow @noticed.daily for tomorrow...").

## Splice (done 13 Nov by the main session, which alone calls ElevenLabs)
Old voice = `six/r2_reality/voice` (original full take; `voice2` has no script_at_voice.json). Opening: n_old_beats_removed = 1 (the original "Eighty dollars for GTA Six sounds like a lot. Here's the reality check."), n_new_hook_beats = 1. Ending: 3 old lines out, 2 new in.
The opening alone, with the older tool:
```
S=/tmp/claude-0/-home-user-echo-player/53197e09-39b2-53e1-ace7-1aefc4b23039/scratchpad; R=$S/six/r2_reality; mkdir -p $R/hook_v2 && cp $R/script_hook_v2.json $R/hook_v2/script.json && python3 $S/engine/splice_hook.py $R/hook_v2 $R/voice 1 1 $R/voice3
```
Both ends, as run: `python3 $S/engine/splice_multi.py $R/voice_spec_v2.json $R/voice $R/voice3`.
Result: hook 13 words (gain +0.4 dB), ending 27 words (gain minus 1.3 dB); 216 words, speech 69.79 s. The build lifts the hook a further 1.5 dB to match the next line (minus 16.8 against minus 16.6 LUFS).

## What changed vs script.json
* Do not use list (rulebook, 13 Nov, narrowed): the one elevator use of shot 74 (offset 0.5 s, Lucia posing) on the Ultimate and Xbox line is replaced by shots 15 and 65; shot 74 at 13, 15 and 21 s stays (inside its clean 4.6 to 39.8 s part). stanier_neon.jpg stays (hands on the wheel, no weapon).
* Beat 0: new hook (say, show, footnote), `compare` split.
* Beat 2 (price card): `compare` split.
* "Buy before November twentieth..." footnote now reads exactly "Rockstar: digital buys before 20 Nov. Boxed preorders while supplies last." (coordinator, 13 Nov).
* Xbox One line: third clip (shot 82 at word 9) so nothing holds; the live R2 held 0.5 s here (no freeze rule).
* Ending and end card as above.

## GTA 5 vs GTA 6 beats (owner rule: GTA V visuals beside GTA VI)
* Beat 0 (hook): split, top GTA V still 500 (Los Santos skyline at sunset), bottom GTA VI shot 91 at 2.5 s (BASE jump over Vice City).
* Beat 2 (price card): split, top GTA V still 505 (behind the Vinewood sign in golden haze), bottom GTA VI shot 77 at 6.6 s (waterfront avenue and high rises).
* Renders once `engine/COMPARE_READY` exists. Clips stay in the script only as the fallback.

## Fact check
* CPI, Sept 2013: 234.149 (BLS CPI U, US city average, not seasonally adjusted; BLS release of 30 Oct 2013 and the BLS historical table). VERIFIED.
* CPI, Oct 2026 (latest month): 337.511 (BLS CPI release of 10 Nov 2026: "increased to an index level of 337.511"). VERIFIED. BLS could not publish a 12 month change for Oct 2026 (no Oct 2025 data after the funding lapse); the index level is published.
* Math: 59.99 x 337.511 / 234.149 = 86.47, so "$86 in today's money". VERIFIED (OUR MATH).
* GTA V $59.99 at launch (17 Sept 2013) and GTA VI Standard $79.99: VERIFIED (already in the approved R2 and its caption).
* FRED and the BLS data API could not be reached from this session, so the two index values were read from BLS release pages through search.

## DM for keyword CHECK (paste as the auto reply)
Auto reply: here's your GTA 6 launch checklist ✅
1. Launch is 19 Nov. Your PS5 or Xbox store page shows your exact unlock time (the PlayStation Store lists midnight local time).
2. Free up to 212 GB (Rockstar).
3. Pre load is open now. On PS5 turn on Stay Connected to the Internet in Rest Mode so it finishes overnight.
4. Boxed copy? It holds a download code, no disc (Rockstar). Redeem it now so you can pre load.
5. Vintage Vice City Pack ('55 Vapid Stanier, Shore Court garage, vintage outfits): digital buys before 20 Nov, boxed preorders while supplies last (Rockstar).
6. Xbox: Standard $79.99 now plus the $20 upgrade later equals Ultimate's $99.99 (Microsoft Store). PlayStation had no upgrade price as of 12 Nov.
7. Xbox One: stream only, through Xbox Cloud Gaming from 1 a.m. ET on 19 Nov (Xbox Wire). Game sold separately.
8. Every console targets 30 fps. PS5 Pro adds PSSR and ray traced shadows (Rockstar).
9. Reviews are reported for 18 Nov (Insider Gaming), not confirmed by Rockstar.
That's the full list. New GTA 6 breakdown every day on @noticed.daily. See you in Leonida.

(Changed from the 12 Nov version: no single US unlock time and no fixed pre load date, because reports conflict; the bonus rule follows Rockstar's digital and boxed wording.)
