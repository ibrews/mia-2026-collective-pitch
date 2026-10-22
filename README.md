# MIA XR Collective Pitch: Two Talks, One Slide Pool

Alex Coulombe's pitch (a 10-minute slot; Talk A is budgeted at about 19:40 and Talk B at about 16:35, including the 88-second showreel, to be trimmed with the guide below) for the **MIA XR Collective Pitch** (MIA | Mercato Internazionale Audiovisivo, Rome, 22 October 2026), for an audience of film and TV producers, distributors and IP holders. Two complete versions of the talk are drawn from one shared slide pool, and both close on the same partnership ask.

| | Talk | Thesis | Open it |
|---|---|---|---|
| **A** | *Old Stories, New Doors* | Beloved stories need new audiences and new revenue beyond the stage and screen; *A Christmas Carol VR* is the working model | [ibrews.github.io/mia-2026-collective-pitch](https://ibrews.github.io/mia-2026-collective-pitch/) |
| **B** | *Engine Mastery × Craft* | The studios winning in immersive pair engine mastery with craft | […/?talk=b](https://ibrews.github.io/mia-2026-collective-pitch/?talk=b) |

The full script (running orders, trim priorities with clock times, every slide's beats and speaker notes, and the open `[FILL]` list) is in **[TALKS.md](TALKS.md)**.

## Quickstart

```bash
git clone https://github.com/ibrews/mia-2026-collective-pitch
cd mia-2026-collective-pitch
python -m http.server 8748
```

Then open `http://localhost:8748/` for Talk A or `http://localhost:8748/?talk=b` for Talk B. Opening `index.html` directly also works.

## If you only have N minutes

Every slide carries a trim priority (`CORE`, `TRIM-1` cut first, `TRIM-2`, `TRIM-3`), shown in its presenter-notes header. `build_pitch.py` turns those into cut lists (also in [TALKS.md](TALKS.md) and each talk's cover-slide notes); each line adds to the one above:

**Talk A:**

- Full talk: 19:38.
- 12 min (12:00): cut `carol-how` (45s), `carol-belle` (15s), `replay-line` (35s), `camera-toy` (40s), `normal-film` (15s), `heavenue` (35s), `lincoln` (10s), `fs-flash` (10s), `joby` (10s), `act-a2` (10s), `intro-lens` (15s), `showreel` (88s), `carol-inside` (10s), `carol-quote` (15s), `phase-tour` (45s), `portalcam-reel` (60s).
- 10 min (9:35): cut `rsc-compare` (30s), `ask-first` (30s), `carol-origin` (40s), `working-cut` (45s).
- 8 min (8:15): cut `rsc` (40s), `ask-copro` (40s).

**Talk B:**

- Full talk: 16:33.
- 12 min (11:50): cut `pico` (10s), `fs-build` (15s), `fs-dbox` (10s), `joby` (10s), `carol-belle` (15s), `camera-toy` (40s), `intro-lens` (15s), `showreel` (88s), `teach` (35s), `carol-quote` (15s), `rsc-compare` (30s).
- 10 min (9:40): cut `portalcam-reel` (60s), `ask-first` (30s), `rsc` (40s).
- 8 min (8:15): cut `working-cut` (45s), `ask-copro` (40s).

## Offline pack

The deck needs no internet once it is on the laptop: fonts (`assets/fonts`), three.js (`assets/vendor/three`), the closing QR code (`assets/qr`) and every image and clip (`media/`) are local, and stepping through either talk makes zero external requests (checked in the browser's network log, 2026-10-21).

1. Before travel: `git clone https://github.com/ibrews/mia-2026-collective-pitch` (or download the repo ZIP from GitHub and unzip it).
2. On stage: double-click `index.html` (Talk A), or serve the folder with `python -m http.server 8748` and open `?talk=b` for Talk B. A local server is the safer choice for the clips.
3. If the browser fails entirely, open the PDF backups in `pdf/`: `MIA-2026-Collective-Pitch-Talk-A.pdf` and `...-Talk-B.pdf`, one page per slide, with each clip shown as its poster frame.

## How it is built

- **`talk/pitch.json` is the single source of truth.** It holds the shared `pool` (each slide appears once, tagged `talks: A | B | A+B`, `pace: FLASH | DWELL`, and `sec`) and the two `talks`, each an optional `intro` list (slides between the cover and Act I) plus an ordered list of acts that reference pool ids. A slide cut for time keeps its tags and gets a `parked` reason instead of being deleted, so it can be restored by adding its id back; `TALKS.md` lists every parked slide.
- **`python tools/build_pitch.py`** validates the pool, splices it into `index.html` between the `PITCH-JSON` sentinels, regenerates `TALKS.md`, and prints each talk's running time against the 10-minute slot (plus how long its notes take to read aloud). It fails, writing nothing, on an unknown id, a tag mismatch (a slide used by a talk it isn't tagged for), an orphan slide, a FLASH slide over 15 seconds, a DWELL slide under 30 seconds, missing notes, or a missing media file. It warns when a slide's notes take longer to say at 150 wpm than the slide is budgeted.
- Pacing and talk tags lead every slide's presenter notes, for example `[DWELL · 50s · A+B]`, so they show in the **N** popup and the `?notes` phone view.
- Fork-local additions to Spatial Deck: `?talk=b`, `bigScale` on `layout: 'big'` slides, a guard for case slides without a subtitle, and a wider statement column. The framework's Bonus and Map end-markers are hidden because each talk ends on its own ask.
- **Quote rain** (`layout: 'rain'`, ported from Alex's HarvardXR and FMX decks): ten verbatim, attributed comments about *A Christmas Carol VR* fall in and settle into a readable collage. With `prefers-reduced-motion`, and in `?shot`/`?print` exports, the same quotes show as a static grid. The build refuses a quote without its name, source and year.
- **Standard intro** (`layout: 'intro-alex'` and `'intro-lens'`, ported from spatial-deck-pmre2026 `talk/intro.js`, itself the FMX 2026 / HarvardXR intro): the 8-bit Alex walks in and puts on a headset; click 1 shows the bio; click 2 chains five power-ups in Alex's order (architecture, theater, film, computer, VR: the first, second and fourth are the HarvardXR Venn slide's pixel icons, film is the deck's pixel clapperboard, VR is the slide's pixel headset enlarged), then the Unreal Engine badge block and Unreal-logo fireballs; click 3 tallies the stats. `intro.icons` in `talk/pitch.json` sets the order. The Agile Lens monocle slide is a single beat (clients orbiting); `lens.steps: 5` restores the 2026 → 2016 countdown and the shrink-and-dash beats.
- **Motion diagrams** (`layout: 'pipeline'` and `'ip-web'`): one SVG each, drawn by a pure `render(t)` function, so the build (about 7 seconds, replayed on every entry), the ambient loop and the static frame used by `?print`, `?shot` and reduced motion are the same code. `pipeline` takes three `phases` of up to three items (`al: true` fills the dot: Agile Lens has built it); `ip-web` takes a `center`, up to five `branches` (`t`, `d`, `proof`, `al`) and an `only` list.
- **Round-2 interactive layouts** (all click-to-advance with →, replay on entry, still frames for `?print` and reduced motion): `phase-tour` (tabs for pre-production, production and post, each with a still or clip), `camera-toy` (a concept demo: drag a camera on a plan, pick 24/35/50/85 mm, add a 2.39 mask, take three shots; three.js with a 2D fallback when WebGL is missing), `replay-line` (one performance, four lives, with a draggable playhead), `compare` (a before/after slider) and `reel` (stills in a letterboxed flat frame). `ip-web` branches can carry an `img` or `doorText`, which makes → open each door in turn; `layout: 'big'` takes `bgImg`. Every nested media path is checked by the build.
- **Showreel** (`layout: 'showreel'`, after the intro in both talks): the 88 s Agile Lens reel, full-bleed with sound, re-encoded to 1920x1080 H.264/AAC (29 MB) from Alex's 244 MB master. It plays on entry, pauses and rewinds on exit, never auto-advances; a "Tap to play" button appears if the browser blocks audio, and a small mute button sits bottom-right.
- **Splat slides** (`layout: 'splat'`): `splats-why` shows a portrait clip in a phone-shaped frame beside the benefit rows, followed by `portalcam-reel`, a full-bleed handheld-scanner walkthrough with sound (59 s, 27 MB, same behavior as the showreel). The old limits slide is parked. Josette's splat clip has a slot as `clips[1]` on `splats-why`: while its `img` is `[FILL: Josette's splat clip]` nothing is drawn. To add it, compress it into `media/video/`, put its path in that `img`, fill in `poster`, `alt` and `credit`, and run `python tools/build_pitch.py`.
- **Clips**: five muted, looping H.264 clips in `media/video/` (8.5 to 14 seconds, about 18 MB in all), each with alt text, a credit line and a poster frame. Only the active slide's clip plays.
- Speaker notes may end with `ALEX TO CONFIRM: ...`, a direction for the speaker that is not counted as spoken time.

## Things to Try

1. Open Talk A and press **→** to step through it, then open `?talk=b` and notice which slides reappear: those are the `[A+B]` pool slides.
2. Go to `#17` of Talk A (the camera demo): drag the camera on the plan, switch lenses and press Take shot. Then go to `#12` and `#14`: the film-pipeline and one-story diagrams build in, then keep a gentle loop. Turn on your OS "reduce motion" setting and reload: they, and the quote rain on `#8`, show as still frames.
3. Press **N** for the presenter popup, or open `index.html?talk=b&notes` on a phone: each slide's notes start with its pacing tag, and the timer shows elapsed time.
4. In `talk/pitch.json`, change a slide's `sec`, run `python tools/build_pitch.py`, and watch the running times update. Then delete a rain quote's `year` and see the build refuse.
5. Turn off Wi-Fi and step through both talks: fonts, clips and the QR code all still load.

## Media and rights

Round-2 stills (RSC rehearsal and virtual Swan, Perfect Day Mexico renders, holodeck photos, the Carol Ghost of Christmas Future) come from the HarvardXR keynote's `media/` folder on Alex's MacBook, resized to 1600 px; the RSC compare pair is cut from `RSC_compare.png`. Clearance items are listed as `ALEX TO CONFIRM` in each slide's notes. Earlier images were reused from Alex's earlier talk repos ([harvardxr-keynote](https://github.com/ibrews/harvardxr-keynote), [fmx-2026-spatial-storytelling](https://github.com/ibrews/fmx-2026-spatial-storytelling), [sensai-2026-mcp-engines](https://github.com/ibrews/sensai-2026-mcp-engines), [pmre-2026-xr-chitect](https://github.com/ibrews/pmre-2026-xr-chitect)). The David Geffen Hall photo (Fisher Dachs Associates imagery) is no longer shown; that slide is text only.

Clips, all from Agile Lens productions, trimmed and re-encoded without audio:

| Clip | Slide | Source |
|---|---|---|
| `carol-trailer-dance.mp4` | Talk A, the audience's view | *A Christmas Carol VR* 2025 trailer, 0:00-0:11 ([YouTube](https://www.youtube.com/watch?v=PdLtRbvx3V8)) |
| `carol-trailer-ghosts.mp4` | Talk B, Photoreal That Actually Runs | same trailer, 0:24-0:34 |
| `carol-replay-marley.mp4` | Talk A, The Run Ended | "Replay Recording" by Yu-Jun Yeh, 0:18-0:30 ([YouTube](https://www.youtube.com/watch?v=0UYW7AleAsk)) |
| `rsc-rehearsal-room.mp4` | Both talks, Royal Shakespeare Company | XR Network+ RSC Challenge 2025 film, 2:00-2:14 ([YouTube](https://www.youtube.com/watch?v=6or3BUzP3RU)) |
| `fsla-in-vr.mp4` | Talk A, Four Seasons | in-headset part of the Lake Austin tour capture used in the HarvardXR keynote, 0:52-1:00 |
| `carol-belle.mp4` | Both talks, live capture close-up | Alex's local copy of *A Christmas Carol VR -- Scrooge Remembers Belle*, 0:40-0:50 |
| `fs-holodeck-build.mp4` | Talk B, The Part Nobody Sees | holodeck build time-lapse, first 12 s of `fsla_video.mp4` in the HarvardXR keynote |

Quotes on the rain slide come from the show's site (xmascarolvr.com), the Voices of VR podcast, UploadVR (editorial) and Instinctively Real Media, which is labeled as the show's media sponsor.

Fonts: Space Grotesk, Inter, Outfit, JetBrains Mono and Playfair Display, SIL Open Font License 1.1 (`assets/fonts/OFL.txt`). three.js: MIT (`assets/vendor/three/LICENSE`).

## Credits

**Alex Coulombe Presents** · framework: [Spatial Deck](https://github.com/ibrews/spatial-deck) · house style: [acp-style-guide](https://github.com/ibrews/acp-style-guide)
