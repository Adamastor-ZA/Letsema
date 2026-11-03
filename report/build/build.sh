#!/usr/bin/env bash
# Build the final report: render figures, assemble the docx (two passes for the contents pages), convert to PDF.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/../outputs"
export NODE_PATH="$(npm root -g)"
mkdir -p "$OUT" "$HERE/assets/png"

if [ -d "$HERE/assets/svg" ] && ls "$HERE/assets/svg"/*.svg >/dev/null 2>&1; then
  node "$HERE/render_svg.js" "$HERE/assets/svg" "$HERE/assets/png" 2
fi

NAME="${1:-Unlocking_Tourism_Growth_Final_Report_DRAFT_v1}"

# Pass 1: build without page numbers in the contents, convert, scan headings.
node "$HERE/report.js" --out "$OUT/$NAME.docx" --pass 1
(cd "$OUT" && timeout 600 soffice --headless --convert-to pdf "$NAME.docx" >/dev/null 2>&1)
node "$HERE/scan_pages.js" "$OUT/$NAME.pdf" "$HERE/pagemap.json"

# Pass 2: rebuild with the page map, convert again.
node "$HERE/report.js" --out "$OUT/$NAME.docx" --pass 2 --pagemap "$HERE/pagemap.json"
(cd "$OUT" && timeout 600 soffice --headless --convert-to pdf "$NAME.docx" >/dev/null 2>&1)
pdfinfo "$OUT/$NAME.pdf" | grep Pages
echo "built $OUT/$NAME.docx and .pdf"
