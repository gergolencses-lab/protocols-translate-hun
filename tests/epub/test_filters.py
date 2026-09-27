import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FILTERS = ROOT / "tools" / "epub" / "filters"


def render(md: str) -> str:
    if not shutil.which("pandoc"):
        pytest.skip("pandoc nincs telepítve")
    # Ugyanazok a kapcsolók, mint a build.sh-ban.
    cmd = ["pandoc", "-f", "markdown-smart-implicit_figures", "-t", "html",
           "--wrap=none", "--shift-heading-level-by=-1"]
    for f in ("chapter.lua", "protocol.lua", "sidebar.lua"):
        cmd += ["--lua-filter", str(FILTERS / f)]
    return subprocess.run(cmd, input=md, capture_output=True, text=True, check=True).stdout


@pytest.fixture(scope="module")
def html():
    return render((Path(__file__).parent / "fixture.md").read_text(encoding="utf-8"))


def test_chapter_opener(html):
    assert html.count('<h1 class="chapter-opener"') == 1
    assert '<span class="chapter-label">1. fejezet</span>' in html
    assert '<span class="chapter-title">Alvásprotokollok</span>' in html
    assert 'epub:type="chapter"' in html


def test_epub_types(html):
    assert 'epub:type="dedication"' in html


def test_protocols(html):
    assert html.count('class="protocol"') == 2
    assert '<span class="protocol-num">2</span>' in html
    assert '<span class="protocol-label">stresszszabályozási protokoll</span>' in html
    assert "A libikókamodell" in html and html.count("protocol-num") == 2


def test_block_labels(html):
    assert html.count('class="block-label"') == 2


def test_blockquotes(html):
    assert html.count('class="sidebar"') == 1
    assert 'class="sidebar-title"' in html
    assert html.count('class="dedication"') == 1
    assert html.count('class="example"') == 1
    assert "<blockquote" not in html


def test_images(html):
    assert '<div class="emblem">' in html
    assert "<figure" not in html and "figcaption" not in html
    assert '<div class="author-photo">' in html


def test_heading_text_intact_for_toc(html):
    # A spanok nélkül a címsor szövege változatlan (a tartalomjegyzék ezt mutatja).
    import re
    h2 = re.search(r'<h2[^>]*class="protocol"[^>]*>(.*?)</h2>', html, re.S).group(1)
    assert re.sub(r"<[^>]+>", "", h2) == "1. alvásprotokoll: Nézz napfényt ébredés után"
