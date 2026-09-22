# Speaking transcript sources

How each talk's cleaned reading transcript (`speaking/<slug>/reading.html`) is produced.

Regenerate: `python3 scripts/extract_readings.py`
Then build: `python3 scripts/build_speaking.py`

| Slug | Source | Notes |
|------|--------|-------|
| all-hands-on-deck | `all-hands-on-deck.docx` | docx headings=7 lists=2 strong=3 fn=0 blocks=81 |
| avoid-sabotage | `avoid-sabotage.docx` | docx headings=0 lists=1 strong=3 fn=0 blocks=17 |
| build-and-fight | `build-and-fight.docx` | Use second manuscript copy after Titus 2 note (closer to video cues); never both tabs. ALL-CAPS → h2; lists/strong preserved. |
| fear-to-faith-favor | `fear-to-faith-favor.docx` | docx headings=5 lists=1 strong=3 fn=0 blocks=90 |
| from-confusion-to-obedience | `Confusion-Turns-to-Obedience.pdf` | PDF; section titles (Introduction, Review, Correcting, …) → h2. |
| from-fear-to-faith-again | `from-fear-to-faith-again.docx` | docx headings=1 lists=5 strong=2 fn=3 blocks=83 |
| from-ignorance-to-repentance | `cues` | No full manuscript; cue-based reading. Flat paragraphs. |
| good-shepherd | `good-shepherd.docx` | docx headings=12 lists=10 strong=9 fn=0 blocks=72 |
| guard-the-gates | `guard-the-gates.docx` | docx headings=9 lists=10 strong=2 fn=0 blocks=75 |
| how-can-i-start-building | `how-can-i-start-building.docx` | docx headings=3 lists=7 strong=1 fn=0 blocks=80 |
| learning-to-live-in-the-story | `learning-to-live-in-the-story.docx` | docx headings=9 lists=0 strong=1 fn=0 blocks=55 |
| make-war-not-peace | `make-war-not-peace.docx` | docx headings=1 lists=8 strong=19 fn=1 blocks=72 |
| mens-preconference-2 | `cues` | No manuscript on hand; cue/prior reading. |
| pray-lots-work-hard | `pray-lots-work-hard-from-cues.txt` | Cue-derived prose (docx was scripture-only). Flat paragraphs. |
| put-your-name-on-something | `put-your-name-on-something.docx` | Skip First Draft / Explanatory Outline; start at Heading Introduction; keep sermon section headings. |
| resurrection-jesus-is-king | `resurrection-jesus-is-king.docx` | docx headings=28 lists=6 strong=14 fn=0 blocks=212 |
| who-can-stand-against-us | `who-can-stand-against-us.docx` | docx headings=11 lists=0 strong=1 fn=0 blocks=49 |
| win-the-world-through-the-word | `win-the-world-through-the-word.docx` | docx headings=7 lists=4 strong=6 fn=0 blocks=78 |

Heading mapping: Word `Heading1` / `Heading2` → `<h2>`; `Heading3` → `<h3>`; body → `<p>`.
Skip redundant Heading1 when it matches the page H1 title.

Page layout: YouTube `#yt-player` → **Transcript** (`reading-transcript`) → **Follow along** (`#transcript`).

Preview only: sync `speaking/` to `ncolestock/ncolestock.github.io`.
Never push `nathan.colestock.me` / production CNAME from this lane.
