# Építés és ellenőrzés

Ezek a szkriptek a [`2-szoveg/magyar/protokollok.md`](../2-szoveg/magyar/protokollok.md) szövegéből és a [`3-kinezet/`](../3-kinezet/) stílusaiból építik fel a [`1-kesz-konyv/`](../1-kesz-konyv/) fájljait, majd ellenőrzik őket.

## Egy parancs mindenre

```bash
EPUBCHECK_JAR=/út/epubcheck.jar bash eszkozok/mindent-epit.sh
```

Sorrend: borító → EPUB (+ EPUBCheck és szerkezeti ellenőrzés) → PDF (+ tördelési ellenőrzés) → tesztek. Az első hibánál megáll. Ha a borító nem változott, a `--borito-nelkul` kapcsolóval ez a lépés kihagyható (ehhez nem kell Chromium).

## Kell hozzá

- Pandoc ≥ 3.1 (pl. `pip install pypandoc_binary`)
- Python 3.10+, `pip install -r eszkozok/requirements-dev.txt` (pytest, pyphen, weasyprint, pymupdf)
- Java 11+ és az [EPUBCheck](https://github.com/w3c/epubcheck/releases) jar
- A borítóhoz és a képernyőképekhez: `pip install playwright` + Chromium (`CHROMIUM=/út/chrome`)

## Mi hol van

| Mappa | Mi van benne |
|---|---|
| `kozos/` | Mindkét kimenet közös része: `prepare.py` (a szöveg előkészítése: kötött szóközök, elválasztás, jegyzetek) és a `szurok/` Pandoc-szűrői (fejezetnyitó, protokollcím, keretes dobozok, alcímek). |
| `epub/` | `build.sh` (EPUB + EPUBCheck), `verify.py` (16 szerkezeti ellenőrzés), `screenshots.py` (mintaoldalak e-könyv-olvasó méretben). |
| `pdf/` | `build_pdf.py` (A5 PDF, WeasyPrint), `qa.py` (hézag, betűtípus, túlfutás, számok; `--shots`: mintaoldalak), `szurok/notes.lua` (a jegyzetek fejezetenkénti számozása). |
| `borito/` | `render_cover.py`: a `3-kinezet/borito/cover.html`-ből képet készít (`cover.jpg`, és egy másolatot a `1-kesz-konyv/borito.jpg` helyre). |
| `tesztek/` | A szűrők és az előkészítő tesztjei: `python3 -m pytest eszkozok/tesztek`. |

A köztes fájlok a `build/` mappába kerülnek. Ez csak helyben létezik, a GitHubra nem kerül fel.
