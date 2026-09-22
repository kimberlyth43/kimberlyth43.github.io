# Speaking transcript sources

How each talk's cleaned reading transcript (`speaking/<slug>/reading.html`) was produced.

| Slug | Source | Notes |
|------|--------|-------|
| pray-lots-work-hard | `manuscripts/pray-lots-work-hard-from-cues.txt` (from `transcript.json` cues) | Manuscript docx was scripture-only; rebuilt from spoken cues as full sermon prose. |
| put-your-name-on-something | manuscript / prior reading | Dropped Explanatory Outline / First Draft material before Introduction. |
| from-ignorance-to-repentance | spoken cues / prior reading | Light ASR polish only. |
| *(other talks)* | manuscript docx or cue-derived | See each `speaking/<slug>/reading.html`. |

Build: `python3 scripts/build_speaking.py` embeds each `reading.html` under the talk page **Transcript** section (keeps YouTube iframe + **Follow along** cues).

Preview only: sync `speaking/` to `ncolestock/ncolestock.github.io`. Never push `nathan.colestock.me` / production CNAME from this lane.
