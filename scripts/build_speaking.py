#!/usr/bin/env python3
"""Build the Speaking section from speaking/talks.json.

Writes speaking/index.html and speaking/<slug>/index.html. Dates sort newest
first. Sermons require scripture; conference talks do not. The page set is
Nathan Colestock at Christ the King only — the builder rejects other names.

    python3 scripts/build_speaking.py
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TALKS_PATH = ROOT / "speaking" / "talks.json"
SPEAKING = ROOT / "speaking"
SITE = "https://nathan.colestock.me"

MONTHS = (
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)
SHORT_MONTHS = (
    "",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)

# Other preachers and guests the strict catalog keeps off this list.
FORBIDDEN = re.compile(
    r"\b(andy|naselli|wilson|dustin|piper|dodds|zeigler|wittenburg|abigail|jenni|manley)\b",
    re.I,
)
YOUTUBE_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")

ICON = (
    "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAg"
    "MCA2NCA2NCI+PGNpcmNsZSBjeD0iMzIiIGN5PSIzMiIgcj0iMzIiIGZpbGw9IiM0QzVBMkIiLz48dGV4dCB4PSIzMiIgeT0i"
    "MzQiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGRvbWluYW50LWJhc2VsaW5lPSJjZW50cmFsIiBmb250LWZhbWlseT0iUGFsYXRp"
    "bm8sIEdlb3JnaWEsIHNlcmlmIiBmb250LXdlaWdodD0iNzAwIiBmb250LXNpemU9IjMwIiBmaWxsPSIjRUJFNEQwIj5OQzwv"
    "dGV4dD48L3N2Zz4="
)

THEME_BUTTON = """<button id="theme-toggle" type="button" aria-label="Toggle light and dark mode" title="Toggle theme">
  <svg class="moon" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
  <svg class="sun" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/></svg>
</button>"""

THEME_SCRIPT = """<script>
  (function () {
    var root = document.documentElement;
    var stored = null;
    try { stored = localStorage.getItem("nc-theme"); } catch (e) {}
    var initial = stored || ((window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light");
    root.setAttribute("data-theme", initial);
    var btn = document.getElementById("theme-toggle");
    if (btn) {
      btn.addEventListener("click", function () {
        var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        try { localStorage.setItem("nc-theme", next); } catch (e) {}
      });
    }
  })();
</script>"""

ANALYTICS = """<script data-goatcounter="https://ncolestock.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>"""

SECTIONS = (
    ("Writing", "/"),
    ("Speaking", "/speaking/"),
    ("Reading", "/reading/"),
    ("Thoughts", "/thoughts/"),
)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def parts(iso: str) -> tuple[int, int, int]:
    match = DATE.match(iso)
    if not match:
        raise SystemExit(f"bad date: {iso}")
    year, month, day = (int(match.group(i)) for i in (1, 2, 3))
    if not 1 <= month <= 12 or not 1 <= day <= 31:
        raise SystemExit(f"bad date: {iso}")
    return year, month, day


def full_date(iso: str) -> str:
    year, month, day = parts(iso)
    return f"{MONTHS[month]} {day}, {year}"


def rail_day(iso: str) -> str:
    _year, month, day = parts(iso)
    return f"{SHORT_MONTHS[month]} {day}"


def load_talks() -> list[dict]:
    raw = json.loads(TALKS_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise SystemExit("speaking/talks.json must be a list")
    if len(raw) != 18:
        raise SystemExit(f"expected 18 confirmed talks, found {len(raw)}")

    slugs: set[str] = set()
    videos: set[str] = set()
    for talk in raw:
        title = talk.get("title") or ""
        if FORBIDDEN.search(title) or FORBIDDEN.search(talk.get("scripture") or ""):
            raise SystemExit(f"refusing non-Nathan talk: {title}")
        slug = talk.get("slug") or ""
        video = talk.get("youtube") or ""
        if not SLUG.match(slug):
            raise SystemExit(f"bad slug: {slug}")
        if slug in slugs:
            raise SystemExit(f"duplicate slug: {slug}")
        slugs.add(slug)
        if not YOUTUBE_ID.match(video):
            raise SystemExit(f"bad youtube id for {slug}: {video}")
        if video in videos:
            raise SystemExit(f"duplicate youtube id: {video}")
        videos.add(video)
        parts(talk["date"])
        kind = talk.get("kind")
        scripture = talk.get("scripture")
        if kind == "sermon":
            if not scripture:
                raise SystemExit(f"sermon missing scripture: {slug}")
        elif kind == "conference":
            if scripture:
                raise SystemExit(f"conference talk should not carry scripture: {slug}")
        else:
            raise SystemExit(f"kind must be sermon or conference: {slug}")

    raw.sort(key=lambda item: item["date"], reverse=True)
    return raw


def tabs(active: str) -> str:
    lines = ['    <nav class="tabs" aria-label="Sections">']
    for label, href in SECTIONS:
        if label == active:
            lines.append(
                f'      <a class="tab is-active" href="{href}" aria-current="page">{label}</a>'
            )
        else:
            lines.append(f'      <a class="tab" href="{href}">{label}</a>')
    lines.append("    </nav>")
    return "\n".join(lines)


def head(title: str, description: str, path: str) -> str:
    url = f"{SITE}{path}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Nathan Colestock">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:image" content="{SITE}/avatar.jpg">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{SITE}/avatar.jpg">
<meta name="theme-color" content="#4C5A2B">
<link rel="icon" type="image/svg+xml" href="{ICON}">
<title>{esc(title)} — Nathan Colestock</title>
<link rel="stylesheet" href="/style.css">
</head>"""


def chrome_close() -> str:
    return f"""{THEME_SCRIPT}

{ANALYTICS}
</body>
</html>
"""


def index_page(talks: list[dict]) -> str:
    description = "Sermons and talks by Nathan Colestock at Christ the King Church in Stillwater."
    items: list[str] = []
    year_open: int | None = None
    for talk in talks:
        year = parts(talk["date"])[0]
        if year != year_open:
            year_open = year
            items.append(
                f'      <li class="speaking-year"><h2 class="speaking-year-label">{year}</h2></li>'
            )
        scripture = ""
        if talk["scripture"]:
            scripture = f'\n            <p class="scripture">{esc(talk["scripture"])}</p>'
        kind = "Conference" if talk["kind"] == "conference" else "Sermon"
        items.append(
            f"""      <li>
        <a class="post speaking-item" href="/speaking/{esc(talk["slug"])}/">
          <div class="speaking-date" aria-hidden="true"><span class="speaking-day">{esc(rail_day(talk["date"]))}</span></div>
          <div class="speaking-body">
            <div class="meta"><span class="tag">{kind}</span><time datetime="{esc(talk["date"])}">{esc(full_date(talk["date"]))}</time></div>
            <h3>{esc(talk["title"])}</h3>{scripture}
            <span class="more">Watch →</span>
          </div>
        </a>
      </li>"""
        )

    body = "\n".join(items)
    return f"""{head("Speaking", description, "/speaking/")}
<body>
<div id="mapbg" aria-hidden="true"></div>
{THEME_BUTTON}
<main class="view active" id="view-speaking">
  <div class="shell">
{tabs("Speaking")}
    <section class="speaking" aria-labelledby="speaking-h">
      <header class="page-head">
        <h1 class="page-title" id="speaking-h">Speaking</h1>
        <p class="speaking-intro">Sermons and talks from Christ the King Church in Stillwater, newest first. Video on each page. Transcripts will follow.</p>
      </header>
    <ul class="speaking-list">
{body}
    </ul>
    </section>
    <footer class="home-foot">© 2026 Nathan Colestock</footer>
  </div>
</main>
{chrome_close()}"""


def talk_page(talk: dict) -> str:
    title = talk["title"]
    kind = "Conference" if talk["kind"] == "conference" else "Sermon"
    when = full_date(talk["date"])
    scripture = talk["scripture"]
    if scripture:
        description = f"{title} — {scripture}. Nathan Colestock at Christ the King Church."
        meta_scripture = f"<span>·</span><span>{esc(scripture)}</span>"
        kicker = f"Preached {when} at Christ the King Church in Stillwater."
    else:
        description = f"{title}. Nathan Colestock."
        meta_scripture = ""
        kicker = f"{when}. Men's pre-conference."
    video = talk["youtube"]
    watch = f"https://www.youtube.com/watch?v={video}"
    return f"""{head(title, description, f"/speaking/{talk['slug']}/")}
<body>
<div id="mapbg" aria-hidden="true"></div>
{THEME_BUTTON}
<main class="view active">
  <div class="shell">
{tabs("Speaking")}
    <a class="backlink" href="/speaking/">← Speaking</a>
    <article class="speaking-talk">
      <header class="art-head">
        <div class="art-meta"><span class="tag">{kind}</span><time datetime="{esc(talk["date"])}">{esc(when)}</time>{meta_scripture}</div>
        <h1 class="art-title">{esc(title)}</h1>
        <div class="art-byline">
          <span class="pic" role="img" aria-label="Nathan Colestock"></span>
          <span class="who"><b>Nathan Colestock</b><small>Christ the King Church</small></span>
        </div>
      </header>
      <p class="speaking-kicker">{esc(kicker)}</p>
      <div class="rule"></div>
      <div class="video-wrap">
        <iframe src="https://www.youtube.com/embed/{esc(video)}" title="{esc(title)}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="eager" referrerpolicy="strict-origin-when-cross-origin"></iframe>
      </div>
      <section class="transcript" id="transcript" aria-labelledby="transcript-h">
        <h2 id="transcript-h">Transcript</h2>
        <p class="transcript-placeholder">A cleaned transcript will be added from the manuscript.</p>
      </section>
      <p class="speaking-note">Watch on <a href="{esc(watch)}" target="_blank" rel="noopener">YouTube</a>.</p>
    </article>
    <footer class="home-foot">© 2026 Nathan Colestock</footer>
  </div>
</main>
{chrome_close()}"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    talks = load_talks()
    write(SPEAKING / "index.html", index_page(talks))
    keep = set()
    for talk in talks:
        keep.add(talk["slug"])
        write(SPEAKING / talk["slug"] / "index.html", talk_page(talk))
    for child in SPEAKING.iterdir():
        if child.is_dir() and child.name not in keep:
            shutil.rmtree(child)
    print(f"wrote {len(talks)} talks, newest {talks[0]['date']}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
