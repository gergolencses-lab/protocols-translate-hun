"""Protokollok – nyomtatható A5 PDF.

2-szoveg/magyar/protokollok.md → build/pdf/protokollok.html → 1-kesz-konyv/protokollok-A5.pdf
Ugyanaz a forrás és ugyanazok a szűrők, mint az EPUB-nál; döntések: 4-dokumentacio/pdf-dontesek.md.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eszkozok/kozos"))
from prepare import prepare  # noqa: E402

SRC = ROOT / "2-szoveg/magyar/protokollok.md"
BUILD = ROOT / "build/pdf"
OUT = ROOT / "1-kesz-konyv/protokollok-A5.pdf"
CSS = ROOT / "3-kinezet/pdf/print.css"
COVER = ROOT / "3-kinezet/borito/cover.jpg"
FILTERS = [
    ROOT / "eszkozok/pdf/szurok/notes.lua",  # a címsorok átalakítása előtt kell futnia
    ROOT / "eszkozok/kozos/szurok/chapter.lua",
    ROOT / "eszkozok/kozos/szurok/protocol.lua",
    ROOT / "eszkozok/kozos/szurok/sidebar.lua",
    ROOT / "eszkozok/kozos/szurok/pseudohead.lua",  # a sidebar.lua után
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
        items.append(f'<li class="toc-{level[-1]}"><a href="#{sid}">{text}</a></li>')
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
<meta name="generator" content="Pandoc + WeasyPrint (eszkozok/pdf/build_pdf.py)"/>
<link rel="stylesheet" href="{CSS.as_uri()}"/>
</head>
<body>
<div class="cover"><img src="{COVER.as_uri()}" alt="Borító"/></div>
{TITLE_PAGE}
{build_toc(body)}
{body}
</body>
</html>
"""
    html_path = BUILD / "protokollok.html"
    html_path.write_text(doc, encoding="utf-8")

    from weasyprint import HTML
    # base_url: a magyar szöveg mappája — innen oldódnak fel a Markdown képei (../kepek/…).
    HTML(string=doc, base_url=str(SRC.parent) + "/").write_pdf(OUT)
    print(OUT, f"{OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
