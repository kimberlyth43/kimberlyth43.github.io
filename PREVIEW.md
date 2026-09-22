# Speaking preview

Public preview, for review before anything goes on the live site:

**https://ncolestock.github.io/speaking/**

The rest of the site is on that same host, so Writing, Reading, and Thoughts still work:

**https://ncolestock.github.io/**

Open those links in a private window. There is no login. A banner at the top of each page says it is a preview.

This preview is the GitHub Pages site for the public repo [ncolestock/ncolestock.github.io](https://github.com/ncolestock/ncolestock.github.io). It is not `nathan.colestock.me`. The production repo `ncolestock/nathan.colestock.me` was not pushed, and its `CNAME` was not copied here.

## What is on the list

Eighteen talks from `nathan-ctk-sermons-strict-catalog.md`, Nathan Colestock at Christ the King only. Newest first, grouped by year, with the full date.

Writing, Speaking, Reading, and Thoughts share one masthead (photo, name, bio, Stillwater, and X). The section tabs sit under that masthead and switch only the content below them. A talk page keeps a back link to Speaking instead of repeating the masthead.

On the Speaking list, scripture sits in the meta row beside the Sermon tag, in the same sans font as the tag and the date. There is no “Watch” link. Under each title is a short snippet, saved on the talk in `speaking/talks.json`.

Each talk page embeds the catalog YouTube video. Where English captions exist, the transcript follows the video: the current line highlights, the panel scrolls to keep up, and clicking a line seeks the video. A talk with no captions still plays, and says so.

## How to promote this to nathan.colestock.me

The files to publish are the working tree in this checkout of `nathan.colestock.me`, not a copy of the preview repo. Those files already use production paths (`/speaking/`, canonical `https://nathan.colestock.me/...`) and do not include the preview banner or the preview `noindex` tag.

1. Read `git status` and `git diff` in this checkout.
2. Commit the Speaking changes (`speaking/`, including each `transcript.json`, `scripts/build_speaking.py`, `scripts/fetch_transcripts.py`, the shared masthead on Writing, Reading, and Thoughts, and the Speaking styles in `style.css`).
3. Push `main` on `ncolestock/nathan.colestock.me`. GitHub Pages and the existing `CNAME` publish to https://nathan.colestock.me/speaking/.
4. After the live page looks right, delete the repo `ncolestock/ncolestock.github.io` if you want https://ncolestock.github.io to stop serving the preview.

Leave the preview repo without a `CNAME` file. A `CNAME` there would attach the live domain to the preview.

## Adding another talk later

Edit `speaking/talks.json` (`date`, `title`, `snippet`, `scripture` or `null`, `kind` of `sermon` or `conference`, `youtube` id, `slug`), then run:

```bash
python3 scripts/fetch_transcripts.py
python3 scripts/build_speaking.py
```

`fetch_transcripts.py` uses yt-dlp (`python3 -m yt_dlp`) to write `speaking/<slug>/transcript.json`. Set `snippet` once in `talks.json` so later rebuilds keep the same line. The builder keeps the list newest-first and refuses other preachers. The confirmed set lives in `nathan-ctk-sermons-strict-catalog.md`.
