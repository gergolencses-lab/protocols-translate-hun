# Protocols – magyar fordítás: megvalósítási terv

> **Agentnek (OpenAI Codex):** Ezt a tervet feladatról feladatra hajtsd végre, a sorrendet tartva. A lépések jelölőnégyzetesek (`- [ ]`): amelyik kész, azt pipáld ki ebben a fájlban, és commitold. Minden feladat előtt olvasd el az `AGENTS.md`-t és a specifikációt. Ha a Superpowers skillek telepítve vannak, a `superpowers:executing-plans` szerint dolgozz. A **🛑 KAPU** jelzésű lépéseknél állj meg, és várd meg az ember válaszát.

**Cél:** Andrew Huberman *Protocols* című könyvének angol Markdown-változatából teljes, kiadható minőségű magyar fordítás Markdownban (`book/protocols-hu.md`), ellenőrzött terminológiával és dokumentált döntésekkel.

**Architektúra:** Kis Python-eszközök (csak a standard könyvtárból) végzik a mechanikus munkát: fejezetekre és részletekre (chunk) bontás, kontextuscsomag összeállítása fordításhoz, gépi ellenőrzések (struktúra, számok, tipográfia, terminológia, hosszarány), kérdésnapló, összefűzés. A fordítást és a lektorálást a Codex végzi, részletenként friss munkamenetben, egy összeállított kontextuscsomagból (`work/packs/`). A csomag csak azt tartalmazza, ami az adott részlethez kell. Az igazság forrása mindig a részletfájl (`work/hu/<fejezet>/cNN.md`). A fejezet- és a könyvfájl generált, kézzel nem szerkesztjük.

**Technológia:** Python ≥ 3.10 (csak stdlib), pytest, git, Markdown (UTF-8, LF).

**Specifikáció:** `docs/superpowers/specs/2026-09-26-protocols-hu-translation-design.md`. A §-jelek erre utalnak, pl. „spec §5” = magyar nyelvi szabályok.

## Előfeltételek (az ember végzi el, mielőtt a Codex elindul)

1. A repó legyen **privát** (spec §11).
2. ✔ Az angol Markdown a `source/en/protocols.md` fájlban van (227 179 szó). A mintaeszközökkel lefuttatott próbabontás eredménye:
   - `--level 2` bontással veszteségmentes, 18 fejezet;
   - `--max-words 1800 --min-words 500` mellett 188 részlet, ebből kb. 160 fordítandó (a Notes és az Index a D5/D6 szerint nem kap teljes fordítást).
3. A Codex a legmagasabb elérhető gondolkodási szinten (reasoning effort: high) fusson.

## Globális megkötések

- A `source/en/` és a PDF **csak olvasható**. Soha ne módosítsd őket.
- A Python-eszközök csak a standard könyvtárat használják. Tesztelésre a `pytest` az egyetlen függőség (`requirements-dev.txt`).
- Minden szövegfájl UTF-8 és LF sorvégű. A JSON-t `ensure_ascii=False` beállítással írd.
- Az igazság forrása a `work/hu/<fejezet>/cNN.md`. A `work/hu/<fejezet>.md` és a `book/protocols-hu.md` csak az `assemble.py` kimenete.
- A kérdésjelölő formátuma pontosan `<!-- Q:Q-0007 -->`, a kérdésazonosító pontosan `Q-` + 4 számjegy.
- Commit minden feladat végén, fordítás közben minden részlet után. Az üzenetek előtagja: `tools:`, `hu(<fejezet-id>):`, `editorial:`, `review:`, `book:`, `docs:`.
- Minden feladat végén frissítsd a `STATUS.md`-t.
- A chunkméret alapértéke `--max-words 1800 --min-words 500`.
- A hosszarány küszöbei (HU/EN karakter): FAIL `< 0,70`; WARN `< 0,85` vagy `> 1,45`.
- A fordítás szabályai: spec §4–§6. A döntési pontok: spec §7. A kérdések útvonalai: spec §9.

## Kiemelt kockázatok (review focus)

1. **Csendes kihagyás vagy összefoglalás egy hosszú részletben.** A modell „rövidít”, és ez nem tűnik fel. Két teszt védi ki: a `check_ratio` FAIL-t ad 0,70 alatt, a `check_structure` pedig WARN-t, ha a bekezdésszám több mint 20%-kal eltér (2. feladat: `test_ratio`, `test_structure_paragraph_drift_is_warn`). A 3. menet (angol–magyar egyeztetés) bekezdésenként is végignézi.
2. **Terminológiai sodródás a munkamenetek között.** Ugyanaz a fogalom a 2. fejezetben másképp szól. Védelem: a szójegyzék és a `check_terms` (2. feladat: `test_terms_missing_and_forbidden`), a szomszédos fejezetek összevetése (18. feladat), valamint egy teljes könyvre futó tiltott változat keresés (19. feladat).
3. **Szám- és adaghiba, rossz mértékegység-átváltás.** Védelem: a `check_numbers` FAIL-t ad hiányzó számra (2. feladat: `test_numbers_missing_is_fail_unless_excepted`). Minden átváltás naplózott kivétel, és a végső lektorálás tételesen kipipálja a biztonsági mondatokat (20. feladat).
4. **Kereszthivatkozás a még le nem fordított vagy később átnevezett címre** (pl. „lásd a 4. alvásprotokollt”). Védelem: a kereszthivatkozási lista a szerkesztői ívben (7. feladat), valamint a 18. és a 19. feladat ellenőrző lépései.
5. **Nyitva maradt kérdés a kész könyvben.** Védelem: az `assemble.py book` nem engedi összeállni a könyvet, amíg nyitott jelölő van benne (5. feladat: `test_markers`; 19. feladat).

## Fájlszerkezet

```
AGENTS.md                              # a Codex állandó szabályai (1. feladat)
STATUS.md                              # haladás fejezet × lépés bontásban
requirements-dev.txt                   # pytest
source/en/protocols.md                 # angol Markdown (az ember adja, csak olvasható)
tools/split_chapters.py                # fejezetekre bontás
tools/chunker.py                         # részletekre bontás
tools/check.py                         # gépi ellenőrzések és szójegyzék-betöltés
tools/questions.py                     # kérdésnapló
tools/pack.py                          # kontextuscsomag a fordításhoz
tools/assemble.py                      # fejezet és könyv összefűzése
tests/conftest.py, tests/test_*.py
prompts/translate_chunk.md             # fordítási utasítás (a csomag FELADAT része)
prompts/chapter_plan.md                # fejezetterv sablon
prompts/adjacent_review.md             # szomszédos fejezetek összevetése
prompts/final_review.md                # végső angol–magyar lektorálás
prompts/second_opinion.md              # második modell véleménye
editorial/arc.md                       # 1. lépés: szerkesztői ív
editorial/style-guide.md               # stílusútmutató (spec §4–§7 és a döntések)
glossary/glossary.tsv                  # szójegyzék
work/en/chapters.json, work/en/<id>.md, work/en/<id>/cNN.md, work/en/<id>/manifest.json
work/plans/<id>.md                     # 2. lépés: fejezetterv
work/packs/<id>/cNN.md                 # generált csomagok (gitignore)
work/hu/<id>/cNN.md                    # FORDÍTÁS – az igazság forrása
work/hu/<id>.md                        # generált fejezet
work/checks/number-exceptions.tsv      # számkivételek és átváltási napló
work/reports/checks/<id>.txt           # ellenőrzési jelentések
work/questions/questions.jsonl, for-human.md, decisions.md, packets/
work/review/adjacent/<A>__<B>.md       # 3. lépés
work/review/final/<id>.md              # 5. lépés
book/manifest.txt, book/protocols-hu.md  # 4. lépés
```

---

# A. SZAKASZ – Eszközök (TDD)

### 1. feladat: Váz és fejezetekre bontás

**Fájlok:**
- Létrehozandó: `AGENTS.md`, `STATUS.md`, `requirements-dev.txt`, `.gitignore`, `tools/split_chapters.py`, `tests/conftest.py`, `tests/test_split_chapters.py`

**Interfészek:**
- Előállítja:
  - `Chapter` (dataclass: `id: str`, `title: str`, `text: str`)
  - `slugify(title: str) -> str`
  - `split_chapters(md: str, level: int = 1) -> list[Chapter]`
  - `verify_lossless(md: str, chapters: list[Chapter]) -> bool`
  - `write_chapters(chapters: list[Chapter], out_dir: Path) -> None`: minden fejezetet `<id>.md` néven ír ki, a `chapters.json` pedig `[{"id":…,"title":…}]` sorrendben
  - CLI: `python tools/split_chapters.py <md> <out_dir> --level N`. Kilépési kód 1, ha a bontás nem veszteségmentes.

- [ ] **1. lépés: Hozd létre a vázat**

`requirements-dev.txt`: egyetlen sor, `pytest`. A `.gitignore` tartalma:

```
__pycache__/
.pytest_cache/
work/packs/
```

`AGENTS.md` pontos tartalma:

```markdown
# Szabályok a Codexnek – Protocols magyar fordítás

- Terv: docs/superpowers/plans/2026-09-26-protocols-hu-translation.md (a sorrendet tartsd, pipáld a lépéseket).
- Specifikáció: docs/superpowers/specs/2026-09-26-protocols-hu-translation-design.md (fordítási szabályok: §4–§6).
- Stílusútmutató: editorial/style-guide.md. Szójegyzék: glossary/glossary.tsv – mindkettő kötelező.
- source/en/ és a PDF: CSAK OLVASHATÓ.
- Fordítani csak részletenként (work/hu/<fejezet>/cNN.md), a tools/pack.py csomagjából, friss munkamenetben.
- Soha ne hagyj ki, ne foglalj össze, ne tegyél hozzá tartalmat.
- Kétes pont: `python tools/questions.py add …` + `<!-- Q:Q-NNNN -->` jelölő a szövegben; haladj tovább a javaslatoddal.
- Minden részlet után: `python tools/check.py pair …` → 0 FAIL, majd commit.
- A 🛑 KAPU lépéseknél állj meg, és várd meg az ember válaszát.
- Minden feladat végén frissítsd a STATUS.md-t.
```

`STATUS.md` fejléc (a sorokat a 6. feladat tölti ki):

```markdown
# Állapot

| Fejezet | Terv | Részletek (kész/össz) | Ellenőrzés | Szomszéd-összevetés | Végső lektorálás |
|---|---|---|---|---|---|
```

`tests/conftest.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
```

- [ ] **2. lépés: Írd meg a bukó tesztet** – `tests/test_split_chapters.py`:

```python
from split_chapters import slugify, split_chapters, verify_lossless

MD = (
    "Title page\n\n"
    "# Introduction\nIntro text.\n\n## Sub\nMore.\n"
    "# Chapter 1: Protocols for Sleep\nSleep text.\n"
)


def test_slugify():
    assert slugify("Chapter 1: Protocols for Sleep") == "chapter-1-protocols-for-sleep"
    assert slugify("Apply James Hollis’s Guide") == "apply-james-holliss-guide"
    assert slugify("Árvíztűrő tükörfúrógép") == "arvizturo-tukorfurogep"


def test_split_level1_ids_and_text():
    chs = split_chapters(MD, level=1)
    assert [c.id for c in chs] == [
        "00-front",
        "01-introduction",
        "02-chapter-1-protocols-for-sleep",
    ]
    assert chs[1].title == "Introduction"
    assert chs[1].text == "# Introduction\nIntro text.\n\n## Sub\nMore.\n"


def test_split_is_lossless():
    assert verify_lossless(MD, split_chapters(MD, level=1))


def test_no_front_when_md_starts_with_heading():
    chs = split_chapters("# A\nx\n# B\ny\n", level=1)
    assert [c.id for c in chs] == ["01-a", "02-b"]


def test_split_level2_ignores_level1():
    chs = split_chapters("# A\n## B\nx\n## C\ny\n", level=2)
    assert [c.id for c in chs] == ["00-front", "01-b", "02-c"]
    assert chs[0].text == "# A\n"
```

- [ ] **3. lépés: Futtasd, és győződj meg róla, hogy bukik**

Futtatás: `python -m pytest tests/test_split_chapters.py -v`
Elvárt: FAIL, `ModuleNotFoundError: No module named 'split_chapters'`

- [ ] **4. lépés: Valósítsd meg a `tools/split_chapters.py`-t**

- A `slugify`: NFKD-normalizálás, majd ASCII-ra kódolás `ignore` hibakezeléssel (így esik ki a `’`), kisbetűsítés, a `[^a-z0-9]+` cseréje `-`-re, a szélső `-` levágása, legfeljebb 60 karakter.
- A `split_chapters`: a pontosan `level` szintű címsor (`^#{level} `, magasabb szintű nem) új fejezetet nyit, és a címsor sora a fejezet szövegének része. Az első címsor előtti, nem üres szöveg `00-front` azonosítót kap. A fejezetek sorszáma mindig 01-ről indul.
- A CLI kiírja a fejezetek számát és a (`id`, `title`) sorokat.

- [ ] **5. lépés: Futtasd a teszteket, győződj meg róla, hogy átmennek**

Futtatás: `python -m pytest tests/test_split_chapters.py -v`
Elvárt: 5 passed

- [ ] **6. lépés: Commit**

```bash
git add AGENTS.md STATUS.md requirements-dev.txt .gitignore tools/split_chapters.py tests/
git commit -m "tools: váz és fejezetekre bontás"
```

### 2. feladat: Gépi ellenőrzések

**Fájlok:**
- Létrehozandó: `tools/check.py`, `tests/test_check.py`, `work/checks/number-exceptions.tsv` (csak fejléc: `hu_file	number	reason`)

**Interfészek:**
- Előállítja:
  - `Issue` (dataclass: `level: str` – `"FAIL"` vagy `"WARN"`; `code: str`; `message: str`)
  - `Term` (dataclass: `en`, `hu`, `hu_match`, `status`, `forbidden: list[str]`, `note`)
  - `load_glossary(path: Path) -> list[Term]`: TSV, fejléc `en	hu	hu_match	status	forbidden	note`; a `forbidden` mező `;`-vel tagolt; üres sorokat kihagy
  - `term_to_tsv(t: Term) -> str`
  - `check_structure(en: str, hu: str) -> list[Issue]`
  - `extract_numbers(text: str, lang: str) -> list[str]`
  - `check_numbers(en: str, hu: str, exceptions: set[str] = frozenset()) -> list[Issue]`
  - `check_ratio(en: str, hu: str, lo=0.85, hi=1.45, fail_below=0.70) -> list[Issue]`
  - `check_typography(hu: str) -> list[Issue]`
  - `check_terms(en: str, hu: str, terms: list[Term]) -> list[Issue]`
  - `run_pair(en_path: Path, hu_path: Path, glossary: Path, exceptions: Path) -> list[Issue]`
  - CLI:
    - `python tools/check.py pair <en> <hu>`: kiírja a sorokat `LEVEL code: message` formában, és 1-gyel lép ki, ha van FAIL
    - `python tools/check.py chapter <id>`: a manifest minden részletére lefut, a jelentést a `work/reports/checks/<id>.txt` fájlba írja, és 1-gyel lép ki, ha van FAIL

- [ ] **1. lépés: Írd meg a bukó tesztet** – `tests/test_check.py`:

```python
from check import (
    Term,
    check_numbers,
    check_ratio,
    check_structure,
    check_terms,
    check_typography,
    extract_numbers,
)


def codes(issues):
    return sorted(i.code for i in issues)


def levels(issues):
    return sorted(i.level for i in issues)


def test_structure_equal():
    en = "## Title\n\n- a\n- b\n\nText[^1] and [link](http://x).\n"
    hu = "## Cím\n\n- a\n- b\n\nSzöveg[^1] és [link](http://x).\n"
    assert check_structure(en, hu) == []


def test_structure_missing_list_item_and_footnote():
    en = "- a\n- b\n\nText[^1].\n"
    hu = "- a\n\nSzöveg.\n"
    assert codes(check_structure(en, hu)) == ["structure:footnotes", "structure:list_items"]
    assert set(levels(check_structure(en, hu))) == {"FAIL"}


def test_structure_paragraph_drift_is_warn():
    en = "".join(f"P{i}.\n\n" for i in range(10))
    hu = "".join(f"B{i}.\n\n" for i in range(7))
    issues = check_structure(en, hu)
    assert codes(issues) == ["structure:paragraphs"]
    assert levels(issues) == ["WARN"]


def test_extract_numbers():
    assert extract_numbers("Take 1,000 mg or 2.5 g in 2020.", "en") == ["1000", "2.5", "2020"]
    assert extract_numbers("Vegyél be 10 000 mg-ot vagy 2,5 g-ot.", "hu") == ["10000", "2.5"]


def test_numbers_match():
    en = "Take 1,000 mg or 2.5 g for 10 days."
    hu = "Vegyél be 1000 mg-ot vagy 2,5 g-ot 10 napig."
    assert check_numbers(en, hu) == []


def test_numbers_missing_is_fail_unless_excepted():
    issues = check_numbers("Wait 90 minutes.", "Várj másfél órát.")
    assert codes(issues) == ["numbers:missing"]
    assert levels(issues) == ["FAIL"]
    assert "90" in issues[0].message
    assert check_numbers("Wait 90 minutes.", "Várj másfél órát.", exceptions={"90"}) == []


def test_numbers_extra_is_warn():
    issues = check_numbers("Wait five days.", "Várj 5 napot.")
    assert codes(issues) == ["numbers:extra"]
    assert levels(issues) == ["WARN"]


def test_ratio():
    en = "a" * 1000
    assert levels(check_ratio(en, "a" * 600)) == ["FAIL"]
    assert levels(check_ratio(en, "a" * 800)) == ["WARN"]
    assert check_ratio(en, "a" * 1100) == []
    assert levels(check_ratio(en, "a" * 1500)) == ["WARN"]


def test_typography_clean():
    assert check_typography("„Igen” – mondta. Legalább 5–10 percig, 2,5 mg.\n\n- listaelem\n") == []


def test_typography_problems():
    assert "typo:straight-quote" in codes(check_typography('Azt mondta: "igen".'))
    assert "typo:english-open-quote" in codes(check_typography("“Igen” – mondta."))
    assert "typo:decimal-point" in codes(check_typography("Ez 2.5 gramm."))
    assert "typo:spaced-hyphen" in codes(check_typography("A kutatás - mint láttuk - fontos."))
    assert "typo:english-residue" in codes(
        check_typography("This is the text and the rest of the words that you see.")
    )
    assert set(levels(check_typography('Azt mondta: "igen".'))) == {"WARN"}


def test_typography_ignores_inline_code():
    assert check_typography('Futtasd: `grep -c "x" f.md` most.') == []


SIGH = Term(
    en="physiological sigh",
    hu="fiziológiai sóhaj",
    hu_match="fiziológiai sóhaj",
    status="approved",
    forbidden=["élettani sóhaj"],
    note="",
)


def test_terms_ok():
    assert check_terms("Do one physiological sigh.", "Végezz egy fiziológiai sóhajt.", [SIGH]) == []


def test_terms_missing_and_forbidden():
    issues = check_terms("Do one physiological sigh.", "Végezz egy élettani sóhajt.", [SIGH])
    assert codes(issues) == ["terms:forbidden", "terms:missing"]
    assert levels(issues) == ["FAIL", "WARN"]


def test_terms_ignore_non_approved():
    proposed = Term(**{**SIGH.__dict__, "status": "proposed"})
    assert check_terms("Do one physiological sigh.", "Végezz egy élettani sóhajt.", [proposed]) == []
```

- [ ] **2. lépés: Futtasd, és győződj meg róla, hogy bukik**

Futtatás: `python -m pytest tests/test_check.py -v`
Elvárt: FAIL, `ModuleNotFoundError: No module named 'check'`

- [ ] **3. lépés: Valósítsd meg a `tools/check.py`-t**

- **Struktúra (FAIL eltérésnél).** A számolt minták neve (a kód `structure:<név>`) és regexe, `re.M` módban (a sorvégi szóköz a regex része):

  ```
  headings_h1   ^# 
  headings_h2   ^## 
  headings_h3   ^### 
  headings_h4   ^#### 
  headings_h5   ^##### 
  list_items    ^\s*(?:[-*+]|\d+\.)\s
  footnotes     \[\^[^\]]+\]
  sup           <sup>
  links         \]\(
  images        !\[
  blockquotes   ^>
  table_rows    ^\|
  ```

  A `structure:paragraphs` WARN, ha az üres sorral tagolt, nem üres blokkok számában `|EN−HU|/EN > 0,2`.
- **Számok.** Angolul: `\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?`, a vesszők törlésével. Magyarul: `(?<![\d,])\d{1,3}(?:[   ]\d{3})+(?:,\d+)?(?!\d)|\d+(?:,\d+)?`; a szóközök törlődnek, a tizedesvessző pontra vált. Az összevetés multihalmaz-különbséggel (`Counter`) történik: a hiányzó szám FAIL `numbers:missing` (az üzenetben a számokkal), a többletszám WARN `numbers:extra`.
- **Tipográfia (minden találat WARN).** Előtte a `` `…` `` kódrészleteket töröld.
  - `typo:straight-quote`: `"`
  - `typo:english-open-quote`: `“`
  - `typo:spaced-hyphen`: `(?<=\S) - (?=\S)`
  - `typo:decimal-point`: `(?<![\d.])\d+\.\d+(?![\d.])`
  - `typo:thousands-comma`: `(?<![\d,])\d{1,3},\d{3}(?![\d,])`
  - `typo:english-residue`: WARN, ha a {the, and, of, to, is, that, with, for, this, you} szavak aránya a betűszavak között nagyobb 0,03-nál
- **Terminusok.** Csak `status == "approved"` sorokra. A `terms:missing` WARN, ha az angol terminus szóhatárral, kis- és nagybetűtől függetlenül szerepel az angolban, de a `hu_match` (kisbetűs részsztring) hiányzik a magyarból. A `terms:forbidden` FAIL, ha a magyarban szerepel bármelyik `forbidden` változat.
- **`run_pair`.** Az összes ellenőrzés együtt. A kivételek közül csak azok a sorok számítanak, amelyeknek a `hu_file` mezője megegyezik a `hu_path` repó-relatív alakjával.

- [ ] **4. lépés: Futtasd a teszteket, győződj meg róla, hogy átmennek**

Futtatás: `python -m pytest tests/test_check.py -v`
Elvárt: 14 passed

- [ ] **5. lépés: Commit**

```bash
git add tools/check.py tests/test_check.py work/checks/number-exceptions.tsv
git commit -m "tools: gépi ellenőrzések (struktúra, számok, arány, tipográfia, terminusok)"
```

### 3. feladat: Részletekre bontás

**Fájlok:**
- Létrehozandó: `tools/chunker.py`, `tests/test_chunker.py`

**Interfészek:**
- Előállítja:
  - `chunk_chapter(text: str, max_words: int = 1800, min_words: int = 500) -> list[str]`
  - `write_chunks(chapter_id: str, text: str, out_root: Path, max_words: int, min_words: int) -> list[str]`: kiírja a `out_root/<chapter_id>/c01.md`, `c02.md` stb. fájlokat, a `manifest.json` pedig `{"chapter": id, "chunks": ["c01", …]}` alakú. Visszaadja a részletazonosítókat.
  - CLI: `python tools/chunker.py work/en --max-words 1800 --min-words 500`: a `chapters.json` minden fejezetére lefut, és táblázatot ír ki (id, részletszám, szószám).

- [ ] **1. lépés: Írd meg a bukó tesztet** – `tests/test_chunker.py`:

```python
from chunker import chunk_chapter


def p(n):
    return " ".join(["word"] * n) + "\n\n"


def test_splits_at_subheadings_when_min_reached():
    text = "# T\n\n" + p(500) + "## S1\n\n" + p(500) + p(500) + "## S2\n\n" + p(100)
    chunks = chunk_chapter(text, max_words=1200, min_words=400)
    assert chunks == [
        "# T\n\n" + p(500),
        "## S1\n\n" + p(500) + p(500),
        "## S2\n\n" + p(100),
    ]


def test_heading_never_ends_a_chunk():
    text = p(1000) + "## H\n\n" + p(500)
    chunks = chunk_chapter(text, max_words=1200, min_words=5000)
    assert chunks == [p(1000), "## H\n\n" + p(500)]


def test_oversize_paragraph_stays_whole():
    assert chunk_chapter(p(3000), max_words=2000, min_words=500) == [p(3000)]


def test_lossless():
    text = "# T\n\n" + p(900) + "## A\n\n" + p(700) + "\n\n\n" + p(1500) + "## B\nno trailing blank"
    assert "".join(chunk_chapter(text, max_words=1000, min_words=300)) == text
```

- [ ] **2. lépés: Futtasd, és győződj meg róla, hogy bukik**

Futtatás: `python -m pytest tests/test_chunker.py -v`
Elvárt: FAIL, `ModuleNotFoundError: No module named 'chunker'`

- [ ] **3. lépés: Valósítsd meg a `chunk_chapter`-t és a `write_chunks`-ot**

Az algoritmust a tesztek nem határozzák meg egyértelműen, ezért ez a kötelező:

```
blokkok = a szöveg feldarabolva az üres sor(ok)nál; a darabolás veszteségmentes, a sorközök az előző blokkhoz tartoznak
szószám(s) = len(re.findall(r"\w+", s))
alcím(b) = re.match(r"^#{2,6} ", b)
minden b blokkra:
  ha a jelenlegi részlet nem üres ÉS alcím(b) ÉS a jelenlegi szószám >= min_words:
      a jelenlegi részlet lezárul, új indul
  különben ha a jelenlegi részlet nem üres ÉS a jelenlegi szószám + szószám(b) > max_words ÉS nem alcím(b):
      a jelenlegi részlet végén álló alcím-blokkok átkerülnek az új részletbe (címsor soha nem zár részletet)
      a maradék lezárul (ha nem üres), az új részlet az átvitt blokkokkal indul
  b hozzáadódik a jelenlegi részlethez
```

- [ ] **4. lépés: Futtasd a teszteket, győződj meg róla, hogy átmennek**

Futtatás: `python -m pytest tests/test_chunker.py -v`
Elvárt: 4 passed

- [ ] **5. lépés: Commit**

```bash
git add tools/chunker.py tests/test_chunker.py
git commit -m "tools: részletekre bontás"
```

### 4. feladat: Kérdésnapló

**Fájlok:**
- Létrehozandó: `tools/questions.py`, `tests/test_questions.py`

**Interfészek:**
- Előállítja:
  - `load(path) -> list[dict]`, `save(path, qs: list[dict]) -> None`: JSONL formátum
  - `add_question(path, *, chapter, chunk, category, severity, route, question, en, hu_current, options: list[str], recommendation) -> str`: a következő azonosítót adja (`Q-0001`…), és beállítja a `status="open"`, `resolution=""`, `resolved_by=""` mezőket
  - `format_question(q: dict) -> str`: a blokk formátuma:

    ```
    ## Q-0001 · <fejezet> · <részlet> · <kategória> · <súly>

    **Kérdés:** …

    **Angol:**
    > …

    **Jelenlegi magyar:**
    > …

    **Opciók:**
    - A: …
    - B: …

    **Javaslat:** …

    Döntés: 
    ```

  - `export_for_human(qs) -> str`: csak az `open` és `human` útvonalú kérdések, `\n`-nel összefűzve
  - `parse_decisions(md: str) -> dict[str, str]`
  - `import_decisions(qs, decisions: dict[str, str], resolved_by: str = "human") -> int`: az egybetűs döntés (`A`, `B`…) a megfelelő opció szövegére fordul
  - `render_packet(q: dict, template: str) -> str`: a `{{question_block}}` helyére kerül a `format_question(q)` (a záró soremelések nélkül)
  - CLI (az alapértelmezett napló `work/questions/questions.jsonl`):
    - `add --chapter --chunk --category --severity --route --question --en --hu-current --option (ismételhető) --recommendation`: kiírja az azonosítót
    - `list [--open] [--route R]`
    - `export`: kiírja a `work/questions/for-human.md` fájlt
    - `import <md>`
    - `packet <Q-id>`: a `prompts/second_opinion.md` alapján kiírja a `work/questions/packets/<Q-id>.md` fájlt
    - `resolve <Q-id> --resolution TEXT --by WHO`

- [ ] **1. lépés: Írd meg a bukó tesztet** – `tests/test_questions.py`:

```python
from questions import add_question, export_for_human, import_decisions, load, parse_decisions


def make(path, route="human"):
    return add_question(
        path,
        chapter="02-chapter-1-protocols-for-sleep",
        chunk="c04",
        category="term",
        severity="high",
        route=route,
        question="Hogyan fordítsuk a „physiological sigh” kifejezést?",
        en="Do one physiological sigh.",
        hu_current="Végezz egy fiziológiai sóhajt.",
        options=["fiziológiai sóhaj", "élettani sóhaj"],
        recommendation="A",
    )


def test_ids_increment_and_persist(tmp_path):
    path = tmp_path / "questions.jsonl"
    assert make(path) == "Q-0001"
    assert make(path) == "Q-0002"
    qs = load(path)
    assert [q["id"] for q in qs] == ["Q-0001", "Q-0002"]
    assert qs[0]["status"] == "open"
    assert qs[0]["resolution"] == ""


def test_export_only_open_human(tmp_path):
    path = tmp_path / "questions.jsonl"
    make(path)
    make(path, route="agent")
    md = export_for_human(load(path))
    assert "## Q-0001" in md
    assert "Q-0002" not in md
    assert "- A: fiziológiai sóhaj" in md
    assert "Döntés:" in md


def test_parse_decisions_skips_empty():
    md = "## Q-0001 · x\nszöveg\nDöntés: B\n\n## Q-0002 · y\nDöntés:   \n"
    assert parse_decisions(md) == {"Q-0001": "B"}


def test_import_maps_letter_and_keeps_free_text(tmp_path):
    path = tmp_path / "questions.jsonl"
    make(path)
    make(path)
    qs = load(path)
    n = import_decisions(qs, {"Q-0001": "B", "Q-0002": "légzőgyakorlat"}, resolved_by="human")
    assert n == 2
    assert qs[0]["resolution"] == "élettani sóhaj"
    assert qs[1]["resolution"] == "légzőgyakorlat"
    assert qs[0]["status"] == "resolved"
    assert qs[0]["resolved_by"] == "human"


def test_format_and_packet(tmp_path):
    from questions import format_question, render_packet

    path = tmp_path / "questions.jsonl"
    make(path)
    q = load(path)[0]
    block = format_question(q)
    assert block.startswith("## Q-0001 · 02-chapter-1-protocols-for-sleep · c04 · term · high")
    assert block.rstrip().endswith("Döntés:")
    packet = render_packet(q, "ELEJE\n{{question_block}}\nVÉGE\n")
    assert packet.startswith("ELEJE\n## Q-0001")
    assert packet.endswith("VÉGE\n")
```

- [ ] **2. lépés: Futtasd, és győződj meg róla, hogy bukik**

Futtatás: `python -m pytest tests/test_questions.py -v`
Elvárt: FAIL, `ModuleNotFoundError: No module named 'questions'`

- [ ] **3. lépés: Valósítsd meg a `tools/questions.py`-t**

A `parse_decisions` a `## (Q-\d{4})` fejlécet követő első `Döntés:` sort olvassa ki. Ha az érték a levágás után üres, a kérdés kimarad.

- [ ] **4. lépés: Futtasd a teszteket, győződj meg róla, hogy átmennek**

Futtatás: `python -m pytest tests/test_questions.py -v`
Elvárt: 5 passed

- [ ] **5. lépés: Commit**

```bash
git add tools/questions.py tests/test_questions.py
git commit -m "tools: kérdésnapló"
```

### 5. feladat: Kontextuscsomag és összefűzés

**Fájlok:**
- Létrehozandó: `tools/pack.py`, `tools/assemble.py`, `tests/test_pack.py`, `tests/test_assemble.py`

**Interfészek:**
- Felhasználja: `check.load_glossary`, `check.term_to_tsv`, `check.Term` (2. feladat); a `manifest.json` formátumát (3. feladat)
- Előállítja:
  - `pack.arc_section(arc_md: str, chapter_id: str) -> str`: a `## <chapter_id>` sortól a következő `## ` sorig; ha nincs ilyen szakasz, `KeyError`
  - `pack.tail_words(text: str, n: int = 250) -> str`
  - `pack.build_pack(chapter_id: str, chunk_id: str, root: Path) -> str`: a kimenetet a `work/packs/<id>/<chunk>.md` fájlba is kiírja
  - CLI:
    - `python tools/pack.py <chapter_id> <chunk_id>`
    - `python tools/pack.py --check-arc`: 1-gyel lép ki, ha a `chapters.json` valamelyik fejezetének nincs ívszakasza
  - `assemble.assemble_chapter(chapter_id: str, root: Path) -> str`: kiírja a `work/hu/<id>.md` fájlt; hiányzó részletnél `FileNotFoundError`, az üzenetben a részletazonosítókkal
  - `assemble.open_markers(text: str) -> list[str]`
  - `assemble.strip_markers(text: str, ids: set[str]) -> str`: a jelölőt és az előtte álló egy szóközt törli
  - `assemble.assemble_book(entries: list[str], root: Path) -> str`: az `en:<id>` bejegyzés a `work/en/<id>.md` fájlt veszi. A fejezetek a záró soremelések levágása után `\n\n`-nel fűződnek össze, a végére egy `\n` kerül.
  - CLI:
    - `python tools/assemble.py chapter <id>`
    - `python tools/assemble.py book`: beolvassa a `book/manifest.txt`-t (soronként egy bejegyzés), a `resolved` kérdések jelölőit törli; ha marad nyitott jelölő, kilistázza és 1-gyel lép ki; a kimenet a `book/protocols-hu.md`

- [ ] **1. lépés: Írd meg a bukó teszteket** – `tests/test_pack.py`:

```python
import json

import pytest

from pack import arc_section, build_pack, tail_words

ARC = "# Ív\n\n## 01-introduction\nBevezető.\n\n## 02-chapter-1-sleep\nAlvás.\n"


def test_arc_section():
    assert arc_section(ARC, "01-introduction") == "## 01-introduction\nBevezető.\n\n"
    with pytest.raises(KeyError):
        arc_section(ARC, "09-missing")


def test_tail_words():
    assert tail_words("a b c d e", 2) == "d e"
    assert tail_words("a b", 5) == "a b"


def _setup(root):
    (root / "prompts").mkdir()
    (root / "prompts/translate_chunk.md").write_text("Írd ide: {{hu_path}}\n", encoding="utf-8")
    (root / "editorial").mkdir()
    (root / "editorial/style-guide.md").write_text("STÍLUS\n", encoding="utf-8")
    (root / "editorial/arc.md").write_text(ARC, encoding="utf-8")
    (root / "glossary").mkdir()
    (root / "glossary/glossary.tsv").write_text(
        "en\thu\thu_match\tstatus\tforbidden\tnote\n"
        "sunlight\tnapfény\tnapfény\tapproved\t\t\n"
        "cortisol\tkortizol\tkortizol\tapproved\t\t\n",
        encoding="utf-8",
    )
    (root / "work/plans").mkdir(parents=True)
    (root / "work/plans/02-chapter-1-sleep.md").write_text("TERV\n", encoding="utf-8")
    en = root / "work/en/02-chapter-1-sleep"
    en.mkdir(parents=True)
    (en / "manifest.json").write_text(json.dumps({"chapter": "02-chapter-1-sleep", "chunks": ["c01", "c02"]}))
    (en / "c01.md").write_text("First sunlight chunk.\n", encoding="utf-8")
    (en / "c02.md").write_text("Second sunlight chunk.\n", encoding="utf-8")


def test_build_pack_first_chunk(tmp_path):
    _setup(tmp_path)
    pack = build_pack("02-chapter-1-sleep", "c01", tmp_path)
    heads = [line for line in pack.splitlines() if line.startswith("# ")]
    assert heads == [
        "# FELADAT",
        "# STÍLUSÚTMUTATÓ",
        "# SZÓJEGYZÉK (RELEVÁNS)",
        "# A KÖNYV ÍVE – EZ A FEJEZET",
        "# FEJEZETTERV",
        "# FORDÍTANDÓ SZÖVEG (EN)",
    ]
    assert "Írd ide: work/hu/02-chapter-1-sleep/c01.md" in pack
    assert "sunlight\tnapfény" in pack
    assert "cortisol" not in pack
    assert pack.rstrip().endswith("First sunlight chunk.")
    assert (tmp_path / "work/packs/02-chapter-1-sleep/c01.md").read_text(encoding="utf-8") == pack


def test_build_pack_second_chunk_has_previous(tmp_path):
    _setup(tmp_path)
    hu = tmp_path / "work/hu/02-chapter-1-sleep"
    hu.mkdir(parents=True)
    (hu / "c01.md").write_text("Első napfényes rész.\n", encoding="utf-8")
    pack = build_pack("02-chapter-1-sleep", "c02", tmp_path)
    assert "# ELŐZŐ RÉSZLET VÉGE (EN)" in pack
    assert "# ELŐZŐ RÉSZLET VÉGE (HU)" in pack
    assert "Első napfényes rész." in pack
```

és `tests/test_assemble.py`:

```python
import json

import pytest

from assemble import assemble_book, assemble_chapter, open_markers, strip_markers


def _chapter(root, ch, chunks, hu_texts):
    en = root / "work/en" / ch
    en.mkdir(parents=True)
    (en / "manifest.json").write_text(json.dumps({"chapter": ch, "chunks": chunks}))
    hu = root / "work/hu" / ch
    hu.mkdir(parents=True)
    for cid, text in hu_texts.items():
        (hu / f"{cid}.md").write_text(text, encoding="utf-8")


def test_assemble_chapter_in_manifest_order(tmp_path):
    _chapter(tmp_path, "01-x", ["c01", "c02"], {"c02": "B\n", "c01": "A\n\n"})
    assert assemble_chapter("01-x", tmp_path) == "A\n\nB\n"
    assert (tmp_path / "work/hu/01-x.md").read_text(encoding="utf-8") == "A\n\nB\n"


def test_assemble_chapter_missing_chunk(tmp_path):
    _chapter(tmp_path, "01-x", ["c01", "c02"], {"c01": "A\n"})
    with pytest.raises(FileNotFoundError, match="c02"):
        assemble_chapter("01-x", tmp_path)


def test_markers():
    text = "Szöveg <!-- Q:Q-0003 --> és <!-- Q:Q-0010 -->.\n"
    assert open_markers(text) == ["Q-0003", "Q-0010"]
    assert strip_markers(text, {"Q-0003"}) == "Szöveg és <!-- Q:Q-0010 -->.\n"


def test_assemble_book_with_en_passthrough(tmp_path):
    (tmp_path / "work/hu").mkdir(parents=True)
    (tmp_path / "work/en").mkdir(parents=True)
    (tmp_path / "work/hu/01-a.md").write_text("# Egy\n", encoding="utf-8")
    (tmp_path / "work/en/02-notes.md").write_text("# Notes\n", encoding="utf-8")
    book = assemble_book(["01-a", "en:02-notes"], tmp_path)
    assert book == "# Egy\n\n# Notes\n"
```

- [ ] **2. lépés: Futtasd, és győződj meg róla, hogy bukik**

Futtatás: `python -m pytest tests/test_pack.py tests/test_assemble.py -v`
Elvárt: FAIL, `ModuleNotFoundError`

- [ ] **3. lépés: Valósítsd meg a `tools/pack.py`-t**

- A szakaszok sorrendje:
  1. `# FELADAT`: a `prompts/translate_chunk.md`, benne a `{{hu_path}}`, `{{chapter_id}}` és `{{chunk_id}}` helyettesítve; a `hu_path` alakja `work/hu/<id>/<chunk>.md`
  2. `# STÍLUSÚTMUTATÓ`
  3. `# SZÓJEGYZÉK (RELEVÁNS)`: a TSV fejléce, majd azok az `approved` és `proposed` sorok, amelyeknek az angol terminusa szóhatárral, kis- és nagybetűtől függetlenül szerepel a részletben
  4. `# A KÖNYV ÍVE – EZ A FEJEZET`
  5. `# FEJEZETTERV`
  6. csak ha nem az első részletről van szó: `# ELŐZŐ RÉSZLET VÉGE (EN)`, és ha a magyar fájl már létezik, `# ELŐZŐ RÉSZLET VÉGE (HU)`; mindkettő `tail_words(…, 250)`
  7. `# FORDÍTANDÓ SZÖVEG (EN)`
- Minden szakasz formátuma `# <cím>\n\n<tartalom levágva>\n\n`.

- [ ] **4. lépés: Valósítsd meg a `tools/assemble.py`-t** az interfész szerint.

- [ ] **5. lépés: Futtasd az összes tesztet**

Futtatás: `python -m pytest -v`
Elvárt: 36 passed

- [ ] **6. lépés: Commit**

```bash
git add tools/pack.py tools/assemble.py tests/test_pack.py tests/test_assemble.py
git commit -m "tools: kontextuscsomag és összefűzés"
```

---

# B. SZAKASZ – Előkészítés

### 6. feladat: A forrás bevétele, bontása, részletezése

**Fájlok:**
- Létrehozandó (generált): `work/en/chapters.json`, `work/en/<id>.md`, `work/en/<id>/cNN.md`, `work/en/<id>/manifest.json`
- Módosítandó: `STATUS.md`

- [ ] **1. lépés: Ellenőrizd, hogy megvan-e a forrás.** Futtatás: `test -s source/en/protocols.md && wc -w source/en/protocols.md`. Ha a fájl hiányzik: 🛑 **KAPU**, kérd el az embertől.

- [ ] **2. lépés: Nézd meg a címsorszinteket.** Futtatás: `grep -n '^#\{1,3\} ' source/en/protocols.md | head -120`

  Elvárt (a próbabontás alapján):
  - egyetlen `#` címsor van, a könyvcím;
  - a fejezetek `##` szintűek: Contents, Disclaimer, Dedication, Introduction, Chapter 1–7, Before You Turn the Last Page, Acknowledgments, About the Author, Notes, Index, Copyright;
  - a protokollok `###`, a „What to Do” / „How It Works” blokkok `####` szintűek.

  A 4. lépésben tehát `--level 2` kell; a borító és a könyvcím a `00-front` fejezetbe kerül. Ha a szerkezet ettől eltér, 🛑 **KAPU**: írd le az embernek, amit találtál, és javasolj bontási szintet.

- [ ] **3. lépés: Nézd meg a lábjegyzetformát.** Futtatás: `grep -c '^\[\^' source/en/protocols.md; grep -o '\[\^[^]]*\]' source/en/protocols.md | sort -u | wc -l`

  Elvárt: `1124` és `1124`.
  - A hivatkozások `[^i-1]`, `[^c1-1]` … formájúak.
  - A definíciók (`[^c1-1]: …`) mind a Notes fejezetben vannak, így a `footnotes` minta a hivatkozásokat és a definíciókat is számolja.

  Ha eltér, 🛑 **KAPU**.

- [ ] **4. lépés: Bontsd fejezetekre.** Futtatás: `python tools/split_chapters.py source/en/protocols.md work/en --level 2`

  Elvárt: 0-s kilépési kód, és a fejezetlista megfelel a 2. lépésnek.

- [ ] **5. lépés: Bontsd részletekre.** Futtatás: `python tools/chunker.py work/en --max-words 1800 --min-words 500`

  Elvárt: 188 részlet. A Notes fejezetben van egy kb. 13 700 szavas részlet, mert a lábjegyzet-definíciók között nincs üres sor. Ez rendben van, a Notes a D5 szerint angol marad. Minden más részlet 1850 szó alatt van.

- [ ] **6. lépés: Ellenőrizd a veszteségmentességet.** Futtatás:

```bash
python - <<'EOF'
import json, pathlib
root = pathlib.Path("work/en")
chs = json.loads((root / "chapters.json").read_text())
whole = "".join("".join((root / c["id"] / f"{k}.md").read_text(encoding="utf-8")
                        for k in json.loads((root / c["id"] / "manifest.json").read_text())["chunks"])
                for c in chs)
assert whole == pathlib.Path("source/en/protocols.md").read_text(encoding="utf-8"), "NEM veszteségmentes"
print("OK", len(chs), "fejezet")
EOF
```

  Elvárt: `OK <n> fejezet`

- [ ] **7. lépés: Töltsd ki a `STATUS.md`-t.** Minden fejezetnek legyen egy sora, a részletek oszlopában `0/<n>`. Az Index sorában jelöld: „kimarad (D6)”.

- [ ] **8. lépés: Commit**

```bash
git add work/en STATUS.md
git commit -m "editorial: forrás fejezetekre és részletekre bontva"
```

### 7. feladat: Szerkesztői ív (a felhasználó 1. lépése)

**Fájlok:**
- Létrehozandó: `editorial/arc.md`

**Interfészek:**
- Előállítja: az `editorial/arc.md` minden fejezetnek pontosan egy `## <chapter_id> – <cím>` szakaszt ad. Ezt a `pack.arc_section` olvassa.

- [ ] **1. lépés: Olvasd végig az egész angol könyvet** a `work/en/<id>.md` fájlokon át, fejezetenként. Közben jegyzetelj a 2. lépés sablonja szerint. A Notes és az Index fejezetnél csak a szerkezetet nézd.

- [ ] **2. lépés: Írd meg az `editorial/arc.md`-t** pontosan ezzel a szerkezettel:

```markdown
# A könyv szerkesztői íve

## Egész könyv
- **Tézis (3–5 mondat):** …
- **Olvasó:** …
- **A szerző hangja:** (5–8 jellemző, mindegyikhez egy rövid angol példamondat a könyvből és javasolt magyar megoldás)
- **Visszatérő motívumok és fogalmak:** (fogalom → mely fejezetekben → a jelentés röviden)
- **Kereszthivatkozások:** (táblázat: honnan [fejezet/részlet] → hová [protokoll vagy fejezet] → az eredeti szövegrész)
- **Nehéz helyek listája:** (szójáték, idióma, amerikai kulturális utalás, mértékegység, adag – fejezet/részlet szerint)

## <chapter_id> – <eredeti cím>
- **Szerepe az ívben:** (2–3 mondat: mit ad hozzá, mire épít, mit készít elő)
- **Fő állítások:** (felsorolás)
- **Protokollok:** (cím + 1 mondat mindegyikhez)
- **Kulcsfogalmak:** (angol → rövid jelentés; ha új terminus, jelöld: ÚJ)
- **Hangnem-megjegyzés:** …
- **Kapcsolódás a szomszédokhoz:** (az előző fejezet vége → e fejezet eleje; e fejezet vége → a következő eleje)
```

- [ ] **3. lépés: Gyűjtsd ki a terminusjelölteket.** Minden ÚJ jelölésű fogalom, amely még nincs a spec §8 táblázatában, kerüljön egy listába az `editorial/arc.md` végére, `## Terminusjelöltek` címmel (angol, előfordulásszám `grep -ci` alapján, fejezetek).

- [ ] **4. lépés: Ellenőrizd a lefedettséget.** Futtatás: `python tools/pack.py --check-arc`

  Elvárt: 0-s kilépési kód.

- [ ] **5. lépés: Commit**

```bash
git add editorial/arc.md STATUS.md
git commit -m "editorial: a könyv szerkesztői íve"
```

### 8. feladat: Stílusútmutató, szójegyzék, promptok – 🛑 döntési kapu

**Fájlok:**
- Létrehozandó: `editorial/style-guide.md`, `glossary/glossary.tsv`, `prompts/translate_chunk.md`, `prompts/chapter_plan.md`, `prompts/adjacent_review.md`, `prompts/final_review.md`, `prompts/second_opinion.md`, `work/questions/questions.jsonl`

- [ ] **1. lépés: Írd meg az `editorial/style-guide.md`-t.** Másold át bele szó szerint a spec §4, §5 és §6 szakaszát. Utána jöjjön egy `## Döntések` szakasz a spec §7 táblázatával; az állapot oszlopban egyelőre „JAVASLAT” áll. A végére kerüljön egy `## Hangminták` szakasz az `editorial/arc.md` „A szerző hangja” pontjából.

- [ ] **2. lépés: Hozd létre a `glossary/glossary.tsv`-t.** Fejléc: `en	hu	hu_match	status	forbidden	note`. Legyen benne a spec §8 minden sora és a 7. feladat terminusjelöltjei, mind `status=proposed` állapotban.

  A `hu_match` a magyar alak toldalékolás közben is változatlan eleje. Példák:
  - kortizol → `kortizol`
  - fiziológiai sóhaj → `fiziológiai sóhaj`
  - zóna → `zón` (mert zónát, zónában)

  A `forbidden` a tipikus rossz változatok listája, pl. `élettani sóhaj`.

- [ ] **3. lépés: Hozd létre a promptokat** pontosan ezzel a tartalommal.

`prompts/translate_chunk.md`:

```markdown
Te a könyv magyar fordítója vagy. Egyetlen részletet fordítasz: {{chapter_id}} / {{chunk_id}}.

KIMENET: írd a teljes magyar fordítást ide: {{hu_path}} – csak a lefordított Markdownt, semmi mást.

Háromszor menj végig a szövegen, sorrendben:

1. NYERSFORDÍTÁS. Fordítsd le a FORDÍTANDÓ SZÖVEG-et a STÍLUSÚTMUTATÓ és a SZÓJEGYZÉK szerint. Az approved terminusok kötelezők, a proposed terminusokat használd, hacsak nem találsz jobbat. Ha jobbat találsz, vedd fel kérdésként (lásd lent). Tartsd meg a Markdown-szerkezetet: címszintek, listák, lábjegyzetjelek, linkek, kiemelések. Az ELŐZŐ RÉSZLET VÉGE (HU) szövegéhez csatlakozz stílusban és terminológiában.
2. HIDEG OLVASÁS. Most csak a magyar szöveget olvasd, mintha eredeti magyar könyv volna. Minden mondatot, amely fordításízű, írj át a stílusútmutató §5 táblázata szerint: névelő, birtokos névmás, szenvedő szerkezet, szórend, anglicizmus, túl hosszú mondat. A hangnem legyen közvetlen, lelkes, magyarázó (lásd: A KÖNYV ÍVE).
3. EGYEZTETÉS. Menj végig bekezdésről bekezdésre az angol és a magyar szövegen. Ellenőrizd: van-e kihagyott vagy betoldott mondat; ugyanaz-e a jelentés; megmaradt-e az óvatossági fok (may → -hat/-het) és a tagadás; minden szám, adag és mértékegység helyes-e (az átváltás a döntések szerint); kiemelés és lábjegyzetjel a helyén van-e.

KÉTES PONT esetén ne állj meg. Válaszd a legjobb megoldást, a mondat végére tegyél egy `<!-- Q:Q-NNNN -->` jelölőt, és vedd fel a kérdést:
python tools/questions.py add --chapter {{chapter_id}} --chunk {{chunk_id}} --category <term|meaning|register|culture|safety|style|fact|other> --severity <low|medium|high> --route <agent|model|human> --question "…" --en "…" --hu-current "…" --option "…" --option "…" --recommendation "…"
Az útvonal szabályai a stílusútmutatóban vannak (spec §9). Adagnál, gyógyszernél, figyelmeztetésnél mindig: safety / high / human.

TILOS: összefoglalni, kihagyni, magyarázatot vagy fordítói megjegyzést betoldani, a tudományos tartalmat „javítani”.

A végén futtasd: python tools/check.py pair work/en/{{chapter_id}}/{{chunk_id}}.md {{hu_path}}
A FAIL-okat javítsd. Mértékegység-átváltásnál a számkivételt vedd fel a work/checks/number-exceptions.tsv fájlba (hu_file, number, reason: „°F→°C: 65→18”). A WARN-okat javítsd, vagy egy mondattal indokold a work/reports/checks/{{chapter_id}}.notes.md fájlban.
```

`prompts/chapter_plan.md`:

```markdown
Készíts fordítási tervet ehhez a fejezethez: {{chapter_id}}. Bemenet: work/en/{{chapter_id}}.md, editorial/arc.md (a fejezet szakasza), glossary/glossary.tsv, editorial/style-guide.md.
Kimenet: work/plans/{{chapter_id}}.md, pontosan ezekkel a szakaszokkal:
## Szerep az ívben (2–3 mondat)
## Részlettérkép (a manifest minden cNN-jéhez: 1 mondat tartalom | kulcsterminusok | kockázatos helyek)
## Új terminusok (angol | javasolt magyar | előfordulás | indoklás) → vedd fel őket proposed állapotban a szójegyzékbe
## Idiómák és kulturális utalások (hely | eredeti | javasolt megoldás)
## Számok, mértékegységek, adagok (hely | eredeti | magyar alak / átváltás)
## Kereszthivatkozások (hely | cél | magyar alak a D3 döntés szerint)
## Hangnem (mire figyelj ebben a fejezetben)
## Nyitott kérdések (amit már most fel kell venni a questions.py-val – az azonosítókkal)
```

`prompts/adjacent_review.md`:

```markdown
Vesd össze két szomszédos, lefordított fejezetet: {{a}} → {{b}}. Bemenet: work/hu/{{a}}.md, work/hu/{{b}}.md, a két angol megfelelő, editorial/arc.md, glossary/glossary.tsv.
Ellenőrizd:
1. ÁTKÖTÉS: az {{a}} vége és a {{b}} eleje ugyanazt a gondolatmenetet folytatja-e, stílusban is.
2. VISSZATÉRŐ FOGALMAK: mindkét fejezetben szereplő fogalmak ugyanúgy szólnak-e, és ugyanúgy vannak-e magyarázva. (grep a szójegyzék angol terminusaira mindkét angol fejezetben.)
3. KERESZTHIVATKOZÁSOK: minden hivatkozás, amely a másik fejezetre vagy egy protokollra mutat, a cél pontos magyar címét használja-e.
4. HANGNEM ÉS REGISZTER: a tegezés/magázás és a hangnem egységes-e.
5. ISMÉTLŐDŐ MONDATOK: ugyanaz az angol mondat vagy fordulat (pl. protokollcímke) azonos-e magyarul.
A javításokat MINDIG a részletfájlokban (work/hu/<id>/cNN.md) végezd, utána futtasd újra: python tools/assemble.py chapter <id>.
Kimenet: work/review/adjacent/{{a}}__{{b}}.md
## Összefoglaló (3–5 mondat)
## Eltérések (táblázat: # | fájl:részlet | probléma | javítás | állapot [javítva / kérdés Q-NNNN])
## Módosított fájlok
```

`prompts/final_review.md`:

```markdown
Végső angol–magyar lektorálás: {{chapter_id}}. Bemenet: a manifest minden részletpárja (work/en/{{chapter_id}}/cNN.md ↔ work/hu/{{chapter_id}}/cNN.md), a stílusútmutató, a szójegyzék, a work/checks/number-exceptions.tsv.
Menj végig részletenként, és azon belül bekezdésenként. Hibakategóriák: kihagyás, betoldás, félrefordítás, óvatossági fok, tagadás, szám/adag/mértékegység, terminus, regiszter, magyartalanság, formázás.
Minden találatnál:
- ha az útvonal agent (spec §9): javítsd a részletfájlban;
- különben: questions.py add a megfelelő útvonallal + jelölő a szövegben.
Kimenet: work/review/final/{{chapter_id}}.md
## Összefoglaló (a talált hibák száma kategóriánként)
## Találatok (táblázat: # | részlet | kategória | EN | HU előtte | HU utána | állapot)
## Biztonsági mondatok (MINDEN mondat, amelyben adag, gyógyszer, kiegészítő, figyelmeztetés vagy ellenjavallat van: részlet | EN | HU | ✔ / Q-NNNN)
## Mértékegység-átváltások (a number-exceptions.tsv minden, ehhez a fejezethez tartozó sora: eredeti | átváltott | ✔ helyes / hibás)
```

`prompts/second_opinion.md`:

```markdown
Tapasztalt magyar szakfordító és lektor vagy (ismeretterjesztő, egészségtudományi könyvek). Egy angolból magyarra készülő fordítás egyetlen kétes pontjáról kérek véleményt. A könyv: Andrew Huberman: Protocols. A regiszter: lásd a döntéseket (tegezés/magázás). Stílus: közvetlen, lelkes, magyarázó, magyar ismeretterjesztő próza.

{{question_block}}

Válaszolj így:
1. Melyik opciót választod (vagy adj újat)?
2. Indoklás (legfeljebb 5 mondat).
3. Biztosság: alacsony / közepes / magas.
4. Ha mást is érint a döntés (más terminus, más fejezet), jelezd.
```

- [ ] **4. lépés: Vedd fel a döntési kérdéseket.** A spec §7 minden döntésére (D1–D8), valamint a szójegyzék minden NYITOTT és minden új terminusára, amely legalább 5-ször előfordul, futtass egy `python tools/questions.py add … --route human` parancsot. A D-kérdéseknél a kategória `register` vagy `other`. Az opciók a spec szerinti alternatívák, a javaslat a spec alapértelmezése.

- [ ] **5. lépés: Exportáld a kérdéseket.** Futtatás: `python tools/questions.py export`

  Elvárt: a `work/questions/for-human.md` minden D1–D8 kérdést tartalmaz.

- [ ] **6. lépés: Commit**

```bash
git add editorial glossary prompts work/questions
git commit -m "editorial: stílusútmutató, szójegyzék, promptok, döntési kérdések"
```

- [ ] **7. lépés: 🛑 KAPU – döntési kapu.** Jelezd az embernek: „Kérlek, töltsd ki a `Döntés:` sorokat a `work/questions/for-human.md`-ben (betű vagy saját szöveg), és mentsd el `work/questions/decisions.md` néven.” Várj.

- [ ] **8. lépés: Emeld be a döntéseket.** Futtatás: `python tools/questions.py import work/questions/decisions.md`

  Vezesd át a döntéseket:
  - `style-guide.md` → a `## Döntések` állapot oszlopában „ELFOGADVA” és a végleges érték;
  - `glossary.tsv` → a döntött terminusok `approved` állapotba kerülnek, a végleges magyar alakkal és `hu_match`-csel.

- [ ] **9. lépés: Commit**

```bash
git add editorial glossary work/questions
git commit -m "editorial: emberi döntések átvezetve"
```

### 9. feladat: Pilot – 🛑 kalibrációs kapu

**Fájlok:**
- Létrehozandó: `work/plans/<az 1. fejezet id-ja>.md`, `work/hu/<az 1. fejezet id-ja>/<az 1. alvásprotokoll részletei>.md`, `work/review/pilot.md`

- [ ] **1. lépés: Készítsd el az 1. fejezet (Protocols for Sleep) fejezettervét** a `prompts/chapter_plan.md` szerint. Ez egyben a 10. feladat első lépése is.

- [ ] **2. lépés: Fordítsd le az „1. alvásprotokoll” (View Sunlight as Soon as Possible After Waking) összes részletét** a szabványos fejezeteljárás (lásd C. szakasz) 2–6. lépése szerint.

- [ ] **3. lépés: Írd meg a `work/review/pilot.md`-t.** Tartalma:
  - 3 olyan bekezdés angol–magyar párban, amelyben a legtöbb stílusdöntést hoztad;
  - a felvett kérdések listája;
  - a `check.py` eredménye.

  Commitold: `git commit -m "hu: pilot – 1. alvásprotokoll"`.

- [ ] **4. lépés: 🛑 KAPU – kalibráció.** Kérd meg az embert (vagy az általa kijelölt második modellt), hogy olvassa el a pilot fordítást, és írja a `work/review/pilot.md` végére, mi nem tetszik. Várj.

- [ ] **5. lépés: Vezesd át a visszajelzést.** Minden általánosítható megjegyzés kerüljön új sorként a `style-guide.md` §5 táblázatába (rossz → jó példával). A pilot részleteit javítsd, majd commitold: `git commit -m "editorial: pilot-visszajelzés átvezetve"`.

---

# C. SZAKASZ – Fordítás fejezetenként (a felhasználó 2. lépése)

## Szabványos fejezeteljárás (SZFE)

Minden fordítási feladat (10–17.) ezt hajtja végre a saját fejezet-azonosítóival. A `<id>` a `work/en/chapters.json` azonosítója.

1. **Fejezetterv:** a `prompts/chapter_plan.md` alapján megírod a `work/plans/<id>.md`-t. Ellenőrzés: minden részletazonosító szerepel benne. Futtatás:
   ```bash
   python -c "import json,sys;m=json.load(open('work/en/<id>/manifest.json'));t=open('work/plans/<id>.md',encoding='utf-8').read();miss=[c for c in m['chunks'] if c not in t];print('hiányzik:',miss);sys.exit(bool(miss))"
   ```
   Elvárt: `hiányzik: []`. Commit: `hu(<id>): fejezetterv`.
2. **Csomag:** `python tools/pack.py <id> cNN`
3. **Fordítás friss munkamenetben:** egy új Codex-munkamenet (pl. `codex exec`) bemenete a `work/packs/<id>/cNN.md` tartalma. A munkamenet a csomag FELADAT része szerint három menetben dolgozik, és a `work/hu/<id>/cNN.md` fájlba ír. Egy munkamenet = egy részlet.
4. **Gépi ellenőrzés:** `python tools/check.py pair work/en/<id>/cNN.md work/hu/<id>/cNN.md`. Elvárt: 0-s kilépési kód, azaz nincs FAIL.
5. **Részletcommit:** `git add work/hu/<id>/cNN.md work/questions work/checks work/reports && git commit -m "hu(<id>): cNN"`. Frissítsd a `STATUS.md` részletszámlálóját.
6. **Ismétlés:** a 2–5. lépés a manifest minden részletére, sorrendben (az előző magyar részlet végét a csomag már tartalmazza).
7. **Fejezet összefűzése:** `python tools/assemble.py chapter <id>`, utána `python tools/check.py chapter <id>`. Elvárt: 0-s kilépési kód; a `work/reports/checks/<id>.txt` minden WARN-ja javítva, vagy indokolva a `<id>.notes.md`-ben.
8. **Varratok olvasása:** olvasd el a teljes `work/hu/<id>.md`-t egyben. Különösen figyelj minden részlethatár előtti és utáni 2 bekezdésre: ismétlődés, megszakadt gondolat, eltérő terminus. A javítás a részletfájlban történik, utána jön újra a 7. lépés.
9. **Szójegyzék véglegesítése:** a fejezetben felvett `proposed` terminusok közül:
   - amelyik `agent` útvonalú, azt az agent véglegesíti (`approved`);
   - amelyikhez emberi kérdés tartozik, az `proposed` marad.

   Ha egy terminus végleges alakja eltér a már használttól, keresd meg: `grep -rn "<régi alak>" work/hu/`. Javítsd minden korábbi részletben, és futtasd újra az érintett fejezetek 7. lépését.
10. **Agent-kérdések lezárása:** `python tools/questions.py list --open --route agent`. Mindegyiket döntsd el, zárd le a `resolve … --by agent` paranccsal, és vezesd át a szövegbe (a jelölő maradhat, az `assemble.py book` törli). A `model` útvonalú kérdéseknél futtasd a `packet` parancsot; ha elérhető második modell, add oda neki a csomagot, a válaszát rögzítsd `resolve … --by model:<név>` formában, és vezesd át. Ha nem elérhető, a kérdés nyitva marad a 21. feladatig.
11. **Lezárás:** `STATUS.md` → a Terv és az Ellenőrzés oszlopba ✔. Commit: `hu(<id>): fejezet kész`.

### 10. feladat: 1. fejezet – Protocols for Sleep (15 protokoll)
- [ ] **1. lépés:** SZFE 1–11. A fejezetterv és az 1. alvásprotokoll a pilotból már megvan. A részleteit csak akkor fordítsd újra, ha a pilot-visszajelzés ezt kéri.
- [ ] **2. lépés:** Ellenőrizd a speciális pontokat:
  - a 9. és 10. alvásprotokoll (kiegészítők, altatók) minden adagmondata `safety` kérdés vagy ✔ a tervben;
  - az 1. és 15. alvásprotokoll a jet lagről a D2 szerint vált mértékegységet és időt.

### 11. feladat: Címoldal (`00-front`), Contents, Disclaimer, Dedication, Introduction
- [ ] **1. lépés:** SZFE 1–11 minden érintett fejezetre.
  - A Disclaimer jogi szöveg: pontos, semleges nyelvezet; eltérés esetén `safety`/`human` kérdés.
  - A Contents fejezetben csak a link szövegét fordítsd. A `](#…)` horgonyok ekkor még angolul maradnak, a 19. feladat 4. lépése igazítja őket.
- [ ] **2. lépés:** A címoldalon a D7 szerinti cím szerepeljen.

### 12. feladat: 2. fejezet – Protocols for Exercise (4 protokoll)
- [ ] **1. lépés:** SZFE 1–11. Különösen figyelj a mértékegységekre (font, mérföld) és a pulzus- és ismétlésszámokra.

### 13. feladat: 3. fejezet – Protocols for Stress Control (6 protokoll)
- [ ] **1. lépés:** SZFE 1–11. A hidegterhelés hőmérsékleteinél (°F→°C) szerepeljen átváltási napló. A kiegészítők adagjai `safety` kategóriába tartoznak.

### 14. feladat: 4. fejezet – Protocols for Nutrition (7 protokoll)
- [ ] **1. lépés:** SZFE 1–11. A „CP:C ratio” definícióját a fejezet első előfordulásánál rögzítsd a szójegyzékben. Az élelmiszernevek magyar köznévi alakban szerepeljenek; az amerikai terméknevek `culture` kérdések.

### 15. feladat: 5. fejezet – Protocols for Light (5 protokoll)
- [ ] **1. lépés:** SZFE 1–11. A hullámhosszak (nm) és a fényerősség (lux) számai változatlanok maradnak.

### 16. feladat: 6. fejezet – Protocols for Focus, Motivation, and Learning (6 protokoll)
- [ ] **1. lépés:** SZFE 1–11.

### 17. feladat: 7. fejezet – Protocols for Personal Growth (4 protokoll) és a hátsó rész
- [ ] **1. lépés:** SZFE 1–11 a 7. fejezetre. James Hollis könyveinek magyar kiadását `fact` kérdésként ellenőrizd.
- [ ] **2. lépés:** SZFE 1–11 a Before You Turn the Last Page, az Acknowledgments és az About the Author fejezetre. A köszönetnyilvánításban a személynevek változatlanok.
- [ ] **3. lépés:** Notes (D5): csak a fejezetcímeket (`### Chapter 1: …`) és a bevezető bekezdést („A note to the reader about the references…”) fordítsd. A `[^…]: …` definíciós sorok szó szerint maradnak, a fordításukhoz nem kell csomagot készíteni. A struktúraellenőrzésnek ennél a fejezetnél is 0 FAIL-lel kell lefutnia.
- [ ] **4. lépés:** Copyright (D8): az angol szöveg marad, fölé kerül egy magyar megjegyzés: „Nem hivatalos, személyes használatra készült fordítás.” Az Index a D6 szerint kimarad.

---

# D. SZAKASZ – Szomszédos fejezetek (a felhasználó 3. lépése)

### 18. feladat: Szomszédos fejezetpárok összevetése

**Fájlok:**
- Létrehozandó: `work/review/adjacent/<A>__<B>.md` minden szomszédos párra
- Módosítandó: az érintett `work/hu/<id>/cNN.md` fájlok

- [ ] **1. lépés: Írd meg a `book/manifest.txt`-t.** Soronként egy fejezet-azonosító a könyv sorrendjében, a `chapters.json` alapján. A Notes `en:` előtaggal akkor szerepel, ha a D5 szerint teljesen angol maradt; egyébként előtag nélkül. Az Index nem szerepel (D6). A párok a manifest egymást követő, nem `en:` előtagú sorai. Commit.

- [ ] **2. lépés: Nézd végig minden párt** a `prompts/adjacent_review.md` szerint, sorrendben (Introduction → 1. fejezet, 1. → 2. fejezet, …, 7. fejezet → Before You Turn the Last Page).

  Minden pár után:
  - `python tools/assemble.py chapter <A>` és `python tools/assemble.py chapter <B>`
  - `python tools/check.py chapter <A>` és `python tools/check.py chapter <B>` → elvárt: 0-s kilépési kód
  - commit: `review: szomszéd <A>__<B>`

- [ ] **3. lépés: Futtass egy teljes könyvre kiterjedő konzisztencia-keresést.** A szójegyzék minden `approved` sorára, amelynek van `forbidden` változata:

```bash
python - <<'EOF'
import pathlib, sys
sys.path.insert(0, "tools")
from check import load_glossary
bad = 0
for t in load_glossary(pathlib.Path("glossary/glossary.tsv")):
    for f in t.forbidden:
        for p in pathlib.Path("work/hu").glob("*/c*.md"):
            if f and f.lower() in p.read_text(encoding="utf-8").lower():
                print(p, "→", f); bad += 1
sys.exit(bad > 0)
EOF
```

  Elvárt: nincs kimenet, 0-s kilépési kód.

- [ ] **4. lépés:** A `STATUS.md` „Szomszéd-összevetés” oszlopába ✔ minden fejezetnél. Commit: `review: szomszédos fejezetek kész`.

---

# E. SZAKASZ – Összefűzés (a felhasználó 4. lépése)

### 19. feladat: A könyv összeállítása

**Fájlok:**
- Létrehozandó: `book/protocols-hu.md`

- [ ] **1. lépés: Fűzd össze a fejezeteket.** Futtatás: `for id in $(grep -v '^en:' book/manifest.txt); do python tools/assemble.py chapter "$id" || exit 1; done`

  Elvárt: 0-s kilépési kód.

- [ ] **2. lépés: Állítsd össze a könyvet.** Futtatás: `python tools/assemble.py book`

  Elvárt:
  - ha maradt nyitott jelölő, a parancs kilistázza őket és 1-gyel lép ki: ez ebben a fázisban még várható, a 21. feladat zárja le őket;
  - a könyvfájl akkor jön létre, ha nincs nyitott jelölő.

  Ha van nyitott jelölő, a 21. feladat után ismételd meg ezt a lépést.

- [ ] **3. lépés: Ellenőrizd a kereszthivatkozásokat.** Futtatás: `grep -noE '[0-9]+\. [a-záéíóöőúüű-]*protokoll' work/hu/*.md | sort | uniq -c`

  Minden találat egy létező protokollcímre mutasson. Vesd össze az `editorial/arc.md` kereszthivatkozás-táblázatával. Minden angol „Protocol N” hivatkozásnak legyen magyar párja: `grep -c 'Protocol [0-9]' work/en/<id>.md` ≈ a magyar találatok száma fejezetenként. Az eltéréseket javítsd a részletfájlban. Commit: `book: kereszthivatkozások`.

- [ ] **4. lépés: Fejezetcímek és tartalomjegyzék.** Futtatás: `grep -n '^#\{1,2\} ' book/protocols-hu.md` (vagy nyitott jelölők esetén a `work/hu/*.md` fájlokon).

  Elvárt:
  - minden címsor magyar, mondatszerű nagybetűzéssel (spec §6);
  - a protokollcímek a D3 formájúak;
  - a Contents fejezet tételei szó szerint megegyeznek a címsorokkal.

  Utána igazítsd a horgonyokat: a Contents részletfájljaiban minden `](#…)` célja a hozzá tartozó magyar címsor GitHub-stílusú horgonya legyen. Ellenőrzés (ha nincs kimenet, rendben van):

```bash
python - <<'PY'
import re, pathlib
book = pathlib.Path("book/protocols-hu.md").read_text(encoding="utf-8")
slug = lambda h: re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
anchors = {slug(m) for m in re.findall(r"^#{1,6} (.+)$", book, re.M)}
for a in re.findall(r"\]\(#([^)]+)\)", book):
    if a not in anchors: print("törött horgony:", a)
PY
```

  Commit: `book: összefűzés`.

---

# F. SZAKASZ – Végső lektorálás (a felhasználó 5. lépése)

### 20. feladat: Végső angol–magyar összevetés fejezetenként

**Fájlok:**
- Létrehozandó: `work/review/final/<id>.md` minden fordított fejezetre
- Módosítandó: `work/hu/<id>/cNN.md`, `work/questions/questions.jsonl`

- [ ] **1. lépés: Lektorálj minden fejezetet** a `book/manifest.txt` sorrendjében, a `prompts/final_review.md` szerint, **friss munkamenetben fejezetenként**. Ha egy fejezet nem fér el egy munkamenetben, vedd részletenként, de a jelentés fejezetenként egy.

- [ ] **2. lépés: Ellenőrzés és commit fejezetenként.**
  - `python tools/assemble.py chapter <id> && python tools/check.py chapter <id>` → elvárt: 0-s kilépési kód
  - a jelentés „Biztonsági mondatok” és „Mértékegység-átváltások” tábláiban minden sor ✔ vagy Q-azonosító
  - commit: `review: végső lektorálás <id>`

- [ ] **3. lépés:** `STATUS.md` → a „Végső lektorálás” oszlopba ✔.

### 21. feladat: A kérdések lezárása – 🛑 emberi kapu

- [ ] **1. lépés: Agent-kérdések.** `python tools/questions.py list --open --route agent` → mindet döntsd el, és zárd le a `resolve … --by agent` paranccsal.

- [ ] **2. lépés: Modell-kérdések.** `python tools/questions.py list --open --route model` → mindegyikre futtasd a `packet` parancsot, majd add a második modellnek. Ha a modell válasza „magas” biztosságú, és nem mond ellent a javaslatodnak, zárd le (`--by model:<név>`). Ha ellentmond, és a súly `high`: állítsd át az útvonalat `human`-re, a `questions.jsonl`-ban a `route` mezőt szerkesztve.

- [ ] **3. lépés: Exportáld az emberi kérdéseket, és commitolj.** `python tools/questions.py export`, majd `git commit -m "review: nyitott kérdések az embernek"`.

- [ ] **4. lépés: 🛑 KAPU.** Kérd meg az embert, hogy töltse ki a `Döntés:` sorokat, és mentse el `work/questions/decisions.md` néven (felülírva a régit). Várj.

- [ ] **5. lépés: Emeld be és vezesd át a döntéseket.**
  - `python tools/questions.py import work/questions/decisions.md`
  - minden lezárt kérdés döntését vezesd át a részletfájlban: a szövegcsere után a jelölő maradhat, az `assemble.py book` törli
  - ha a döntés terminus, frissítsd a szójegyzéket, és futtasd újra a 18. feladat 3. lépését

- [ ] **6. lépés: Ellenőrizd, hogy nem maradt nyitott kérdés.** Futtatás: `python tools/questions.py list --open`

  Elvárt: üres lista. Ha nem az, ismételd a 21. feladatot.

- [ ] **7. lépés: Commit.** `git commit -m "review: kérdések lezárva"`

### 22. feladat: Átvétel

- [ ] **1. lépés: Állítsd össze a könyvet.** Futtatás: `python tools/assemble.py book`

  Elvárt: 0-s kilépési kód, és létrejön a `book/protocols-hu.md`.

- [ ] **2. lépés: Futtasd a teljes gépi ellenőrzést.** Futtatás: `python -m pytest -q && for id in $(grep -v '^en:' book/manifest.txt); do python tools/check.py chapter "$id" || exit 1; done`

  Elvárt: 36 passed, és minden fejezet 0-s kilépési kóddal fut le.

- [ ] **3. lépés: Ellenőrizd, hogy nem maradt jelölő.** Futtatás: `grep -c '<!-- Q:' book/protocols-hu.md`

  Elvárt: `0`.

- [ ] **4. lépés:** A `STATUS.md` minden sora ✔; a sorok alá kerüljön egy összefoglaló:
  - részletek száma;
  - kérdések száma útvonalanként (agent / model / human);
  - a könyv szószáma (`wc -w`) és az angol forrásé.

- [ ] **5. lépés: Commit.** `git commit -m "book: magyar fordítás kész"`, majd értesítsd az embert.
