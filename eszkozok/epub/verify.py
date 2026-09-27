"""A kész EPUB szerkezeti ellenőrzése (a terv 5. feladatának 3. lépése).

Használat: python3 eszkozok/epub/verify.py [1-kesz-konyv/protokollok.epub]
Kilépési kód 1, ha bármelyik ellenőrzés elbukik.
"""
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPINE_ORDER = [
    "Protokollok", "Tartalom", "Jogi nyilatkozat", "Ajánlás", "Bevezetés",
    "1. fejezet", "2. fejezet", "3. fejezet", "4. fejezet", "5. fejezet", "6. fejezet", "7. fejezet",
    "Mielőtt az utolsó oldalra lapoznál", "Köszönetnyilvánítás", "A szerzőről", "Copyright",
]
MAX_FILE_KB = 300


def text_of(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def main(epub: Path) -> int:
    z = zipfile.ZipFile(epub)
    opf = z.read("EPUB/content.opf").decode()
    items = dict(re.findall(r'<item id="([^"]+)" href="([^"]+)"', opf))
    spine = [items[i] for i in re.findall(r'<itemref idref="([^"]+)"', opf)]
    xhtml = {name: z.read("EPUB/" + name).decode() for name in spine}
    body = "".join(xhtml.values())
    fails = []

    def check(ok: bool, msg: str) -> None:
        print(("OK   " if ok else "HIBA ") + msg)
        if not ok:
            fails.append(msg)

    # Gerinc: a fejezetnyitók sorrendje.
    heads = []
    for name, t in xhtml.items():
        m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
        if m:
            h = text_of(m.group(1))
            if not heads or heads[-1] != h:
                heads.append(h)
    order = [next((s for s in SPINE_ORDER if h.startswith(s)), None) for h in heads]
    order = [o for i, o in enumerate(order) if o and (i == 0 or o != order[i - 1])]
    check(order == SPINE_ORDER, f"gerincsorrend: {order}")
    check(not any(x in heads for x in ("Index", "Jegyzetek")), "nincs Index/Jegyzetek fejezet")

    counts = {
        'class="protocol"': 47, 'class="sidebar"': 10, 'class="dedication"': 1,
        'class="example"': 1, 'class="emblem"': 7, 'class="author-photo"': 1,
    }
    for needle, want in counts.items():
        got = body.count(needle)
        check(got == want, f"{needle}: {got} (elvárt {want})")

    refs = body.count('epub:type="noteref"')
    notes = body.count('epub:type="footnote"')
    check(refs == notes and refs >= 1124, f"lábjegyzet: {refs} hivatkozás, {notes} jegyzet (≥1124, egyenlő)")
    check("<figure" not in body and "figcaption" not in body, "nincs automatikus képaláírás")
    check("-­" not in body and "­-" not in body, "nincs lágy elválasztójel kötőjel mellett")
    check(not re.search(r"\w+@\w*­", body), "nincs lágy elválasztójel e-mail-címben")

    sizes = sorted(((len(t.encode()) // 1024, n) for n, t in xhtml.items()), reverse=True)
    check(sizes[0][0] < MAX_FILE_KB, f"legnagyobb fájl: {sizes[0][1]} {sizes[0][0]} KB (< {MAX_FILE_KB})")

    nav = z.read("EPUB/nav.xhtml").decode()
    toc = nav.split('epub:type="toc"')[1].split("</nav>")[0]
    entries = [text_of(a) for a in re.findall(r"<a[^>]*>(.*?)</a>", toc, re.S)]
    check(len(entries) == 61, f"tartalomjegyzék: {len(entries)} tétel (elvárt 61)")
    proto = [e for e in entries if re.match(r"^\d+\. \S", e) and "fejezet" not in e]
    check(len(proto) == 47 and all(re.match(r"^\d+\. [^:]*protokoll: .+", e) for e in proto),
          "a protokollok a tartalomjegyzékben teljes címmel („N. …protokoll: cím”)")
    check("vegyétek meg az eredeti könyvet" in xhtml[[n for n in spine if "Copyright" in xhtml[n]][-1]],
          "fordítói megjegyzés a Copyright oldalon")

    print(f"\n{len(fails)} hiba.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "1-kesz-konyv/protokollok.epub"))
