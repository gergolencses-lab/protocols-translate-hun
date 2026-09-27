# Protokollok – EPUB-build

`book/protocols-hu.md` → `dist/protokollok.epub` (EPUB 3, validált).

## Kell hozzá

- Pandoc ≥ 3.1 (pl. `pip install pypandoc_binary`, a bináris a csomag `files/pandoc` útvonalán van)
- Python 3.10+, `pip install -r requirements-dev.txt` (pytest, pyphen)
- Java 11+ és az [EPUBCheck](https://github.com/w3c/epubcheck/releases) jar
- A borítóhoz és a képernyőképekhez: `pip install playwright` + Chromium (`CHROMIUM=/út/chrome`)

## Parancsok

```bash
python -m pytest tests/epub                                  # szűrők és előkészítő tesztjei
python tools/epub/render_cover.py                            # borító: cover/cover.html → cover/cover.jpg (csak ha változott)
EPUBCHECK_JAR=/út/epubcheck.jar bash tools/epub/build.sh     # build + EPUBCheck + szerkezeti ellenőrzés
python tools/epub/screenshots.py                             # szemrevételező képek: build/epub/shots/
```

`build.sh --no-soft-hyphens` lágy elválasztójelek nélkül buildel.

## Fájlok

- `metadata.yaml`: cím, szerző, nyelv, azonosító, jogi megjegyzés
- `epub.css`: a teljes kinézet (az eredeti e-könyv mintájára)
- `cover/`: a borító HTML-forrása, Montserrat betűtípus (OFL), renderelt JPG
- `DECISIONS.md`: az E1–E12 döntések és a végrehajtás közbeni eltérések
- `tools/epub/`: `prepare.py` (előkészítő), `filters/*.lua` (Pandoc-szűrők), `build.sh`, `verify.py`, `screenshots.py`, `render_cover.py`
