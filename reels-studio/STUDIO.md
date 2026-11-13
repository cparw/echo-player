# Reels Studio: standing notes (read this first)

Owner: Chaitanya. Project: GTA 6 explainer reels account (Instagram first, then TikTok and YouTube Shorts). Started 12 Nov 2026.

## Owner preferences (durable, from the owner's own instructions)
1. Narration must be the owner's OWN voice: his ElevenLabs Instant Voice Clone named "Instagram" (voice_id bqoGL6z7prHxVFnnNfsb) in the ElevenLabs account connected to the cloud environment, delivered through the Speech to Speech method below. Accent target: about 70% American, 30% Indian. Never ship a placeholder voice as final.
2. Delivery and pattern: like the reference account @unseenbyneuralway (calm, cinematic, second person, short sentences, about 175 to 190 words per minute, first word within 0.2 s, midpoint rehook, sourced numbers). Copy the pattern, never their lines, names, sign off or topics.
3. Visuals: use REAL official GTA VI footage by default (Rockstar trailers), credited on screen. AI b roll only for things the footage cannot show. The owner was unhappy when the first cut used only AI b roll.
4. Output: 1080x1920, 9:16, full bleed, no bars, no stretching. 61 to 90 seconds (TikTok Creator Rewards needs over 1 minute).
5. Speed: the owner wants many parallel agents (20 to 25 is fine) for research and scripting, and finished media fast.
6. Every fact verified with a source; label CONFIRMED, REPORTED, ESTIMATE, OUR MATH. Never invent numbers.
7. No dash characters (hyphen, en dash, em dash) in any prose shown to the owner, captions or on screen text.

## Account ownership (stated by the owner, 12 Nov 2026)
* The Instagram account is owned and run by the owner's mother, an Indian citizen living in India; payouts go to her. The owner makes the reels (his cloned voice).
* Platform split (owner wants Instagram, TikTok and YouTube): Instagram and YouTube are the mother's accounts (India, payouts to her). TikTok is banned in India (since June 2020; still blocked as of mid 2026), so TikTok is held by the owner in the US as a reach channel with monetization OFF (TikTok pays only the account holder). Never suggest a VPN to run TikTok from India. Facebook Creator Fast Track is US, CA, UK and AU only.
* Instagram in India: Gifts about 500 followers, Creator Marketplace about 1,000, Subscriptions about 10,000 (third party sources; confirm in app). YouTube Partner Program works in India (1,000 subscribers plus 10M Shorts views in 90 days).
* Posting from India: 12:00 ET is 22:30 IST (post live); 18:00 ET is 04:30 IST (use Instagram's Schedule). Deliver each reel with caption and cover ready to schedule.
* Recommended: a fresh dedicated account (handle to match the chosen brand) switched to Creator, not her existing personal account.

## Accounts and limits (as of 12 Nov 2026)
* ElevenLabs: Starter plan, 40,000 characters a month. API reached through the environment proxy (no key needed in code; send header `xi-api-key: dummy`). Speech to text costs about 3 credits per second, so avoid it. `mp3_44100_192` needs the Creator tier; use `mp3_44100_128`. Eleven v4 supports `/with-timestamps`. Voice Remix endpoint exists (`/v1/text-to-voice/{voice_id}/remix`) for nudging accent.
* Higgsfield (MCP): Plus plan, about 2,000 credits. Kling 4.0 text to video 9:16 5 s 1080p is about 16 credits; ElevenLabs Music v2.5 instrumental 75 s is about 11 credits. Higgsfield can also publish to TikTok (tiktok_connect, tiktok_prepare_publish).
* Network: environment set to unrestricted on 12 Nov 2026 at the owner's request.

## Where official GTA VI footage comes from
* WORKS: Rockstar's official TikTok `https://www.tiktok.com/@rockstargames` with yt-dlp. Files are 1080x1920 HEVC. Trailer posts (Launch Trailer, Trailer 2) are stored ROTATED 90 degrees; restore with ffmpeg `transpose=2`, then crop 608x1080 and scale to 1080x1920. Pre Load and Extended Look cuts are native vertical.
* WORKS: official 4K screenshots on `https://www.rockstargames.com/VI` (paths under `/VI/_next/static/media/`).
* BLOCKED: YouTube downloads from the cloud IP hit "Sign in to confirm you're not a bot". Do not bypass with cookies or proxies.
* LIMITED: Instagram anonymous access rate limits after about 15 requests. Do not use logins to bypass.
* Rockstar's own player (`videos.rockstargames.com`, `graph.rockstargames.com`) marks GTA VI trailers `youtubeOnly`, so no direct files there.
* Audio from official videos is licensed music: always strip it.

## Brand and format (working)
* Scope (owner, 12 Nov 2026): the account covers EVERYTHING GTA 6 (news, trailers, people, places, music, launch guides, gameplay after launch), not only numbers. The owner rejected HARD NUMBERS for that reason. Wanted: a minimal, modern, premium name and mark in the spirit of Unseen (never copying it).
* Round 6 (13 Nov): gallery of 15 logos in `brand/round6/`, built with `engine/brand_v6.html` + `engine/brand_v6_data.js` (flat marks are SVG in the html; premium ones are Higgsfield GPT Image 2.6 renders in `brand/round6/ai/`). Render: `node brand_shot.js brand_v6.html out.png "mode=gallery" 1080 2560 2` (also `mode=top`, `mode=mock&n=1`, `mode=lockup&n=1`, `mode=flat&k=m`). Fonts come from `node_modules/@fontsource`, so run it from a folder that has them (`npm i` in `engine/`). Recommended: **missed.** (handle missed.gg, Name field "missed. | GTA 6").
* Name: NOT CHOSEN YET. Recommended 12 Nov (round 5, after the owner said minimap lacks curiosity): **plain sight.** (backups one frame., look again.). Assets in `brand/plainsight/` (cinematic profile picture, flat master, lockup, board, Instagram mock); marks drawn in `engine/brand_v4.html` (`node engine/brand_shot.js brand_v4.html <out.png> "mode=pfp&mark=plainsight" 1080 1080`), cinematic version made on Higgsfield GPT Image 2.6 from the flat mark. Wordmark: Unbounded 500, letter spacing 0.03em, orange gradient period. Setup: Instagram username plainsight.gg (no period at the end allowed; @plainsight.gg free on YouTube, plainsight.tv unregistered), Name field "plain sight. | GTA 6" (search reads it; change limit 2 per 14 days). Round 4 (minimap.) assets stay in `brand/minimap/`. Until the owner picks, end cards say brand "GTA 6". Handle must not contain GTA, Rockstar, VI or Vice City. Add "Not affiliated with Rockstar Games or Take Two" to the bio and captions.
* Look: near black, off white, orange #FF7A1A highlighter boxes, Anton headlines, Inter Tight body, Instrument Serif italic for quotes, JetBrains Mono labels, tiny source footnotes, credit tags (FOOTAGE: ROCKSTAR GAMES, AI VISUAL). Data cards sit on official footage in our plum duotone (bg "duo"), never on plain black.
* Caption labels: ROCKSTAR SAYS, REPORTED, ANALYST ESTIMATE, OUR MATH. Max 5 hashtags. End with an easy riffable question and a follow line. Final spoken line: "Follow for tomorrow. See you in Leonida." End card: brand, series ("6 days out", "Launch day", "Day 2"...), episode title, cta "Follow for tomorrow".

## Voice (the owner's clone with a directed delivery)
* The owner's ElevenLabs Instant Voice Clone is named "Instagram", voice_id `bqoGL6z7prHxVFnnNfsb`. Plain TTS with the clone did not match Unseen's delivery ("None of the voice matches", owner, 12 Nov). What works: `engine/tts_sts.py`.
* Method: a licensed ElevenLabs guide voice performs the script with word timestamps, then Speech to Speech (`eleven_multilingual_sts_v2`, stability 0.45, similarity 0.95) turns it into the owner's voice. STS keeps the guide's timing, so the timestamps stay valid for on screen sync.
* Guide settings that matched Unseen best (prosody fingerprint, `engine/prosody.py`): Brian `nPczCjzI2devNBz1zQrb`, model eleven_multilingual_v2, guide_speed 1.08, guide_stability 0.30, guide_style 0.25; then the pace fix toward 184 wpm (factor clamped 0.92 to 1.10). Unseen reference: 184 wpm, 22 pauses a minute, pitch spread 9.3 semitones. Reel 1 landed at 181 wpm. Owner approved the direction ("this is going in a better direction") and asked for it even closer.
* Never clone or imitate a third party's voice (including Unseen's narrator). Only the owner's own clone.
* Cost: about 1,150 ElevenLabs credits per 70 s reel (guide about 440, STS about 710). Starter plan: 40,000 a month, resets on the 11th.

## Engine v3 visual kit (built 12 Nov 2026 after studying Unseen)
* Unseen looks richer because it is footage first, cuts on the spoken line every 1.5 to 2 s, puts footage behind every graphic, and uses maps, clocks, grids, icons, quote cards and per card sources.
* Our answers: `bg: "duo"` (footage graded to our plum duotone behind data cards); clip anchors `{"shot": N, "at": k}` cut on spoken word k; layouts `countdown` (live ticking clock, `remaining` seconds), `waffle` (`filled`, `fill_at`, `caption`), `map` (dot matrix world map, `cities` with lon, lat, time, `at`, optional westward `sweep` for the midnight rollout), `quote` (serif italic, big quote mark, `attrib`); `icon` on words beats (Lucide set in `engine/icons.js`). Examples: `examples/components_demo_script.json`, `examples/reel01_v3_script.json`.
* Do not auto share reels to Facebook (keeps Creator Fast Track eligibility). TikTok account must be personal, not business, for Creator Rewards.
* Compliance: the account and payouts belong to the owner's mother in India. If the owner is on a US student visa, he should still confirm with his DSO, since the rules look at who does the work.

## Footage safety (12 Nov 2026, important)
* The first shot catalog was WRONG in places: a reviewer found a man holding a submachine gun in shot 5 at 4.0 to 5.6 s (Reel 1 v1 used it at 11 s), and fights, a robbery, pasties, a pole dancer, a gun store and police chases inside shots the catalog called safe (5, 8, 9, 10, 11, 15, 22, 52, 54, 56, 57). The cut detector also merged several real shots into one "shot".
* Rule: never trust a description alone. Check frames with `engine/shot_frames.py` (tiles every 0.4 s in the exact 9:16 crop) or `engine/preview.py` (graphics composited over the real frames) before any render. Use only audited clean windows; no weapons, violence, sexual or suggestive content, police action, logos or rating badges (except shot 72 at 4.6 s, by choice).

## Open decisions (asked 12 Nov 2026)
* Voice: owner said "I don't recognize my voice", wants about 10% more of his own voice and asked to choose from options. Lineup sent (same Reel 1 opening, paced alike): 1 Brian guide STS (current), 2 Brian guide STS with timbre locked (stability 0.8, similarity 1.0), 3 clone direct (multilingual v2), 4 clone direct (eleven_v4), 5 Indian American guide (Teja) STS, 6 Indian guide (Viraj) STS, 7 option 2 pitched down 2 semitones to his real pitch (rubberband, formants kept; his real F0 is about 97 Hz, STS output was about 108 Hz). Tool: `engine/voice_lineup.py`. His clone was made from ONE 30 second sample; 2 to 3 more minutes of clean recordings would raise likeness for every option.
* Name: see Brand above and RULEBOOK section 5 for the rejected list. Fourth round (12 Nov, broad names with research): minimap. recommended, tooltip. and cutscene. as backups. Vetting found: every .com taken; @minimap on YouTube belongs to a small Korean gamer app (medium conflict); sidequest, blip, fasttravel, roam have big brand conflicts; freeroam is a GTA Online mode name. No formal USPTO search yet (their API refused automated queries); run one before merch. Fifth round vetting (12 Nov): plain sight. low conflicts (Plainsight, a B2B vision AI company; the Steam games Plain Sight and Hidden in Plain Sight), look again. and one frame. clean; blindspot. high (183K Blindspot Shorts channel, Ground News trademark filing).

## Engine (this folder)
Setup once per session: `cd reels-studio/engine && npm install` (fonts) and `pip install -U yt-dlp`. Playwright and Chromium are preinstalled in the cloud image.
1. Write `reelNN/script.json` (format: see `examples/reel01_script_v2.json`; markup `*word*` box, `^word^` orange, `@k` sync to spoken word k; layouts words, number, bars, list, endcard; footage via `clips: [{shot, offset, cx}]` from `shots.json`).
2. Validate: `python3 engine/validate.py reelNN/script.json reelNN/caption.txt`.
3. Render with the owner's voice: `bash engine/make_reel.sh reelNN final assets/music_a.mp3` (validate, guide TTS then Speech to Speech into the owner's clone, pace fix to about 184 wpm, timeline, graphics in headless Chromium, ffmpeg mix to -14 LUFS, 12 Mbps cap). To change only visuals, reuse the approved narration.mp3 and words.json and run build, render and compose (no new voice credits).
4. Shot library: `python3 engine/shots.py <out_dir> <clips...>` detects cuts and makes numbered contact sheets.
5. Cover: `node engine/cover.js cover.json cover.png`.

## Engine v4 (12 Nov 2026, after the owner asked for continuous full colour GTA 6 footage)
* `bg: "scrim"` is the default for every beat: vivid footage (saturation 1.10, contrast 1.05) with a soft local shadow behind the text block plus light top and bottom bands. `duo` and `black` are no longer used (validator errors on black or footage free beats).
* End card sits over blurred footage: give the endcard beat `clips` (one calm clean shot).
* `layout: "versus"` for comparisons: `topic`, `left` and `right` = {label, value, sub, at}; the right side is the hero in orange.
* Extended Look gameplay clips carry `crop_box: [170, 140, 910, 1618]` in shots.json to zoom past Rockstar's rating badge.
* Voice: `voice_preset: 1` (approved). `engine/voice_only.sh reelDir` makes narration.mp3 and words.json in reelDir/voice.
* Fast checks before rendering: `engine/preview.py <built dir> sheet.jpg` (graphics over the real frames) and `engine/shot_frames.py` (audit tiles).
* Render: `engine/render_par.sh timeline.json graphics.mov 3` (parallel chunks), then `engine/compose.py dir music.mp3 out.mp4`.
* Instagram plays reels at 1080x1920, so that is our output; quality comes from the sharpest sources (native vertical gameplay, 4K stills) and, where needed, Topaz upscaling of trailer clips via Higgsfield.

## Skills worth using (installed here or from github.com/ComposioHQ/awesome-claude-skills)
* Research: deep-research, recursive-research, article-extractor, youtube-transcript, reddit-fetch, Content Research Writer.
* Growth: Twitter Algorithm Optimizer, Competitive Ads Extractor, Domain Name Brainstormer (handles), Raffle Winner Picker (giveaways), CSV Data Summarizer (Insights exports).
* Media: Video Downloader (yt-dlp), Image Enhancer, Canvas Design, imagen, Pixelbin, theme-factory; Higgsfield workflows (thumbnail-generation, video-montage, reel-effects, faceless-video, /shorts).
* Automation: Connect (Composio, 1000+ apps), n8n-skills, postiz (social scheduling, installed), Playwright Browser Automation, OpenWeb, Full-Page Screenshot.
* Packaging: Skill Creator, Skill Seekers (turn this engine into a reusable skill).
* Monid CLI (owner suggested): paid data endpoints; needs the owner's Monid API key. Use only for data the owner's own tools cannot get, and never to get around a platform's login wall or bot check.

## Research
`research/all_streams.json` and the launch plan in `PLAYBOOK.md`: 12 research streams from 12 Nov 2026 (facts with sources and confidence, algorithm, monetization, legal, production, hooks, creators). Recheck time sensitive facts before each post.
