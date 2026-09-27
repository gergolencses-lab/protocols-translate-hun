# Tervek és döntések

Időrendben:

| Fájl | Mi ez |
|---|---|
| [`forditas-spec.md`](forditas-spec.md) | A fordítás specifikációja: stílus, szójegyzék, minőségi elvárások. |
| [`forditas-terv.md`](forditas-terv.md) | A fordítás lépésenkénti terve (a Codexnek készült). |
| [`epub-terv.md`](epub-terv.md) | Az EPUB elkészítésének terve. |
| [`epub-dontesek.md`](epub-dontesek.md) | Az EPUB döntései (E1–E12: borító, fejezetek, jegyzetek, képek…) és az átolvasás utáni javítások. |
| [`pdf-dontesek.md`](pdf-dontesek.md) | A nyomtatható PDF döntései (P1–P12: méret, betűk, tördelés…) és az ellenőrzés eredménye. |
| [`repo-atszervezes-terv.md`](repo-atszervezes-terv.md) | A repó mostani mappaszerkezetének terve. |

## Régi útvonalak

A dokumentumok az átszervezés előtt készültek, ezért a régi útvonalakat említik. Ezek így felelnek meg az újaknak:

| Régi | Új |
|---|---|
| `dist/` | `1-kesz-konyv/` |
| `book/protocols-hu.md` | `2-szoveg/magyar/protokollok.md` |
| `source/en/protocols.md`, `Protocols - Andrew Huberman.pdf` | `2-szoveg/angol/` |
| `book/images/`, `source/en/images/` | `2-szoveg/kepek/` |
| `book/epub/cover/` | `3-kinezet/borito/` |
| `book/epub/epub.css`, `metadata.yaml` | `3-kinezet/epub/` |
| `book/pdf/print.css`, `fonts/` | `3-kinezet/pdf/` |
| `book/epub/DECISIONS.md`, `book/pdf/DECISIONS.md` | `4-dokumentacio/epub-dontesek.md`, `pdf-dontesek.md` |
| `docs/superpowers/…` | `4-dokumentacio/` |
| `tools/epub/prepare.py`, `tools/epub/filters/` | `eszkozok/kozos/`, `eszkozok/kozos/szurok/` |
| `tools/epub/`, `tools/pdf/` | `eszkozok/epub/`, `eszkozok/pdf/` |
| `tests/` | `eszkozok/tesztek/` |
