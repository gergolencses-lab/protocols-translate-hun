import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def render(md: str) -> str:
    if not shutil.which("pandoc"):
        pytest.skip("pandoc nincs telepítve")
    cmd = ["pandoc", "-f", "markdown-smart-implicit_figures", "-t", "html", "--wrap=none",
           "--lua-filter", str(ROOT / "tools/pdf/filters/notes.lua")]
    return subprocess.run(cmd, input=md, capture_output=True, text=True, check=True).stdout


@pytest.fixture(scope="module")
def html():
    return render((Path(__file__).parent / "fixture.md").read_text(encoding="utf-8"))


def test_no_pandoc_footnotes_left(html):
    assert "footnote" not in html and 'role="doc-noteref"' not in html


def test_refs_numbered_per_chapter(html):
    refs = re.findall(r'<sup><a href="#n-([\w-]+)" id="r-[\w-]+" class="noteref">(\d+)</a></sup>', html)
    assert refs == [("bevezetes-1", "1"), ("c01-1", "1"), ("c01-2", "2"), ("c01-3", "3"), ("c02-1", "1")]


def test_notes_under_matching_subheads(html):
    notes_part = html.split('id="jegyzetek"')[1]
    order = re.findall(r'<h3[^>]*>(.*?)</h3>|id="n-([\w-]+)"', notes_part)
    flat = [a or b for a, b in order]
    assert flat == ["Bevezetés", "bevezetes-1", "1. fejezet: Alvásprotokollok", "c01-1", "c01-2", "c01-3",
                    "2. fejezet: Edzésprotokollok", "c02-1"]
    assert '<a href="#r-c01-2" class="backref">2.</a> Kettes.' in notes_part


def test_notes_before_copyright(html):
    assert html.index('id="n-c02-1"') < html.index("Copyright")
