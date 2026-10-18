"""
Convert a resume .md file → PDF.
Usage:
    python build_pdf.py                          # builds default (FabianAlvarez_Master_Updated.md)
    python build_pdf.py MyResume.md              # builds any named file in RESUME_DIR

Install dependencies:
    pip install -r requirements.txt

See README_build_pdf.md for full setup and usage notes.
"""
import re
import sys
from pathlib import Path

# Monkey-patch: expose bidi.algorithm.get_display at the bidi module level
# so xhtml2pdf 0.2.17 (which does `from bidi import get_display`) can import cleanly.
import bidi.algorithm
import bidi as _bidi_mod
if not hasattr(_bidi_mod, "get_display"):
    _bidi_mod.get_display = bidi.algorithm.get_display

import markdown
from xhtml2pdf import pisa

RESUME_DIR = Path(r"C:\Users\f4l\iCloudDrive\iCloud~md~obsidian\Professional\Resumes")

if len(sys.argv) > 1:
    md_path = Path(sys.argv[1])
    if not md_path.is_absolute():
        md_path = RESUME_DIR / md_path
else:
    md_path = RESUME_DIR / "FabianAlvarez_Master_Updated.md"

pdf_path = md_path.with_suffix(".pdf")

raw = md_path.read_text(encoding="utf-8")

# Strip YAML frontmatter
body = re.sub(r"^---\n.*?\n---\n", "", raw, flags=re.DOTALL).strip()
# Strip HTML comments (page-length flags, working notes)
body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL).strip()
# Strip LP Anchors blockquote (working note, not resume copy)
body = re.sub(r"^> \*\*LP Anchors.*$", "", body, flags=re.MULTILINE).strip()

html_body = markdown.markdown(body, extensions=["tables", "extra"])

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: letter;
    margin: 1.4cm 1.8cm 1.4cm 1.8cm;
  }}

  body {{
    font-family: Helvetica, Arial, sans-serif;
    font-size: 9.5pt;
    color: #000000;
    line-height: 1.35;
  }}

  h1 {{
    font-size: 18pt;
    color: #1A233A;
    text-align: center;
    margin: 0 0 4px 0;
  }}

  h2 {{
    font-size: 9.5pt;
    color: #1F4E79;
    text-transform: uppercase;
    margin: 8px 0 1px 0;
    border-bottom: 1px solid #1F4E79;
    padding-bottom: 2px;
  }}

  h3 {{
    font-size: 10pt;
    color: #000000;
    margin: 6px 0 2px 0;
    font-weight: bold;
  }}

  p {{
    margin: 3px 0;
    text-align: center;
  }}

  ul {{
    margin: 2px 0;
    padding-left: 1.1em;
  }}

  li {{
    margin-bottom: 2px;
    text-align: left;
  }}

  hr {{
    border-top: 1px solid #1F4E79;
    margin: 5px 0;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 4px 0;
    font-size: 9pt;
  }}

  td {{
    padding: 2px 4px;
    vertical-align: top;
    border: none;
  }}

  blockquote {{
    display: none;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

try:
    with open(pdf_path, "wb") as out:
        result = pisa.CreatePDF(HTML_TEMPLATE, dest=out)
except PermissionError:
    print(f"Permission denied: {pdf_path}\nClose the file in your PDF viewer and try again.")
    raise SystemExit(1)

if result.err:
    print(f"Errors: {result.err}")
else:
    print(f"Saved: {pdf_path}")
