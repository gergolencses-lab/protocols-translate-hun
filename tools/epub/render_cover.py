"""book/epub/cover/cover.html → book/epub/cover/cover.jpg (1600×2560, Chromium)."""
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "book/epub/cover/cover.html"
DST = ROOT / "book/epub/cover/cover.jpg"
CHROMIUM = os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium")


def main() -> None:
    with sync_playwright() as p:
        kw = {"executable_path": CHROMIUM} if Path(CHROMIUM).exists() else {}
        browser = p.chromium.launch(**kw)
        page = browser.new_page(viewport={"width": 1600, "height": 2560})
        page.goto(SRC.as_uri())
        page.wait_for_timeout(300)
        page.screenshot(path=str(DST), type="jpeg", quality=90, full_page=False)
        browser.close()
    print(DST)


if __name__ == "__main__":
    main()
