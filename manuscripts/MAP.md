# Speaking transcript sources

How each talk's cleaned reading transcript (`speaking/<slug>/reading.html`) is produced.

Regenerate: `python3 scripts/extract_readings.py`
Then build: `python3 scripts/build_speaking.py`

| Slug | Source | Notes |
|------|--------|-------|
| all-hands-on-deck | `all-hands-on-deck.docx` | docx headings=7 blocks=95 |
| avoid-sabotage | `avoid-sabotage.docx` | docx headings=0 blocks=17 |
| build-and-fight | `build-and-fight.docx` | No Word heading styles; ALL-CAPS section labels promoted to h2. |
| fear-to-faith-favor | `fear-to-faith-favor.docx` | docx headings=5 blocks=92 |
| from-confusion-to-obedience | `Confusion-Turns-to-Obedience.pdf` | PDF; section titles (Introduction, Review, Correcting, …) → h2. |
| from-fear-to-faith-again | `from-fear-to-faith-again.docx` | docx headings=8 blocks=96 |
| from-ignorance-to-repentance | `cues` | No full manuscript; cue-based reading. Flat paragraphs. |
| good-shepherd | `good-shepherd.docx` | docx headings=12 blocks=114 |
| guard-the-gates | `guard-the-gates.docx` | docx headings=9 blocks=105 |
| how-can-i-start-building | `how-can-i-start-building.docx` | docx headings=3 blocks=103 |
| learning-to-live-in-the-story | `learning-to-live-in-the-story.docx` | docx headings=9 blocks=55 |
| make-war-not-peace | `make-war-not-peace.docx` | docx headings=1 blocks=81 |
| mens-preconference-2 | `cues` | No manuscript on hand; cue/prior reading. |
| pray-lots-work-hard | `pray-lots-work-hard-from-cues.txt` | Cue-derived prose (docx was scripture-only). Flat paragraphs. |
| put-your-name-on-something | `put-your-name-on-something.docx` | Skip First Draft / Explanatory Outline; start at Heading Introduction; keep sermon section headings. |
| resurrection-jesus-is-king | `resurrection-jesus-is-king.docx` | docx headings=28 blocks=224 |
| who-can-stand-against-us | `who-can-stand-against-us.docx` | docx headings=11 blocks=49 |
| win-the-world-through-the-word | `win-the-world-through-the-word.docx` | docx headings=7 blocks=90 |

Heading mapping: Word `Heading1` / `Heading2` → `<h2>`; `Heading3` → `<h3>`; body → `<p>`.
Skip redundant Heading1 when it matches the page H1 title.

Page layout: YouTube `#yt-player` → **Transcript** (`reading-transcript`) → **Follow along** (`#transcript`).

Preview only: sync `speaking/` to `ncolestock/ncolestock.github.io`.
Never push `nathan.colestock.me` / production CNAME from this lane.
