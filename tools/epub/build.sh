#!/usr/bin/env bash
# Protokollok EPUB: book/protocols-hu.md → dist/protokollok.epub, EPUBCheckkel.
# Használat: bash tools/epub/build.sh [--no-soft-hyphens]
# Környezet: EPUBCHECK_JAR=/út/epubcheck.jar (ha nincs megadva, a validálás kimarad, hibával jelezve)
set -euo pipefail
cd "$(dirname "$0")/../.."

python3 tools/epub/prepare.py book/protocols-hu.md build/epub/protokollok.md "$@"
mkdir -p dist
pandoc build/epub/protokollok.md \
  -f markdown-smart-implicit_figures -t epub3 \
  --metadata-file book/epub/metadata.yaml \
  --shift-heading-level-by=-1 --split-level=2 \
  --toc --toc-depth=2 \
  --lua-filter tools/epub/filters/chapter.lua \
  --lua-filter tools/epub/filters/protocol.lua \
  --lua-filter tools/epub/filters/sidebar.lua \
  --resource-path=book \
  -o dist/protokollok.epub
ls -l dist/protokollok.epub

if [[ -z "${EPUBCHECK_JAR:-}" ]]; then
  echo "HIBA: EPUBCHECK_JAR nincs beállítva, a validálás kimaradt." >&2
  exit 2
fi
java -jar "$EPUBCHECK_JAR" dist/protokollok.epub
python3 tools/epub/verify.py dist/protokollok.epub
