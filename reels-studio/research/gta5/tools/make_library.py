"""Build official/gta5/shots_gta5.json (GTA V library, ids 500 and up) from the frame by frame audit (13 Nov 2026).
Usage: python3 make_library.py <scratchpad dir>
Stills are copied untouched into official/gta5/img/; clips point at the official trailers in official/gta5/vid/.
crop_box = [x, y, w, h], the only part of the source that may ever be shown (letterbox, logos or flagged corners removed).
focus = [fx, fy] inside crop_box: where the subject sits, so the engine centres its 9:8 (split) or 9:16 (ab) window on it."""
import json, os, shutil, sys

S = sys.argv[1]
SRC = os.path.join(S, "gta5src"); G = os.path.join(S, "official", "gta5")
os.makedirs(os.path.join(G, "img"), exist_ok=True)
GTAV_PAGE = "https://www.rockstargames.com/gta-v"
NW = {
    "1748koo9o829a9": "https://www.rockstargames.com/newswire/article/1748koo9o829a9/screens-from-grand-theft-auto-v-for-pc",
    "52396": "https://www.rockstargames.com/newswire/article/52396/new-grand-theft-auto-v-pc-screens",
    "4k41288381494k": "https://www.rockstargames.com/newswire/article/4k41288381494k/gtav-pc-new-release-date-first-screens-and-system-specs",
    "172872k8a375k8": "https://www.rockstargames.com/newswire/article/172872k8a375k8/gtav-and-gta-online-coming-march-15-for-playstation-5-and-xbox-series",
    "4ka18ao8a4o227": "https://www.rockstargames.com/newswire/article/4ka18ao8a4o227/grand-theft-auto-v-and-gta-online-out-now-on-playstation-5-and-xbox-se",
    "7551a7k917554a": "https://www.rockstargames.com/newswire/article/7551a7k917554a/free-upgrade-for-grand-theft-auto-v-on-pc-now-available",
    "akk98a4o755825": "https://www.rockstargames.com/newswire/article/akk98a4o755825/free-upgrade-for-grand-theft-auto-v-on-pc-coming-march-4",
    "89k8a55458a1ak": "https://www.rockstargames.com/newswire/article/89k8a55458a1ak/grand-theft-auto-v-release-dates-and-exclusive-content",
}
OLD = "https://media.rockstargames.com/rockstargames/img/global/news/upload/"
TINA = "https://media-rockstargames-com.akamaized.net/tina-uploads/"

# ---------- stills: (id, slug, local source, file url, page url, size, crop_box or None, focus, description, tags, audit note) ----------
STILLS = [
 (500, "skyline_sunset_palm", "dl_page/07edb091bb329145ee3f3f01476adb40acc6457b.jpg", TINA + "tina-modules/3871/07edb091bb329145ee3f3f01476adb40acc6457b.jpg", GTAV_PAGE, (3840, 2160), None, (0.62, 0.40),
  "Downtown Los Santos skyline at sunset behind a tall palm, rail yards, streets and rooftops in front", ["skyline", "city", "sunset", "Los Santos", "streets"], "whole frame clean"),
 (501, "downtown_day_park", "dl_page/24ba6644deb404944cdbe64705285bbad80154a4.jpg", TINA + "tina-modules/gta-v/24ba6644deb404944cdbe64705285bbad80154a4.jpg", GTAV_PAGE, (3840, 2160), None, (0.5, 0.45),
  "Downtown towers on a clear day over a palm lined park with a lake, footbridge, traffic, pedestrians and an ice cream truck", ["skyline", "city", "daytime", "streets", "pedestrians", "park"], "checked at full size: ordinary pedestrians and traffic"),
 (502, "skyline_dusk_golf", "dl_page/fdac18d4377f55a8b9aed1dcb882c4ffa0c60959.jpg", TINA + "tina-modules/6a84/fdac18d4377f55a8b9aed1dcb882c4ffa0c60959.jpg", GTAV_PAGE, (2560, 1401), None, (0.45, 0.40),
  "Los Santos skyline at dusk over a golf course pond and trees (softly stylized, painterly look)", ["skyline", "city", "dusk", "stylized"], "whole frame clean; stylized grade"),
 (503, "downtown_freeway_dusk", "nw_raw/1748koo9o829a9/10_gtavpc_03272015.jpg", OLD + "10_gtavpc_03272015.jpg", NW["1748koo9o829a9"], (3840, 2160), None, (0.58, 0.45),
  "Downtown at dusk over a busy freeway interchange, a civilian helicopter and the torch monument", ["skyline", "city", "dusk", "streets", "traffic", "freeway"], "helicopter checked at full size: civilian, no police markings"),
 (504, "vinewood_sign_day", "nw_raw/172872k8a375k8/7248c8a095c3af9a0b646d2e7ac1661f7e49cbb5.jpg", TINA + "posts/172872k8a375k8/7248c8a095c3af9a0b646d2e7ac1661f7e49cbb5.jpg", NW["172872k8a375k8"], (3840, 2160), None, (0.55, 0.45),
  "From behind the Vinewood sign: the hills and downtown Los Santos on a clear day", ["landmark", "Vinewood sign", "city", "wide", "aerial", "hills"], "whole frame clean"),
 (505, "vinewood_sign_haze", "nw_raw/4k41288381494k/pcvinewood_full.jpg", OLD + "pcvinewood_full.jpg", NW["4k41288381494k"], (3840, 2160), None, (0.5, 0.55),
  "Behind the Vinewood sign in golden afternoon haze, downtown towers and the hills beyond", ["landmark", "Vinewood sign", "city", "golden hour", "wide"], "whole frame clean"),
 (506, "vinewood_sign_sunset", "nw_raw/89k8a55458a1ak/gtav_details09122014_002.jpg", OLD + "gtav_details09122014_002.jpg", NW["89k8a55458a1ak"], (1920, 1080), [0, 0, 1620, 1080], (0.33, 0.55),
  "The Vinewood sign on its hill at sunset with a radio mast, a passing jet and a helicopter, valley lights below", ["landmark", "Vinewood sign", "sunset", "hills", "aerial"], "GTA V logo in the lower right corner removed by crop_box (x 1620 and up)"),
 (507, "freeway_night", "nw_raw/4k41288381494k/pchighway_full.jpg", OLD + "pchighway_full.jpg", NW["4k41288381494k"], (3840, 2160), None, (0.5, 0.5),
  "Night freeway traffic heading to Downtown Los Santos, freeway signs, palms and lit towers", ["streets", "cars", "driving", "night", "traffic", "city"], "cars checked at full size: no police"),
 (508, "golf_skyline", "nw_raw/52396/gtav02272015_4.jpg", OLD + "gtav02272015_4.jpg", NW["52396"], (3840, 2160), None, (0.45, 0.5),
  "A golfer tees off under palms with the downtown skyline and a jet overhead", ["city", "skyline", "leisure", "golf", "daytime"], "whole frame clean"),
 (509, "vinewood_blvd_crowd", "nw_raw/1748koo9o829a9/7_gtavpc_03272015.jpg", OLD + "7_gtavpc_03272015.jpg", NW["1748koo9o829a9"], (3840, 2160), [420, 0, 3000, 2160], (0.45, 0.5),
  "Crowd on the Vinewood Boulevard walk of fame at dusk: tourists, taxis, theatre marquee and neon", ["crowds", "pedestrians", "streets", "city", "nightlife"], "crowd checked at full size; crop_box trims a movie poster at the left edge"),
 (510, "street_race_night", "dl_page/a9877dd12c6baf42e1def32e0218c540cc95a13d.jpg", TINA + "tina-modules/gta-v/a9877dd12c6baf42e1def32e0218c540cc95a13d.jpg", GTAV_PAGE, (3840, 2160), None, (0.58, 0.5),
  "A striped blue sports car with neon underglow leads a street race at dusk (GTA Online)", ["cars", "driving", "racing", "GTA Online"], "car behind checked at full size: no police"),
 (511, "supercar_drift_rain", "nw_raw/4ka18ao8a4o227/abdd0e8b80a131af933993a9dd1a3bac6c25b5e6.jpg", TINA + "posts/4ka18ao8a4o227/abdd0e8b80a131af933993a9dd1a3bac6c25b5e6.jpg", NW["4ka18ao8a4o227"], (3840, 2160), None, (0.55, 0.55),
  "A green supercar with a big rear wing drifts across a wet street at night, spray flying (GTA Online)", ["cars", "driving", "night", "rain", "GTA Online"], "whole frame clean"),
 (512, "quad_coyote_canyon", "nw_raw/7551a7k917554a/eaa402b2d9943ce9f1a3ea37dee8aab074a2a965.jpg", TINA + "posts/7551a7k917554a/eaa402b2d9943ce9f1a3ea37dee8aab074a2a965.jpg", NW["7551a7k917554a"], (3840, 1620), None, (0.5, 0.6),
  "A quad bike rider and a running coyote in a rocky canyon, a hawk and a small plane overhead", ["countryside", "wildlife", "driving", "off road"], "whole frame clean"),
 (513, "quad_jump_skyline", "nw_raw/52396/gtav02272015_5.jpg", OLD + "gtav02272015_5.jpg", NW["52396"], (3840, 2160), None, (0.5, 0.5),
  "A quad bike leaps off a hilltop at sunset with the downtown skyline in the distance", ["driving", "stunt", "sunset", "skyline", "hills"], "whole frame clean (a jump, no crash)"),
 (514, "chiliad_cable_car", "nw_raw/1748koo9o829a9/6_gtavpc_03272015.jpg", OLD + "6_gtavpc_03272015.jpg", NW["1748koo9o829a9"], (3840, 2160), None, (0.38, 0.5),
  "Mount Chiliad cable car station with a gondola over the mountains, Los Santos far away on the horizon", ["countryside", "mountains", "landmark", "wide", "Mount Chiliad"], "whole frame clean"),
 (515, "country_train_plane", "nw_raw/1748koo9o829a9/12_gtavpc_03272015.jpg", OLD + "12_gtavpc_03272015.jpg", NW["1748koo9o829a9"], (3840, 2160), None, (0.6, 0.55),
  "A freight train winds through green hills by the Alamo Sea, a small plane flies close overhead", ["countryside", "train", "wide", "Blaine County"], "whole frame clean"),
 (516, "train_bridge_lake", "nw_raw/52396/gtav02272015_2.jpg", OLD + "gtav02272015_2.jpg", NW["52396"], (3840, 2160), None, (0.35, 0.6),
  "A long freight train crosses a bridge above the Alamo Sea at golden hour, mountains behind", ["countryside", "train", "lake", "golden hour", "Blaine County"], "whole frame clean"),
 (517, "country_highway_biplane", "nw_raw/52396/gtav02272015_10.jpg", OLD + "gtav02272015_10.jpg", NW["52396"], (3840, 2160), None, (0.45, 0.5),
  "Country highway past grain silos and farmland at dusk, a biplane crop duster overhead", ["countryside", "driving", "farm", "dusk", "Blaine County"], "whole frame clean"),
 (518, "tree_rocky_point", "nw_raw/4k41288381494k/pctree_full.jpg", OLD + "pctree_full.jpg", NW["4k41288381494k"], (3840, 2160), None, (0.32, 0.5),
  "A lone tree on a rocky point by the water, a dirt road and pines in the hills at dusk", ["countryside", "nature", "dusk", "lake"], "whole frame clean"),
 (519, "river_waterfall_animals", "nw_raw/52396/gtav02272015_7.jpg", OLD + "gtav02272015_7.jpg", NW["52396"], (3840, 2160), None, (0.5, 0.5),
  "A river and waterfall under a bridge: rabbits in the grass, a deer on the rocks, a mountain lion drinking", ["wildlife", "nature", "countryside", "river", "animals"], "animals calm, nothing violent"),
 (520, "stag_doe_sunset", "nw_raw/akk98a4o755825/4cad70fc6a2a979203c33ff0e9bec5ce0c020817.jpg", TINA + "posts/akk98a4o755825/4cad70fc6a2a979203c33ff0e9bec5ce0c020817.jpg", NW["akk98a4o755825"], (3840, 2160), [560, 0, 3280, 2160], (0.37, 0.5),
  "A stag looks into the camera beside a grazing doe in a pine forest at sunset, a bridge behind", ["wildlife", "deer", "nature", "sunset", "forest"], "a police car chasing a car sits in the far lower left (x under 300): crop_box starts at x 560"),
 (521, "deer_meadow", "nw_raw/89k8a55458a1ak/gtav_details09122014_008.jpg", OLD + "gtav_details09122014_008.jpg", NW["89k8a55458a1ak"], (1920, 1080), [0, 0, 1620, 1080], (0.47, 0.55),
  "A stag and a doe in a grassy meadow below wooded hills", ["wildlife", "deer", "nature", "countryside"], "GTA V logo in the lower right corner removed by crop_box"),
 (522, "lighthouse_topdown", "nw_raw/1748koo9o829a9/2_gtavpc_03272015.jpg", OLD + "2_gtavpc_03272015.jpg", NW["1748koo9o829a9"], (3840, 2160), None, (0.6, 0.5),
  "Straight down on a red and white lighthouse on a rock, waves breaking, a speedboat passing", ["ocean", "coast", "aerial", "boat"], "whole frame clean"),
 (523, "pier_night_from_water", "nw_raw/52396/gtav02272015_15.jpg", OLD + "gtav02272015_15.jpg", NW["52396"], (3840, 2160), None, (0.45, 0.45),
  "Del Perro pier, its Ferris wheel and the downtown skyline at night seen from a boat; a hand holds a phone taking the photo", ["ocean", "beach", "night", "skyline", "pier"], "whole frame clean"),
 (524, "map_art_los_santos", "dl_page/3360902d782314fee48567a8a70bb9996e569698.jpg", TINA + "tina-modules/6a84/3360902d782314fee48567a8a70bb9996e569698.jpg", GTAV_PAGE, (2560, 1321), None, (0.5, 0.5),
  "Rockstar's gold map art of Los Santos: the street grid, freeways and hills (graphic, not a game screenshot)", ["map", "city", "graphic"], "whole frame clean; no labels or logos"),
 (525, "trevor_helicopter_sandy", "dl_page/a457313ec277b6e74bd25238768cbcecda739549.jpg", TINA + "tina-modules/gta-v/a457313ec277b6e74bd25238768cbcecda739549.jpg", GTAV_PAGE, (3840, 2160), None, (0.42, 0.45),
  "Trevor flies a helicopter low over the desert town of Sandy Shores", ["protagonists", "Trevor", "aerial", "countryside", "desert"], "cockpit checked at full size: hands on the controls, no weapon"),
 (526, "michael_phone_night", "nw_raw/1748koo9o829a9/3_gtavpc_03272015.jpg", OLD + "3_gtavpc_03272015.jpg", NW["1748koo9o829a9"], (3840, 2160), None, (0.45, 0.4),
  "Michael on the phone on a terrace at night, downtown towers and the moon behind him", ["protagonists", "Michael", "night", "skyline"], "calm moment, no weapon"),
 (527, "franklin_chop_doorstep", "nw_raw/52396/gtav02272015_14.jpg", OLD + "gtav02272015_14.jpg", NW["52396"], (3840, 2160), None, (0.42, 0.5),
  "Franklin sits on his doorstep on the phone with his dog Chop beside him", ["protagonists", "Franklin", "dog", "night", "calm"], "calm moment, phone in hand, no weapon"),
 (528, "michael_classic_car", "nw_raw/89k8a55458a1ak/gtav_details09122014_015.jpg", OLD + "gtav_details09122014_015.jpg", NW["89k8a55458a1ak"], (1920, 1080), [0, 0, 1620, 1080], (0.4, 0.55),
  "Michael leans on a red classic sports car in a sunny driveway while a cat walks past (his head is cropped by the top edge)", ["protagonists", "Michael", "cars", "calm"], "GTA V logo in the lower right corner removed by crop_box"),
]

# ---------- clips: (id, slug, video id, start, end, focus x, description, tags, segments [(from, to, content, flags)], GTA Online) ----------
VID = {"r3too449": ("Coming March 2022 for PS5 and Xbox Series X|S (Sept 2021)", "2160p", [0, 216, 3840, 1728]),
       "1s626s55": ("Out Now on PlayStation 5 and Xbox Series X|S (March 2022)", "2160p", [0, 0, 3840, 2160]),
       "tr45r42o": ("PlayStation 4, Xbox One and PC Announcement Trailer (June 2014)", "1080p", [0, 108, 1920, 864]),
       "kc1a9kco": ("A Picket Fence and a Dog Named Skip (Sept 2014)", "1080p", [0, 108, 1920, 864]),
       "s6rrr5ao": ("60 Frames Per Second PC Trailer (April 2015)", "1080p60", [0, 110, 1920, 860])}
C = lambda a, b, txt, fl=("none",): (a, b, txt, list(fl))
CLIPS = [
 (530, "sunset_power_lines", "r3too449", 2.32, 4.05, 0.5, "Golden hour over South Los Santos: power lines with sneakers hanging, palms and a street below", ["city", "streets", "sunset"], None, False),
 (531, "skyline_from_hills", "1s626s55", 2.82, 4.78, 0.65, "Downtown Los Santos rising out of the morning haze, seen from the hills at sunrise", ["skyline", "city", "wide", "sunrise"], None, False),
 (532, "skyscrapers_from_below", "1s626s55", 4.88, 6.88, 0.45, "Looking straight up at glass skyscrapers in the sun", ["city", "skyline", "architecture"], None, False),
 (533, "city_hall_tower", "1s626s55", 40.65, 41.62, 0.55, "The city hall tower and downtown high rises against the sun, palms at the edge", ["city", "skyline", "landmark"], None, False),
 (534, "river_bridge_skyline", "1s626s55", 46.25, 48.02, 0.6, "An arched bridge over the Los Santos river channel with downtown behind", ["city", "skyline", "streets", "bridge"], None, False),
 (535, "smokestacks_sunset", "1s626s55", 29.45, 30.95, 0.6, "City lights at sunset with two smokestacks and a suspension bridge in the haze", ["city", "skyline", "sunset", "industry"], None, False),
 (536, "maze_tower_topdown", "1s626s55", 31.05, 31.98, 0.45, "Straight down on the Maze Bank tower helipad and the city far below", ["aerial", "city", "skyline", "landmark"], None, False),
 (537, "richman_hotel", "1s626s55", 35.28, 36.25, 0.45, "The Richman Hotel sign and grounds with a distant tower", ["city", "streets", "landmark", "hotel"], None, False),
 (538, "penthouse_skyline_view", "r3too449", 55.85, 66.82, 0.55, "A player in an orange jacket looks out of a penthouse window at the downtown skyline at sunset (GTA Online)", ["skyline", "city", "sunset", "interior", "GTA Online"],
  [C(0, 5.1, "party in a penthouse with arcade cabinets whose art shows guns", ["weapon"]), C(5.1, 8.6, "player at the curved window looking at the skyline at sunset, a few guests"),
   C(8.6, 10.97, "jets fly in and explosions burst over the city", ["violence", "crash_or_fire"])], True),
 (539, "neighborhood_skyline", "tr45r42o", 43.33, 44.56, 0.55, "Low rise neighborhood with power lines, downtown towers in the haze", ["city", "streets", "skyline", "neighborhood"], None, False),
 (540, "vinewood_hills_sunset", "tr45r42o", 50.77, 52.07, 0.5, "Hillside villas, palms and a tennis court at sunset", ["city", "hills", "sunset", "houses"], None, False),
 (541, "freeway_interchange", "1s626s55", 11.15, 13.12, 0.5, "Traffic on a curving freeway interchange in the morning haze", ["streets", "traffic", "driving", "freeway", "city"], None, False),
 (542, "freeway_signs", "s6rrr5ao", 25.28, 26.61, 0.5, "Driving under green freeway signs (Del Perro Fwy, W. Elipse Blvd) with palms and traffic", ["streets", "driving", "freeway", "signs"], None, False),
 (543, "lowriders_downtown", "1s626s55", 26.52, 27.72, 0.5, "Three lowriders roll toward the camera on a downtown street (GTA Online)", ["cars", "streets", "city", "GTA Online"], None, True),
 (544, "coastal_highway_drive", "r3too449", 37.35, 39.12, 0.55, "A red sports car cruises a coastal highway with traffic at sunset", ["cars", "driving", "coast", "sunset"], None, False),
 (545, "franklin_convertible_sunset", "r3too449", 39.22, 40.98, 0.6, "Franklin drives a convertible along the coast at sunset", ["protagonists", "Franklin", "driving", "sunset"], None, False),
 (546, "boardwalk_crowd_mime", "kc1a9kco", 9.66, 11.29, 0.55, "Busy Vespucci Beach boardwalk: tourists, beachgoers, a mime and Michael walking past", ["crowds", "pedestrians", "beach", "Michael"], None, False),
 (547, "mime_closeup", "kc1a9kco", 11.39, 12.6, 0.5, "A mime performs on the boardwalk, passers by behind", ["pedestrians", "beach", "fun"], None, False),
 (548, "sandy_shores_street", "kc1a9kco", 14.7, 16.47, 0.55, "Sandy Shores main road: a biplane flies over, cyclists, a dog and a local waving", ["countryside", "pedestrians", "small town", "desert"], None, False),
 (549, "plane_over_countryside", "r3too449", 32.28, 33.58, 0.5, "A small plane flies over Blaine County toward mountains and white clouds", ["aerial", "countryside", "wide", "plane"],
  [C(0, 0.35, "end of the character switch transition (desaturated aerial)", ["transition"]), C(0.35, 1.3, "plane over the countryside, mountains and clouds")], False),
 (550, "chiliad_sunset", "tr45r42o", 14.03, 17.3, 0.7, "Mount Chiliad and misty ridges at sunset", ["countryside", "mountains", "sunset", "Mount Chiliad"], None, False),
 (551, "train_forest", "tr45r42o", 17.4, 19.3, 0.3, "A freight train comes round a bend through a pine forest", ["countryside", "train", "forest"], None, False),
 (552, "lumber_mill", "tr45r42o", 19.4, 21.24, 0.45, "A lumber mill with a smoking chimney and a train in forested hills", ["countryside", "industry", "forest"], None, False),
 (553, "quarry", "tr45r42o", 21.34, 24.14, 0.5, "A miner by a giant dump truck, then workers overlooking a terraced quarry with the city far away", ["countryside", "work", "quarry"], None, False),
 (554, "paleto_bay_aerial", "s6rrr5ao", 38.14, 39.44, 0.5, "Aerial over the coastal town of Paleto Bay at sunset, pines in front", ["aerial", "countryside", "coast", "sunset", "small town"], None, False),
 (555, "beach_topdown_island", "1s626s55", 48.12, 49.08, 0.5, "Straight down on a beach party with tents, palms and turquoise water (Cayo Perico, GTA Online)", ["beach", "ocean", "aerial", "GTA Online"], None, True),
 (556, "vespucci_beach_pier", "s6rrr5ao", 27.96, 29.48, 0.45, "Vespucci Beach from above: palms, beachgoers and the Del Perro pier in the haze", ["beach", "ocean", "pier", "wide"], None, False),
 (557, "quad_beach_sunset", "s6rrr5ao", 26.71, 27.86, 0.55, "A quad bike rides across the beach into the sunset, people strolling", ["beach", "driving", "sunset"], None, False),
 (558, "underwater_swimmer", "1s626s55", 13.22, 15.18, 0.5, "Looking up from underwater as a swimmer dives into the sunset sea", ["ocean", "underwater"], None, False),
 (559, "stag_hillside_sunset", "r3too449", 13.38, 14.22, 0.4, "A stag on a flowering hillside looks out over the mountains at sunset", ["wildlife", "deer", "nature", "sunset"], None, False),
 (560, "deer_forest", "tr45r42o", 8.53, 11.16, 0.45, "Deer graze in a forest clearing below tall pines and a mountain", ["wildlife", "deer", "nature", "forest"], None, False),
 (561, "hammerhead_sharks", "tr45r42o", 11.26, 13.93, 0.5, "Hammerhead sharks circle underwater, the sun above the surface", ["wildlife", "ocean", "underwater", "sharks"], None, False),
 (562, "orca", "kc1a9kco", 29.38, 30.58, 0.3, "An orca glides past underwater (dark blue water)", ["wildlife", "ocean", "underwater", "orca"], None, False),
 (563, "dog", "kc1a9kco", 44.86, 45.6, 0.35, "A golden retriever beside a man's legs on a dirt path", ["animals", "dog", "pets"], None, False),
 (564, "trio_kitchen", "r3too449", 46.92, 48.35, 0.5, "Michael, Franklin and Trevor talk in a kitchen, Trevor gesturing", ["protagonists", "Michael", "Franklin", "Trevor", "calm"], None, False),
 (565, "michael_tennis_court", "r3too449", 26.32, 28.92, 0.45, "Michael walks across his tennis court as a woman in white passes", ["protagonists", "Michael", "calm", "home"],
  [C(0, 2.3, "Michael at his tennis court, sunny, a woman in a white jacket passes"), C(2.3, 2.6, "darkens into the character switch", ["transition"])], False),
 (566, "michael_yoga", "tr45r42o", 52.17, 53.44, 0.5, "Michael does a yoga pose on his patio", ["protagonists", "Michael", "calm", "home", "yoga"], None, False),
 (567, "yoga_by_the_pool", "tr45r42o", 53.54, 55.17, 0.65, "Yoga by the pool: Amanda and the instructor hold a pose while Michael wobbles", ["protagonists", "Michael", "calm", "home", "humor"], None, False),
 (568, "trio_car_lester", "s6rrr5ao", 41.72, 43.04, 0.5, "Lester, Trevor and Michael sit in a red car at a gas station", ["protagonists", "Michael", "Trevor", "Lester", "calm"], None, False),
]


def clean_from(segs):
    out = []
    for a, b, txt, fl in segs:
        if fl == ["none"] and b - a >= 0.3:
            lo, hi = round(a + 0.1, 2), round(b - 0.1, 2)
            if out and lo - out[-1][1] <= 0.25: out[-1][1] = hi
            else: out.append([lo, hi])
    return out


lib = []
for (i, slug, src, url, page, size, box, focus, desc, tags, note) in STILLS:
    ext = os.path.splitext(src)[1]
    dst = os.path.join(G, "img", f"{i}_{slug}{ext}")
    shutil.copyfile(os.path.join(SRC, src), dst)
    region = box or [0, 0, size[0], size[1]]
    lib.append({"id": i, "kind": "still", "game": "GTA V", "name": slug, "src": dst, "start": 0.0, "end": 10.0, "dur": 10.0,
                "w": size[0], "h": size[1], "crop_box": region, "focus": list(focus), "res": [region[2], region[3]],
                "sharp_full": region[3] >= 1500, "desc": desc, "tags": tags, "gta_online": "GTA Online" in tags,
                "source_url": url, "page_url": page,
                "segments": [{"from": 0.0, "to": 10.0, "content": desc + " (still image, held with a slow push in)", "flags": ["none"], "clean": True, "good_for": tags, "audit": note}],
                "clean": [[0.0, 10.0]], "safe": [0.0, 10.0], "banned": False})
for (i, slug, vid, st, en, fx, desc, tags, segs, online) in CLIPS:
    title, res, box = VID[vid]
    L = round(en - st, 2)
    segs = segs or [C(0, L, desc)]
    clean = clean_from(segs)
    lib.append({"id": i, "kind": "clip", "game": "GTA V", "name": slug, "src": os.path.join(G, "vid", f"{vid}.mp4"), "start": st, "end": en, "dur": L,
                "w": 3840 if res == "2160p" else 1920, "h": 2160 if res == "2160p" else 1080, "crop_box": box, "focus": [fx, 0.5], "res": [box[2], box[3]],
                "sharp_full": box[3] >= 1500, "desc": desc, "tags": tags, "gta_online": online,
                "source_url": f"https://videos-rockstargames-com.akamaized.net/v4/{vid}/flv/en-us-{res}.mp4", "page_url": f"https://www.rockstargames.com/videos/{vid}",
                "source_title": title,
                "segments": [{"from": a, "to": b, "content": txt, "flags": fl, "clean": fl == ["none"], "good_for": tags if fl == ["none"] else []} for a, b, txt, fl in segs],
                "clean": clean, "safe": max(clean, key=lambda w: w[1] - w[0]) if clean else None, "banned": not clean})
# per clip crop overrides found in the audit (allowed area narrowed inside the letterbox free picture)
for s in lib:
    if s["id"] == 539:  # liquor store and beer signs fill the left edge (x under 290): keep only x 320 and up
        s["crop_box"] = [320, 108, 1600, 864]; s["res"] = [1600, 864]; s["focus"] = [0.6, 0.5]
        s["desc"] = "Low rise neighborhood with power lines, downtown towers in the haze (left edge with store signs cropped out)"
        s["segments"][0]["content"] = s["desc"]; s["segments"][0]["audit"] = "liquor and beer signs at x under 290 removed by crop_box"
ids = [s["id"] for s in lib]
assert len(ids) == len(set(ids)) and min(ids) >= 500, "ids must be unique and 500 or more"
json.dump(lib, open(os.path.join(G, "shots_gta5.json"), "w"), indent=1)
print(len(lib), "shots:", sum(s["kind"] == "still" for s in lib), "stills,", sum(s["kind"] == "clip" for s in lib), "clips; ids", min(ids), "to", max(ids))
