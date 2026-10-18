# Career Database & Resume Workspace — Fabian Alvarez-Primo

## Purpose

This workspace is a **career database for brainstorming professional progression**, not just a resume factory. Two files anchor everything else:

- **`Career_Ledger.md`** — single source of truth for verified facts (employment timeline, metrics, publications, portfolio evidence). Every resume/CV/statement variant should pull from here, not re-derive facts independently. It also tracks unresolved conflicts explicitly — check "Open Items" before stating anything as fact in a new document.
- **`Career_Preferences.md`** — what Fabian actually wants, not just what the record supports. North Star: ownership of his own venture; every track below is instrumental toward that, evaluated on leverage/bandwidth/positioning, not evidentiary strength alone.
- **`Career_Direction.md`** — the actual brainstorming layer: candidate career tracks with evidence for/against, open strategic questions, and a decision log. Read this (and `Career_Preferences.md`) first to understand what direction(s) are currently active before building new materials.

Below that, the master resume (`FabianPrimoResume2026.md`) is broadly positioned for **Director/VP Operations in cell therapy, gene therapy, or biomanufacturing** — currently the primary track (see `Career_Direction.md` Track 1). Each application gets a targeted variant — same candidate, same facts, tuned language and emphasis. Retired tracks (e.g., Upwork/freelance, dropped 2026-08-27) live in `Archive/`, not deleted.

---

## Master Resume

**File:** `FabianPrimoResume2026.md`

This is the canonical source of truth. Do not overwrite it. Create named variants for each application (e.g., `FabianAlvarez_BlueRock_DirectorOps.md`).

### Candidate positioning

- PhD in Biomedical Materials Science & Engineering (UTEP, 2020)
- Current: Operations Manager II at Amazon — 60+ team, 99.7% quality compliance, Python automation, Lean
- Prior: iPSC/cGMP postdoc (TTUHSCEP), CLIA/COLA clinical lab supervisor (WTPI), doctoral R&D lead (IMSTEL/UTEP)
- 8 peer-reviewed publications; engineering honor societies; Society for Biomaterials president (2 terms)
- Key differentiator: rare blend of regulated scientific depth (cGMP, CLIA, COLA) + operational scale leadership + quantitative automation skills

### Sections (in order)

1. Executive Summary — 2-3 sentences, adapt per role emphasis
2. Core Competencies — 3-column table, swap keywords to match JD
3. Professional Experience — Amazon → TTUHSCEP → WTPI → IMSTEL
4. Education
5. Publications & Professional Honors

### Immutable facts (never change)

| Metric | Value |
|--------|-------|
| Team size (Amazon) | 60+ associates |
| Quality compliance (Amazon) | 99.7% |
| Dock rate improvement | 82% (220 → 400+ units/hr) |
| Recirculation reduction | 5% → <2% |
| PAs trained | 15 total, 9 concurrent |
| Lab samples/month (WTPI) | 1,300+ |
| Lab team size (WTPI) | 9 |
| Students mentored (IMSTEL) | 30+ |
| 3D printer precision improvement | 30% |
| Publications | 8 peer-reviewed |

### LP Anchors (Amazon promo language — keep in blockquote, stripped from PDF)

`> **LP Anchors:** Ownership · Deliver Results · Dive Deep · Insist on Highest Standards`

---

## Workflow: Build PDF

```bash
python build_pdf.py
```

**Dependencies:** `markdown`, `xhtml2pdf` (`pip install markdown xhtml2pdf`)

**Note:** `build_pdf.py` has hardcoded paths — update `MD_FILE` and `PDF_FILE` at the top of the script when building a variant. The script strips YAML frontmatter and LP Anchors blockquotes automatically.

**PDF style:** Letter, 1.4cm/1.8cm margins, Helvetica 9.5pt, navy (`#1F4E79`) section headers, bold metrics.

---

## Creating a Targeted Variant

When given a job description, follow this process:

1. **Copy** `FabianPrimoResume2026.md` → new file named `FabianAlvarez_<Company>_<Role>.md`
2. **Update frontmatter** `title`, `target_role` fields
3. **Executive Summary** — mirror the JD's language (e.g., if JD says "scale-up" lean into scale-up; if it says "compliance" lead with CLIA/cGMP)
4. **Core Competencies table** — swap or reorder cells to surface JD keywords in positions 1-3
5. **Amazon bullets** — pick 5-6 most relevant; always keep the 82% dock rate and 99.7% compliance
6. **TTUHSCEP** — lead with cGMP and iPSC for cell/gene therapy roles; deemphasize for pure ops roles
7. **WTPI** — lead with regulatory compliance (CLIA/COLA) for quality-heavy roles
8. **IMSTEL** — useful for roles that value scientific credibility or team building; can condense to 2-3 bullets
9. **ATS pass** — ensure JD title keywords appear verbatim at least once in the document
10. Build PDF, confirm 2-page max

---

## Tone & Constraints

- All metrics must be real — no placeholders (`[X]%`)
- 2-page PDF maximum; trim bullets before cutting sections
- ATS-friendly: no columns in experience, no text boxes, standard section headers
- Blockquotes (`> ...`) are working notes only — `build_pdf.py` strips them
- Bold numbers/metrics in bullets for scannability

---

## File Index

| File | Purpose |
|------|---------|
| `Career_Ledger.md` | **Source of truth** — reconciled facts, verified metrics, open conflicts |
| `Career_Preferences.md` | **What Fabian wants** — North Star, selection criteria, constraints |
| `Career_Direction.md` | **Brainstorming hub** — candidate tracks, evidence, decision log |
| `FabianPrimoResume2026.md` | Master resume — do not overwrite |
| `build_pdf.py` | MD → PDF converter; update paths per variant |
| `Resume2026.pdf` | Last built PDF output |
| `FabianAlvarez_Master_Updated.md` | Master resume updated with LabOps.AI venture entry and Apps Script bullet — flagged for 2-page review; note LabOps.AI dates need correcting per Career_Ledger.md |
| `Fabian_Alvarez_Director_Ops_Biopharma.md` | Director Ops (biopharma) variant — Track 1 in Career_Direction.md |
| `FabianAlvarezPrimo_GATech_*` | Academic faculty application package — Track 2 in Career_Direction.md |
| `prompt.txt` | Execution brief for Master Updated file (context only) |
| `PORTFOLIO_REVIEW.md` | Gemini-generated technical audit of GitHub portfolio — superseded by `GitHub_Portfolio_Audit.md` for verified claims |
| `PROJECT_PORTFOLIO.md` | Structured project overview by domain — defer to `GitHub_Portfolio_Audit.md`/`Career_Ledger.md` for verified tech stacks |
| `GitHub_Portfolio_Audit.md` | Ground-truth audit of all 23 GitHub repos against real git history — trust this over self-summaries |
| `Amazon_Role_Context.md`, `Amazon_Performance_Metrics.md`, `Amazon_Accomplishments_Tools.md` | Raw Amazon source extracts — reconciled into `Career_Ledger.md` |
| `Archive/` | Retired tracks/materials (not deleted) — currently: Upwork/freelance profile |
| Older `*-2024.md` files | Prior positioning versions — reference only |
| `Job_Search_Mechanism.md` | **Start here for job-finder work** — how to source postings, run scans, do the AI-judgment pass, extend the rubric |
| `Job_Search_Criteria.md` | Job-match scoring rubric spec — `strategic` and `bridge` weight profiles |
| `job_match_score.py` | Executable scorer — `python job_match_score.py jobs.json --mode strategic\|bridge [--append]` |
| `Job_Matches.md` | Running log of scored postings + AI-judgment notes |
