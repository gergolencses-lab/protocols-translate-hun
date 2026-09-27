"""Protokollok – nyomtatható A5 PDF.

book/protocols-hu.md → build/pdf/protokollok.html → dist/protokollok-A5.pdf
Ugyanaz a forrás és ugyanazok a szűrők, mint az EPUB-nál; döntések: book/pdf/DECISIONS.md.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/epub"))
from prepare import prepare  # noqa: E402

SRC = ROOT / "book/protocols-hu.md"
BUILD = ROOT / "build/pdf"
OUT = ROOT / "dist/protokollok-A5.pdf"
FILTERS = [
    ROOT / "tools/pdf/filters/notes.lua",  # a címsorok átalakítása előtt kell futnia
    ROOT / "tools/epub/filters/chapter.lua",
    ROOT / "tools/epub/filters/protocol.lua",
    ROOT / "tools/epub/filters/sidebar.lua",
    ROOT / "tools/epub/filters/pseudohead.lua",  # a sidebar.lua után
]

TITLE_PAGE = """
<section class="titlepage">
  <p class="t-title">Protokollok</p>
  <p class="t-sub">Használati útmutató<br/>az emberi testhez</p>
  <p class="t-author">Andrew D. Huberman, <span>PhD</span></p>
  <p class="t-with">Jessica Wapner közreműködésével</p>
</section>
"""


def to_html_body(md: str) -> str:
    cmd = ["pandoc", "-f", "markdown-smart-implicit_figures", "-t", "html5", "--wrap=none",
           "--section-divs", "--shift-heading-level-by=-1"]
    for f in FILTERS:
        cmd += ["--lua-filter", str(f)]
    return subprocess.run(cmd, input=md, capture_output=True, text=True, check=True).stdout


def build_toc(body: str) -> str:
    """Tartalomjegyzék a fejezetekből (level1) és a protokollokból, oldalszámmal (CSS)."""
    items = []
    pat = re.compile(r'<section id="([^"]+)" class="(level[12])([^"]*)"[^>]*>\s*<h[12][^>]*>(.*?)</h[12]>', re.S)
    for sid, level, classes, inner in pat.findall(body):
        if level == "level2" and "protocol" not in classes:
            continue
        text = html.escape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html.unescape(inner))).strip())
        head, _, tail = text.rpartition(" ")
        tail_span = f'<span class="toc-tail" data-target="#{sid}">{tail}</span>'
        link_body = f"{head} {tail_span}" if head else tail_span
        items.append(f'<li class="toc-{level[-1]}"><a href="#{sid}">{link_body}</a></li>')
    return '<nav class="toc"><h1>Tartalom</h1><ol>' + "".join(items) + "</ol></nav>"


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    md = prepare(SRC.read_text(encoding="utf-8"), soft_hyphens=False, keep_notes=True)
    (BUILD / "protokollok.md").write_text(md, encoding="utf-8")
    body = to_html_body(md)
    doc = f"""<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="utf-8"/>
<title>Protokollok – Használati útmutató az emberi testhez</title>
<meta name="author" content="Andrew D. Huberman"/>
<meta name="description" content="Nem hivatalos, személyes használatra készült fordítás. Használjátok egészséggel, de vegyétek meg az eredeti könyvet mindenképp!"/>
<meta name="generator" content="Pandoc + WeasyPrint (tools/pdf/build_pdf.py)"/>
<link rel="stylesheet" href="pdf/print.css"/>
</head>
<body>
<div class="cover"><img src="epub/cover/cover.jpg" alt="Borító"/></div>
{TITLE_PAGE}
{build_toc(body)}
{body}
</body>
</html>
"""
    html_path = BUILD / "protokollok.html"
    html_path.write_text(doc, encoding="utf-8")

    from weasyprint import HTML
    # base_url: book/ — innen oldódnak fel a képek (images/…, epub/cover/…) és a CSS (pdf/print.css).
    HTML(string=doc, base_url=str(ROOT / "book") + "/").write_pdf(OUT)
    print(OUT, f"{OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
