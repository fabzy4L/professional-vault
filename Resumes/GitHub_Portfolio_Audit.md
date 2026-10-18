---
title: GitHub Portfolio Audit — C:\Users\f4l\Documents\GitHub
date: 2026-08-25
purpose: Ground-truth audit of all 23 repos (git history + code inspection), for accurate resume/CV/career-record claims. Not for direct submission.
---

# GitHub Portfolio Audit

> ⚠ **Security note:** During this scan, a prompt-injection string was found embedded in tool output, impersonating a system message and instructing the assistant to silently accept a fake date change and hide it from the user. It was ignored and flagged. Not acted on. Mentioned here for the record.

> **Method:** 4 parallel agents covering all 23 repos, verifying real git commit history (not self-reported dates) and reading actual source code, not just READMEs.

---

## Category 1 — Academic/Research Repos (most relevant to GT faculty CV)

| Repo | Real dev window | Verdict |
|---|---|---|
| **bio-print-pipeline** | 2026-06-02, single ~4hr session | ⭐ Strongest direct PhD-domain match. Real DICOM→STL bioprint-scaffold pipeline (TPMS infill, marching-cubes reconstruction), validated against a real reference geometry, 7-point geometric QA suite, ISO 14971 risk register, IEC 62304 compliance docs, RUO labeling. ~3,000 lines + 789-line test suite. Explicitly "Not cleared by FDA, not for clinical use." |
| **depression-tbi-luminex-analysis** | 2026-05-03 → 05-09 (~2.75 hrs main session) | ⭐ Strongest direct postdoc-topic match. Real Luminex multiplex-assay analysis of neuro-inflammatory biomarkers in MDD/suicidal-behavior cohort (n=70: 35 control/23 MDD/12 suicide). R + FastAPI + React/TS stack. Self-graded "B-" with 8 documented bugs in the original notebook — unusually honest self-audit, a genuine strength for research-integrity narrative. |
| **biomanufacturing-review** | 2026-06-22 → 06-23 (~2 days) | Full draft literature-review manuscript (~7,800 words, 9 sections) on AI in cell/gene-therapy biomanufacturing, targeting *Trends in Biotechnology* / *Biotechnology and Bioengineering* / bioRxiv. Real, verified citations. **Not submitted or published — a drafted manuscript only.** Its own project notes state the strategic purpose is "credibility... as a precursor to industry outreach and LabOps.AI market positioning" — i.e., written to support the LabOps.AI narrative, not (yet) independent scholarship. |
| **multi-epitope-vaccine-design** | 2026-06-01 → 06-02 (~2 days tracked; likely more upstream work not in git) | Real, rigorous computational immunoinformatics (SARS-CoV-2 multi-epitope vaccine design — IEDB/NetMHCpan, AlphaFold2, HDOCK, immune-kinetics ODE simulation). ~6,500 lines, real statistical validation (KS test, p=6.87×10⁻²⁴). Unusually candid "Known Design Flags" and limitations section. **Topically adjacent, not core** to BME/neuroscience — best framed as evidence of computational rigor, not subject-matter fit. |
| CMAM-tools | 2026-06-16 → 07-02 | Amazon SAV4 dock dashboard. **No BME/research relevance — explicitly confidential Amazon operational data per its own README. Do not reference in academic materials or publicly.** |

**Cross-repo pattern:** all of these (and the earlier-reviewed LabOps.AI, sert-s438t-escitalopram, qpcr-react-dashboard) were built in short, intensive single-day-to-few-week sprints, several AI-assisted — not slow-burn, multi-month research programs. Be accurate about this pacing if it comes up (e.g., "rapid independent prototyping," not "an ongoing multi-year research program"). A real, recurring strength across the rigorous ones: unusually candid self-documentation of limitations, bugs, and design flags — a genuine, evidenced pattern worth naming explicitly in a research statement.

---

## Category 2 — Amazon Operations Tools

| Repo | Real dev window | Verdict |
|---|---|---|
| **foresight-tool** | 2026-06-09 → 07-02 (~3.5 wks, 10 commits) | Most sustained of the Amazon tools. Real Next.js dashboard + a genuine Tampermonkey DOM-scraper hitting a live internal Amazon URL (`sort.aka.amazon.com/foresight`). Contains real, dated SAV4 Kiva WIP export files — strong evidence of actual floor use, not just a demo. |
| **rtb-comment-generator** | 2025-08-30 → 2026-05-09 (~8.4 months, sporadic) | Longest calendar span. Python/Streamlit tool with real curve-fitting (power-law learning curves per associate) and an automated performance-comment generator. Contains a real, unsanitized Aug 2025 output file with actual generated commentary on real associates — direct proof of real operational use. Covers Waterspider/Directed Loader/Container Builder roles. |
| **rtb-dashboard** | 2026-07-03, single 22-minute window | Real, working TypeScript port of the above tool's logic (code comments explicitly cite the port). Built essentially in one sitting. |
| **dea-staging-audit-tool** | 2026-06-29, single ~36-minute session | Real, working barcode-scan audit workflow app. No README. Built in one short session — accurately a fast personal tool, not an engineered system. |
| **AppScriptFXNS** | 2026-05-05 → 05-06 (~18 hrs) | Small, real Google Apps Script utilities (RTB analysis ancestor script, sheet-formatting tools). **See correction below — this is where the recirculation-tool discrepancy was found.** |

### ⚠ Correction needed: "AI-Driven Recirculation Tool" claim

Your Q2 2026 Amazon Growth Plan (and my earlier `Amazon_Accomplishments_Tools.md` summary, now flagged for correction) credits you with a **"Custom AI-Driven Recirculation Tool... built with a PhD-level data science background."** The audit did not find this in your repos. What actually exists:

- The only large, AI-branded, recirculation-focused file present anywhere (`AppScriptFXNS/DockSense-8.1.1.user.js`, 25,354 lines) is **not tracked in git** (never committed — added to your working directory separately) and its own script header identifies the author as **`cesolis`** — a different Amazon employee — distributed via an internal Amazon script host as a colleague's tool.
- The actual Fabian-authored recirculation-adjacent artifact in that repo is a small, non-AI spreadsheet-formatting script (`Eject Recirc Format.gs.txt`, 134 lines — sorts/filters rows, no AI/LLM logic).

**This is worth resolving directly** — either the growth-plan claim refers to a different, not-yet-found tool, or it's describing a colleague's tool you use locally in a way that could read as your own authorship if scrutinized. Given this is in an official internal HR document (not just a resume), I'd suggest clarifying/correcting it there before it comes up in a promotion review.

---

## Category 3 — BLK PHX LABS Venture

**Honest overall picture:** BLK PHX LABS is a personal-brand umbrella under early-stage development, built across a concentrated ~10-week window (Apr 23 – Jul 1, 2026). It is **not** a formed legal entity, has **no live product, no revenue, no domains purchased, no bank account** — a detailed corporate-structure plan exists (`BLK PHX, INC.` as a Delaware C-Corp holding `BLK PHX LABS` as a "science & biotech arm") but every item on its formation checklist is unchecked.

| Repo | Real dev window | Biotech-relevant? | Status |
|---|---|---|---|
| BLKPHXLABS.AI_BRIEFING | 2026-04-23, single day, 7 commits | Yes | ⭐ **Real, working, iterated** — the one genuinely functioning biotech-relevant piece (autonomous news-intelligence pipeline) |
| BLKPHXLABS.AI | 2026-05-11, single day, 1 commit | Yes (thesis) | Well-researched market thesis site ("AI-native OS for CGT biomanufacturing") — a **pitch deck**, not a product. (Distinct from the actual working `LabOps.AI` codebase reviewed earlier — don't conflate the two.) |
| BLKPHXLABS_Dissertation_Chatbot | 2026-05-04 → 05-05 | Indirectly | Real small tool, but generic infrastructure (works on any PDF) |
| blk-phx-labs-e-commerce | 2026-06-11 → 06-17 | **No** | Nootropics/supplement dropshipping scaffold — substantial code (~2,500 lines, 33 tests) but **no entity, no deployment, nothing live** |
| blkphx-ph3 | 2026-06-04 → 06-08 | No | Personal fitness/martial-arts tracker |
| blk-phx-landing-dashboard | 2026-06-10 → 07-01 | No | Personal link-in-bio page |

**Recommendation:** it would overstate things to describe BLK PHX LABS as "a real regenerative-medicine venture" anywhere formal (CV, cover letter). Accurate framing: an early-stage personal venture umbrella with one working biotech-intelligence tool and a market thesis, alongside unrelated consumer/personal side projects sharing the brand name — no formed company yet.

---

## Category 4 — Data Science & Misc

| Repo | Real dev window | Verdict |
|---|---|---|
| **DATA_ANALYTICS** | **2022-01-01 → 2026-05-27, 153 commits** | Real, substantial, multi-year monorepo — by far the longest-running project in the portfolio. Contains the `nicotine_gene_expression` subproject tied to the real Frontiers in Psychiatry 2023 publication. ⚠ **"SIR/SEIR epidemiology models" claim (from the earlier PROJECT_PORTFOLIO.md audit) was not found anywhere in the repo** — grepped fully, zero real matches. Should be dropped or corrected. The COVID Shiny app is real but has an unfixed placeholder bug (region dropdown doesn't match the real country data). |
| **biotech-intel** | 2025-10-24 → 2026-05-09 | Real, tested (25/25 tests passing, independently re-run), honestly labeled "Dormant" in its own README. Good, legitimate CV item. |
| **email-digest-scheduler** | 2025-10-20 → 2026-05-09 | Real, working single-file tool, honestly self-documented limitations. Legitimate. |
| **OpenSource_Data_Sci_MS** | Single commit, 2023-03-06 | Empty stub (24-byte README only). Not usable as portfolio evidence. |
| **pydata-book** | 2012-07-27 → 2022-11-03, 69 commits | ⚠ **Not your work.** 100% of commits are by Wes McKinney (the book's actual author) and two outside contributors — you have never committed to this repo. It's the official companion repo to *Python for Data Analysis*, sitting in your GitHub account as reference material. **Should not appear as a project on any CV** — at most, cite it as study material. |
| **elite-fitness-dashboard** | — | Empty, not even a git repo. Nothing here. |

---

## Summary of Corrections Needed Elsewhere

1. **`Amazon_Accomplishments_Tools.md`** — the "Custom AI-Driven Recirculation Tool" entry needs correction/clarification per the DockSense finding above.
2. **`PROJECT_PORTFOLIO.md` / `PORTFOLIO_REVIEW.md`** — drop or caveat the "SIR/SEIR Models" claim (not found in DATA_ANALYTICS); the "Drug Discovery/docking pipeline" reference in DATA_ANALYTICS is an auto-generated ChimeraX session file, not hand-written code — reword if cited.
3. Do not cite `pydata-book` as original work anywhere.
4. Do not reference `CMAM-tools` publicly — it contains explicitly confidential Amazon data per its own README.
