"""Az A5 PDF ellenőrzése (4-dokumentacio/pdf-dontesek.md, „Ellenőrzés”).

1. Hézag a lap alján (a html-to-pdf skill qa_gaps módszere A5-re skálázva)
2. Betűtípusok: csak a beágyazott Source Serif 4 / Source Sans 3 (nincs tartalék font)
3. Túlfutás: nincs szöveg a margón kívül
4. Számok: protokollok, jegyzetek, tartalomjegyzék-oldalszámok, könyvjelzők
5. Mintaoldalak képe: build/pdf/shots/

Használat: python3 eszkozok/pdf/qa.py [--shots]
"""
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "1-kesz-konyv/protokollok-A5.pdf"
HTML = ROOT / "build/pdf/protokollok.html"
SHOTS = ROOT / "build/pdf/shots"

MM = 72 / 25.4
TOP_MM, BOTTOM_MM = 17, 20
GAP_OK, GAP_WARN = 30, 40          # A5 tartalomterület 173 mm (a skill 45/60 mm-es A4-es küszöbe arányosan)
EDGE_MM = 12                       # a margók legalább 14 mm-esek; 12 mm-en belül szöveg nem lehet
ALLOWED_FONT = re.compile(r"Proto(Serif|Sans)|SourceSerif|SourceSans")


def bottom_gap_mm(page: pymupdf.Page) -> float:
    pix = page.get_pixmap(dpi=60, colorspace=pymupdf.csGRAY)
    h, w = pix.height, pix.width
    px_per_mm = h / (page.rect.height / MM)
    top, bottom = round(TOP_MM * px_per_mm), h - round(BOTTOM_MM * px_per_mm)
    s = pix.samples
    for row in range(bottom - 1, top - 1, -1):
        line = s[row * w:(row + 1) * w]
        if min(line) < 235:
            return round((bottom - 1 - row) / px_per_mm, 1)
    return round((bottom - top) / px_per_mm, 1)


def main() -> int:
    doc = pymupdf.open(PDF)
    fails, warns = [], []
    toc = doc.get_toc()
    starts = {p for _, _, p in toc}          # fejezet- és protokollkezdő oldalak (1-alapú)

    # 1. Hézagok
    print("== Hézagok (✓ <30 mm, ⚠ 30–40, ✗ >40; kényszerített törés előtti és utolsó oldal kivéve)")
    body_first = min(p for lvl, t, p in toc if t == "Jogi nyilatkozat")
    for i in range(body_first - 1, doc.page_count - 1):
        pno = i + 1
        if (pno + 1) in starts:
            continue
        gap = bottom_gap_mm(doc[i])
        if gap > GAP_WARN:
            fails.append(f"{pno}. oldal: {gap} mm hézag")
        elif gap > GAP_OK:
            warns.append(f"{pno}. oldal: {gap} mm hézag")
    print(f"   ✗ {len(fails)} oldal, ⚠ {len(warns)} oldal")
    for x in fails[:15]: print("   ✗", x)
    for x in warns[:15]: print("   ⚠", x)

    # 2. Betűtípusok
    fonts = {f[3] for p in doc for f in p.get_fonts()}
    bad = sorted(f for f in fonts if not ALLOWED_FONT.search(f))
    print("== Betűtípusok:", sorted(fonts))
    if bad: fails.append(f"tartalék betűtípus: {bad}")
    text_all = "".join(p.get_text() for p in doc)
    if "�" in text_all: fails.append("helyettesítő karakter (U+FFFD) a szövegben")

    # 3. Túlfutás
    over = []
    for i, p in enumerate(doc):
        if i == 0: continue  # borító
        W = p.rect.width
        for b in p.get_text("blocks"):
            x0, y0, x1, y1 = b[:4]
            if x0 < EDGE_MM * MM - 0.5 or x1 > W - EDGE_MM * MM + 0.5:
                over.append(f"{i + 1}. oldal: {b[4][:50]!r}")
    print(f"== Túlfutás: {len(over)}")
    for x in over[:10]: print("  ", x)
    if over: fails.append(f"{len(over)} szövegblokk a margóban")

    # 4. Számok
    html = HTML.read_text(encoding="utf-8")
    counts = {
        "protokoll (HTML)": (html.count('class="level2 protocol"'), 47),
        "jegyzethivatkozás": (html.count('class="noteref"'), 1124),
        "jegyzet": (html.count('class="note"'), 1124),
        "könyvjelző: protokoll": (sum(1 for lvl, t, p in toc if lvl == 2), 47),
    }
    for k, (got, want) in counts.items():
        ok = got == want
        print(f"== {k}: {got} (elvárt {want}) {'✓' if ok else '✗'}")
        if not ok: fails.append(f"{k}: {got} ≠ {want}")
    bad_marks = [t for lvl, t, p in toc if re.search(r"\d(fejezet|[a-zá]+protokoll)|protokoll[A-ZÁ-Ű]", t)]
    if bad_marks: fails.append(f"hibás könyvjelző: {bad_marks[:3]}")

    toc_pages = [p for lvl, t, p in toc if t == "Tartalom"][0], body_first - 1
    toc_text = "".join(doc[i].get_text() for i in range(toc_pages[0] - 1, toc_pages[1]))
    toc_items = html.split('<nav class="toc">')[1].split("</nav>")[0].count("<li")
    numbered = len(re.findall(r"\.\s*(\d{1,3})\s*$", toc_text, re.M))
    print(f"== Tartalomjegyzék: {toc_items} tétel, {numbered} oldalszám")
    if numbered < toc_items: fails.append(f"tartalomjegyzék: {toc_items - numbered} tételnél hiányzik az oldalszám")

    print(f"\n{doc.page_count} oldal; {len(fails)} hiba, {len(warns)} figyelmeztetés.")

    if "--shots" in sys.argv:
        SHOTS.mkdir(parents=True, exist_ok=True)
        find = lambda title: next(p for lvl, t, p in toc if t.startswith(title))
        picks = {
            "01-borito": 1, "02-cimoldal": 2, "03-tartalom": find("Tartalom"),
            "04-fejezetnyito": find("1. fejezet"), "05-protokoll": find("1. alvásprotokoll"),
            "06-protokoll-lista": find("1. alvásprotokoll") + 1, "07-doboz": find("4. alvásprotokoll") + 1,
            "08-jegyzetek": find("Jegyzetek") + 1, "09-szerzo": find("A szerzőről"),
            "10-copyright": find("Copyright"), "11-ajanlas": find("Jogi nyilatkozat") + 1,
        }
        for name, pno in picks.items():
            doc[pno - 1].get_pixmap(dpi=110).save(SHOTS / f"{name}-p{pno}.png")
        print("képek:", SHOTS)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
