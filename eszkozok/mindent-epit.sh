#!/usr/bin/env bash
# Mindent újraépít és ellenőriz: borító → EPUB (+ EPUBCheck, verify) → PDF (+ qa) → tesztek.
# Az első hibánál megáll.
# Használat: EPUBCHECK_JAR=/út/epubcheck.jar bash eszkozok/mindent-epit.sh [--borito-nelkul]
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ "${1:-}" != "--borito-nelkul" ]]; then
  echo "== Borító"
  python3 eszkozok/borito/render_cover.py
fi

echo "== EPUB"
bash eszkozok/epub/build.sh

echo "== PDF"
python3 eszkozok/pdf/build_pdf.py
python3 eszkozok/pdf/qa.py

echo "== Tesztek"
python3 -m pytest -q eszkozok/tesztek

echo "== Kész: 1-kesz-konyv/"
ls -l 1-kesz-konyv/
