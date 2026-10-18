"""
Convert an academic-application .md file (CV, statements, letters) -> PDF.
Distinct from build_pdf.py, which is tuned for the compact 2-page industry resume
(centered text, 9.5pt cramped font). Academic documents need normal prose formatting:
left-aligned paragraphs, readable body size, standard margins, no length compression.

Usage:
    python build_academic_pdf.py <file.md>          # single file, in RESUME_DIR
    python build_academic_pdf.py <file1.md> <file2.md> ...   # multiple files

Install dependencies: pip install -r requirements.txt (same deps as build_pdf.py)
"""
import re
import sys
from pathlib import Path

import bidi.algorithm
import bidi as _bidi_mod
if not hasattr(_bidi_mod, "get_display"):
    _bidi_mod.get_display = bidi.algorithm.get_display

import markdown
from xhtml2pdf import pisa

RESUME_DIR = Path(r"C:\Users\f4l\iCloudDrive\iCloud~md~obsidian\Professional\Resumes")

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: letter;
    margin: 1.9cm 2.2cm 1.9cm 2.2cm;
  }}

  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 11.5pt;
    color: #000000;
    line-height: 1.3;
  }}

  h1 {{
    font-family: Helvetica, Arial, sans-serif;
    font-size: 17pt;
    color: #1A233A;
    text-align: left;
    margin: 0 0 6px 0;
  }}

  h2 {{
    font-family: Helvetica, Arial, sans-serif;
    font-size: 12pt;
    color: #1F4E79;
    margin: 14px 0 4px 0;
    border-bottom: 1px solid #1F4E79;
    padding-bottom: 2px;
  }}

  h3 {{
    font-family: Helvetica, Arial, sans-serif;
    font-size: 11.5pt;
    color: #000000;
    margin: 10px 0 3px 0;
    font-weight: bold;
  }}

  p {{
    margin: 0 0 6px 0;
    text-align: left;
  }}

  ul, ol {{
    margin: 4px 0 8px 0;
    padding-left: 1.4em;
  }}

  li {{
    margin-bottom: 3px;
    text-align: left;
  }}

  strong {{
    font-weight: bold;
  }}

  em {{
    font-style: italic;
  }}

  hr {{
    border: none;
    border-top: 0.75px solid #999999;
    margin: 10px 0;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0 10px 0;
    font-size: 10.5pt;
  }}

  th {{
    text-align: left;
    padding: 3px 6px;
    border-bottom: 1px solid #1F4E79;
    font-family: Helvetica, Arial, sans-serif;
    font-weight: bold;
  }}

  td {{
    padding: 3px 6px;
    vertical-align: top;
    border-bottom: 0.5px solid #dddddd;
  }}

  blockquote {{
    display: none;
  }}

  a {{
    color: #1F4E79;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""


def build_one(md_path: Path) -> None:
    if not md_path.is_absolute():
        md_path = RESUME_DIR / md_path
    pdf_path = md_path.with_suffix(".pdf")

    raw = md_path.read_text(encoding="utf-8")

    # Strip YAML frontmatter (title/date/target/status metadata — internal notes, not for the PDF)
    body = re.sub(r"^---\n.*?\n---\n", "", raw, flags=re.DOTALL).strip()
    # Strip HTML comments
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL).strip()

    html_body = markdown.markdown(body, extensions=["tables", "extra"])
    full_html = HTML_TEMPLATE.format(html_body=html_body)

    try:
        with open(pdf_path, "wb") as out:
            result = pisa.CreatePDF(full_html, dest=out)
    except PermissionError:
        print(f"Permission denied: {pdf_path}\nClose the file in your PDF viewer and try again.")
        return

    if result.err:
        print(f"Errors building {md_path.name}: {result.err}")
    else:
        print(f"Saved: {pdf_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_academic_pdf.py <file1.md> [file2.md ...]")
        raise SystemExit(1)
    for arg in sys.argv[1:]:
        build_one(Path(arg))
