# Protokollok – EPUB-előállítás: megvalósítási terv

> **Megjegyzés (2026-09-27):** a repó azóta átszerveződött. A régi útvonalak új helyét a [`README.md`](README.md) „Régi útvonalak” táblázata mutatja.

> **Állapot (2026-09-27):** az 1–6. feladat 1–2. lépése végrehajtva (Claude). A tervtől való eltérések a `book/epub/DECISIONS.md` „Végrehajtás közbeni döntések” szakaszában vannak. Hátravan: a 6. feladat 3. lépése (tesztelés az ember eszközén) és az opcionális 7. feladat.
>
> **Végrehajtónak (Codex vagy Claude):** feladatról feladatra haladj, a sorrendet tartva. A lépések jelölőnégyzetesek (`- [x]`); a kész lépést pipáld ki, és commitolj. A **🛑 KAPU** jelzésű lépésnél állj meg, és várd meg az ember válaszát. A 0. feladat döntéseit az ember hagyja jóvá; amíg ez nem történt meg, a javasolt alapértelmezéssel dolgozz.

**Cél:** A kész magyar fordításból (`book/protocols-hu.md`) igényes, validált EPUB 3 készüljön (`dist/protokollok.epub`). Kinézetben kövesse az eredeti Simon & Schuster e-könyvet, a magyar tipográfia szabályai szerint, és működjön Kindle-ön, Kobón, PocketBookon és Apple Booksban.

**Architektúra:** A forrás-Markdownt kézzel nem szerkesztjük a konverzió kedvéért. Egy Python-előkészítő (`tools/epub/prepare.py`) készít belőle egy EPUB-ra szánt köztes Markdownt: kivágja, ami nem kell, kötött szóközöket és lágy elválasztójeleket szúr be. A Pandoc ebből EPUB 3-at gyárt, három Lua-szűrővel:
- fejezetnyitók,
- protokollcímek,
- keretes dobozok.

A kinézetet egyetlen CSS adja. A végén EPUBCheck validál, és képernyőképes szemrevételezés következik.

**Technológia:** Pandoc ≥ 3.1 (Lua-szűrők), Python 3.10+ (stdlib + `pyphen`), EPUBCheck 5.x (Java), Playwright/Chromium a szemrevételező képekhez.

**Előzmény:** a fordítási specifikáció ([`forditas-spec.md`](forditas-spec.md)) §6 (tipográfia) és §7 (D1–D8) döntései érvényesek; ez a terv ezekre épít.

---

## Mit mutat az eredeti e-könyv (a PDF alapján)

A repóban lévő PDF az eredeti Simon & Schuster e-könyvből készült export (2. oldal: „Thank you for downloading this Simon & Schuster ebook”), vagyis az eredeti EPUB kinézetét mutatja. Ezt vesszük mintának.

| Elem | Az eredetiben (PDF-oldal) | A magyar Markdownban |
|---|---|---|
| Fejezetnyitó | külön oldal: „CHAPTER 1” címke → embléma (PROTOCOLS logó) → „*for* SLEEP” (24.) | `## 1. fejezet: Alvásprotokollok` + `![…](images/chapter-emblem.jpeg)` |
| Protokollnyitó | új oldal; kis félkövér „SLEEP PROTOCOL” címke, szám szürke körben, nagy sans-serif cím (30., 59.) | `### 1. alvásprotokoll: Nézz napfényt…` |
| Blokkcímek | „WHAT TO DO:”, „HOW IT WORKS:” – kis, csupa nagybetűs sans-serif (30–31.) | `#### Mit tegyél?` (46×), `#### Hogyan működik?` (46×), `#### Gyakori kérdések` (29×) |
| Keretes dobozok | szürke hátterű doboz, sans-serif félkövér cím, 6 hosszabb + néhány rövid (59–64., 161–162., 172–173., 295–296., 391–392., 438–439.) | megvannak idézetblokként: `> **cím**` – 10 db, az angollal egyezően |
| Felsorolás | a tételek eleje félkövér sans-serif (30.) | `- **Kezdő mondat.** szöveg` |
| Törzsszöveg | serif, sorkizárt, első soros behúzás, bekezdésköz nélkül; címsor utáni első bekezdés behúzás nélkül (6.) | – |
| Ajánlás | külön oldal, rövid, kis betűs (5.) | idézetblokk, dőlt |
| A szerzőről | cím → fotó középen, kb. a szélesség 40%-a → szöveg (516.) | `![Andrew D. Huberman](images/andrew-huberman.jpeg)` |
| Jegyzetek | a könyv végén, fejezetenként csoportosítva, **fejezetenként újrainduló számozással**, oda-vissza linkkel (520.) | `[^c1-12]` hivatkozás; mind az 1124 definíció a `## Jegyzetek` fejezetben |
| Tárgymutató | a nyomtatott kiadás oldalszámaira mutat | angolul maradt (`## Index`) |

### Hibák a magyar Markdownban, amelyeket a konverzió előtt javítani kell (1. feladat)

1. **Eltérő fejezetcím.** A törzsszövegben „3. fejezet: Protokollok a stressz szabályozásához”, a Jegyzetekben „3. fejezet: Stresszkezelési protokollok”.
2. **Eltérő alternatív szövegek az emblémánál:** „Fejezetembléma”, „Fejezet emblémája”, „Fejezetjelvény” → legyen mind „Fejezetembléma”.
3. **Tipográfia.** 9 szóközös kötőjel (` - ` a ` – ` helyett) és 4 angol ezres tagolás (`1,000`) a törzsszövegben.
4. **Hiányzik a D8/E12 szerinti magyar megjegyzés.** Két helyre kell: (a) a Copyright fölé, (b) a „Jogi nyilatkozat” elé egy új, rövid `## Megjegyzés a fordításhoz` szakaszba. A szöveg: „Nem hivatalos, személyes használatra készült fordítás. Használjátok egészséggel, de vegyétek meg az eredeti könyvet mindenképp!”

---

## 0. feladat – Döntések ✔ (az ember 2026-09-27-én jóváhagyta)

**Minden javaslat elfogadva.** Az E12-höz az ember kiegészítése: fordító neve nem szerepel; helyette a könyvben és a metaadatban ez a megjegyzés áll:

> Nem hivatalos, személyes használatra készült fordítás. Használjátok egészséggel, de vegyétek meg az eredeti könyvet mindenképp!

| ID | Kérdés | Javaslat | Indoklás / alternatíva |
|---|---|---|---|
| **E1** | Borító | **Új magyar tipográfiai borító**, 1600×2560 px, a címoldal stílusában (PROTOKOLLOK szórács szürke körrel, alcím, szerző), HTML/CSS-ből Chromiummal renderelve | Az eredeti borító angol és kicsi (600×943 px): a mai olvasókon (1264×1680 és nagyobb) elmosódik. Alternatíva: az angol borító változatlanul. |
| **E2** | Fejezetembléma (angol „PROTOCOLS” logó) | **Marad** az eredeti, díszként | A magyar fejezetcím szövegként alatta áll („1. FEJEZET” → embléma → „Alvásprotokollok”). Alternatíva: magyar PROTOKOLLOK embléma, az E1 borítóval azonos eszközzel. |
| **E3** | Jegyzetek | **A Pandoc saját lábjegyzetei**: felugró ablakban nyílnak (`epub:type="noteref"` / `footnote`), a fejezet végén gyűjtve, oda-vissza linkkel. A számozás könyvszinten folyamatos (1–1124). | Megbízhatóan működik minden olvasón. Alternatíva: az eredeti szerinti, fejezetenként újrainduló számozás és könyv végi Jegyzetek fejezet. Ehhez utólag bele kell nyúlni az EPUB-ba (azonosítók átírása fájlok között), több a hibalehetőség. |
| **E4** | Tárgymutató | **Kimarad** (a D6 szerint) | A nyomtatott kiadás oldalszámaira mutat, és angol. |
| **E5** | Tartalomjegyzék | A könyv saját „Tartalom” fejezete **helyett** a Pandoc generálja, 2 szint mélységben: fejezetek + protokollok és alfejezetek | A Markdown horgonyai GitHub-stílusúak, a Pandoc másképp képzi az azonosítókat, így a régi linkek eltörnének. A generált tartalomjegyzék az olvasó menüjében is megjelenik. |
| **E6** | Keretes dobozok | **Visszaállítjuk**: halványszürke háttér, finom bal szegély, sans-serif cím | Az eredetiben így néznek ki. Az idézetblokkok már jelölik őket, egy Lua-szűrő elég. |
| **E7** | Protokollcímek | **Az eredeti szerint**: kis félkövér címke („ALVÁSPROTOKOLL”), szám körben, alatta nagy cím; új oldalon kezdődik | Ez a könyv legjellegzetesebb tipográfiai eleme. Feltétel: az olvasó tartalomjegyzékében a cím teljes marad („1. alvásprotokoll: …”), lásd a 3. feladatot. |
| **E8** | Szótagolás | **Lágy elválasztójel** (U+00AD) a 10 betűnél hosszabb szavakba a `pyphen` `hu_HU` szótárával, szélenként legalább 3 betűt hagyva, kötőjel mellé nem téve. Mellette `lang="hu"` és CSS `hyphens: auto`. | A szövegben 2055 különböző, legalább 15 betűs szó van (pl. „testmaghőmérsékletedet”). Sorkizárt szövegben, keskeny kijelzőn elválasztás nélkül nagy lyukak lesznek, a magyar automatikus elválasztást pedig nem minden olvasó tudja. Kikapcsolható kapcsoló (`--no-soft-hyphens`). |
| **E9** | Kötött szóköz | **Igen**: szám és mértékegység között (289 hely, pl. `10 mg`, `18 °C`, `90%` előtt), valamint sorszám után kisbetűs szó előtt (`1. alvásprotokoll`) | Ne törjön a sor „10” és „mg” közé. |
| **E10** | Betűtípus | **Nem ágyazunk be**; általános `serif` a szöveghez, `sans-serif` a címekhez | Az olvasó a saját betűtípusát választhatja. A beépített betűtípusok (Bookerly, Kobo-fontok, Literata) tudják az ő/ű betűt. Alternatíva: Literata beágyazása (+~1 MB). |
| **E11** | Bekezdés | **Sorkizárt, első soros behúzás, bekezdésköz nélkül** (mint az eredetiben) | Alternatíva: balra zárt + bekezdésköz. |
| **E12** | Metaadat | Cím: *Protokollok*; alcím: *Használati útmutató az emberi testhez*; szerző: Andrew D. Huberman; közreműködő: Jessica Wapner; nyelv: `hu`; azonosító: egyszer generált `urn:uuid` (nem az angol ISBN); **fordító: nincs megnevezve**; `rights` és `description`: a fenti megjegyzés | **Elfogadva.** A megjegyzés két helyen jelenik meg: a címoldal utáni rövid oldalon és a Copyright fölött. |

- [x] **1. lépés:** A döntések a `book/epub/DECISIONS.md` fájlban vannak, kitöltve. Ha a végrehajtás közben egy döntés módosul (pl. az E7 tartalomjegyzék-kérdése, 3. feladat), azt ott kell rögzíteni.

---

## Globális megkötések

- A `book/protocols-hu.md` a fordítás forrása. A konverzió miatt csak az 1. feladat hibajavításai érintik; minden más átalakítás a `build/` köztes fájljában történik.
- A `dist/` és a `build/` legyen a `.gitignore`-ban. A kész `.epub`-ot csak az ember kérésére commitoljuk.
- Pandoc beállítás: `-f markdown-smart`. A forrásban már tipográfiai idézőjelek és gondolatjelek vannak; a `smart` kiterjesztés elrontaná őket.
- Képméret CSS-ben relatív (%), a kép sosem nagyítható a natív méreténél nagyobbra: embléma 200 px, szerzőfotó 196×300 px.
- CSS-ben nincs rögzített betűszín és px-es betűméret (éjszakai mód, felhasználói betűméret). Háttérszín csak áttetszően: `rgba(0,0,0,.06)`.
- Minden szűrő és szkript tesztelt. Az EPUBCheck eredménye: 0 hiba, 0 figyelmeztetés.

## Fájlszerkezet

```
book/protocols-hu.md               # magyar forrás (az 1. feladat javításaival)
book/images/                       # meglévő képek (cover, chapter-emblem, andrew-huberman, title-page)
book/epub/DECISIONS.md             # E1–E12
book/epub/metadata.yaml            # EPUB-metaadat
book/epub/epub.css                 # a teljes kinézet
book/epub/cover/cover.html         # E1: a borító forrása
book/epub/cover/cover.jpg          # E1: renderelt borító, 1600×2560
tools/epub/prepare.py              # forrás → build/epub/protokollok.md
tools/epub/filters/chapter.lua     # fejezetnyitó + epub:type
tools/epub/filters/protocol.lua    # protokollcím
tools/epub/filters/sidebar.lua     # keretes dobozok, ajánlás, példa
tools/epub/build.sh                # teljes build + EPUBCheck
tools/epub/screenshots.py          # szemrevételező képek
tests/epub/test_prepare.py, tests/epub/test_filters.py, tests/epub/fixture.md
dist/protokollok.epub              # kimenet (gitignore)
```

---

### 1. feladat: Forrás a repóba + tartalmi javítások

**Fájlok:** Módosítandó: `book/protocols-hu.md`, `.gitignore`.

- [x] **1. lépés:** A magyar fordítás a `book/protocols-hu.md` fájlban van (a tervvel együtt került a repóba, változatlanul). Egészítsd ki a `.gitignore`-t: `build/`, `dist/`.
- [x] **2. lépés:** Javítsd a „Hibák a magyar Markdownban” szakasz 1–4. pontját. A 3. ponthoz futtasd: `grep -nE '[^ ] - [^ ]|[0-9]{1,3},[0-9]{3}' book/protocols-hu.md | grep -v '^\s*-'` (csak a Jegyzetek előtti találatok számítanak; a hivatkozások angolok, azokhoz nem nyúlunk).
- [x] **3. lépés:** Ellenőrzés:
  - `grep -c '!\[Fejezetembléma\]' book/protocols-hu.md` → `7`
  - `grep -c 'vegyétek meg az eredeti könyvet mindenképp' book/protocols-hu.md` → `2`
  - `grep -n '^#\{2,3\} 3\. fejezet' book/protocols-hu.md` → két azonos cím
- [x] **4. lépés:** Commit: `book: magyar forrás + konverzió előtti javítások`.

### 2. feladat: Előkészítő szkript (`prepare.py`)

**Fájlok:** Létrehozandó: `tools/epub/prepare.py`, `tests/epub/test_prepare.py`, `requirements-dev.txt` (+`pyphen`).

**Interfészek (mind `str -> str`, tisztán szöveg):**
- `strip_front(md)`: az első `## ` címsor előtti részt törli (borítókép-sor, `# Protokollok` címblokk). Ezeket a metaadat adja.
- `remove_sections(md, titles: list[str])`: törli a `## <cím>` szakaszokat a következő `## ` sorig. Alkalmazás: `["Tartalom", "Index"]` (E4, E5).
- `unwrap_notes_section(md)`: a `## Jegyzetek` szakaszból megtartja a `[^…]: …` definíciókat, a címsort, a bevezető bekezdést és a `### ` alcímeket törli (E3). A Pandoc a definíciókat a hivatkozás helyén használja, a jegyzetek a fejezetek végére kerülnek.
- `nbsp_units(md)`: E9. Csak a definíciós (`[^`) sorokon kívül, és linkcélon (`](…)`) kívül.
  - `(\d)[ ](mg|g|kg|mcg|µg|ml|l|dl|cm|m|km|°C|%|perc|óra|nap|hét|lux|nm|NE|IU|kcal)\b` → U+00A0
  - `\b(\d{1,3})\. (?=[a-záéíóöőúüű])` → U+00A0
- `soft_hyphenate(md, min_len=10)`: E8.
  - `pyphen.Pyphen(lang="hu_HU", left=3, right=3)`, a szavakba U+00AD kerül.
  - Kötőjeles összetételnél darabonként, a kötőjel mellé nem kerül jel.
  - Kihagyandó: címsorsorok, definíciós sorok, linkcélok, `<…>` URL-ek, `images/…` útvonalak, `{…}` attribútumok.
- `main(src, dst, soft_hyphens=True)` + CLI: `python tools/epub/prepare.py book/protocols-hu.md build/epub/protokollok.md [--no-soft-hyphens]`

- [x] **1. lépés: Írd meg a bukó teszteket** (`tests/epub/test_prepare.py`), legalább ezekkel az állításokkal:

```python
NB, SHY = " ", "­"

def test_strip_front():
    md = "![b](images/cover.jpeg)\n\n# Protokollok\n\n*al*\n\n## Jogi nyilatkozat\nX\n"
    assert strip_front(md) == "## Jogi nyilatkozat\nX\n"

def test_remove_sections():
    md = "## A\na\n## Tartalom\n- [x](#x)\n## B\nb\n## Index\n- i\n"
    assert remove_sections(md, ["Tartalom", "Index"]) == "## A\na\n## B\nb\n"

def test_unwrap_notes_keeps_definitions_only():
    md = "## Z\nz[^c1-1]\n## Jegyzetek\n\nBevezető.\n\n### 1. fejezet: X\n\n[^c1-1]: Ref.\n"
    out = unwrap_notes_section(md)
    assert "[^c1-1]: Ref." in out and "Jegyzetek" not in out and "Bevezető" not in out and "### 1. fejezet" not in out

def test_nbsp_units():
    assert nbsp_units("Vegyél be 10 mg-ot, 18 °C, 1. alvásprotokoll.") == \
        f"Vegyél be 10{NB}mg-ot, 18{NB}°C, 1.{NB}alvásprotokoll."
    assert nbsp_units("[^c1-1]: Vol. 10 m 5 g") == "[^c1-1]: Vol. 10 m 5 g"

def test_soft_hyphenate_roundtrip_and_skips():
    src = "A testmaghőmérsékletedet csökkentsd. Az étrend-kiegészítőket is.\n### Hosszúhosszúcímsorszó\n[x](https://example.com/nagyonhosszuutvonal)\n"
    out = soft_hyphenate(src)
    assert out.replace(SHY, "") == src
    assert SHY in out.split("\n")[0]
    assert "-" + SHY not in out and SHY + "-" not in out
    assert SHY not in out.split("\n")[1] and SHY not in out.split("\n")[2]
```

- [x] **2. lépés:** `python -m pytest tests/epub/test_prepare.py -v` → FAIL (a modul még nem létezik).
- [x] **3. lépés:** Valósítsd meg a függvényeket az interfész szerint.
- [x] **4. lépés:** `python -m pytest tests/epub -v` → minden átmegy. Utána a valódi forráson: `python tools/epub/prepare.py book/protocols-hu.md build/epub/protokollok.md`, majd ellenőrzés:
  - `grep -c '^\[\^' build/epub/protokollok.md` → `1124`
  - `grep -c '^## \(Tartalom\|Index\|Jegyzetek\)$' build/epub/protokollok.md` → `0`
  - `sed 's/\xc2\xad//g' build/epub/protokollok.md | cmp - <(python tools/epub/prepare.py book/protocols-hu.md /dev/stdout --no-soft-hyphens)` → nincs kimenet
- [x] **5. lépés:** Commit: `tools(epub): előkészítő szkript`.

### 3. feladat: Lua-szűrők

**Fájlok:** Létrehozandó: `tools/epub/filters/{chapter,protocol,sidebar}.lua`, `tests/epub/fixture.md`, `tests/epub/test_filters.py`.

A szűrők a `--shift-heading-level-by=-1` utáni szinteken dolgoznak: fejezet = 1. szint, protokoll = 2. szint, blokkcím = 3. szint.

- **`chapter.lua`**
  - Az `^(%d+)%. fejezet: (.+)$` mintájú 1. szintű címsor `chapter-opener` osztályt és `epub:type=chapter` attribútumot kap. A tartalma: `Span.chapter-label("1. FEJEZET")`, `LineBreak`, `Span.chapter-title("Alvásprotokollok")`.
  - Ha a címsort közvetlenül egy csak emblémát tartalmazó bekezdés követi, az `emblem` osztályt kap.
  - További `epub:type` attribútumok: „Ajánlás” → `dedication`, „Bevezetés” → `introduction`, „Köszönetnyilvánítás” → `acknowledgments`, „Copyright” → `copyright-page`.
- **`protocol.lua`:** a `^(%d+)%. (%S*protokoll): (.+)$` mintájú 2. szintű címsor (a magyar címkék, pl. `alvásprotokoll`, `edzésprotokoll`, `tanulási protokoll`: futtasd előbb a `grep -oE '^### [0-9]+\. [^:]+' book/protocols-hu.md | sort | uniq -c` parancsot, és a mintát igazítsd a tényleges címkékhez) `protocol` osztályt kap. A tartalma: `Span.protocol-label("ALVÁSPROTOKOLL")`, `Span.protocol-num("1")`, `LineBreak`, `Span.protocol-title(…)`.
  - **A tartalomjegyzék szövege:** a Pandoc a navigációhoz a címsor szövegét használja. Ellenőrizd, hogy a `nav.xhtml`-ben a bejegyzés „ALVÁSPROTOKOLL 1 Nézz napfényt…” vagy ehhez hasonló formában jelenik-e meg. Ha igen, a címsor kapjon `toc-text` / `nav-title` jellegű attribútumot, ha a Pandoc-verzió támogatja. Ha nem támogatja, a szűrő csak osztályt adjon, és a címke–szám–cím tagolást a CSS `::before` nélkül, a címsor szövegének változatlanul hagyásával oldjuk meg (egyszerűsített E7). A döntést és az okát írd a `book/epub/DECISIONS.md`-be.
  - Az `#### Mit tegyél?`, `#### Hogyan működik?` és `#### Gyakori kérdések` címsorok (3. szinten) `block-label` osztályt kapnak.
- **`sidebar.lua`:** idézetblokkok.
  - Ha az első blokk egyetlen `Strong`-ból álló bekezdés: `Div.sidebar`, a cím bekezdése `sidebar-title` osztályt kap.
  - Ha az első elem `Emph` és az „Ajánlás” szakaszban van: `Div.dedication`.
  - Ha „Példa:” szöveggel kezdődik: `Div.example`.
  - Minden más idézetblokk marad `blockquote`.

- [x] **1. lépés:** `tests/epub/fixture.md`: egy mini könyv, benne:
  - 1 fejezet emblémával;
  - 2 protokoll, `Mit tegyél?` / `Hogyan működik?` blokkcímmel;
  - 1 keretes doboz, 1 ajánlás, 1 „Példa:” idézetblokk;
  - 2 lábjegyzet.

  `tests/epub/test_filters.py`: a Pandoc HTML-kimenetén (`pandoc fixture.md -f markdown-smart --shift-heading-level-by=-1 --lua-filter … -t html`) ellenőrizd:
  - `class="chapter-opener"` 1×, `class="protocol"` 2×, `class="sidebar"` 1×, `class="dedication"` 1×, `class="example"` 1×, `class="block-label"` 2×;
  - a protokollszám `<span class="protocol-num">2</span>`.

  Ha a Pandoc nincs telepítve, a teszt legyen `pytest.skip`.
- [x] **2. lépés:** A teszt bukik → valósítsd meg a szűrőket → a teszt átmegy.
- [x] **3. lépés:** Commit: `tools(epub): Lua-szűrők`.

### 4. feladat: CSS, metaadat, borító

**Fájlok:** Létrehozandó: `book/epub/epub.css`, `book/epub/metadata.yaml`, `book/epub/cover/cover.html`, `book/epub/cover/cover.jpg`.

- [x] **1. lépés: `metadata.yaml`** az E12 szerint. Kulcsok:
  - `title`, `subtitle`, `creator` (`role: author`), `contributor`, `lang: hu`, `identifier` (`scheme: UUID`, egyszer generált érték), `date: 2026`, `rights`, `description`;
  - `cover-image: book/epub/cover/cover.jpg`, `css: book/epub/epub.css`;
  - `toc-title: Tartalom`, `page-progression-direction: ltr`.
- [x] **2. lépés: `epub.css`.** Kötelező szabályok (értékek a „Mit mutat az eredeti” táblázat alapján):
  - **`body`:** `font-family: serif`, `text-align: justify`, `hyphens: auto` (+ `-webkit-hyphens`, `-epub-hyphens`, `adobe-hyphenate: auto`), `widows: 2`, `orphans: 2`.
  - **`p`:** `margin: 0`, `text-indent: 1.2em`. A címsor, lista, doboz vagy kép utáni első bekezdés (`h1+p, h2+p, h3+p, h4+p, ul+p, ol+p, div+p, figure+p, p.first`): `text-indent: 0`.
  - **`h1, h2, h3, h4`:** `font-family: sans-serif`, `hyphens: manual`, `text-align: left`, `page-break-after: avoid; break-after: avoid`.
  - **`h1.chapter-opener`:** `page-break-before: always`, középre zárva, `margin-top: 20%`. A `.chapter-label` kisebb, félkövér, `letter-spacing: .05em`; a `.chapter-title` serif, `1.4em`.
  - **Embléma:** `p.emblem img` legyen `width: 35%`, `max-width: 200px`, középen.
  - **`h2.protocol`:** `page-break-before: always; break-before: page`, `margin-top: 3em`.
    - `.protocol-label`: `display: block`, `font-size: .8em`, félkövér, csupa nagybetű, `letter-spacing: .04em`.
    - `.protocol-num`: `display: inline-block`, `width: 1.8em`, `line-height: 1.8em`, `border-radius: 50%`, `background: rgba(0,0,0,.08)`, középre zárva, `font-weight: normal`, `margin: .4em 0`.
    - `.protocol-title`: `display: block`, `font-size: 1.5em`, `font-weight: normal`, `line-height: 1.2`.
  - **`h3.block-label`:** `font-size: .9em`, csupa nagybetű, `margin-top: 1.5em`.
  - **`li strong:first-child`:** `font-family: sans-serif`, `font-size: .95em`.
  - **`div.sidebar`:** `background: rgba(0,0,0,.06)`, `border-left: 3px solid rgba(0,0,0,.35)`, `padding: .8em 1em`, `margin: 1.2em 0`. `.sidebar-title`: sans-serif, félkövér, behúzás nélkül. A doboz első bekezdése behúzás nélkül kezdődik.
  - **`div.dedication`:** `page-break-before: always`, `margin-top: 25%`, `font-size: .9em`.
  - **`div.example`:** behúzva, `font-size: .95em`.
  - **Szerzőfotó:** `img[src*="andrew-huberman"]`: `width: 40%`, `max-width: 196px`, középen.
  - **Lábjegyzetek:** `a[role="doc-noteref"], a.footnote-ref` felső indexben, `font-size: .75em`, aláhúzás nélkül. A lábjegyzetszakasz (`section.footnotes`) mérete `.85em`, balra zárt, `hyphens: manual`, mert a hivatkozások angolok és URL-eket tartalmaznak.
- [x] **3. lépés: Borító (E1).**
  - A `cover.html` egy 1600×2560 px-es oldal, fehér háttérrel. Rajta: a PROTOKOLLOK felirat 3 betűs sorokra tördelve, mint a címoldal PRO / TO●C / OLS szórácsa (javaslat: `PRO / TO● / KOL / LOK`, az ● halványszürke kör), alatta az alcím csupa nagybetűvel, legalul a szerző.
  - Renderelés Chromiummal: Playwright, `page.screenshot`, JPEG, minőség 90 → `cover.jpg`.
  - Ha az E1 döntés „angol borító”: `cover-image: book/images/cover.jpeg`, és ez a lépés kimarad.
- [x] **4. lépés:** Commit: `book(epub): CSS, metaadat, borító`.

### 5. feladat: Build + validálás

**Fájlok:** Létrehozandó: `tools/epub/build.sh`.

- [x] **1. lépés:** `build.sh` tartalma (`set -euo pipefail`):

```bash
python tools/epub/prepare.py book/protocols-hu.md build/epub/protokollok.md "$@"
pandoc build/epub/protokollok.md -f markdown-smart -t epub3 \
  --metadata-file book/epub/metadata.yaml \
  --shift-heading-level-by=-1 --split-level=1 --toc --toc-depth=2 \
  --lua-filter tools/epub/filters/chapter.lua \
  --lua-filter tools/epub/filters/protocol.lua \
  --lua-filter tools/epub/filters/sidebar.lua \
  --resource-path=book -o dist/protokollok.epub
java -jar "${EPUBCHECK_JAR:?EPUBCHECK_JAR nincs beállítva}" dist/protokollok.epub
```

- [x] **2. lépés:** `bash tools/epub/build.sh`

  Elvárt: `No errors or warnings detected.` Minden EPUBCheck-hibát a forrásánál javíts (szűrő, CSS, prepare), ne az EPUB-ban.
- [x] **3. lépés: Szerkezeti ellenőrzés** az EPUB-on (`unzip -d build/epub/x dist/protokollok.epub`):
  - **Fejezetfájlok:** a gerincben (spine) sorrendben: címoldal, tartalomjegyzék, Jogi nyilatkozat, Ajánlás, Bevezetés, 1–7. fejezet, Mielőtt az utolsó oldalra lapoznál, Köszönetnyilvánítás, A szerzőről, Copyright. Nincs Tartalom-, Index- vagy Jegyzetek-fejezet.
  - **Protokollok:** `grep -o 'class="protocol"' build/epub/x/EPUB/text/*.xhtml | wc -l` → `47`.
  - **Lábjegyzetek:** `grep -o 'epub:type="noteref"' … | wc -l` → `1124` (ha a Pandoc más jelölést használ, pl. `role="doc-noteref"`, arra számolj; az érték 1124).
  - **Dobozok:** `grep -o 'class="sidebar"' … | wc -l` → `10`.
  - **Fájlméret:** a legnagyobb fejezetfájl mérete (`ls -S build/epub/x/EPUB/text | head -3`). Ha 300 KB fölött van, jegyezd fel a `DECISIONS.md`-be; régebbi Kobo- és ADE-olvasókon lassú lehet, ilyenkor a fejezetet `--split-level=2`-vel érdemes bontani.
  - **Nav:** a `nav.xhtml` fejezet- és protokollcímei olvashatók, teljesek, nincs bennük címkeduplázás.
- [x] **4. lépés:** Commit: `tools(epub): build + EPUBCheck`.

### 6. feladat: Szemrevételezés – 🛑 KAPU

**Fájlok:** Létrehozandó: `tools/epub/screenshots.py`, `build/epub/shots/*.png`.

- [x] **1. lépés:** A `screenshots.py` Playwright-tal (Chromium) megnyitja a kicsomagolt EPUB XHTML-fájljait két nézetben: 600×800 (6 hüvelykes olvasó) és 1264×1680 (nagy olvasó), világos és sötét háttérrel (sötétnél `html { filter: invert(1) }` szimulációval). Oldalanként képet készít:
  - borító, címoldal, tartalomjegyzék eleje;
  - Ajánlás;
  - az 1. fejezet nyitója;
  - az 1. alvásprotokoll eleje;
  - a 4. alvásprotokoll a dobozzal;
  - egy „Mit tegyél?” lista;
  - A szerzőről;
  - egy fejezet végi jegyzetblokk.
- [x] **2. lépés:** Vesd össze a képeket az eredeti PDF megfelelő oldalaival (24., 30., 59., 516., 520.). A különbségeket listázd a `build/epub/shots/REVIEW.md`-ben.
- [ ] **3. lépés: 🛑 KAPU.** Add át az embernek:
  - a `dist/protokollok.epub`-ot;
  - a képeket;
  - a kérést, hogy nyissa meg a saját eszközén. Kindle-re a „Send to Kindle” szolgáltatással megy (EPUB-ot elfogad), Kobón és PocketBookon közvetlenül.

  Ellenőrizendő:
  - felugrik-e a lábjegyzet;
  - jó-e az elválasztás;
  - új oldalon kezdődnek-e a protokollok;
  - látszanak-e a dobozok éjszakai módban.

  A visszajelzés alapján javíts, és építs újra (5. feladat).

### 7. feladat (opcionális): Kobo-változat

- [ ] **1. lépés:** Ha az ember Kobót használ, a `kepubify dist/protokollok.epub -o dist/` paranccsal készíts `protokollok.kepub.epub` fájlt: jobb lapozás, statisztika, elválasztás. EPUBCheck erre nem kell, a kiinduló EPUB már validált.

---

## Kiemelt kockázatok (review focus)

1. **Protokollcím a tartalomjegyzékben.** Az E7 spanokra bontása elronthatja a navigációs szöveget. Ellenőrzés: 3. feladat protocol-pontja, 5. feladat 3. lépése (Nav).
2. **Lágy elválasztójel rossz helyen:** URL-ben, képútvonalban, kötőjel mellett. Ellenőrzés: `test_soft_hyphenate_roundtrip_and_skips`, valamint a round-trip `cmp` a 2. feladat 4. lépésében.
3. **Lábjegyzet-szám eltérés.** Ha egy definíció a `unwrap_notes_section` után elveszik, a Pandoc figyelmeztetést ad, és a hivatkozás szövegként marad. Ellenőrzés: 1124 definíció a köztes fájlban, 1124 noteref az EPUB-ban.
4. **Éjszakai mód.** A szürke háttér és a körös szám sötét témán eltűnhet vagy túl világos lehet. Ellenőrzés: sötét képernyőképek (6. feladat).
5. **Kindle-átalakítás.** A Send to Kindle elutasíthatja a hibás EPUB-ot. Ellenőrzés: EPUBCheck 0/0, és az ember tesztje a saját eszközén.
