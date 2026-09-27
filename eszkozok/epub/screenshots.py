"""Szemrevételező képek a kész EPUB kulcsoldalairól (Chromium, e-könyv-olvasó méretben).

1-kesz-konyv/protokollok.epub → build/epub/shots/<név>-<nézet>.png
Nézetek: 6 hüvelykes olvasó (600×800) világos és sötét (invertált) témával.
"""
import os
import re
import shutil
import zipfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / "1-kesz-konyv/protokollok.epub"
X = ROOT / "build/epub/x"
OUT = ROOT / "build/epub/shots"
CHROMIUM = os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium")

# Reader-szerű alapbeállítás: margó, alapméret. A könyv CSS-e ezen felül érvényesül.
READER_CSS = "html { font-size: 17px; } body { margin: 28px 30px !important; }"
DARK_CSS = "html { filter: invert(1) hue-rotate(180deg); background: #fff; } img { filter: invert(1) hue-rotate(180deg); }"


def find(pattern: str) -> Path:
    for f in sorted((X / "EPUB/text").glob("*.xhtml")):
        if re.search(pattern, f.read_text(encoding="utf-8")):
            return f
    raise LookupError(pattern)


def targets() -> list[tuple[str, Path, str | None]]:
    t = X / "EPUB/text"
    return [
        ("01-borito", t / "cover.xhtml", None),
        ("02-cimoldal", t / "title_page.xhtml", None),
        ("03-tartalom", X / "EPUB/nav.xhtml", None),
        ("04-ajanlas", find(r'class="dedication"'), None),
        ("05-fejezetnyito", find(r'<h1 class="chapter-opener"'), None),
        ("06-protokoll-1", find(r'protocol-title">Nézz napfényt minél hamarabb'), None),
        ("07-doboz", find(r'class="sidebar"'), "div.sidebar"),
        ("08-mit-tegyel-lista", find(r'protocol-title">Nézz napfényt késő délután'), None),
        ("09-szerzo", find(r'class="author-photo"'), None),
        ("10-labjegyzetek", find(r'protocol-title">Nézz napfényt minél hamarabb'), "section.footnotes"),
        ("11-copyright", find(r'vegyétek meg az eredeti könyvet'), None),
    ]


def main() -> None:
    shutil.rmtree(X, ignore_errors=True)
    zipfile.ZipFile(EPUB).extractall(X)
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        kw = {"executable_path": CHROMIUM} if Path(CHROMIUM).exists() else {}
        browser = p.chromium.launch(**kw)
        for theme, extra in (("vilagos", ""), ("sotet", DARK_CSS)):
            page = browser.new_page(viewport={"width": 600, "height": 800}, device_scale_factor=1.5)
            for name, path, anchor in targets():
                page.goto(path.as_uri())
                page.add_style_tag(content=READER_CSS + extra)
                if anchor:
                    page.locator(anchor).first.scroll_into_view_if_needed()
                    page.evaluate("window.scrollBy(0, -40)")
                page.wait_for_timeout(150)
                page.screenshot(path=str(OUT / f"{name}-{theme}.png"))
            page.close()
        browser.close()
    print(OUT)


if __name__ == "__main__":
    main()
