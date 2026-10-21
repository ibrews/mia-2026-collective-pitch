# MIA XR Collective Pitch: Two Talks, One Slide Pool

Alex Coulombe's 10-minute pitch for the **MIA XR Collective Pitch** (MIA | Mercato Internazionale Audiovisivo, Rome, 22 October 2026), for an audience of film and TV producers, distributors and IP holders. Two complete versions of the talk are drawn from one shared slide pool, and both close on the same partnership ask.

| | Talk | Thesis | Open it |
|---|---|---|---|
| **A** | *Old Stories, New Doors* | Beloved stories need new audiences and new revenue beyond the stage and screen; *A Christmas Carol VR* is the working model | [ibrews.github.io/mia-2026-collective-pitch](https://ibrews.github.io/mia-2026-collective-pitch/) |
| **B** | *Engine Mastery × Craft* | The studios winning in immersive pair engine mastery with craft | […/?talk=b](https://ibrews.github.io/mia-2026-collective-pitch/?talk=b) |

The full script (running orders with clock times, every slide's beats and speaker notes, and the open `[FILL]` list) is in **[TALKS.md](TALKS.md)**.

## Quickstart

```bash
git clone https://github.com/ibrews/mia-2026-collective-pitch
cd mia-2026-collective-pitch
python -m http.server 8748
```

Then open `http://localhost:8748/` for Talk A or `http://localhost:8748/?talk=b` for Talk B. Opening `index.html` directly also works.

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
- **Standard intro** (`layout: 'intro-alex'` and `'intro-lens'`, ported from spatial-deck-pmre2026 `talk/intro.js`, itself the FMX 2026 / HarvardXR intro): the 8-bit Alex walks in and puts on a headset, then three clicks show the bio, a clapperboard power-up and the stat tallies; the Agile Lens monocle has clients orbiting it, then five clicks run the 2026 → 2016 countdown. The Unreal badge and logo fireballs of earlier decks are replaced by a pixel clapperboard and stars, because this deck shows no Epic logos. Both talks open with these two slides.
- **Motion diagrams** (`layout: 'pipeline'` and `'ip-web'`): one SVG each, drawn by a pure `render(t)` function, so the build (about 7 seconds, replayed on every entry), the ambient loop and the static frame used by `?print`, `?shot` and reduced motion are the same code. `pipeline` takes three `phases` of up to three items (`al: true` fills the dot: Agile Lens has built it); `ip-web` takes a `center`, up to five `branches` (`t`, `d`, `proof`, `al`) and an `only` list.
- **Clips**: five muted, looping H.264 clips in `media/video/` (8.5 to 14 seconds, about 18 MB in all), each with alt text, a credit line and a poster frame. Only the active slide's clip plays.
- Speaker notes may end with `ALEX TO CONFIRM: ...`, a direction for the speaker that is not counted as spoken time.

## Things to Try

1. Open Talk A and press **→** to step through it, then open `?talk=b` and notice which slides reappear: those are the `[A+B]` pool slides.
2. Go to `#12` and `#14` of Talk A: the film-pipeline and one-story diagrams build in, then keep a gentle loop. Turn on your OS "reduce motion" setting and reload: they, and the quote rain on `#8`, show as still frames.
3. Press **N** for the presenter popup, or open `index.html?talk=b&notes` on a phone: each slide's notes start with its pacing tag, and the timer shows elapsed time.
4. In `talk/pitch.json`, change a slide's `sec`, run `python tools/build_pitch.py`, and watch the running times update. Then delete a rain quote's `year` and see the build refuse.
5. Turn off Wi-Fi and step through both talks: fonts, clips and the QR code all still load.

## Media and rights

Images were reused from Alex's earlier talk repos ([harvardxr-keynote](https://github.com/ibrews/harvardxr-keynote), [fmx-2026-spatial-storytelling](https://github.com/ibrews/fmx-2026-spatial-storytelling), [sensai-2026-mcp-engines](https://github.com/ibrews/sensai-2026-mcp-engines), [pmre-2026-xr-chitect](https://github.com/ibrews/pmre-2026-xr-chitect)). The David Geffen Hall photo (Fisher Dachs Associates imagery) is no longer shown; that slide is text only.

Clips, all from Agile Lens productions, trimmed and re-encoded without audio:

| Clip | Slide | Source |
|---|---|---|
| `carol-trailer-dance.mp4` | Talk A, the audience's view | *A Christmas Carol VR* 2025 trailer, 0:00-0:11 ([YouTube](https://www.youtube.com/watch?v=PdLtRbvx3V8)) |
| `carol-trailer-ghosts.mp4` | Talk B, Photoreal That Actually Runs | same trailer, 0:24-0:34 |
| `carol-replay-marley.mp4` | Talk A, The Run Ended | "Replay Recording" by Yu-Jun Yeh, 0:18-0:30 ([YouTube](https://www.youtube.com/watch?v=0UYW7AleAsk)) |
| `rsc-rehearsal-room.mp4` | Both talks, Royal Shakespeare Company | XR Network+ RSC Challenge 2025 film, 2:00-2:14 ([YouTube](https://www.youtube.com/watch?v=6or3BUzP3RU)) |
| `fsla-in-vr.mp4` | Talk A, Four Seasons (slide parked) | in-headset part of the Lake Austin tour capture used in the HarvardXR keynote, 0:52-1:00 |

Quotes on the rain slide come from the show's site (xmascarolvr.com), the Voices of VR podcast, UploadVR (editorial) and Instinctively Real Media, which is labeled as the show's media sponsor.

Fonts: Space Grotesk, Inter, Outfit, JetBrains Mono and Playfair Display, SIL Open Font License 1.1 (`assets/fonts/OFL.txt`). three.js: MIT (`assets/vendor/three/LICENSE`).

## Credits

**Alex Coulombe Presents** · framework: [Spatial Deck](https://github.com/ibrews/spatial-deck) · house style: [acp-style-guide](https://github.com/ibrews/acp-style-guide)
