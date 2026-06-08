#!/bin/bash
set -e
export HOME=/tmp/lohome TMPDIR=/tmp/lotmp
PPTX="${1:-Big-Data-and-Databricks-Training.pptx}"
pkill -9 soffice 2>/dev/null || true; sleep 1
rm -rf /tmp/loconv && mkdir -p /tmp/loconv build
timeout 200 soffice --headless --invisible --norestore --nologo \
  -env:UserInstallation=file:///tmp/loconv \
  --convert-to pdf --outdir build "$PPTX" >/dev/null 2>&1
PDF="build/$(basename "${PPTX%.pptx}").pdf"
python3 - "$PDF" <<'PY'
import sys, fitz, glob, os
for f in glob.glob("build/slide_*.png"): os.remove(f)
d = fitz.open(sys.argv[1])
for i, pg in enumerate(d):
    pg.get_pixmap(dpi=int(os.environ.get("DPI","96"))).save(f"build/slide_{i+1:02d}.png")
print("rendered", d.page_count, "slides")
PY
