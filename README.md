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

## How it is built

- **`talk/pitch.json` is the single source of truth.** It holds the shared `pool` (each slide appears once, tagged `talks: A | B | A+B`, `pace: FLASH | DWELL`, and `sec`) and the two `talks`, each an ordered list of acts that reference pool ids.
- **`python tools/build_pitch.py`** validates the pool, splices it into `index.html` between the `PITCH-JSON` sentinels, regenerates `TALKS.md`, and prints each talk's running time against the 10-minute slot. It fails, writing nothing, on an unknown id, a tag mismatch (a slide used by a talk it isn't tagged for), an orphan slide, a FLASH slide over 15 seconds, a DWELL slide under 30 seconds, missing notes, or a missing media file. It warns when a slide's notes take longer to say at 150 wpm than the slide is budgeted.
- Pacing and talk tags lead every slide's presenter notes, for example `[DWELL · 50s · A+B]`, so they show in the **N** popup and the `?notes` phone view.
- Fork-local additions to Spatial Deck: `?talk=b`, `bigScale` on `layout: 'big'` slides, a guard for case slides without a subtitle, and a wider statement column. The framework's Bonus and Map end-markers are hidden because each talk ends on its own ask.

## Things to Try

1. Open Talk A and press **→** to step through it, then open `?talk=b` and notice which slides reappear: those are the `[A+B]` pool slides.
2. Press **N** for the presenter popup: each slide's notes start with its pacing tag, and the timer shows elapsed time against the talk.
3. Open `index.html?talk=b&notes` on a phone for the speaker companion, with the script and the next-slide preview.
4. In `talk/pitch.json`, change a slide's `sec`, run `python tools/build_pitch.py`, and watch the running times update. Then add a Talk A slide id to Talk B without retagging it, and see the build refuse.
5. Read the "Open [FILL] items" list at the bottom of `TALKS.md`. Every unverified fact is marked there instead of being guessed.

## Media and rights

Images were reused from Alex's earlier talk repos ([harvardxr-keynote](https://github.com/ibrews/harvardxr-keynote), [fmx-2026-spatial-storytelling](https://github.com/ibrews/fmx-2026-spatial-storytelling), [sensai-2026-mcp-engines](https://github.com/ibrews/sensai-2026-mcp-engines), [pmre-2026-xr-chitect](https://github.com/ibrews/pmre-2026-xr-chitect)). Confirm client photo rights before public use: Four Seasons Lake Austin session photos, and the David Geffen Hall photo (Fisher Dachs Associates project imagery).

## Credits

**Alex Coulombe Presents** · framework: [Spatial Deck](https://github.com/ibrews/spatial-deck) · house style: [acp-style-guide](https://github.com/ibrews/acp-style-guide)
