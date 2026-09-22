# Speaking preview

Public preview, for review before anything goes on the live site:

**https://ncolestock.github.io/speaking/**

The rest of the site is on that same host, so Writing, Reading, and Thoughts still work:

**https://ncolestock.github.io/**

Open those links in a private window. There is no login. A banner at the top of each page says it is a preview.

This preview is the GitHub Pages site for the public repo [ncolestock/ncolestock.github.io](https://github.com/ncolestock/ncolestock.github.io). It is not `nathan.colestock.me`. The production repo `ncolestock/nathan.colestock.me` was not pushed, and its `CNAME` was not copied here.

## What is on the list

Eighteen talks from `nathan-ctk-sermons-strict-catalog.md`, Nathan Colestock at Christ the King only. Newest first, grouped by year, with the full date. Sermons show scripture. The September 3, 2026 men’s pre-conference session is included and has no scripture line. Each talk page embeds the catalog YouTube id and leaves a transcript placeholder.

## How to promote this to nathan.colestock.me

The files to publish are the working tree in this checkout of `nathan.colestock.me`, not a copy of the preview repo. Those files already use production paths (`/speaking/`, canonical `https://nathan.colestock.me/...`) and do not include the preview banner or the preview `noindex` tag.

1. Read `git status` and `git diff` in this checkout.
2. Commit the Speaking changes (`speaking/`, `scripts/build_speaking.py`, the nav link on Writing, Reading, and Thoughts, and the Speaking styles in `style.css`).
3. Push `main` on `ncolestock/nathan.colestock.me`. GitHub Pages and the existing `CNAME` publish to https://nathan.colestock.me/speaking/.
4. After the live page looks right, delete the repo `ncolestock/ncolestock.github.io` if you want https://ncolestock.github.io to stop serving the preview.

Leave the preview repo without a `CNAME` file. A `CNAME` there would attach the live domain to the preview.

## Adding another talk later

Edit `speaking/talks.json` (`date`, `title`, `scripture` or `null`, `kind` of `sermon` or `conference`, `youtube` id, `slug`), then run:

```bash
python3 scripts/build_speaking.py
```

The builder keeps the list newest-first and refuses other preachers. The confirmed set lives in `nathan-ctk-sermons-strict-catalog.md`.
