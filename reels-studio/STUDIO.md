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
* Name: NOT CHOSEN YET. Shortlist shown to the owner: SUBTEXT (recommended), FOOTNOTE, PARALLAX, VANTAGE; emblem options 1 to 6 (recommended 3 or 2). Until the owner picks, end cards say brand "GTA 6". Handle must not contain GTA, Rockstar, VI or Vice City. Add "Not affiliated with Rockstar Games or Take Two" to the bio and captions.
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

## Engine (this folder)
Setup once per session: `cd reels-studio/engine && npm install` (fonts) and `pip install -U yt-dlp`. Playwright and Chromium are preinstalled in the cloud image.
1. Write `reelNN/script.json` (format: see `examples/reel01_script_v2.json`; markup `*word*` box, `^word^` orange, `@k` sync to spoken word k; layouts words, number, bars, list, endcard; footage via `clips: [{shot, offset, cx}]` from `shots.json`).
2. Validate: `python3 engine/validate.py reelNN/script.json reelNN/caption.txt`.
3. Render with the owner's voice: `bash engine/make_reel.sh reelNN final assets/music_a.mp3` (validate, guide TTS then Speech to Speech into the owner's clone, pace fix to about 184 wpm, timeline, graphics in headless Chromium, ffmpeg mix to -14 LUFS, 12 Mbps cap). To change only visuals, reuse the approved narration.mp3 and words.json and run build, render and compose (no new voice credits).
4. Shot library: `python3 engine/shots.py <out_dir> <clips...>` detects cuts and makes numbered contact sheets.
5. Cover: `node engine/cover.js cover.json cover.png`.

## Skills worth using (installed here or from github.com/ComposioHQ/awesome-claude-skills)
* Research: deep-research, recursive-research, article-extractor, youtube-transcript, reddit-fetch, Content Research Writer.
* Growth: Twitter Algorithm Optimizer, Competitive Ads Extractor, Domain Name Brainstormer (handles), Raffle Winner Picker (giveaways), CSV Data Summarizer (Insights exports).
* Media: Video Downloader (yt-dlp), Image Enhancer, Canvas Design, imagen, Pixelbin, theme-factory; Higgsfield workflows (thumbnail-generation, video-montage, reel-effects, faceless-video, /shorts).
* Automation: Connect (Composio, 1000+ apps), n8n-skills, postiz (social scheduling, installed), Playwright Browser Automation, OpenWeb, Full-Page Screenshot.
* Packaging: Skill Creator, Skill Seekers (turn this engine into a reusable skill).
* Monid CLI (owner suggested): paid data endpoints; needs the owner's Monid API key. Use only for data the owner's own tools cannot get, and never to get around a platform's login wall or bot check.

## Research
`research/all_streams.json` and the launch plan in `PLAYBOOK.md`: 12 research streams from 12 Nov 2026 (facts with sources and confidence, algorithm, monetization, legal, production, hooks, creators). Recheck time sensitive facts before each post.
