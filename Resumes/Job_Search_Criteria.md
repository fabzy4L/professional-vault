---
title: Job Search Scoring Rubric
date: 2026-09-01
purpose: Transparent, tunable weighted rubric used by job_match_score.py to rank job postings against Career_Preferences.md and Career_Direction.md. Not a resume — a scoring reference.
status: LIVING DOCUMENT
---

# Job Search Scoring Rubric

Every job a search turns up gets scored 0–100 against this rubric, then bucketed. This file is the human-readable spec; `job_match_score.py` is the executable version — keep them in sync if weights change.

Sources this rubric encodes:
- `Career_Preferences.md` — North Star (ownership), Selection Criteria (leverage / bandwidth cost / positioning), constraints (location, workload, comp)
- `Career_Direction.md` — Track 1 (Director Ops), Track 3 (Quality/Regulatory Director), Track 2 (academic — excluded from this rubric, separate application clock)
- Current reality (2026-09-01): no active strategic move in flight — priority is a role that funds runway on a normal schedule without burning bandwidth, while staying open to strong Track 1/3 hits opportunistically.

---

## Two Modes

`job_match_score.py` scores in one of two modes — same six categories, different weights, because "good fit" means something different depending on what the search is actually for right now:

- **`strategic` (default)** — weighted toward Director/VP-level title, cell/gene therapy industry fit, and Director-level comp. Use when scanning Track 1/3 target companies.
- **`bridge`** — weighted toward local/remote location, standard-hours workload signal, and a livable comp floor; industry and title level barely move the score. Use when the actual goal is income + a normal schedule (current priority as of 2026-09-01 — "no strategy, out of moves for the time being, need something that doesn't stain me financially and allows a normal schedule").

### `strategic` mode (100 pts)

| Category | Points | What it measures |
|---|---|---|
| **Title Alignment** | 30 | Does the title match Director/VP Ops, Director Quality/Regulatory, or (fallback) general Operations Manager? |
| **Industry Fit** | 20 | Cell therapy/gene therapy/CDMO/biomanufacturing (full) vs. adjacent regulated (pharma, med device, clinical lab) vs. unrelated |
| **Location/Remote Fit** | 20 | Remote > Savannah/local > Southeast on-site > other hub with relocation incentive > other on-site |
| **Bandwidth/Workload Signal** | 15 | JD language suggesting standard hours vs. 24/7, rotating shifts, heavy on-call, "fast-paced/wear many hats" red flags |
| **Compensation Signal** | 10 | Listed salary vs. Director-level ($150K+) or acceptable bridge-role floor (~$100K+); unlisted = neutral |
| **Regulatory/Compliance Match** | 5 | Explicit CLIA/COLA/cGMP/GMP mention — plays directly to the one hardest-to-replicate credential in the record |

### `bridge` mode (100 pts)

| Category | Points | What it measures |
|---|---|---|
| **Title Alignment** | 15 | Any real management-level title counts fully — level/specialty don't matter for a bridge job |
| **Industry Fit** | 5 | Barely weighted — a bridge job doesn't need to be biopharma |
| **Location/Remote Fit** | 30 | Savannah/local and remote both score near-max; other Southeast lower; elsewhere low unless relocation is covered |
| **Bandwidth/Workload Signal** | 30 | The main point of this mode — standard-hours language scores high, shift/on-call/24-7 language scores very low |
| **Compensation Signal** | 20 | Two-tier: clears a livable floor (~$60K+) or doesn't; no bonus for reaching Director-level pay |
| **Regulatory/Compliance Match** | 0 | Not scored in this mode |

**Tiers (both modes):** High ≥ 70 · Medium 45–69 · Low < 45

---

## AI-judgment pass (no separate integration needed)

The rubric above is pure keyword matching — it can't tell that "Field" as a location usually means remote-friendly, or that a JD's tone reads as calmer or more frantic than its literal words. Rather than build a standalone script against the Anthropic API (a real per-call cost, a new API key to manage — overkill for occasional scans, and the opposite of the "doesn't stain me financially" goal that motivated `bridge` mode), that judgment call is made by asking Claude directly in a conversation to read the top-scoring JDs and add a qualitative read next to the rubric score. Free, no extra infra. Revisit a standalone API integration only if this ever needs to run unattended/scheduled.

---

## Notes on use

- Weights are a starting point, not fixed — revisit if scored results don't match Fabian's gut read on a posting.
- Scoring a posting does not create a resume variant automatically — build one only for postings Fabian wants to actually pursue.
