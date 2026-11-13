FIRST, before anything else: read the full chat this work came from, every word: the private Artifact "GTA6 Handoff 2026-11-13" (https://claude.ai/artifact/UyDvR2e9yS5vapcTc8ksbm), files chat/part01.md to part04.md, then `reels-studio/RULEBOOK.md` and `reels-studio/STUDIO.md`. They hold every decision, rule and piece of owner feedback. Then do the steps below without asking the owner any question.

You run LOCALLY on the owner's Mac, in the Claude desktop app. Do this whole job yourself, end to end, fast, and verify each step on screen. Use the Claude in Chrome tools: the owner's Instagram is already logged in in his Chrome (current username smangal.mangal, 0 posts). If the Chrome tools are not available, say so in one line and stop.

## Hard rules
* Never type, read or change a password, email, phone number or two factor setting. Never accept a login, security or "confirm it's you" prompt; if one appears, stop and tell the owner what it shows.
* Never touch the AI label setting (the owner handles it himself).
* Never delete anything. Act at a normal human pace. No dash characters in anything you type into Instagram.

## Step 0: files on the owner's external SSD
1. `ls /Volumes`; use the volume whose name contains "G-DRIVE" (case insensitive; largest if several). Create `/Volumes/<it>/noticed_studio/posting_kit/` and work there. If none exists, use `~/noticed_studio/posting_kit/` and say so.
2. Download the reels:
   * `curl -fL -o R1_gta5_vs_gta6.mp4 https://d2ol7oe51mr4n9.cloudfront.net/user_2xHq8jjC87NVNOB6tw86bFKkWSL/5b5bde9c-5aa5-45c6-81af-117861e78f87.mp4` (about 66 MB)
   * `curl -fL -o R2_reality_check.mp4 https://d2ol7oe51mr4n9.cloudfront.net/user_2xHq8jjC87NVNOB6tw86bFKkWSL/b3800bde-86c1-4f39-930e-2891f97a4cdb.mp4` (about 71 MB)
3. Get the rest from GitHub repo `cparw/echo-player`, branch `claude/practical-gauss-781z79` (if the current folder is not a clone of it, clone it to `~/echo-player` first): `git fetch origin claude/practical-gauss-781z79`, then for each of `profile_picture.jpg`, `R1_cover.jpg`, `R2_cover.jpg`, `R1_caption.txt`, `R2_caption.txt` run `git show origin/claude/practical-gauss-781z79:reels-studio/posting_kit/<name> > <name>`. Also save `reels-studio/reels/POSTING_PLAN.md` (DM reply texts).

## Attaching files in Instagram
Use a Claude in Chrome file upload tool if you have one. Otherwise, when the macOS file dialog is open, press Cmd+Shift+G, type the full path, press Enter, then Enter again (use `osascript` System Events keystrokes if the browser tools cannot reach the dialog). Only if every method fails, ask the owner to pick that one file, naming the exact path.

## Step 1: profile (instagram.com/accounts/edit/, or Accounts Center, Profiles)
1. Name: `noticed. | GTA 6`
2. Username: `noticed.gg`; if taken try `noticed.tv`, `noticedhq`, `itsnoticed`, `noticed.daily`. Report which worked.
3. Bio, exactly two lines:
   `The GTA 6 details nobody noticed. Every big game next.`
   `Not affiliated with Rockstar Games or Take Two.`
4. Profile photo: `profile_picture.jpg` (chrome letter n with an orange notification dot).
5. Save, reload the profile, confirm all four.

## Step 2: Creator account
Settings, Account type and tools, Switch to professional account, Creator, category "Gaming Video Creator" (else "Video Creator", else "Digital creator"), show the category on the profile, skip contact options, keep the account public. If the web does not offer the switch, try Accounts Center; if only the phone app can do it, report that.

## Step 3: post Reel 1 now
1. Create (+), Post or Reel, attach `R1_gta5_vs_gta6.mp4`; crop Original or 9:16, nothing cut.
2. Cover: upload `R1_cover.jpg` if offered, else keep the first frame.
3. Caption: the full text of `R1_caption.txt`, exactly, every line break and emoji (its 5 hashtags stay).
4. Advanced settings: Share to Facebook OFF if shown, comments ON, highest quality upload ON if offered. Do not touch the AI label.
5. Share. Open the reel, check it plays and the caption is right.
6. Comment and pin: `Which change are you most excited about? Comment SIX for the one I couldn't fit 👇`

## Step 4: Reel 2, two hours after Reel 1
Wait with a background timer, then repeat Step 3 with `R2_reality_check.mp4`, `R2_cover.jpg`, `R2_caption.txt` and the pinned comment `Standard or Ultimate? Comment CHECK for my launch checklist 👇`. While waiting, DM anyone who comments SIX or CHECK with the matching text from `POSTING_PLAN.md` (start with "Auto reply"; never ask anyone to follow first).

## Do not
Post any other reel (Reel 4 is outdated) or change anything else on the account.

## Finish
Write `posting_log.md` in the noticed_studio folder (what was done, the username that worked, reel links, anything that failed) and reply with the same summary.
