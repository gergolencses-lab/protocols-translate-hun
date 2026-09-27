#!/usr/bin/env bash
# Protokollok EPUB: 2-szoveg/magyar/protokollok.md → 1-kesz-konyv/protokollok.epub, EPUBCheckkel.
# Használat: bash eszkozok/epub/build.sh [--no-soft-hyphens]
# Környezet: EPUBCHECK_JAR=/út/epubcheck.jar (ha nincs megadva, a validálás kimarad, hibával jelezve)
set -euo pipefail
cd "$(dirname "$0")/../.."

python3 eszkozok/kozos/prepare.py 2-szoveg/magyar/protokollok.md build/epub/protokollok.md "$@"
mkdir -p 1-kesz-konyv
pandoc build/epub/protokollok.md \
  -f markdown-smart-implicit_figures -t epub3 \
  --metadata-file 3-kinezet/epub/metadata.yaml \
  --shift-heading-level-by=-1 --split-level=2 \
  --toc --toc-depth=2 \
  --lua-filter eszkozok/kozos/szurok/chapter.lua \
  --lua-filter eszkozok/kozos/szurok/protocol.lua \
  --lua-filter eszkozok/kozos/szurok/sidebar.lua \
  --lua-filter eszkozok/kozos/szurok/pseudohead.lua \
  --resource-path=2-szoveg/magyar \
  -o 1-kesz-konyv/protokollok.epub
ls -l 1-kesz-konyv/protokollok.epub

if [[ -z "${EPUBCHECK_JAR:-}" ]]; then
  echo "HIBA: EPUBCHECK_JAR nincs beállítva, a validálás kimaradt." >&2
  exit 2
fi
java -jar "$EPUBCHECK_JAR" 1-kesz-konyv/protokollok.epub
python3 eszkozok/epub/verify.py 1-kesz-konyv/protokollok.epub
