# Official GTA V library (Rockstar Games), audited frame by frame

Built 13 Nov 2026 for the owner's rule: "if you want to show GTA 5 comparison with GTA 6, then you should show the GTA 5 pictures also for that properly."
Every GTA 5 vs GTA 6 beat shows these official GTA V visuals beside the GTA VI shot with the engine's `compare` key (split screen or A/B cut; see `engine/COMPARE.md`).
Ids start at 500 so they never clash with the GTA VI library (`official/shots/shots.json`). Data: `official/gta5/shots_gta5.json`; contact sheet: `catalog_gta5.jpg`.

## Sources (official Rockstar only, public pages, no logins, cookies or proxies)

* The Grand Theft Auto V page, https://www.rockstargames.com/gta-v (4K screenshots and the map art in its page modules).
* Rockstar Newswire posts with official screenshots: Screens from GTA V for PC (27 Mar 2015), New GTA V PC Screens (27 Feb 2015), GTAV PC: New Release Date, First Screens and System Specs (Jan 2015), GTAV and GTA Online Coming March 15 for PS5 and Xbox Series X|S (2022), GTA V and GTA Online Out Now on PS5 and Xbox Series X|S (2022), Free Upgrade for GTA V on PC Now Available / Coming March 4 (2025), GTA V Release Dates and Exclusive Content Details for PS4, Xbox One and PC (Sept 2014). Each shot lists its exact page and file URL.
* Rockstar's own video pages (https://www.rockstargames.com/videos/ID), files Rockstar marks downloadable: Coming March 2022 for PS5 and Xbox Series X|S (r3too449, 2160p), Out Now on PS5 and Xbox Series X|S (1s626s55, 2160p), PS4, Xbox One and PC Announcement Trailer (tr45r42o, 1080p), A Picket Fence and a Dog Named Skip (kc1a9kco, 1080p), 60 Frames Per Second PC Trailer (s6rrr5ao, 1080p60). The videos stay in `official/gta5/vid/` (not committed; audio is never used).
* Not used: the age gated GTA V trailers on Rockstar's site (Trailer 1, Gameplay Video, the Michael, Franklin and Trevor trailers, the PS5 announcement, First Person), YouTube (bot wall), fan uploads and mods.

## How it was audited

* Stills: every candidate viewed at 1500 px, then busy areas (crowds, hands, cars, cockpits, signs, corners) zoomed at full 4K. A still is held for any length with a slow push in (`clean` 0 to 10 s).
* Clips: cut detection, then tiles every 0.4 s of the FULL letterbox free frame, so any crop the engine takes (9:8 split half or 9:16 full frame) is covered. Clean windows trim 0.1 s at both ends, like the GTA VI library.
* `crop_box` [x, y, w, h] is the only part of a source that may ever be shown: it removes letterboxes, the GTA V logo on the 2014 screenshots, and flagged corners (a police chase far left in 520, store signs in 539, a movie poster in 509).
* `focus` [fx, fy] is where the subject sits; the engine centres its crop window there unless a script gives `cx` / `cy`.
* `sharp_full`: false means a 1080p letterboxed source (864 px tall); fine in a split half, soft as a full screen A/B shot. Prefer 4K stills or 4K clips for `ab`.

## Clean visuals by type

### City skyline and landmarks (21)

| id | kind | what is on screen | clean window (s) | shown area | source |
|---|---|---|---|---|---|
| 500 | still | Downtown Los Santos skyline at sunset behind a tall palm, rail yards, streets and rooftops in front | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/gta-v) |
| 501 | still | Downtown towers on a clear day over a palm lined park with a lake, footbridge, traffic, pedestrians and an ice cream truck | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/gta-v) |
| 502 | still | Los Santos skyline at dusk over a golf course pond and trees (softly stylized, painterly look) | any length (still) | 2560x1401, soft full screen | [page](https://www.rockstargames.com/gta-v) |
| 503 | still | Downtown at dusk over a busy freeway interchange, a civilian helicopter and the torch monument | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/1748koo9o829a9/screens-from-grand-theft-auto-v-for-pc) |
| 504 | still | From behind the Vinewood sign: the hills and downtown Los Santos on a clear day | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/172872k8a375k8/gtav-and-gta-online-coming-march-15-for-playstation-5-and-xbox-series) |
| 505 | still | Behind the Vinewood sign in golden afternoon haze, downtown towers and the hills beyond | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/4k41288381494k/gtav-pc-new-release-date-first-screens-and-system-specs) |
| 506 | still | The Vinewood sign on its hill at sunset with a radio mast, a passing jet and a helicopter, valley lights below | any length (still) | 1620x1080, soft full screen | [page](https://www.rockstargames.com/newswire/article/89k8a55458a1ak/grand-theft-auto-v-release-dates-and-exclusive-content) |
| 508 | still | A golfer tees off under palms with the downtown skyline and a jet overhead | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/52396/new-grand-theft-auto-v-pc-screens) |
| 513 | still | A quad bike leaps off a hilltop at sunset with the downtown skyline in the distance | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/52396/new-grand-theft-auto-v-pc-screens) |
| 514 | still | Mount Chiliad cable car station with a gondola over the mountains, Los Santos far away on the horizon | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/1748koo9o829a9/screens-from-grand-theft-auto-v-for-pc) |
| 523 | still | Del Perro pier, its Ferris wheel and the downtown skyline at night seen from a boat; a hand holds a phone taking the photo | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/52396/new-grand-theft-auto-v-pc-screens) |
| 531 | clip | Downtown Los Santos rising out of the morning haze, seen from the hills at sunrise | 0.10 to 1.86 | 3840x2160 | [video](https://www.rockstargames.com/videos/1s626s55) |
| 532 | clip | Looking straight up at glass skyscrapers in the sun | 0.10 to 1.90 | 3840x2160 | [video](https://www.rockstargames.com/videos/1s626s55) |
| 533 | clip | The city hall tower and downtown high rises against the sun, palms at the edge | 0.10 to 0.87 | 3840x2160 | [video](https://www.rockstargames.com/videos/1s626s55) |
| 534 | clip | An arched bridge over the Los Santos river channel with downtown behind | 0.10 to 1.67 | 3840x2160 | [video](https://www.rockstargames.com/videos/1s626s55) |
| 535 | clip | City lights at sunset with two smokestacks and a suspension bridge in the haze | 0.10 to 1.40 | 3840x2160 | [video](https://www.rockstargames.com/videos/1s626s55) |
| 536 | clip | Straight down on the Maze Bank tower helipad and the city far below | 0.10 to 0.83 | 3840x2160 | [video](https://www.rockstargames.com/videos/1s626s55) |
| 537 | clip | The Richman Hotel sign and grounds with a distant tower | 0.10 to 0.87 | 3840x2160 | [video](https://www.rockstargames.com/videos/1s626s55) |
| 538 | clip | A player in an orange jacket looks out of a penthouse window at the downtown skyline at sunset (GTA Online) | 5.20 to 8.50 | 3840x1728 | [video](https://www.rockstargames.com/videos/r3too449) |
| 539 | clip | Low rise neighborhood with power lines, downtown towers in the haze (left edge with store signs cropped out) | 0.10 to 1.13 | 1600x864, soft full screen | [video](https://www.rockstargames.com/videos/tr45r42o) |
| 540 | clip | Hillside villas, palms and a tennis court at sunset | 0.10 to 1.20 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/tr45r42o) |

### Crowds and pedestrians (4)

| id | kind | what is on screen | clean window (s) | shown area | source |
|---|---|---|---|---|---|
| 509 | still | Crowd on the Vinewood Boulevard walk of fame at dusk: tourists, taxis, theatre marquee and neon | any length (still) | 3000x2160 | [page](https://www.rockstargames.com/newswire/article/1748koo9o829a9/screens-from-grand-theft-auto-v-for-pc) |
| 546 | clip | Busy Vespucci Beach boardwalk: tourists, beachgoers, a mime and Michael walking past | 0.10 to 1.53 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/kc1a9kco) |
| 547 | clip | A mime performs on the boardwalk, passers by behind | 0.10 to 1.11 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/kc1a9kco) |
| 548 | clip | Sandy Shores main road: a biplane flies over, cyclists, a dog and a local waving | 0.10 to 1.67 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/kc1a9kco) |

### Streets, cars and driving (8)

| id | kind | what is on screen | clean window (s) | shown area | source |
|---|---|---|---|---|---|
| 507 | still | Night freeway traffic heading to Downtown Los Santos, freeway signs, palms and lit towers | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/4k41288381494k/gtav-pc-new-release-date-first-screens-and-system-specs) |
| 510 | still | A striped blue sports car with neon underglow leads a street race at dusk (GTA Online) | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/gta-v) |
| 511 | still | A green supercar with a big rear wing drifts across a wet street at night, spray flying (GTA Online) | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/4ka18ao8a4o227/grand-theft-auto-v-and-gta-online-out-now-on-playstation-5-and-xbox-se) |
| 530 | clip | Golden hour over South Los Santos: power lines with sneakers hanging, palms and a street below | 0.10 to 1.63 | 3840x1728 | [video](https://www.rockstargames.com/videos/r3too449) |
| 541 | clip | Traffic on a curving freeway interchange in the morning haze | 0.10 to 1.87 | 3840x2160 | [video](https://www.rockstargames.com/videos/1s626s55) |
| 542 | clip | Driving under green freeway signs (Del Perro Fwy, W. Elipse Blvd) with palms and traffic | 0.10 to 1.23 | 1920x860, soft full screen | [video](https://www.rockstargames.com/videos/s6rrr5ao) |
| 543 | clip | Three lowriders roll toward the camera on a downtown street (GTA Online) | 0.10 to 1.10 | 3840x2160 | [video](https://www.rockstargames.com/videos/1s626s55) |
| 544 | clip | A red sports car cruises a coastal highway with traffic at sunset | 0.10 to 1.67 | 3840x1728 | [video](https://www.rockstargames.com/videos/r3too449) |

### Countryside and wide aerials (11)

| id | kind | what is on screen | clean window (s) | shown area | source |
|---|---|---|---|---|---|
| 515 | still | A freight train winds through green hills by the Alamo Sea, a small plane flies close overhead | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/1748koo9o829a9/screens-from-grand-theft-auto-v-for-pc) |
| 516 | still | A long freight train crosses a bridge above the Alamo Sea at golden hour, mountains behind | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/52396/new-grand-theft-auto-v-pc-screens) |
| 517 | still | Country highway past grain silos and farmland at dusk, a biplane crop duster overhead | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/52396/new-grand-theft-auto-v-pc-screens) |
| 518 | still | A lone tree on a rocky point by the water, a dirt road and pines in the hills at dusk | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/4k41288381494k/gtav-pc-new-release-date-first-screens-and-system-specs) |
| 524 | still | Rockstar's gold map art of Los Santos: the street grid, freeways and hills (graphic, not a game screenshot) | any length (still) | 2560x1321, soft full screen | [page](https://www.rockstargames.com/gta-v) |
| 549 | clip | A small plane flies over Blaine County toward mountains and white clouds | 0.45 to 1.20 | 3840x1728 | [video](https://www.rockstargames.com/videos/r3too449) |
| 550 | clip | Mount Chiliad and misty ridges at sunset | 0.10 to 3.17 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/tr45r42o) |
| 551 | clip | A freight train comes round a bend through a pine forest | 0.10 to 1.80 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/tr45r42o) |
| 552 | clip | A lumber mill with a smoking chimney and a train in forested hills | 0.10 to 1.74 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/tr45r42o) |
| 553 | clip | A miner by a giant dump truck, then workers overlooking a terraced quarry with the city far away | 0.10 to 2.70 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/tr45r42o) |
| 554 | clip | Aerial over the coastal town of Paleto Bay at sunset, pines in front | 0.10 to 1.20 | 1920x860, soft full screen | [video](https://www.rockstargames.com/videos/s6rrr5ao) |

### Beach and ocean (5)

| id | kind | what is on screen | clean window (s) | shown area | source |
|---|---|---|---|---|---|
| 522 | still | Straight down on a red and white lighthouse on a rock, waves breaking, a speedboat passing | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/1748koo9o829a9/screens-from-grand-theft-auto-v-for-pc) |
| 555 | clip | Straight down on a beach party with tents, palms and turquoise water (Cayo Perico, GTA Online) | 0.10 to 0.86 | 3840x2160 | [video](https://www.rockstargames.com/videos/1s626s55) |
| 556 | clip | Vespucci Beach from above: palms, beachgoers and the Del Perro pier in the haze | 0.10 to 1.42 | 1920x860, soft full screen | [video](https://www.rockstargames.com/videos/s6rrr5ao) |
| 557 | clip | A quad bike rides across the beach into the sunset, people strolling | 0.10 to 1.05 | 1920x860, soft full screen | [video](https://www.rockstargames.com/videos/s6rrr5ao) |
| 558 | clip | Looking up from underwater as a swimmer dives into the sunset sea | 0.10 to 1.86 | 3840x2160 | [video](https://www.rockstargames.com/videos/1s626s55) |

### Wildlife and animals (9)

| id | kind | what is on screen | clean window (s) | shown area | source |
|---|---|---|---|---|---|
| 512 | still | A quad bike rider and a running coyote in a rocky canyon, a hawk and a small plane overhead | any length (still) | 3840x1620 | [page](https://www.rockstargames.com/newswire/article/7551a7k917554a/free-upgrade-for-grand-theft-auto-v-on-pc-now-available) |
| 519 | still | A river and waterfall under a bridge: rabbits in the grass, a deer on the rocks, a mountain lion drinking | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/52396/new-grand-theft-auto-v-pc-screens) |
| 520 | still | A stag looks into the camera beside a grazing doe in a pine forest at sunset, a bridge behind | any length (still) | 3280x2160 | [page](https://www.rockstargames.com/newswire/article/akk98a4o755825/free-upgrade-for-grand-theft-auto-v-on-pc-coming-march-4) |
| 521 | still | A stag and a doe in a grassy meadow below wooded hills | any length (still) | 1620x1080, soft full screen | [page](https://www.rockstargames.com/newswire/article/89k8a55458a1ak/grand-theft-auto-v-release-dates-and-exclusive-content) |
| 559 | clip | A stag on a flowering hillside looks out over the mountains at sunset | 0.10 to 0.74 | 3840x1728 | [video](https://www.rockstargames.com/videos/r3too449) |
| 560 | clip | Deer graze in a forest clearing below tall pines and a mountain | 0.10 to 2.53 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/tr45r42o) |
| 561 | clip | Hammerhead sharks circle underwater, the sun above the surface | 0.10 to 2.57 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/tr45r42o) |
| 562 | clip | An orca glides past underwater (dark blue water) | 0.10 to 1.10 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/kc1a9kco) |
| 563 | clip | A golden retriever beside a man's legs on a dirt path | 0.10 to 0.64 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/kc1a9kco) |

### Protagonists in calm moments (10)

| id | kind | what is on screen | clean window (s) | shown area | source |
|---|---|---|---|---|---|
| 525 | still | Trevor flies a helicopter low over the desert town of Sandy Shores | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/gta-v) |
| 526 | still | Michael on the phone on a terrace at night, downtown towers and the moon behind him | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/1748koo9o829a9/screens-from-grand-theft-auto-v-for-pc) |
| 527 | still | Franklin sits on his doorstep on the phone with his dog Chop beside him | any length (still) | 3840x2160 | [page](https://www.rockstargames.com/newswire/article/52396/new-grand-theft-auto-v-pc-screens) |
| 528 | still | Michael leans on a red classic sports car in a sunny driveway while a cat walks past (his head is cropped by the top edge) | any length (still) | 1620x1080, soft full screen | [page](https://www.rockstargames.com/newswire/article/89k8a55458a1ak/grand-theft-auto-v-release-dates-and-exclusive-content) |
| 545 | clip | Franklin drives a convertible along the coast at sunset | 0.10 to 1.66 | 3840x1728 | [video](https://www.rockstargames.com/videos/r3too449) |
| 564 | clip | Michael, Franklin and Trevor talk in a kitchen, Trevor gesturing | 0.10 to 1.33 | 3840x1728 | [video](https://www.rockstargames.com/videos/r3too449) |
| 565 | clip | Michael walks across his tennis court as a woman in white passes | 0.10 to 2.20 | 3840x1728 | [video](https://www.rockstargames.com/videos/r3too449) |
| 566 | clip | Michael does a yoga pose on his patio | 0.10 to 1.17 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/tr45r42o) |
| 567 | clip | Yoga by the pool: Amanda and the instructor hold a pose while Michael wobbles | 0.10 to 1.53 | 1920x864, soft full screen | [video](https://www.rockstargames.com/videos/tr45r42o) |
| 568 | clip | Lester, Trevor and Michael sit in a red car at a gas station | 0.10 to 1.22 | 1920x860, soft full screen | [video](https://www.rockstargames.com/videos/s6rrr5ao) |

## Flagged inside kept clips (never shown: the engine and validator keep clips inside the clean windows)

* 538: 0.0 to 5.1 weapon: party in a penthouse with arcade cabinets whose art shows guns; 8.6 to 11.0 violence/crash_or_fire: jets fly in and explosions burst over the city
* 549: 0.0 to 0.3 transition: end of the character switch transition (desaturated aerial)
* 565: 2.3 to 2.6 transition: darkens into the character switch

## Rejected candidates (not in the library)

* GTA V key art (cover collage) and the GTA Online key arts: weapons, police, suggestive panels.
* Wanted level or police: every official shot of it shows police action (chases, flashing cruisers), so none were kept.
* Stills: Trevor in the desert among cacti (holds a pistol, seen only at full size); a Vinewood Boulevard street at sunset (billboard with a nude figure, exhaust flame); Trevor on a crop duster (bullet holes, smoke, logo); all stills with guns, police cars, explosions, menus, spec tables or logos (about 40).
* Trailer shots: logo and rating cards, on screen text, a person jumping from an exploding train, a plane trailing smoke, an airport explosion, police lights, arcade cabinets with gun art (538 keeps only its clean window), a nightclub queue in skimpy outfits, a beach boardwalk in underwear, a jet ski branded with a crude joke name, a protester's xenophobic sign, a mountain lion attack, a strip club, a liquor store sign shot, shirtless posing on the beach, gang scenes and heist shootouts.

