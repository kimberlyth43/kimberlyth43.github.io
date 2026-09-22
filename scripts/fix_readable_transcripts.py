#!/usr/bin/env python3
"""Rebuild pray-lots reading from cues; strip put-your-name outline; rebuild speaking pages."""
from __future__ import annotations
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAP = 2.5
MIN_PARA = 220

def clean_text(t: str) -> str:
    t = t.strip()
    t = re.sub(r"\b([A-Za-z][A-Za-z']*)\s+\1\b", r"\1", t, flags=re.I)
    t = t.replace('""', '"')
    return re.sub(r"\s+", " ", t).strip()

def cues_to_paras(cues: list) -> list[str]:
    paras: list[str] = []
    buf: list[str] = []
    prev_end = None

    def buf_text() -> str:
        return clean_text(" ".join(buf))

    def flush() -> None:
        nonlocal buf
        text = buf_text()
        if text:
            paras.append(text)
        buf = []

    for cue in cues:
        text = clean_text(str(cue.get("text") or ""))
        if not text:
            continue
        start = float(cue.get("start") or 0)
        end = float(cue.get("end") or start)
        if buf and prev_end is not None:
            gap = start - prev_end
            prev = buf[-1]
            cur = buf_text()
            if gap > GAP:
                flush()
            elif (
                re.search(r'[.!?]"?\s*$', prev)
                and text[:1].isupper()
                and len(cur) >= MIN_PARA
            ):
                flush()
        buf.append(text)
        prev_end = end
    flush()
    return paras

def write_reading(path: Path, paras: list[str]) -> None:
    parts = ['<div class="reading-body">']
    for p in paras:
        parts.append(f"<p>{html.escape(p, quote=False)}</p>")
    parts.append("</div>")
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")

def fix_pray_lots() -> None:
    slug = "pray-lots-work-hard"
    cues = json.loads((ROOT / "speaking" / slug / "transcript.json").read_text(encoding="utf-8"))
    paras = cues_to_paras(cues)
    write_reading(ROOT / "speaking" / slug / "reading.html", paras)
    ms = ROOT / "manuscripts"
    ms.mkdir(exist_ok=True)
    (ms / "pray-lots-work-hard-from-cues.txt").write_text("\n\n".join(paras) + "\n", encoding="utf-8")
    for p in (ROOT / "speaking" / slug).glob("reading.p*.html"):
        p.unlink()
    for p in (ROOT / "speaking" / slug).glob("reading.part*.html"):
        p.unlink()
    print(f"pray-lots: {len(paras)} paras, reading={(ROOT / 'speaking' / slug / 'reading.html').stat().st_size}")

def fix_put_your_name() -> None:
    path = ROOT / "speaking" / "put-your-name-on-something" / "reading.html"
    raw = path.read_text(encoding="utf-8")
    m = re.search(r'<div class="reading-body">(.*)</div>\s*\Z', raw, flags=re.S)
    if not m:
        raise SystemExit("put-your-name: no reading-body")
    paras = re.findall(r"<p>.*?</p>", m.group(1), flags=re.S)
    texts = []
    for p in paras:
        t = html.unescape(re.sub(r"<[^>]+>", "", p)).strip()
        texts.append(t)
    intro = next((i for i, t in enumerate(texts) if t == "Introduction" or t.startswith("Introduction")), None)
    if intro is None:
        raise SystemExit("put-your-name: Introduction missing")
    meta = []
    for i, t in enumerate(texts):
        if i >= intro:
            break
        if t in {"First Draft", "Explanatory Outline"} or t.startswith("Explanatory Outline"):
            break
        meta.append(paras[i])
    out = ["<div class=\"reading-body\">", *meta, *paras[intro:], "</div>"]
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    new = path.read_text(encoding="utf-8")
    assert "Explanatory Outline" not in new and "First Draft" not in new
    print(f"put-your-name: reading={path.stat().st_size}")

def write_map() -> None:
    (ROOT / "MAP.md").write_text(
        """# Speaking transcript sources

How each talk's cleaned reading transcript (`speaking/<slug>/reading.html`) was produced.

| Slug | Source | Notes |
|------|--------|-------|
| pray-lots-work-hard | `manuscripts/pray-lots-work-hard-from-cues.txt` (from `transcript.json` cues) | Manuscript docx was scripture-only; rebuilt from spoken cues as full sermon prose. |
| put-your-name-on-something | manuscript / prior reading | Dropped Explanatory Outline / First Draft material before Introduction. |
| from-ignorance-to-repentance | spoken cues / prior reading | Light ASR polish only. |
| *(other talks)* | manuscript docx or cue-derived | See each `speaking/<slug>/reading.html`. |

Build: `python3 scripts/build_speaking.py` embeds each `reading.html` under the talk page **Transcript** section (keeps YouTube iframe + **Follow along** cues).

Preview only: sync `speaking/` to `ncolestock/ncolestock.github.io`. Never push `nathan.colestock.me` / production CNAME from this lane.
""",
        encoding="utf-8",
    )

def main() -> None:
    fix_pray_lots()
    fix_put_your_name()
    write_map()
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_speaking  # noqa: E402

    build_speaking.main()

if __name__ == "__main__":
    main()
