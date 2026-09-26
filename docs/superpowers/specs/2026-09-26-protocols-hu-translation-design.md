# Protocols – magyar fordítás: specifikáció

**Dátum:** 2026-09-26
**Könyv:** Andrew Huberman: *Protocols* (angol eredeti PDF a repó gyökerében: `Protocols - Andrew Huberman.pdf`, 696 oldal)
**Végrehajtó:** OpenAI Codex (agent), emberi felügyelettel
**Terv:** `docs/superpowers/plans/2026-09-26-protocols-hu-translation.md`

---

## 1. Cél

A könyv angol Markdown-változatából (már elkészült, a PDF-ből konvertálva) teljes, kiadható minőségű magyar fordítást készítünk Markdownban. A fordítás hű az eredetihez, és úgy szól, mintha eleve magyarul írták volna.

**Bemenet:** `source/en/protocols.md` – az angol Markdown. Ezt az ember teszi a repóba, a munka megkezdése előtt.
**Kimenet:** `book/protocols-hu.md` – a teljes magyar könyv egy fájlban, továbbá a fejezetenkénti munkafájlok, a döntésnapló és a lektori jelentések.

## 2. Nem cél

- Tartalmi rövidítés, összefoglalás, átírás, a tudományos állítások frissítése vagy javítása.
- Nyomdai tördelés (PDF/EPUB). A kész Markdownból ez később külön feladat lehet.
- A PDF módosítása. A PDF csak referencia: ábra vagy formázás kétes eseteinél ebbe kell belenézni.

## 3. A folyamat (a felhasználó által megadott öt lépés)

1. **Szerkesztői ív.** Az angol Markdownból az agent megírja magának a könyv szerkesztői ívét: a tézist, a szerző hangját, a fejezetek szerepét, a visszatérő fogalmakat és a kereszthivatkozásokat (`editorial/arc.md`).
2. **Fejezetenkénti fordítási terv és fordítás.** Minden fejezethez részletes terv készül (`work/plans/<fejezet>.md`), majd a fordítás részletenként (chunk), három menetben:
   - nyersfordítás,
   - „hideg olvasás” csak a magyar szövegen,
   - egyeztetés az angollal.

   Minden részletet gépi ellenőrzések zárnak.
3. **Szomszédos fejezetek összevetése.** Minden szomszédos fejezetpárt (A→B) összevet az agent: átkötések, visszatérő fogalmak, kereszthivatkozások, hangnem, terminológia (`work/review/adjacent/`).
4. **Összefűzés.** A fejezetekből egy könyv lesz (`book/protocols-hu.md`).
5. **Végső angol–magyar összevetés** fejezetről fejezetre, bekezdésszinten. A kétes pontokat vagy maga oldja meg az agent, vagy kérdésként továbbadja egy másik modellnek (második vélemény) vagy az embernek (végső döntés) (`work/review/final/`, `work/questions/`).

A 2. lépés elé két kapu kerül:
- **Döntési kapu:** a regiszter, a mértékegységek, a címek és az alapszójegyzék jóváhagyása.
- **Pilot kapu:** egy protokoll lefordítása, az ember visszajelzése, majd a stílusútmutató hangolása.

Ezek nélkül a teljes könyvre felskálázott hibák túl drágák lennének.

## 4. Fordítási alapelvek

1. **Teljesség.** Semmit nem hagysz ki, semmit nem foglalsz össze, semmit nem teszel hozzá. Minden angol bekezdésnek van magyar megfelelője. Bekezdésen belül a mondathatárokat szabad átrendezni (összevonni, szétbontani).
2. **Jelentéshűség, nem szóhűség.** A mondatot magyarul újraírod úgy, ahogy egy jó magyar ismeretterjesztő szerző írná. Az angol mondatszerkezet nem minta.
3. **A szerző hangja.** Huberman közvetlen, lelkes, magyarázó hangon ír, sokszor ismétel és nyomatékosít. Tudományos, de laikusoknak szól. Ezt tartsd: ne legyen se hivatalos-hivatali, se bulvárosan pörgős.
4. **Az óvatossági fok megőrzése.** A *may/might/can* megfelelője *-hat/-het*. Az *evidence suggests* megfelelője „az eredmények arra utalnak”, a *likely* megfelelője „valószínűleg”. Soha ne erősítsd vagy gyengítsd az állítást, és soha ne fordítsd meg a tagadást.
5. **Biztonsági szövegek:** adagok, gyógyszerek, étrend-kiegészítők, figyelmeztetések, ellenjavallatok. Itt szó szerinti pontosság kell. Bármilyen kétely esetén kérdés készül `safety` kategóriával, `high` súllyal, `human` útvonallal.
6. **Terminológia.** A szójegyzék (`glossary/glossary.tsv`) kötelező. Új szakszót csak javaslatként (`proposed`) vehetsz fel, és a fejezet végén véglegesíted, vagy kérdésként továbbadod.

## 5. Magyar nyelvi szabályok (tipikus gépi hibák → helyes megoldás)

| # | Szabály | Rossz | Jó |
|---|---|---|---|
| 1 | Ne használd túl a határozatlan névelőt | „Ez egy nagyon hatásos eszköz.” | „Nagyon hatásos eszköz.” |
| 2 | Ne fordíts le minden *your*-t | „Tedd a kezed a te hasadra.” | „Tedd a kezed a hasadra.” |
| 3 | Páros testrész egyes számban | „napfény a szemeidbe” | „napfény a szemedbe” |
| 4 | Számnév után egyes szám | „három tanulmányok” | „három tanulmány” |
| 5 | Kerüld a szenvedő és a terpeszkedő szerkezetet | „Megállapításra került, hogy…” / „vizsgálatok lettek végezve” | „A kutatók megállapították, hogy…” |
| 6 | *in order to* ≠ mindig „annak érdekében, hogy” | „Annak érdekében, hogy jobban aludj…” | „Hogy jobban aludj…” |
| 7 | Anglicizmus helyett magyar szó | „erőteljes eszköz”, „adresszálni a problémát”, „implementálni” | „hatásos eszköz”, „foglalkozni a problémával”, „beépíteni” |
| 8 | Töltelékkifejezés | „Fontos megjegyezni, hogy…” (minden oldalon) | elhagyható, vagy „Érdemes tudni, hogy…” |
| 9 | Magyar szórend: a hangsúlyos elem az ige előtt áll | „A reggeli napfény az, ami beállítja az órát.” | „A reggeli napfény állítja be az órát.” |
| 10 | Hosszú angol mondat bontása | 4–5 tagmondatos láncmondat | 2–3 rövidebb mondat |
| 11 | Idióma jelentés szerint | „a nap végén” (*at the end of the day*) | „végső soron” |
| 12 | *he or she* | „ő vagy ő” | egyszerűen „ő”, vagy a névmás elhagyása |
| 13 | Az ismétlés szándékos | az ismétlés kihúzása | megtartod, de nem mindig szó szerint ugyanúgy |
| 14 | A kiemelés marad | a dőlt vagy félkövér szó elveszik | ugyanazon a tartalmon marad |

## 6. Tipográfia és formátum

- **Idézőjel:** „…”, belső idézetben »…«. Soha ne legyen `"` vagy “…”.
- **Gondolatjel:** szóközös nagykötőjel (` – `), az angol em dash (—) is erre vált. **Tartomány:** szóköz nélküli nagykötőjel (`5–10 perc`).
- **Számok:** tizedesvessző (`2,5 mg`). Ezres tagolás öt jegytől szóközzel (`10 000`), a négyjegyű szám egyben marad (`1000`). A számot és a mértékegységet szóköz választja el (`10 °C`, `5 mg`).
- **Toldalék:** betűszóhoz és számjegyhez kötőjellel kapcsolódik (`NSDR-t`, `NSDR-rel`, `10-szer`, `5 mg-ot`).
- **Rövidítések:** *e.g.* → „pl.”, *i.e.* → „azaz”, *etc.* → „stb.”. Dátum: `2023. szeptember 26.`
- **Címek:** magyar mondatszerű nagybetűzés, csak az első szó és a tulajdonnév nagy kezdőbetűs.
- **Intézmények:** a közismert intézménynek a bevett magyar alakja (Stanfordi Egyetem, Harvard Egyetem), egyébként az eredeti név.
- **Idézett könyvek:** ha van magyar kiadás, a magyar cím, első említéskor zárójelben az eredetivel. Ha nincs, az eredeti cím dőlten, első említéskor zárójelben nyersfordítással. Ha nem biztos, hogy van magyar kiadás, kérdés készül `fact` kategóriával.
- **Markdown:** minden jelölő megmarad: címszint, lista, lábjegyzet-hivatkozás, link, kép, kiemelés, táblázat. A lábjegyzetjel ugyanahhoz a tartalomhoz tapad, mint az angolban.

## 7. Döntési pontok (a döntési kapunál az ember hagyja jóvá)

| ID | Kérdés | Javasolt alapértelmezés | Indoklás |
|---|---|---|---|
| D1 | Tegezés vagy magázás? | **Tegezés** | A szöveg közvetlen, edzőszerű, felszólító („Do…”). A magázás merevvé tenné a protokollokat. |
| D2 | Mértékegységek | **Átváltás SI-re** (°F→°C, font→kg, mérföld→km, láb/hüvelyk→m/cm, oz→g/ml), észszerű kerekítéssel, az eredeti érték nélkül | A magyar olvasónak a °F nem mond semmit. Minden átváltás bekerül a `work/checks/number-exceptions.tsv` naplóba, és a végső lektorálásnál ellenőrzött. |
| D3 | A protokollcímek formája | „1. alvásprotokoll: …” | A magyar sorszámnév természetesebb, mint az „Alvásprotokoll 1”. A kereszthivatkozások is így szólnak. |
| D4 | A *WHAT TO DO:* és hasonló visszatérő címkék | „A TEENDŐ:” | Regisztersemleges, rövid. |
| D5 | Jegyzetek (*Notes*) | Az angol hivatkozáslista marad, csak a fejezetcímek és a nem hivatkozás jellegű magyarázó mondatok fordítódnak | Szakirodalmi hivatkozásokat nem fordítunk. |
| D6 | Tárgymutató (*Index*) | **Kimarad** a magyar könyvből | Az oldalszámok a Markdownban értelmetlenek. |
| D7 | A könyv címe | „Protokollok” (alcím az eredeti alcím fordítása) | Az ember dönt. |
| D8 | Copyright oldal | Az angol eredeti marad, magyar megjegyzéssel, hogy ez nem hivatalos fordítás | – |

## 8. Alapszójegyzék (javaslat, a döntési kapunál véglegesítendő)

A felvett sorok `status=proposed` állapotban kerülnek a szójegyzékbe.

| EN | HU (javaslat) | Megjegyzés |
|---|---|---|
| protocol | protokoll | |
| Non-Sleep Deep Rest (NSDR) | NSDR (alvás nélküli mély pihenés) | első előforduláskor kibontva, utána NSDR |
| physiological sigh | fiziológiai sóhaj | tiltott: élettani sóhaj |
| circadian rhythm | cirkadián ritmus | |
| circadian clock | cirkadián óra / belső óra | |
| cortisol | kortizol | |
| morning cortisol peak | reggeli kortizolcsúcs | |
| catecholamines | katekolaminok | |
| adenosine | adenozin | |
| neuroplasticity | neuroplaszticitás | |
| deliberate cold exposure | tudatos hidegterhelés | NYITOTT: hidegexpozíció? |
| deliberate heat exposure | tudatos hőterhelés | a hideggel párban döntendő |
| resistance training | erőedzés | NYITOTT: rezisztenciaedzés? |
| cardiovascular training | állóképességi edzés (kardió) | |
| Zone 2 cardio | 2-es zónás kardió | |
| mental contrasting | mentális kontrasztálás | |
| mind wandering | elkalandozó figyelem | |
| present-tethered awareness | jelenhez kötött tudatosság | NYITOTT |
| expressive writing | expresszív írás | |
| micro rests | mikroszünetek | |
| mental rehearsal | mentális gyakorlás | |
| long wavelength light | hosszú hullámhosszú fény | |
| near-infrared (near-IR) | közeli infravörös | |
| jet lag | jet lag (időzóna-váltás okozta zavar) | NYITOTT |
| CP:C ratio | *(a könyv definíciója alapján)* | a 4. fejezet első előfordulásánál ellenőrizni |

## 9. Kérdések kezelése és eszkaláció

Minden kétes pont bekerül a `work/questions/questions.jsonl` naplóba (`tools/questions.py add`), a szövegben pedig egy `<!-- Q:Q-0007 -->` jelölő mutatja a helyét. A fordítás közben a kérdések nem állítják meg a munkát: az agent a saját javaslatával halad tovább, és csak a kapuknál áll meg.

| Útvonal | Mikor | Ki dönt |
|---|---|---|
| `agent` | tipográfia, nyelvtan; a szójegyzékben már szereplő terminus; egyértelmű jelentés; konzisztenciajavítás; hivatkozás már lefordított címre | az agent maga, és naplózza |
| `model` | két észszerű értelmezés, közepes tét; stílusbizonytalanság kulcshelyen (fejezetnyitás, metafora, szójáték) | egy második modell véleményez (`tools/questions.py packet`), az agent dönt, a második vélemény csak tanácsadó |
| `human` | minden `register` és globális döntés; minden `safety`; új terminus, amely legalább 5-ször előfordul, és legalább 2 életképes változata van; kulturális adaptáció; bizonytalan magyar kiadás; ha az agent és a második modell `high` súlyú kérdésben nem ért egyet | az ember, kötegelve (`work/questions/for-human.md` → `decisions.md`) |

Kategóriák: `term`, `meaning`, `register`, `culture`, `safety`, `style`, `fact`, `other`. Súly: `low`, `medium`, `high`.

## 10. Minőségi kapuk

- Minden részletnél 0 FAIL a `tools/check.py pair` futásán. A WARN-okat vagy javítod, vagy egy mondattal indoklod a fejezet ellenőrzési jelentésében.
- Minden fejezetnél létezik az ellenőrzési jelentés (`work/reports/checks/<fejezet>.txt`), és nincs benne indoklás nélküli WARN.
- A könyv csak akkor áll össze, ha nincs benne nyitott kérdésjelölő.
- Az elfogadás feltételei:
  - a `pytest` zöld;
  - minden fejezet állapota kész a `STATUS.md`-ben;
  - nincs nyitott kérdés;
  - a végső lektori jelentésekben minden biztonsági mondat ki van pipálva.

## 11. Jogi megjegyzés

A könyv szerzői jogvédett. A repó legyen **privát**, a fordítás kizárólag személyes felhasználásra készül.
