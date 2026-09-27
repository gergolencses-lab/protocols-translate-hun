"""A magyar forrás-Markdown előkészítése EPUB-konverzióhoz.

book/protocols-hu.md → build/epub/protokollok.md
Lásd: docs/superpowers/plans/2026-09-27-protokollok-epub.md, 2. feladat.
"""

import argparse
import re
from pathlib import Path

NBSP = " "
SHY = "­"

SYMBOL_UNITS = r"mg|g|kg|mcg|µg|ml|l|dl|cm|mm|m|km|°C|°F|%|lux|nm|NE|IU|kcal|bpm"
WORD_UNITS = r"másodperc|perc|óra|órá|nap|hét|heti|hónap|év"
HU_LOWER = "a-záéíóöőúüű"

_unit_re = re.compile(
    rf"(?<=\d) (?=(?:{SYMBOL_UNITS})(?![\w])|(?:{WORD_UNITS}))"
)
_ordinal_re = re.compile(rf"(?<![\d.,])(\d{{1,3}})\. (?=[{HU_LOWER}])")
# Részek, amelyekhez sem kötött szóköz, sem elválasztójel nem nyúlhat.
_protected_re = re.compile(
    r"\]\([^)]*\)|<[^>\s]+>|https?://\S+|www\.\S+|[\w.+-]+@[\w.-]+|`[^`]*`|\{[^}]*\}"
)
_word_re = re.compile(r"[^\W\d_]+")


def _map_unprotected(line: str, fn) -> str:
    out, pos = [], 0
    for m in _protected_re.finditer(line):
        out.append(fn(line[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(fn(line[pos:]))
    return "".join(out)


def _is_skipped_line(line: str) -> bool:
    s = line.lstrip("> ")
    return s.startswith("#") or s.startswith("[^") or s.startswith("![")


def strip_front(md: str) -> str:
    """Az első `## ` címsor előtti részt (borító, címblokk) törli."""
    m = re.search(r"^## ", md, re.M)
    return md[m.start():] if m else md


def remove_sections(md: str, titles: list[str]) -> str:
    """A `## <cím>` szakaszokat törli a következő `## ` sorig."""
    for title in titles:
        md = re.sub(rf"^## {re.escape(title)}\n.*?(?=^## |\Z)", "", md, flags=re.M | re.S)
    return md


def unwrap_notes_section(md: str) -> str:
    """A `## Jegyzetek` szakaszból csak a `[^…]: …` definíciókat hagyja meg."""
    m = re.search(r"^## Jegyzetek\n(.*?)(?=^## |\Z)", md, re.M | re.S)
    if not m:
        return md
    defs = [line for line in m.group(1).splitlines() if line.startswith("[^")]
    body = "\n\n".join(defs) + "\n\n" if defs else ""
    return md[:m.start()] + body + md[m.end():]


def reflow_copyright(md: str, min_len: int = 50) -> str:
    """A Copyright szakaszban a PDF-ből maradt, mondat közepi kemény sortöréseket
    (hosszú sor + „  \\n”) szóközre cseréli; a rövid címsorok (cím, ISBN) maradnak."""
    m = re.search(r"^## Copyright\n.*?(?=^## |\Z)", md, re.M | re.S)
    if not m:
        return md
    lines = m.group(0).split("\n")
    out = []
    for i, line in enumerate(lines):
        joined = i < len(lines) - 1 and line.endswith("  ") and len(line.rstrip()) >= min_len
        out.append(line.rstrip() + " " if joined else line + "\n")
    sec = "".join(out)[:-1]  # az utolsó sor után nem volt soremelés
    return md[:m.start()] + sec + md[m.end():]


def nbsp_units(md: str) -> str:
    """Kötött szóköz szám és mértékegység közé, valamint sorszám után."""
    def fix(text: str) -> str:
        text = _unit_re.sub(NBSP, text)
        return _ordinal_re.sub(rf"\1.{NBSP}", text)

    return "\n".join(
        line if line.startswith("[^") else _map_unprotected(line, fix)
        for line in md.split("\n")
    )


def soft_hyphenate(md: str, min_len: int = 10) -> str:
    """Lágy elválasztójel a min_len betűnél hosszabb szavakba (pyphen, hu_HU)."""
    import pyphen

    dic = pyphen.Pyphen(lang="hu_HU", left=3, right=3)

    def hyph_word(m: re.Match) -> str:
        w = m.group(0)
        if len(w) <= min_len:
            return w
        # A nem szabványos pontok (pl. alátámasz-sza) betűt is cserélnének: kihagyjuk.
        cuts = [int(p) for p in dic.positions(w) if not getattr(p, "data", None)]
        for c in reversed(cuts):
            w = w[:c] + SHY + w[c:]
        return w

    def fix(text: str) -> str:
        return _word_re.sub(hyph_word, text)

    out, in_copyright = [], False
    for line in md.split("\n"):
        if line.startswith("## "):
            # A Copyright angol nyelvű: magyar elválasztási mintákkal nem bontjuk.
            in_copyright = line.strip() == "## Copyright"
        skip = in_copyright or _is_skipped_line(line)
        out.append(line if skip else _map_unprotected(line, fix))
    return "\n".join(out)


def prepare(md: str, soft_hyphens: bool = True) -> str:
    md = strip_front(md)
    md = remove_sections(md, ["Tartalom", "Index"])
    md = unwrap_notes_section(md)
    md = reflow_copyright(md)
    md = nbsp_units(md)
    if soft_hyphens:
        md = soft_hyphenate(md)
    return md


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--no-soft-hyphens", action="store_true")
    a = ap.parse_args()
    out = prepare(Path(a.src).read_text(encoding="utf-8"), soft_hyphens=not a.no_soft_hyphens)
    dst = Path(a.dst)
    if str(dst) != "/dev/stdout":
        dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
