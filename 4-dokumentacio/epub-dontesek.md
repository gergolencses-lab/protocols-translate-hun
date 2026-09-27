# EPUB – döntések (E1–E12)

> **Megjegyzés (2026-09-27):** a repó azóta átszerveződött. A régi útvonalak új helyét a [`README.md`](README.md) „Régi útvonalak” táblázata mutatja.

**Állapot:** az ember 2026-09-27-én minden javaslatot elfogadott.

**Fordító / megjegyzés (E12):** fordító neve nem szerepel. A könyvben **csak a Copyright fölött** (az ember kérésére), valamint a metaadatban (`rights`, `description`) ez áll:

> Nem hivatalos, személyes használatra készült fordítás. Használjátok egészséggel, de vegyétek meg az eredeti könyvet mindenképp!

| ID | Kérdés | Döntés (elfogadott javaslat) | Indoklás / alternatíva |
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

## Végrehajtás közbeni döntések (2026-09-27)

1. **A megjegyzés helye (E12):** csak a Copyright fölött. A Pandoc a `rights` metaadatot a címoldalra is kiírná, ezt a CSS elrejti (`section.titlepage div.rights`).
2. **Fejezetnyitó (E2):** a sorrend „1. FEJEZET” → cím → embléma (az eredetiben: címke → embléma → cím). Az embléma a címsor után áll, és a negatív margót, ami kellene a közé tételéhez, sok olvasó nem kezeli.
3. **Protokollcím (E7):** magyar sorrend: szám körben + „ALVÁSPROTOKOLL” címke, alatta a cím. A címsor szövege spanokra bontva, de betű szerint változatlan („1. alvásprotokoll: …”), az elválasztókat („. ”, „: ”) csak a címsorban rejti el a CSS. Így a tartalomjegyzék és a CSS nélküli olvasás is teljes címet mutat.
4. **Fájlbontás és tartalomjegyzék (E5):** `--split-level=2`, vagyis minden fejezet és minden protokoll külön fájl (új oldalon kezdődik; legnagyobb fájl 190 KB). A protokollon kívüli 3. szintű szakaszok (pl. „Mi az edzés?”, „A Tiszta mindenevő étrend”) és alcímeik egy szinttel lejjebb kerülnek (`h3.section-head`, a régi súllyal). Így a tartalomjegyzék – mint az eredetiben – csak a fejezeteket és a 47 protokollt listázza (61 tétel).
5. **Lábjegyzetek (E3):** a Pandoc felugró lábjegyzetei fájlonként, tehát protokollonként újraindulva számozódnak. Ez közelebb áll az eredetihez, mint a tervezett folyamatos 1–1124. A fájl végi jegyzetlista sorszámát CSS-számláló adja.
6. **Szótagolás (E8):** a pyphen `hu_HU` szótár nem szabványos pontjait (pl. alátámasz-sza, visz-sza) kihagyjuk, mert lágy elválasztójelként betűt cserélnének. Kimarad a Copyright szakasz (angol), valamint az e-mail- és `www.`-címek.
7. **Copyright:** a forrásban maradt, mondat közepi PDF-sortöréseket az előkészítő összevonja; a rövid címsorok (cím, ISBN) maradnak.
8. **Ajánlás:** az oldalon nem jelenik meg az „Ajánlás” cím (mint az eredetiben), a tartalomjegyzékben igen.
9. **Tartalmi javítások a forrásban** (`book/protocols-hu.md`): a 6. fejezet „Learning Protocol 1–6” címkéi egységesen „tanulási protokoll” (négy eltérő fordításból); a Jegyzetek 3. fejezet-címe egyezik a törzsszövegével; az embléma alternatív szövege egységes; a Tartalom egy eltérő tétele és törött horgonya javítva.
10. **Szűrőszintek:** a Pandoc Lua-szűrői a `--shift-heading-level-by` előtti szinteket látják (fejezet = 2, protokoll = 3, blokkcím = 4), nem az eltolás utániakat, ahogy a terv feltételezte.
11. **Képek:** a Pandoc automatikus képaláírását (`implicit_figures`) kikapcsoltuk, különben a képek alatt megjelenne az alternatív szöveg.
12. **Borító (E1, 2026-09-27):** a négy tervváltozatból (`cover/variants/`) az ember a 3.-at, a kétnyelvűt választotta: nagyban az eredeti PROTOCOLS logó, alatta a magyar PROTOKOLLOK cím. A `cover/cover.html` ennek önálló másolata; a `cover.jpg` ebből renderelődik (`tools/epub/render_cover.py`). Ugyanezt a képet használja az EPUB és a PDF is. A négy tervváltozatot a repó átszervezésekor az ember kérésére töröltük.

## Javítások a teljes átolvasás után (2026-09-27, 2. kör)

**Javítva a forrásban** (`book/protocols-hu.md`; az 1., 2. és 6. pont a konverzióból jött, ezért a `source/en/protocols.md`-ben is):

1. **Alsó index lábjegyzetként:** a PDF→MD konverzió a „VO₂” és „CO₂” alsó indexét lábjegyzet-hivatkozásnak olvasta (`VO[^c2-2] max`, 7×; `CO[^c6-2]`, 4×). Most `VO₂max` (ragozva kötőjellel: `VO₂max-szal`, `VO₂max-od`) és `CO₂`. A `[^c2-2]` és `[^c6-2]` valódi hivatkozása egy-egy helyen megmaradt.
2. **Hibás DOI-linkek a Jegyzetekben (8 db):** hiányzó perjel (`doi.org10.…`), hiányzó kezdő `1` (`doi.org/0.…`), duplázott előtag, `doi:` előtag, a link végére tapadt pont, két csupasz URL `<…>` nélkül, és egy dőlt URL, ahol a dőlt a folyóiratcímről csúszott át. Mind a 8 DOI feloldását ellenőriztük (doi.org → 302).
3. **Founder póz:** a 4. mobilitási gyakorlat címéből hiányzott a pont („4” → „4.”), mint a másik háromnál. (Az eredetiben egyiknél sincs pont; a fordítás egységesen „1.”–„4.”.)
4. **Oldalszám-hivatkozás:** „lapozz a 174. oldalra” (Katch–McArdle-képlet, 1. táplálkozási protokoll) → belső link a 2. edzésprotokoll „Regenerációs tippek” szakaszára (`#regenerációs-tippek`; a GitHub és a Pandoc ugyanazt az azonosítót képzi belőle).
5. **Rhodiola rosea (6. stresszprotokoll):** az adagja a foszfatidil-szerin felsoroláspontjába olvadt, a leírása előtti cím pedig sima dőlt szöveg volt. Most külön pont, és `#####` cím, mint a másik három kiegészítőnél (az eredeti szerint).

**Az eredetiben is így van – szándékosan nem javítva:**

- **Két „2. farmakológiai eszköz”** (teanin és alfa-GPC, 1. tanulási protokoll): a nyomtatott angol kiadásban is kétszer „Pharmacological Tool 2”, utána 3–6. A fordítás követi.
- **„Az ezt követő öt protokollban”** (2. fejezet bevezetője): az eredetiben is „The five protocols that follow”, pedig négy edzésprotokoll van.
- **„erről a fejezet utolsó protokolljánál írok bővebben”** (1. táplálkozási protokoll, GYIK, cukor utáni sóvárgás): az eredetiben is „more on that in the last protocol of this chapter”, de a szokatlan eszközt (L-glutamin) két bekezdéssel lejjebb, helyben tárgyalja; a 7. táplálkozási protokollban nem szerepel.
