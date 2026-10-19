#!/usr/bin/env python3
"""Build the MIA 2026 Collective Pitch from talk/pitch.json.

talk/pitch.json is the single source of truth: one shared slide pool plus two talks that
reference pool ids. This script
  1. validates it (ids unique and resolvable, every slide's talk tags match where it is used,
     pacing tag agrees with its seconds, no orphan pool slides, required fields present),
  2. splices it into index.html between the PITCH-JSON sentinels,
  3. writes TALKS.md: the readable script (pool table + both running orders + notes),
  4. prints each talk's running time against the 10-minute slot.

Exit code is non-zero on any validation error, so a broken pool never reaches index.html.

    python tools/build_pitch.py            # validate + build
    python tools/build_pitch.py --check    # validate only, write nothing
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "talk" / "pitch.json"
HTML = ROOT / "index.html"
MD = ROOT / "TALKS.md"

SLOT_SEC = 600          # 10 minutes on stage
TARGET_MAX = 590        # leave a few seconds for the walk-on and the moderator hand-off
TARGET_MIN = 510
FLASH_MAX_SEC = 15
DWELL_MIN_SEC = 30
FILL = re.compile(r"\[FILL:[^\]]*\]")
WORDS_PER_SEC = 2.5     # 150 wpm conversational delivery
START, END = "/* PITCH-JSON START */", "/* PITCH-JSON END */"


def fail(errors):
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)


def talk_ids(talk):
    for act in talk["acts"]:
        yield act["lesson"]
        yield from act["cases"]


def validate(p):
    errors = []
    pool = {}
    for s in p["pool"]:
        sid = s.get("id")
        if not sid:
            errors.append(f"pool slide without id: {s.get('title')!r}")
            continue
        if sid in pool:
            errors.append(f"duplicate pool id {sid!r}")
        pool[sid] = s
        if s.get("talks") not in ("A", "B", "A+B"):
            errors.append(f"{sid}: talks must be A, B or A+B (got {s.get('talks')!r})")
        pace, sec = s.get("pace"), s.get("sec")
        if pace not in ("FLASH", "DWELL"):
            errors.append(f"{sid}: pace must be FLASH or DWELL")
        elif not isinstance(sec, (int, float)):
            errors.append(f"{sid}: sec must be a number")
        elif pace == "FLASH" and sec > FLASH_MAX_SEC:
            errors.append(f"{sid}: FLASH slides run <= {FLASH_MAX_SEC}s (got {sec}s); retag as DWELL or cut")
        elif pace == "DWELL" and sec < DWELL_MIN_SEC:
            errors.append(f"{sid}: DWELL slides run >= {DWELL_MIN_SEC}s (got {sec}s); retag as FLASH")
        if not s.get("notes"):
            errors.append(f"{sid}: speaker notes are required")
        # Image-only full-bleed beats are deliberate (spatial-deck conventions): no overlay text needed
        if not (s.get("title") or s.get("bigText") or (s.get("layout") == "full" and s.get("img"))):
            errors.append(f"{sid}: needs a title (or bigText for layout 'big', or img for layout 'full')")
        if s.get("img") and not s["img"].startswith(("http", "IFRAME:")) and not (ROOT / s["img"]).exists():
            errors.append(f"{sid}: missing media file {s['img']}")

    used = {"A": set(), "B": set()}
    for key, talk in p["talks"].items():
        letter = key.upper()
        seen = set()
        for sid in talk_ids(talk):
            if sid not in pool:
                errors.append(f"talk {letter}: unknown pool id {sid!r}")
                continue
            if sid in seen:
                errors.append(f"talk {letter}: {sid!r} appears twice")
            seen.add(sid)
            if letter not in pool[sid]["talks"]:
                errors.append(f"talk {letter} uses {sid!r} but it is tagged [{pool[sid]['talks']}]")
            used[letter].add(sid)
        for act in talk["acts"]:
            if pool.get(act["lesson"], {}).get("layout"):
                errors.append(f"talk {letter}: act lesson {act['lesson']!r} must be a plain slide, not layout {pool[act['lesson']]['layout']!r}")
    for sid, s in pool.items():
        for letter in ("A", "B"):
            if letter in s["talks"] and sid not in used[letter]:
                errors.append(f"{sid} is tagged [{s['talks']}] but talk {letter} never uses it (retag or drop it)")
    return pool, errors


def spoken_sec(s):
    """Seconds the speaker notes take to say aloud, ignoring [FILL] markers and stage directions."""
    text = FILL.sub("", s.get("notes", ""))
    text = re.sub(r"^Pause\.[^:]*:", "", text)
    return len(text.split()) / WORDS_PER_SEC


def running_time(talk, pool):
    return sum(pool[sid]["sec"] for sid in talk_ids(talk)) + talk.get("cover_sec", 0)


def fmt(sec):
    return f"{int(sec) // 60}:{int(sec) % 60:02d}"


def strip_html(t):
    return re.sub(r"<[^>]+>", "", (t or "").replace("<br>", " ")).replace("\n", " ").strip()


def slide_lines(s):
    lines = []
    if s.get("subtitle"):
        lines.append(f"*{strip_html(s['subtitle'])}*")
    if s.get("bigText"):
        lines.append(f"**On screen:** {strip_html(s['bigText'])}")
    for b in s.get("bullets", []):
        lines.append(f"- {strip_html(b)}")
    if s.get("tagline") and not s.get("bullets"):
        lines.append(f"- {strip_html(s['tagline'])}")
    return lines


def write_md(p, pool):
    out = [
        f"# {strip_html(p['event_plain'])}: talk scripts",
        "",
        "Generated by `tools/build_pitch.py` from `talk/pitch.json`. Edit the JSON, not this file.",
        "",
        "Tags: **[A]** Talk A only, **[B]** Talk B only, **[A+B]** shared. "
        "**[FLASH]** is a ~10-second visual beat; **[DWELL]** is a ~1-minute story beat.",
        "",
    ]
    for key, talk in p["talks"].items():
        rt = running_time(talk, pool)
        out += [f"- **Talk {key.upper()}: {strip_html(talk['title'])}**, {fmt(rt)} planned "
                f"([open](https://ibrews.github.io/mia-2026-collective-pitch/{'' if key == 'a' else '?talk=b'}))"]
    out += ["", "## Running orders", ""]
    for key, talk in p["talks"].items():
        out += [f"### Talk {key.upper()}: {strip_html(talk['title'])}", "",
                f"Thesis: {talk['thesis']}", "",
                "| # | Act | Slide | Tags | Pace | Sec | Clock |", "|---|---|---|---|---|---|---|"]
        clock, n = talk.get("cover_sec", 0), 1
        out.append(f"| 0 | Cover | {strip_html(talk['title'])} | [{key.upper()}] | FLASH | {talk.get('cover_sec', 0)} | {fmt(clock)} |")
        for act in talk["acts"]:
            for sid in [act["lesson"], *act["cases"]]:
                s = pool[sid]
                clock += s["sec"]
                title = strip_html(s.get("title") or s.get("bigText"))
                out.append(f"| {n} | {act['year']} | {title} (`{sid}`) | [{s['talks']}] | {s['pace']} | {s['sec']} | {fmt(clock)} |")
                n += 1
        out += ["", f"Take-home line: **{strip_html(talk['takeaway'])}**", ""]
    out += ["## Shared slide pool", ""]
    for s in p["pool"]:
        title = strip_html(s.get("title") or s.get("bigText"))
        out += [f"### `{s['id']}`: {title}", "", f"**[{s['talks']}] [{s['pace']}] {s['sec']}s**", ""]
        out += slide_lines(s)
        out += ["", f"> **Notes:** {s['notes']}", ""]
    fills = sorted({m for s in p["pool"] for m in FILL.findall(json.dumps(s, ensure_ascii=False))})
    out += ["## Open [FILL] items", ""] + [f"- {f}" for f in fills] + [""]
    MD.write_text("\n".join(out), encoding="utf-8", newline="\n")
    return fills


def main():
    p = json.loads(SRC.read_text(encoding="utf-8"))
    pool, errors = validate(p)
    if errors:
        fail(errors)
    for key, talk in p["talks"].items():
        rt = running_time(talk, pool)
        n = sum(1 for _ in talk_ids(talk))
        flags = "" if TARGET_MIN <= rt <= TARGET_MAX else f"  <-- outside {fmt(TARGET_MIN)}-{fmt(TARGET_MAX)} target"
        print(f"Talk {key.upper()}: {n} slides + cover, {fmt(rt)} of {fmt(SLOT_SEC)}{flags}")
    for s in p["pool"]:
        if spoken_sec(s) > s["sec"] * 1.1:
            print(f"WARN: {s['id']} notes take ~{spoken_sec(s):.0f}s to say but the slide is budgeted {s['sec']}s")
    if "--check" in sys.argv:
        return
    html = HTML.read_text(encoding="utf-8")
    i, j = html.index(START) + len(START), html.index(END)
    blob = json.dumps({k: v for k, v in p.items()}, ensure_ascii=False, indent=1)
    HTML.write_text(html[:i] + "\n" + blob + "\n" + html[j:], encoding="utf-8", newline="\n")
    fills = write_md(p, pool)
    print(f"Wrote index.html and TALKS.md ({len(fills)} open [FILL] items)")


if __name__ == "__main__":
    main()
