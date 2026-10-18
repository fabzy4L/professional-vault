---
title: Job Search Mechanism — How to Run and Extend It
date: 2026-09-01
purpose: Operating instructions for the job-finder/scorer built 2026-09-01 — how to source postings, run scans, add the AI-judgment pass, and extend the system. Companion to Job_Search_Criteria.md (the rubric spec) and Job_Matches.md (the results log).
status: LIVING DOCUMENT
---

# Job Search Mechanism

Three files make this work:

| File | Role |
|---|---|
| `Job_Search_Criteria.md` | The rubric spec — six scoring categories, two weight profiles (`strategic` / `bridge`). Human-readable source of truth for *why* something scores the way it does. |
| `job_match_score.py` | The executable version of that rubric. Takes a JSON array of job postings, scores each, prints a ranked table, optionally appends to the log. |
| `Job_Matches.md` | Running log of every scan — newest at the bottom, chronological. Includes both rubric scores and any AI-judgment notes. |

This file is the fourth piece: how to actually source postings and run the loop end to end.

---

## The full workflow

1. **Source postings** (see next section — this is the part that needs a human/Claude in the loop each time, not a one-time setup)
2. **Assemble a `jobs.json`** — array of `{title, company, location, url, description, salary_text}` objects (see schema in `job_match_score.py`'s docstring)
3. **Run the scorer**: `python job_match_score.py jobs.json --mode strategic` or `--mode bridge`, add `--append` to log results
4. **AI-judgment pass on the top candidates** — ask Claude (in conversation) to read the full JD text for the highest scorers and flag anything the keyword rubric can't see (see below)
5. **Decide** — only postings Fabian actually wants to pursue get a resume variant built (per `CLAUDE.md`'s existing variant workflow)

Steps 1–4 currently require asking Claude to run them — there's no scheduled/automated version yet (see "Future: automation" at the bottom).

---

## Step 1: Sourcing postings

### What works: ATS JSON APIs (no key, no auth)

Most biotech/pharma companies post jobs through Greenhouse or Lever, both of which expose clean public JSON — no scraping, no key, no ToS risk.

**Greenhouse:**
```bash
curl -s "https://boards-api.greenhouse.io/v1/boards/<company-slug>/jobs?content=true"
```
Returns `{"jobs": [{"title", "location": {"name"}, "absolute_url", "content": "<html>", ...}]}`. `content=true` includes the full JD as HTML — strip tags before feeding to the scorer.

**Lever:**
```bash
curl -s "https://api.lever.co/v0/postings/<company-slug>?mode=json"
```

**Finding the slug:** it's usually the company name lowercased, no spaces/punctuation (e.g. `beamtherapeutics`, `blueprintmedicines`). Guessing works often enough to be worth trying directly before searching. A 404 with `{"status":404,"error":"Job not found"}` (Greenhouse) or `{"ok":false,"error":"Document not found"}` (Lever) means either the slug is wrong or that company uses a different ATS.

**Known-good slugs found so far:** `beamtherapeutics`, `blueprintmedicines` (both Greenhouse). Worth building this list out over time — track working slugs somewhere (bottom of this file) so future scans don't re-guess from scratch.

### What doesn't work

- **LinkedIn** — blocks scraping outright (ToS + anti-bot). Only usable one-at-a-time, pasted by Fabian, fetched individually (this is how the original Adecco posting was scored).
- **Workday-hosted boards** (`*.myworkdayjobs.com`) — JS-rendered, WebFetch gets nothing. Vertex Pharmaceuticals' board hit this. If a target company only posts through Workday, either skip it or use Workday's own JSON API (`https://<tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<board>/jobs` — untested here, worth trying if a specific Workday-only target matters enough).
- **Aggregators** (Indeed, ZipRecruiter, Glassdoor) via `WebSearch` — return search-result summaries and category-page links, not individual structured postings. Useful for market-level context ("129 ops manager jobs in Savannah") but not for feeding the scorer directly.

### Target company list for `strategic` mode

Not yet built out systematically — `Career_Direction.md` notes this as an open question. Candidates worth trying Greenhouse/Lever slugs for: CDMOs and cell/gene therapy companies (Catalent, Lonza, WuXi, Fujifilm Diosynth, Cellares, National Resilience) and clinical-stage biotechs with Director-level Ops/CMC/Quality openings (Sarepta, Intellia, CRISPR Therapeutics, Iovance, Ultragenyx, bluebird bio — none of these resolved on a first guess 2026-09-01, may use a different ATS or a non-obvious slug).

---

## Step 2: Assembling `jobs.json`

Save fetched postings as a JSON array matching the schema in `job_match_score.py`'s docstring. Strip HTML tags from Greenhouse's `content` field before putting it in `description` — the scorer does plain-text keyword matching, tags just add noise (a quick `re.sub('<[^<]+?>', ' ', html)` is enough, no need for a full HTML parser).

Keep working batches in the scratchpad directory (session-temporary) unless a batch is worth preserving — `Job_Matches.md` is the permanent record, not the intermediate `jobs.json`.

---

## Step 3: Running the scorer

```bash
cd Resumes
python job_match_score.py jobs.json --mode strategic
python job_match_score.py jobs.json --mode bridge --append   # append writes to Job_Matches.md
```

Run both modes on the same batch when it's genuinely ambiguous whether a posting matters more strategically or as a bridge — the 2026-09-01 test batch (Adecco + 2 Beam Therapeutics roles) is a working example of the two modes disagreeing on purpose.

---

## Step 4: AI-judgment pass

The rubric is keyword matching — it cannot tell tone, cannot tell whether "Field" as a location means travel-heavy-but-flexible vs. something else, cannot tell whether a title's listed responsibilities are actually a stretch beyond what the keyword match implies. That judgment happens by asking Claude directly:

> "Read the full JD for [posting] and tell me: does the workload sound heavier or lighter than the rubric's score suggests? Does the seniority look like a real stretch or a good fit given Career_Ledger.md? Any red flags the keywords wouldn't catch?"

No separate API integration for this — it's a normal conversational ask, using whatever full JD text is already on hand (fetched via Greenhouse/Lever JSON, or pasted by Fabian for a one-off LinkedIn link). Log anything material as a dated addendum in `Job_Matches.md` under the relevant scan, the way the 2026-09-01 Beam Therapeutics read is logged.

**Why not a standalone AI-scoring script:** would need its own Anthropic API key (not the same thing as this Claude Code session) and would cost real money per call — a bad match for the "doesn't stain me financially" goal that motivated `bridge` mode in the first place. Revisit only if this needs to run unattended (see below).

---

## Extending the rubric

Both `Job_Search_Criteria.md` and `job_match_score.py` must change together — the `.md` is the spec, the `.py` is the implementation, and they drift if only one gets edited.

To add a new mode, category, or keyword:
1. Edit the `MODES` dict in `job_match_score.py` (weights must sum to 100 per mode)
2. Edit the matching keyword list (`TITLE_HIGH`, `INDUSTRY_FULL`, etc.) if adding new terms
3. Mirror the change in `Job_Search_Criteria.md`'s tables
4. Re-run against a known batch (the 2026-09-01 three-job test set is a reasonable regression check — scores shouldn't move in surprising directions)

---

## Future: automation (not built, deliberately)

Explicitly deferred at setup (2026-09-01): no scheduled/cron scan, no standalone AI-scoring API integration. Both are real options if priorities change:

- **Scheduled scanning** — a cron/loop that re-pulls known Greenhouse/Lever boards on an interval and appends new high scorers to `Job_Matches.md` automatically. Feasible without any API key (the ATS endpoints are free/keyless) — only needs the company slug list built out and a dedup check against what's already logged.
- **Standalone AI-scoring script** — calling the Claude API directly per posting instead of doing the judgment pass in conversation. Needs an `ANTHROPIC_API_KEY` (none configured on this machine as of 2026-09-01) and has a small real per-call cost. Only worth it if scanning needs to run fully unattended.

Both are additive — nothing above needs to change to add either later.
