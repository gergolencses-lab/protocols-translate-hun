# Protokollok – nyomtatható A5 PDF

`book/protocols-hu.md` → `dist/protokollok-A5.pdf` (WeasyPrint). Döntések és QA: `DECISIONS.md`.

## Kell hozzá

- Pandoc ≥ 3.1, Python 3.10+, `pip install weasyprint pyphen pymupdf`
- A betűtípusok a `fonts/` mappában vannak (Source Serif 4 SmText, Source Sans 3 – OFL)

## Parancsok

```bash
python3 tools/pdf/build_pdf.py      # build (kb. 1 perc) → dist/protokollok-A5.pdf
python3 tools/pdf/qa.py --shots     # QA: hézag, betűtípus, túlfutás, számok; mintaoldalak: build/pdf/shots/
python3 -m pytest tests             # szűrők és előkészítő tesztjei (EPUB + PDF)
```

## Nyomtatás

- **A5 lapra:** 100%-os méretben, kétoldalas nyomtatásnál „hosszú él mentén”.
- **A4 lapra, két oldal egy lapon:** a nyomtató „2 oldal/lap” beállításával; a margók így is megmaradnak.
- **Füzet (brossúra):** a nyomtató „füzet” módjával A4-es lapra hajtva A5-ös könyv lesz belőle; a 618 oldal miatt érdemes 4–6 füzetre bontani.
