# EPUB – döntések (E1–E12)

**Állapot:** az ember 2026-09-27-én minden javaslatot elfogadott.

**Fordító / megjegyzés (E12):** fordító neve nem szerepel. A könyvben (címoldal után és a Copyright fölött) és a metaadatban (`rights`, `description`) ez áll:

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

## Végrehajtás közbeni döntések

_(ide kerül pl. az E7 tartalomjegyzék-kérdésének eredménye, vagy a fejezetfájl-méret miatti bontás)_
