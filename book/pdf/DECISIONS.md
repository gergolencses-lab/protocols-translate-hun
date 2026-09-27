# Protokollok – nyomtatható A5 PDF: tervezési döntések

Forrás: ugyanaz, mint az EPUB-é (`book/protocols-hu.md` → `tools/epub/prepare.py` → Pandoc + a közös Lua-szűrők), a kimenet `dist/protokollok-A5.pdf` (WeasyPrint).
Minta: az eredeti könyv (a repó PDF-je) és az EPUB-döntések (`book/epub/DECISIONS.md`). Tördelési alapelvek: a `html-to-pdf` skill „szokásos tördelési szabályai” (fattyúsor- és árvasor-védelem, a címsor nem marad a lap alján, dobozok egyben), A5-re igazítva.

| ID | Kérdés | Döntés | Indoklás |
|---|---|---|---|
| P1 | Oldalméret, margók | A5 (148×210 mm); fent 17, lent 20, belső 18, külső 14 mm, páros/páratlan oldalon tükrözve | A belső margó a kötésnek vagy lefűzésnek hagy helyet; a különbség kicsi, így egyoldalas otthoni nyomtatásnál sem feltűnő. |
| P2 | Betűk | Törzs: Source Serif 4 SmText 9,6/13,2 pt; címek, címkék: Source Sans 3 (mindkettő OFL, beágyazva) | Az SmText optikai méret kifejezetten 8–11 pontos szövegre készült. Mindkét család tartalmazza a könyv összes karakterét (ő, ű, görög betűk, ⅔). |
| P3 | Szedés | Sorkizárt, első soros behúzás (1,1 em), bekezdésköz nélkül; magyar elválasztás a WeasyPrint beépített `pyphen` szótárával (`lang="hu"`) | Ez helyesírás szerint bontja a hosszú mássalhangzót is (alátámasz-sza), ami lágy elválasztójellel nem lehetséges. Legfeljebb 2 egymást követő elválasztott sor, és legalább 3 betű marad mindkét oldalon. |
| P4 | Sorrend | Borító → címoldal → tartalomjegyzék oldalszámokkal → Jogi nyilatkozat → Ajánlás → Bevezetés → 1–7. fejezet → Mielőtt… → Köszönetnyilvánítás → A szerzőről → Jegyzetek → Copyright | Az eredeti sorrendje. A tárgymutató kimarad (E4): a magyar kiadás oldalszámaihoz nem igazítható. |
| P5 | Oldaltörés | Minden fejezet és minden protokoll új oldalon kezdődik (mint az EPUB-ban és az eredetiben); a fejezet nem feltétlenül páratlan oldalon | Otthoni, egyoldalas nyomtatásnál az üres oldalak csak pazarlást jelentenének. |
| P6 | Élőfej, lapszám | Bal oldalon a könyv címe, jobb oldalon a fejezet címe, kis sans-serif betűvel; lapszám lent kívül. A borítón, a címoldalon és a fejezetnyitó oldalakon nincs élőfej. | Könyvszokás; nyomtatott példányban így könnyű tájékozódni. |
| P7 | Jegyzetek | Az eredeti nyomtatott könyv szerint: a könyv végén, a Jegyzetek fejezetben, fejezetenként csoportosítva, **fejezetenként újrainduló számozással**; a szövegben felső indexes szám, a PDF-ben kattintható oda-vissza | Az 1124 hivatkozás lap alji lábjegyzetként oldalanként 5–10 sort foglalna el. A könyv végén egyben kereshetők, mint az eredetiben. |
| P8 | Keretes dobozok | Halványszürke háttér (6%) és bal oldali vonal, a sans-serif cím a doboz elején. A doboz oldalhatáron átfolyhat, és a kerete az új oldalon is megismétlődik (`box-decoration-break: clone`). | Az 1500 szavas doboz (4. alvásprotokoll) nem férne el egy oldalon; ha egyben kellene tartani, oldalnyi lyukak keletkeznének. |
| P9 | Képek | Borító teljes oldalon; fejezetembléma 30 mm; szerzőfotó 45 mm széles | A képek natív felbontása (embléma 200 px, fotó 196×300 px) így kb. 170 dpi – nyomtatásban elfogadható. |
| P10 | Tartalomjegyzék | Fejezetek és a 47 protokoll, pontozott vezetővonallal és oldalszámmal (CSS `target-counter`) | Mint az eredetiben; nyomtatásban az oldalszám a navigáció. |
| P11 | PDF-könyvjelzők | A fejezetek és protokollok (2 szint) | Képernyőn olvasva ugyanaz a navigáció, mint az EPUB tartalomjegyzéke. |
| P12 | Fordítói megjegyzés | Csak a Copyright fölött (E12) | Az ember döntése. |

## Ellenőrzés (`tools/pdf/qa.py`)

1. **Hézagvizsgálat:** a skill `qa_gaps.py`-jének módszere A5-re skálázva. A tartalomterület 173 mm; a küszöbök ✓ < 30 mm, ⚠ 30–40 mm, ✗ > 40 mm. Nem számít hibának az utolsó oldal, és az az oldal, amely után kényszerített oldaltörés jön (fejezet- vagy protokollvég).
2. **Betűtípusok:** csak a beágyazott Source Serif 4 és Source Sans 3 szerepelhet. Ha tartalék betűtípus (pl. DejaVu) jelenik meg, az hiányzó karaktert jelez.
3. **Túlfutás:** egyetlen szövegblokk sem lóghat ki a lapból (hosszú URL-ek a jegyzetekben).
4. **Számok:**
   - 47 protokoll;
   - 1124 jegyzet;
   - a szövegközi hivatkozások a könyvjelzők szerint;
   - a tartalomjegyzék minden tételénél van oldalszám.
5. **Szemrevételezés:** a fejezetnyitó, a protokollnyitó, a doboz, a Jegyzetek és a Copyright oldal képe.

## Végrehajtás és QA (2026-09-27)

- **Eredmény:** `dist/protokollok-A5.pdf`, 618 oldal, 2,6 MB. `tools/pdf/qa.py`: 0 hiba, 0 figyelmeztetés.
  - hézag: minden oldal 30 mm alatt;
  - csak beágyazott Source Serif 4 és Source Sans 3;
  - 0 túlfutás;
  - 47 protokoll, 1124 hivatkozás és jegyzet (az első buildben 1135: 11 hamis, alsó indexből lett hivatkozás a VO₂/CO₂-ben, lásd `book/epub/DECISIONS.md`, 2. kör);
  - 62 tartalomjegyzék-tétel, mind oldalszámmal.
- **Talált és javított hibák:**
  1. **Tartalék betűtípus (DejaVu).** A `Serif` és a `Sans` családnév ütközött a rendszer álneveivel, ezért egyedi nevekre cseréltük (`ProtoSerif`, `ProtoSans`). A beágyazott listák ◦/▪ jelölője hiányzik a betűtípusokból, ezért `–` és `·` lett helyette.
  2. **Könyvjelzők.** A rejtett elválasztók kiestek („1. fejezetAlvásprotokollok”). A szűrők mostantól `data-title` attribútumban adják át a teljes címet, és `bookmark-label: attr(data-title)` használja.
  3. **Árva alcímek.** A félkövér alcím-bekezdések (25 db, pl. „MIELŐTT KELET FELÉ UTAZOL”) a lap alján maradtak. Az új közös szűrő (`tools/epub/filters/pseudohead.lua`) `div.run-head`-be teszi őket, és ez a következő bekezdéssel együtt marad.
  4. **Forrásjavítás (`book/protocols-hu.md`).** Négy helyen a PDF-sortörés miatt egy félkövér mondat több bekezdésre esett szét (a „képzeletbeli séta” mondata, az „AMIKOR MEGÉRKEZEL…” alcím, a BMR-szorzó sora, az „EREDMÉNY:” sor). Mindegyiket összevontuk.
  5. **QA 1. kör, 122. oldal (45,6 mm-es hézag).** A cím, az alcím és egy négysoros bekezdés lánca a 3/3 soros szabály miatt oszthatatlan lett, és egészben átugrott a következő oldalra. Az alcím és a blokkcím utáni első bekezdés ezért 2/2 sorral is törhet. Utána minden oldal 30 mm alatt maradt.
  6. **Kétszer emelt jegyzetszám.** A `<sup>` és a link is felső indexet kapott. Most csak a `<sup>` emel.
  7. **Élőfej a fejezetnyitón.** A `@page chapter:first` nem működött, helyette `string(…, first-except)` rejti el. A címoldalon sincs lapszám.
- **A skill eltérései:** az `html-to-pdf` skill A4-es szkriptjei (`convert.py`, `qa_gaps.py`) helyett saját A5-ös build (`tools/pdf/build_pdf.py`) és QA (`tools/pdf/qa.py`) készült ugyanazokkal a szabályokkal és módszerrel, arányosan skálázott küszöbökkel.

## Újraépítés a 2. javítási kör után (2026-09-27)

- **Eredmény:** 617 oldal (korábban 618). `tools/pdf/qa.py`: 0 hiba, 0 figyelmeztetés; az elvárt jegyzetszám 1135 → 1124.
- **`notes.lua`, locale-hiba macOS-en:** a Python a gyermekfolyamatoknak `LC_CTYPE=UTF-8`-at ad, ebben a macOS C-könyvtára bájtonként Latin-1-ként kezeli az UTF-8 ékezeteket, így a Lua `lower()` és `%w` elrontotta a számozatlan fejezetek kulcsát (pl. „Bevezetés” → érvénytelen UTF-8 azonosító). A hivatkozások működtek, de a tesztek elbuktak. Javítás: előbb ékezetcsere (kis- és nagybetű), utána csak ASCII kisbetűsítés és `[^a-z0-9]`. Linuxon ugyanazt adja, mint korábban.
- **macOS-függőségek:** `brew install pandoc epubcheck pango`; a WeasyPrinthez `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`, az EPUBCheckhez a Homebrew-s OpenJDK (`PATH=/opt/homebrew/opt/openjdk/bin:$PATH`, `EPUBCHECK_JAR=/opt/homebrew/opt/epubcheck/libexec/epubcheck.jar`).

