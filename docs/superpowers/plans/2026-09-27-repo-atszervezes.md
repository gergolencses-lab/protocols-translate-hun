# A repó átszervezése – terv

> **Végrehajtónak:** feladatonként haladj, minden feladat után futtasd a „Kész, ha” ellenőrzést, és minden feladat külön commit legyen. Fájlt mindig `git mv`-vel mozgass, hogy a története megmaradjon.

**Cél:** aki megnyitja a repót a GitHubon, első ránézésre lássa, hol van a kész könyv, hol a szöveg, és hol minden más. A könyv tartalma és kinézete nem változhat, csak a fájlok helye.

**Alapelv:** a GitHub ábécérendben mutatja a mappákat. A számozott, magyar nevű mappák ezért abban a sorrendben jelennek meg, ahogy egy olvasónak szüksége van rájuk: 1. kész könyv → 2. szöveg → 3. kinézet → 4. dokumentáció. A technikai rész (`eszkozok/`) a lista végére kerül. Minden mappának saját rövid `README.md`-je lesz, ezt a GitHub a mappa megnyitásakor a fájllista alatt mutatja.

---

## Mi a baj most

| Probléma | Hol |
|---|---|
| Nincs kezdőlap (`README.md`): a repó főoldala csak egy mappalista. | gyökér |
| A kész könyv a `dist/` nevű mappában van, és ez fejlesztői szakszó. | `dist/` |
| Az angol eredeti két helyen van: a PDF a gyökérben, a Markdown a `source/en/`-ben. | gyökér, `source/` |
| A `book/` mappában keveredik a magyar szöveg és az EPUB/PDF beállításai. | `book/` |
| A 4 kép kétszer szerepel, egyformán. | `book/images/`, `source/en/images/` |
| A borító az `epub/` alatt van, pedig a PDF is ezt használja. | `book/epub/cover/` |
| A döntések és a tervek három helyen vannak, és angol nevük (`superpowers`, `DECISIONS`) semmit sem mond. | `docs/superpowers/`, `book/epub/`, `book/pdf/` |
| A PDF-építő az `epub/` mappából veszi a közös részeket, így nem látszik, mi közös. | `tools/` |
| Nincs egyetlen parancs, ami mindent újraépít. | – |

## A cél-szerkezet

```
README.md                          ← KEZDŐLAP: letöltés, térkép, „mit hol keress”
1-kesz-konyv/                      ← ezt kell letölteni
  README.md
  protokollok.epub
  protokollok-A5.pdf
  borito.jpg
2-szoveg/                          ← a könyv szövege
  README.md
  magyar/protokollok.md            ← A MAGYAR FORDÍTÁS (itt kell javítani)
  angol/protocols.md
  angol/Protocols - Andrew Huberman.pdf
  kepek/                           ← a 4 kép, egyszer (+ IMAGE-INDEX.md)
3-kinezet/                         ← hogyan néz ki
  README.md
  borito/                          ← cover.html, fonts/, valtozatok/ (a 4 terv)
  epub/                            ← epub.css, metadata.yaml
  pdf/                             ← print.css, fonts/
4-dokumentacio/                    ← miért ilyen
  README.md
  forditas-terv.md, forditas-spec.md
  epub-terv.md, epub-dontesek.md
  pdf-dontesek.md
  repo-atszervezes-terv.md         ← ez a fájl
eszkozok/                          ← építés és ellenőrzés (nem kell megnyitni)
  README.md
  mindent-epit.sh                  ← EGY parancs: borító → EPUB → PDF → minden ellenőrzés
  kozos/                           ← prepare.py + a közös Lua-szűrők
  epub/                            ← build.sh, verify.py, screenshots.py
  pdf/                             ← build_pdf.py, qa.py, szurok/notes.lua
  borito/render_cover.py
  tesztek/                         ← a mostani tests/
  requirements-dev.txt
.gitignore
```

A `build/` (köztes fájlok) továbbra is csak helyben létezik, a GitHubon nem látszik.

## Döntések, amelyeket jóvá kell hagyni

| # | Kérdés | Javaslat |
|---|---|---|
| D1 | Magyar, számozott mappanevek, vagy a szokásos angol (`dist/`, `src/`, `docs/`)? | **Magyar, számozott.** Nem fejlesztőnek készül, és a számozás a sorrendet is megadja. |
| D2 | A 4 borítóterv maradjon meg? | **Igen**, a `3-kinezet/borito/valtozatok/` mappában. Kicsik, és később jól jöhetnek. |
| D3 | Az angol PDF (12 MB) maradjon a repóban? | **Igen**, a `2-szoveg/angol/` mappában. Ez az összevetés alapja. |
| D4 | A régi letöltési linkek (`…/raw/main/dist/…`) meg fognak szakadni. Baj ez? | Az új linkek a kezdőlapon lesznek. Ha a régiek máshol el vannak mentve, azokat cserélni kell. |

---

## 1. feladat: Kiindulási állapot rögzítése

- Futtasd le a teljes buildet a mostani szerkezetben, és mentsd el az összehasonlítás alapját a `build/alap/` mappába:
  - az EPUB összes `.xhtml` fájlját kicsomagolva;
  - a PDF oldalankénti szövegét (PyMuPDF), és az oldalszámot.
- **Kész, ha:** EPUBCheck 0/0, `verify.py` 0 hiba, `qa.py` 0 hiba, `pytest` zöld (22).

## 2. feladat: Kezdőlap és mappa-README-k (még mozgatás nélkül)

- A gyökér `README.md` tartalma:
  1. egy mondat arról, mi ez;
  2. **letöltés**: két nagy link (EPUB, PDF), és egy mondat arról, melyiket mire;
  3. a fordítói megjegyzés;
  4. térkép: a fenti fa, soronként egy mondattal;
  5. „Mit hol keress” táblázat: *hibát találtam a szövegben* → `2-szoveg/magyar/protokollok.md`; *a borítón változtatnék* → `3-kinezet/borito/`; *miért így döntöttünk* → `4-dokumentacio/`; *újraépítés* → `eszkozok/README.md`.
- Ez a feladat csak új fájlokat hoz létre, önmagában is hasznos, és a többi feladat előtt beolvasztható.
- **Kész, ha:** a GitHubon a README linkjei működnek (a mozgatás után a 8. feladat frissíti őket).

## 3. feladat: Kész könyv → `1-kesz-konyv/`

- `git mv dist/protokollok.epub dist/protokollok-A5.pdf 1-kesz-konyv/`
- A `borito.jpg` a `3-kinezet/borito/cover.jpg` másolata lesz, és a `render_cover.py` mindkét helyre írja.
- `.gitignore`: a `dist/` sor törlése; az `1-kesz-konyv/` ne legyen kizárva, így nem kell `git add -f`.
- A `dist/` minden előfordulását ki kell cserélni: `build.sh`, `build_pdf.py`, `qa.py`, `verify.py`, `screenshots.py`, README-k.

## 4. feladat: Szöveg → `2-szoveg/`

- `book/protocols-hu.md` → `2-szoveg/magyar/protokollok.md`
- `source/en/protocols.md` → `2-szoveg/angol/protocols.md`
- `Protocols - Andrew Huberman.pdf` → `2-szoveg/angol/`
- `source/en/images/*` → `2-szoveg/kepek/`; a `book/images/` törlése (md5-tel ellenőrzötten azonos a kettő).
- Mindkét Markdownban a kép-útvonalak `images/…` helyett `../kepek/…` legyenek. Így a GitHub előnézete is mutatja a képeket.
- A Pandoc `--resource-path` a `2-szoveg/magyar` legyen; a `build_pdf.py` `base_url`-je ennek megfelelően.

## 5. feladat: Kinézet → `3-kinezet/`

- `book/epub/cover/` → `3-kinezet/borito/`, benne `variants/` → `valtozatok/`. A `_base.css` a `../fonts/` útvonalat használja, ez a mappa átnevezése után is jó marad.
- `book/epub/epub.css`, `metadata.yaml` → `3-kinezet/epub/`. A `metadata.yaml`-ban a `cover-image` és a `css` útvonalát frissíteni kell.
- `book/pdf/print.css`, `fonts/` → `3-kinezet/pdf/`; a `print.css` `url(…)` hivatkozásait ellenőrizni kell.
- A `build_pdf.py` HTML-jében a borító és a CSS útvonala.

## 6. feladat: Dokumentáció → `4-dokumentacio/`

- `docs/superpowers/specs/…translation-design.md` → `forditas-spec.md`
- `docs/superpowers/plans/…translation.md` → `forditas-terv.md`
- `docs/superpowers/plans/…epub.md` → `epub-terv.md`
- `book/epub/DECISIONS.md` → `epub-dontesek.md`
- `book/pdf/DECISIONS.md` → `pdf-dontesek.md`
- ez a terv → `repo-atszervezes-terv.md`
- A `book/epub/README.md` és a `book/pdf/README.md` tartalma az `eszkozok/README.md`-be olvad.
- A dokumentumokon belüli útvonal-hivatkozásokat frissíteni kell. A régi útvonalak csak a „mit csináltunk akkor” típusú történeti részekben maradhatnak.

## 7. feladat: Eszközök → `eszkozok/`

- `tools/epub/prepare.py` és `tools/epub/filters/*.lua` → `eszkozok/kozos/` (és `kozos/szurok/`). Ezeket mindkét kimenet használja.
- `tools/epub/{build.sh,verify.py,screenshots.py}` → `eszkozok/epub/`
- `tools/pdf/{build_pdf.py,qa.py}` → `eszkozok/pdf/`; `tools/pdf/filters/notes.lua` → `eszkozok/pdf/szurok/`. A `package.path` a `../../kozos/szurok/` útvonalra mutasson.
- `tools/epub/render_cover.py` → `eszkozok/borito/`
- `tests/` → `eszkozok/tesztek/` (a `conftest.py` útvonalai); `requirements-dev.txt` → `eszkozok/`
- Új: `eszkozok/mindent-epit.sh`. Sorrend: borító → EPUB + EPUBCheck + `verify` → PDF + `qa` → `pytest`. Az első hibánál álljon meg.

## 8. feladat: Takarítás és ellenőrzés

- Maradék régi útvonalak keresése: `grep -rn "book/\|source/\|dist/\|tools/\|docs/superpowers\|tests/"`. Találat csak a dokumentumok történeti részeiben lehet.
- A régi mappák (`book/`, `source/`, `dist/`, `docs/`, `tools/`, `tests/`) megszűntek.
- `bash eszkozok/mindent-epit.sh`: minden zöld.
- **Összevetés az 1. feladattal:**
  - az EPUB `.xhtml` fájljai bájtra azonosak (a módosítás dátumát kivéve);
  - a PDF oldalszáma és oldalankénti szövege azonos;
  - a borítókép md5-je változatlan.
- A GitHubon: a kezdőlap linkjei, a letöltési linkek és a Markdown-előnézet képei működnek.

## Kockázatok

- **Megszakadt letöltési linkek (D4):** a kezdőlapon az újak lesznek.
- **Rejtett útvonal-hivatkozás:** a 8. feladat `grep`-je és a bájtszintű összevetés kiszűri.
- **Ékezet a mappanevekben:** szándékosan nincs (`kesz-konyv`, `kinezet`, `eszkozok`), mert macOS-en és a URL-ekben is gondot okozhatna.
