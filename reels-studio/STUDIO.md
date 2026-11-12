# Reels Studio: standing notes (read this first)

Owner: Chaitanya. Project: GTA 6 explainer reels account (Instagram first, then TikTok and YouTube Shorts). Started 12 Nov 2026.

## Owner preferences (durable, from the owner's own instructions)
1. Narration must be the owner's OWN voice: an ElevenLabs Instant Voice Clone named "Chaitanya" in the ElevenLabs account connected to the cloud environment. Accent target: about 70% American, 30% Indian. Never ship a placeholder voice as final.
2. Delivery and pattern: like the reference account @unseenbyneuralway (calm, cinematic, second person, short sentences, about 175 to 190 words per minute, first word within 0.2 s, midpoint rehook, sourced numbers). Copy the pattern, never their lines, names, sign off or topics.
3. Visuals: use REAL official GTA VI footage by default (Rockstar trailers), credited on screen. AI b roll only for things the footage cannot show. The owner was unhappy when the first cut used only AI b roll.
4. Output: 1080x1920, 9:16, full bleed, no bars, no stretching. 61 to 90 seconds (TikTok Creator Rewards needs over 1 minute).
5. Speed: the owner wants many parallel agents (20 to 25 is fine) for research and scripting, and finished media fast.
6. Every fact verified with a source; label CONFIRMED, REPORTED, ESTIMATE, OUR MATH. Never invent numbers.
7. No dash characters (hyphen, en dash, em dash) in any prose shown to the owner, captions or on screen text.

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
* Name: HARD NUMBERS (working title). Handle must not contain GTA, Rockstar, VI or Vice City. Add "Not affiliated with Rockstar Games or Take Two" to the bio and captions.
* Look: near black, off white, orange #FF7A1A highlighter boxes, Anton headlines, JetBrains Mono labels, tiny source footnotes, credit tags (FOOTAGE: ROCKSTAR GAMES, AI VISUAL).
* Caption labels: ROCKSTAR SAYS, REPORTED, ANALYST ESTIMATE, OUR MATH. Max 5 hashtags. End with an easy riffable question and a follow line. Sign off: "That's the number. Follow, and I'll see you tomorrow."
* Do not auto share reels to Facebook (keeps Creator Fast Track eligibility). TikTok account must be personal, not business, for Creator Rewards.
* Compliance: if the owner is on F-1 status, no payouts, affiliate or paid deals until a DSO confirms work authorization.

## Engine (this folder)
Setup once per session: `cd reels-studio/engine && npm install` (fonts) and `pip install -U yt-dlp`. Playwright and Chromium are preinstalled in the cloud image.
1. Write `reelNN/script.json` (format: see `examples/reel01_script_v2.json`; markup `*word*` box, `^word^` orange, `@k` sync to spoken word k; layouts words, number, bars, list, endcard; footage via `clips: [{shot, offset, cx}]` from `shots.json`).
2. Validate: `python3 engine/validate.py reelNN/script.json reelNN/caption.txt`.
3. Render with the owner's voice: `bash engine/make_reel.sh reelNN <voice_id> final assets/music_a.mp3` (TTS with timestamps, pace fix to about 178 wpm, timeline, graphics in headless Chromium, ffmpeg mix to -14 LUFS, 12 Mbps cap).
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
