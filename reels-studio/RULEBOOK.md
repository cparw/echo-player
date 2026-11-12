# GTA 6 Reels: Rule Book

Read this first, every session, before planning or making anything. Every rule below came from the owner (Chaitanya) or from what we proved works. When the owner gives new feedback, add it to the Feedback log at the bottom and update the rule it touches, the same day, so he never has to say it twice.

Technical details (engine commands, accounts, file paths) live in `STUDIO.md`. This file is the WHAT and WHY.

## 1. Non negotiables (from the owner)

1. **Every frame shows GTA 6.** No black screens, no empty or plain cards, no void frames, start to end card. Real official GTA VI footage and gameplay the whole time, with many different shots. The visuals amaze people and keep them watching while they listen.
2. **Show GTA 6 at its best.** Full colour footage. Text sits on a soft local shadow behind the words, never a full screen tint or heavy filter that hides the graphics.
3. **More gameplay.** Prefer the Extended Look gameplay clips and other native vertical footage, plus Rockstar's official 4K screenshots with slow motion. Landscape trailer crops are softer (upscaled), so use them for variety, not as the base.
4. **Best quality.** 1080x1920, 9:16, full bleed, no bars, no stretching, no rating badges or logos (crop them out). Sharpest sources first.
5. **The owner's own voice** with the approved delivery (section 3). Never ship a stock or placeholder voice as final.
6. **Safe for every platform.** No guns, violence, nudity, suggestive shots, police action, crashes, gore, drugs, logos or rating badges on screen. Only audited clean footage windows (section 4).
7. **Every fact verified and labelled** (ROCKSTAR SAYS, REPORTED, ESTIMATE, OUR MATH). Never invent a number, quote, date or source.
8. **No dash characters** (hyphen, en dash, em dash) in anything shown to the owner, in captions or in on screen text.
9. **Speed.** Use many agents in parallel (the owner asked for 12 to 25). Deliver finished media fast and keep going without waiting when the next step is clear.
10. **Six reels at a time**, each one made "like that properly" (owner, 12 Nov 2026).

## 2. What works for GTA 6 reels

### Formats that pull views
From the owner's reference reel (@themercurialthing, Oct 2026, Hindi, "3 GTA 6 reels that get 100M views"):
1. **GTA 5 vs GTA 6 comparison.** Side by side cards (GTA V value vs GTA VI value) over gameplay.
2. **GTA 6 Reality Check.** Price, editions, is it worth it, which devices, install size, what is missing at launch.
3. **Storyline.** Theories, characters, opinions, everything people are waiting to know (Jason, Lucia and the cast).

Our own pillars that fit the same audience: countdown and launch news, places (the real Florida behind Leonida), hidden trailer details (wildlife, signs, weather), music and radio, launch guides. Ranked ideas: `research/content_bank.md`.

### Structure of a reel
* **Hook in the first 1 to 2 seconds**, 12 words or fewer, with the strongest gameplay shot on screen immediately.
* **Save prompt early** when the reel is useful ("Save this before launch").
* **Share prompt before the best part** ("Send this to the friend who still plays GTA 5").
* **Midpoint rehook** so the second half holds.
* **90/10 rule:** give 90% of the value in the reel; offer the rest with "Comment WORD and I'll DM you ...". A comment to DM tool sends it and asks them to follow. This turns views into followers.
* **End** on an easy question people can answer in one line, then "Follow for tomorrow. See you in Leonida."
* Length 61 to 90 seconds (TikTok rewards need over a minute). 175 to 190 words a minute. Short sentences, second person, calm and cinematic like Unseen.

### Visual grammar (from studying @unseenbyneuralway)
* Footage first. Cut every 1.5 to 2.5 seconds, on a spoken word, never one shot behind a long line.
* Match each shot to the line it sits under.
* Kinetic word synced text; orange highlight box on key words; numbers count up; comparisons as GTA V vs GTA VI cards; maps for places and time zones; quote cards for exact quotes; icons sparingly.
* Tiny source footnote on every stat. Credit tag FOOTAGE: ROCKSTAR GAMES.
* End card over footage, never black.
* Copy their pattern and quality, never their lines, sign off, topics or look.

## 3. Voice

* Approved (owner, 12 Nov 2026: "the voice you have given to the reel ... is fine. That is okay"): **voice preset 1**. A Brian guide performance turned into the owner's ElevenLabs clone "Instagram" with Speech to Speech, paced to about 184 wpm. Use `voice_preset: 1` in script.json.
* History: plain clone TTS was rejected ("none of the voices match how the person was saying"). The owner briefly felt "I don't recognize my voice" and heard a 7 option lineup, then kept preset 1. Options 2 to 7 stay available in `engine/tts_sts.py` if he asks again.
* Accent target: about 70% American, 30% Indian.
* The clone was made from one 30 second sample. If likeness ever comes up again, ask him to add 2 to 3 minutes of clean recordings to the clone in ElevenLabs.
* Never clone or imitate anyone else's voice, including the reference narrator.
* To change only the visuals of a reel, reuse its approved narration and word timings (no new voice credits).

## 4. Footage and safety

* Sources that work: Rockstar's official TikTok (all GTA VI posts are downloaded), official 4K screenshots on rockstargames.com/VI. YouTube and Instagram downloads hit login or bot walls; never bypass them with logins, cookies or proxies.
* **Every shot is audited frame by frame** in the exact 9:16 crop. `official/shots/shots.json` holds `clean` windows; the validator and mixer refuse anything outside them. Descriptions alone are not proof: the first catalog missed a gun, a robbery, nudity and a pole dancer.
* Rockstar's "RP, Likely Mature 17+" badge is burned into the Extended Look clips. Those shots carry a `crop_box` that zooms past it; never show the badge.
* Strip all audio from official footage (licensed music). Credit Rockstar on screen and in the caption.
* AI visuals only when no official footage can carry the line, never more than one or two beats, labelled AI VISUAL. The owner dislikes AI b roll.

## 5. Brand (open decision)

* The account covers everything GTA 6, not only numbers (owner rejected "HARD NUMBERS").
* Wanted: modern, Gen Z, global, unique, minimal like "Unseen.", with a logo. Options sent 12 Nov: paused. (recommended), loredrop., afterglow., palm reader., redacted., deep cut., humid., sixsense. **Not picked yet.** Until then the end card says "GTA 6".
* The handle must not contain GTA, Rockstar, VI or Vice City. Bio and captions say "Not affiliated with Rockstar Games or Take Two".

## 6. Captions and posting

* Caption: one line hook, the facts with labels (ROCKSTAR SAYS, REPORTED, OUR MATH), an easy question, "Follow for tomorrow. See you in Leonida.", disclaimer and credits, max 5 hashtags.
* Turn ON the AI label (the narration is an AI clone of the owner's voice).
* Pin a first comment that invites replies. Reply to every comment in the first hour.
* Do not auto share to Facebook. Upload the original file to TikTok and YouTube Shorts with AI disclosure on.
* The owner's mother runs Instagram and YouTube from India (payouts to her). TikTok is the owner's in the US for reach. Never suggest a VPN for TikTok in India.
* Posting from India: 12:00 ET is 22:30 IST; use Instagram's scheduler for US evening slots.

## 7. Production checklist (per reel)

1. Pick the format and the hook (section 2). Verify every fact with sources.
2. Write script.json: say, show, layouts, clips with word anchors, footnotes; voice_preset 1.
3. Validate (`engine/validate.py`): footage clean windows, anchors, no dashes, word count.
4. Voice (`engine/voice_only.sh`), then build and preview stills (`engine/preview.py`) before any full render.
5. Render (`engine/render_par.sh`) and mix (`engine/compose.py`).
6. QA (section 8), then send the MP4, cover and caption together.

## 8. QA before sending anything

1. Frame sheet across the whole reel: no weapons, violence, nudity, suggestive shots, police, crashes, logos or badges.
2. Every frame shows GTA 6 footage; no black, empty or bar frames.
3. 1080x1920, 30 fps, -14 LUFS, true peak under -1 dB, under 90 seconds, over 61 seconds.
4. Text readable over the footage and synced to the voice; nothing under the Instagram UI zones.
5. Facts, labels and numbers match between the video and the caption.

## 9. Feedback log (newest first)

* 12 Nov: "Make a rule book ... so again and again I don't have to tell you these things." This file.
* 12 Nov: "Show more and more GTA 6 graphics in the whole reel continuously. Do not let any frame be void ... different gameplays ... best quality ... make six reels like that." Rules 1.1 to 1.4 and 1.10.
* 12 Nov: Shared a reference reel showing what works for GTA 6 (comparison, reality check, storyline; save, share and 90/10 DM tactics). Section 2.
* 12 Nov: "We need to use more gameplay." Extended Look gameplay added and audited, badge crop added.
* 12 Nov: Voice: after the lineup, "the voice you have given to the reel ... is fine." Preset 1 locked.
* 12 Nov: "I don't recognize my voice ... show me multiple voices, I'll choose." Lineup of 7 sent.
* 12 Nov: Wants channel names that are modern, Gen Z, global, unique, like Unseen, with logos. Sheet sent; pick pending.
* 12 Nov (self found): Reel 1 v1 showed a gun at 0:11. Full frame audit of all footage; owner told not to post v1.
* 12 Nov: "Why don't we have such good content? Study the whole channel." Visual grammar in section 2.
* 12 Nov: "Not only numbers." HARD NUMBERS dropped.
* 12 Nov: "None of the voice matches ... my voice but exactly the way the person was saying." Speech to Speech method.
* 12 Nov: Accent about 70% American, 30% Indian.
* 12 Nov: "Make sure it fits the proper reel ratio." 9:16 full bleed, letterbox removed.
* 12 Nov: Not happy with AI only visuals; use the actual GTA 6 trailers and gameplay.
* 12 Nov: Use many agents (12 to 15, then 20 to 25) for research and production.
* 12 Nov: His mother runs the Instagram from India; payments later.
