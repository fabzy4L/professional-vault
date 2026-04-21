"""
Convert Fabian_Alvarez_Director_Ops_Biopharma.md → PDF.
Usage: python build_pdf.py
"""
import re
import markdown
from xhtml2pdf import pisa

MD_FILE  = r"E:\iCloudDrive\iCloud~md~obsidian\Professional\Resumes\Fabian_Alvarez_Director_Ops_Biopharma.md"
PDF_FILE = r"E:\iCloudDrive\iCloud~md~obsidian\Professional\Resumes\Fabian_Alvarez_Director_Ops_Biopharma.pdf"

with open(MD_FILE, encoding="utf-8") as f:
    raw = f.read()

# Strip YAML frontmatter
body = re.sub(r"^---\n.*?\n---\n", "", raw, flags=re.DOTALL).strip()
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

with open(PDF_FILE, "wb") as out:
    result = pisa.CreatePDF(HTML_TEMPLATE, dest=out)

if result.err:
    print(f"Errors: {result.err}")
else:
    print(f"Saved: {PDF_FILE}")
