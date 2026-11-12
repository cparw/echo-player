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
  * The hook is a surprising, checkable GTA 6 fact or contrast that makes people curious ("Vice City is twice the size of Los Santos", "after inflation GTA 6 costs less than GTA 5 did", "Florida's highest point is 345 feet, so why does GTA 6 have a mountain?", "real Florida warns about falling iguanas"). Lead with the features that got the biggest reaction. No vague openers.
  * The whole hook sentence is on screen from frame one (`"instant": true` on the first beat), big Anton text, key word highlighted as it is spoken. The first shot matches the line and is the most stunning one in the reel.
  * Write 3 hook options, pick the strongest deliberately; the cover repeats the hook.
* **Save prompt early** when the reel is useful ("Save this before launch").
* **Share prompt before the best part** ("Send this to the friend who still plays GTA 5").
* **Midpoint rehook** so the second half holds.
* **90/10 rule:** give 90% of the value in the reel; offer the rest with "Comment WORD and I'll DM you ...". Rules from Meta's own policies (researched 12 Nov 2026):
  * NEVER make a follow, like, share or tag the price of the DM (a "follow gate"). Meta's Spam standard bans it and a strike kills a new account's reach. The DM gives everything promised, then a soft "Follow for tomorrow" line.
  * The keyword is a word, never "6" (SIX, CHECK). The DM says it is an auto reply. Tell people it may land in message requests.
  * Arm the automation before posting (one private reply per comment, within 7 days). Only DM people who commented the word. Keep public auto replies off or varied.
  * Tools: start with manual replies or a free official option (Meta Business Suite "Comment to message", or SuperProfile free, which uses Meta's API). ManyChat Free now covers only 25 contacts a month; use Essential (250) or Pro (2,500) once volume grows.
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
* To change only the hook, record just the new opening and stitch it on (`engine/splice_hook.py`, about 80 credits), then level its loudness to the following narration. Re-record the whole reel only when middle lines change.

## 4. Footage and safety

* Sources that work: Rockstar's official TikTok (all GTA VI posts are downloaded), official 4K screenshots on rockstargames.com/VI. YouTube and Instagram downloads hit login or bot walls; never bypass them with logins, cookies or proxies.
* **Every shot is audited frame by frame** in the exact 9:16 crop. `official/shots/shots.json` holds `clean` windows; the validator and mixer refuse anything outside them. Descriptions alone are not proof: the first catalog missed a gun, a robbery, nudity and a pole dancer.
* Rockstar's "RP, Likely Mature 17+" badge is burned into the Extended Look clips. Those shots carry a `crop_box` that zooms past it; never show the badge.
* Strip all audio from official footage (licensed music). Credit Rockstar on screen and in the caption.
* AI visuals only when no official footage can carry the line, never more than one or two beats, labelled AI VISUAL. The owner dislikes AI b roll.

## 5. Brand (open decision)

* The account is mostly GTA 6 now, but the NAME must stay open for other games and topics later (owner, 12 Nov). No GTA only words in the name. GTA 6 goes in the display Name field and bio for search, not in the brand.
* Wanted: modern, Gen Z, global, unique, minimal like "Unseen.", professional, futuristic, with ONE logo that reads as a tiny circle (no long text). Back names with real research (conflicts, handles, domains, platform rules).
* Rejected by the owner, never resend: HARD NUMBERS, SUBTEXT, FOOTNOTE, PARALLAX, VANTAGE, paused., loredrop., afterglow., palm reader., redacted., deep cut., humid., sixsense., and the GTA only set six star., hotwire., heat., getaway., riptide., off map., untold., mission passed., and the descriptive set minimap. (liked, but no curiosity), tooltip., cutscene.
* Fifth round sent 12 Nov (curiosity, clear message, futuristic): **plain sight.** recommended ("hidden in plain sight" = it was right there and you missed it; logo: a cinematic eclipse that is also an eye, one flash of light = the detail you missed; `brand/plainsight/`). Backups one frame. and look again. Dropped after vetting: blindspot. (a 183K "Blindspot" Shorts channel and a Ground News trademark filing), enhance. (a game studio), decrypted. (crypto news owns search), unlisted. (near copy of unseen). **Not picked yet.** Until then the end card says "GTA 6".
* Logo rule (research, 12 Nov): the mark must work flat at avatar size first (Instagram shows about 110 px); glass or glow is optional styling on top. One bold glyph inside the central 70% of the circle, no words.
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

* 12 Nov: "minimap is a nice name and everything you gave is wonderful. But it still does not give the futuristic modern vibe like unseen. The message should be clear with the name ... Unseen adds curiosity, something that I missed. That type of curiosity minimap doesn't add." The name itself must be the hook: curiosity ("what did I miss?"), a clear message (this channel shows what you missed) and a futuristic feel, all at once. Descriptive game words (minimap, tooltip, cutscene) are out. The visual quality of round 4 (glass logo, board, Instagram mock) was liked: keep that format.
* 12 Nov: "It doesn't need to only be related to GTA 6 ... we want to keep it open for multiple things ... but mostly we'll have GTA 6. Suggest the name and the best logos with proper research ... do that fast." The name must be broad (gaming wide), GTA 6 lives in the Name field and bio. six star. and the rest of the GTA only set are out. Names now come with research (conflicts, handles, domains, platform rules) and one logo each, delivered fast.
* 12 Nov: "Not do more research. I want something modern, minimalistic, professional, new, Gen Z, futuristic logo ... it just has to be one logo ... you can't write so much because it's an Instagram logo." Deliver ONE logo, not option sheets; a simple mark that reads as a tiny circle, no long text. Sent: six star. (a bold star with a 6 cut out, sunset gradient on black; `engine/logo_sixstar.html`, `brand/six_star_profile_picture.png`).
* 12 Nov: "I already told you I didn't like them. I need something new, different, nice." The second name set (paused., loredrop., afterglow. ...) is rejected too. Third set sent: six star., hotwire., heat., getaway., riptide., off map., untold., mission passed. Never resend rejected names.
* 12 Nov: "Make them more interesting. See the features which hit the most ... out of the box information that they would love ... make it more curious." Reels lead with the GTA 6 features that got the biggest reaction online, told through surprising, curiosity driven facts.
* 12 Nov: "We should be very thoughtful how we start the reels, because that is where we catch the attention of the audience, and that has to be done to its perfect level." Every hook gets 3 written options, the strongest is picked deliberately, with the most stunning shot and big on screen text from frame 1.

* 12 Nov (research, not owner): the reference reel's "they DM you, then ask you to follow" step is a follow gate under Meta's Spam standard. We keep the 90/10 DM but never gate it on a follow.

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
