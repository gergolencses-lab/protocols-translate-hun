from prepare import nbsp_units, remove_sections, soft_hyphenate, strip_front, unwrap_notes_section

NB, SHY = " ", "­"


def test_strip_front():
    md = "![b](images/cover.jpeg)\n\n# Protokollok\n\n*al*\n\n## Jogi nyilatkozat\nX\n"
    assert strip_front(md) == "## Jogi nyilatkozat\nX\n"


def test_remove_sections():
    md = "## A\na\n## Tartalom\n- [x](#x)\n## B\nb\n## Index\n- i\n"
    assert remove_sections(md, ["Tartalom", "Index"]) == "## A\na\n## B\nb\n"


def test_unwrap_notes_keeps_definitions_only():
    md = "## Z\nz[^c1-1]\n## Jegyzetek\n\nBevezető.\n\n### 1. fejezet: X\n\n[^c1-1]: Ref.\n## Index\n"
    out = unwrap_notes_section(md)
    assert "[^c1-1]: Ref." in out
    assert "Jegyzetek" not in out and "Bevezető" not in out and "### 1. fejezet" not in out
    assert out.startswith("## Z\nz[^c1-1]\n") and "## Index" in out


def test_nbsp_units():
    assert nbsp_units("Vegyél be 10 mg-ot, 18 °C, 1. alvásprotokoll.") == (
        f"Vegyél be 10{NB}mg-ot, 18{NB}°C, 1.{NB}alvásprotokoll."
    )
    assert nbsp_units("Legalább 90 % és 2,5 g.") == f"Legalább 90{NB}% és 2,5{NB}g."
    assert nbsp_units("[^c1-1]: Vol. 10 m 5 g") == "[^c1-1]: Vol. 10 m 5 g"
    assert nbsp_units("Lásd [itt](https://x.hu/10 mg)") == "Lásd [itt](https://x.hu/10 mg)"


def test_soft_hyphenate_roundtrip_and_skips():
    src = (
        "A testmaghőmérsékletedet csökkentsd. Az étrend-kiegészítőket is.\n"
        "### Hosszúhosszúcímsorszó\n"
        "[x](https://example.com/nagyonhosszuutvonal)\n"
        "[^c1-1]: Neuroplasticity references.\n"
        "![Fejezetembléma](images/chapter-emblem.jpeg)\n"
    )
    out = soft_hyphenate(src)
    lines = out.split("\n")
    assert out.replace(SHY, "") == src
    assert SHY in lines[0]
    assert "-" + SHY not in out and SHY + "-" not in out
    assert all(SHY not in line for line in lines[1:])


def test_soft_hyphenate_short_words_untouched():
    assert soft_hyphenate("Egy rövid mondat.\n") == "Egy rövid mondat.\n"


def test_soft_hyphenate_never_changes_letters():
    # A pyphen hu_HU a hosszú mássalhangzót helyesírás szerint bontja
    # (alátámassza → alátámasz-sza); lágy elválasztójelnél ez a szót rontaná el.
    src = "Ez alátámassza, hogy a meggyőződésünk visszaállítható.\n"
    out = soft_hyphenate(src)
    assert out.replace(SHY, "") == src
    assert SHY in out
