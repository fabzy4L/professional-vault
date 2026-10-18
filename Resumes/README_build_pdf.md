# build_pdf.py

Converts any resume Markdown file in this folder to a formatted PDF. Strips YAML frontmatter, HTML comments, and LP Anchors blockquotes before rendering.

---

## Setup

**Python 3.13+ required.**

```
pip install -r requirements.txt
```

> **Windows note:** `python-bidi` is pinned to `0.4.2` (the last pure-Python release). Versions `>=0.5.0` require a Rust compiler to build from source. `build_pdf.py` includes a one-line monkey-patch that bridges the API difference so `xhtml2pdf` imports cleanly.

---

## Usage

```
# Build the default resume (FabianAlvarez_Master_Updated.md)
python build_pdf.py

# Build any variant by filename (must be in the same folder)
python build_pdf.py FabianAlvarez_Upwork_FreelanceProfile.md
python build_pdf.py FabianAlvarez_BlueRock_DirectorOps.md
```

Output is saved as a `.pdf` alongside the source `.md` file, same name.

---

## What gets stripped

| Source element | Behavior |
|---|---|
| YAML frontmatter (`---` block) | Removed |
| HTML comments (`<!-- ... -->`) | Removed — used for page-length flags |
| LP Anchors blockquote (`> **LP Anchors...**`) | Removed — Amazon promo note, not resume copy |
| All other `blockquote` elements | Hidden via CSS (`display: none`) |

---

## PDF style

| Property | Value |
|---|---|
| Page size | US Letter |
| Margins | 1.4 cm top/bottom · 1.8 cm left/right |
| Body font | Helvetica / Arial, 9.5 pt |
| Line height | 1.35 |
| Section headers (`##`) | 9.5 pt, navy `#1F4E79`, uppercase, underlined |
| Role headers (`###`) | 10 pt, bold, black |
| Body paragraphs | Centered (contact line only) |
| Bullet lists | Left-aligned, 2 px bottom margin |

---

## Adding a new variant

1. Copy `FabianPrimoResume2026.md` (master — do not overwrite) to a new file.
2. Edit the copy following the workflow in `CLAUDE.md`.
3. Run: `python build_pdf.py YourNewFile.md`
4. Check page count — target is 2 pages maximum.

---

## Troubleshooting

**`ImportError: cannot import name 'get_display' from 'bidi'`**
This means `python-bidi` upgraded past `0.4.2`. Pin it back:
```
pip install "python-bidi==0.4.2"
```

**`ModuleNotFoundError: No module named 'xhtml2pdf'`**
Run `pip install -r requirements.txt` from this folder.

**PDF renders but metrics look wrong**
All immutable metrics are in the `CLAUDE.md` facts table. Do not edit them in the PDF — edit the source `.md` file.
