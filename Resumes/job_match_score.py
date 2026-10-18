"""
Score job postings against the rubric in Job_Search_Criteria.md.

Usage:
    python job_match_score.py jobs.json                    # strategic mode (default), prints ranked table
    python job_match_score.py jobs.json --mode bridge       # bridge-job mode (income/schedule/location first)
    python job_match_score.py jobs.json --append            # also appends results to Job_Matches.md

Modes:
    strategic (default) - weighted toward Director/VP-level title, cell/gene therapy industry fit,
                           and comp reaching Director level. Use for Track 1/3 target companies.
    bridge              - weighted toward local/remote location, standard-hours workload, and a
                           livable comp floor; industry/title level barely matter. Use when the goal
                           is income + a normal schedule, not career-track positioning.

Input JSON shape (list of objects):
[
  {
    "title": "Director of Operations",
    "company": "Example CDMO",
    "location": "Remote (US)",
    "url": "https://...",
    "description": "full JD text...",
    "salary_text": "$160,000 - $190,000"   // optional, free text
  },
  ...
]

See Job_Search_Criteria.md for the rubric this encodes. Keep weights in sync if either file changes.

AI-judgment pass: this script only does the keyword rubric. For semantic judgment a regex can't
catch (does the workload actually sound demanding, does "Field" location really mean remote-friendly,
is the seniority a real stretch) - paste the ranked output into a conversation with Claude and ask it
to read the top candidates' JDs and add that read. No separate API integration needed for that step.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

RESUME_DIR = Path(__file__).parent
MATCHES_FILE = RESUME_DIR / "Job_Matches.md"

# --- Keyword sets (mirrors Job_Search_Criteria.md) ---

TITLE_HIGH = [
    r"director.*operations", r"vp.*operations", r"vice president.*operations",
    r"director.*quality", r"director.*regulatory", r"head of operations",
]
TITLE_MED = [
    r"senior operations manager", r"operations director", r"plant manager",
    r"site director", r"quality director",
]
TITLE_LOW = [
    r"operations manager", r"ops manager", r"general manager", r"program manager",
]
TITLE_ANY_MANAGEMENT = [
    r"manager", r"director", r"supervisor", r"lead\b", r"head of", r"chief",
]

INDUSTRY_FULL = [
    "cell therapy", "gene therapy", "cgt", "biomanufacturing", "cdmo",
    "cell and gene", "biologics manufacturing", "regenerative medicine",
]
INDUSTRY_ADJACENT = [
    "pharma", "biotech", "medical device", "clinical lab", "life sciences",
    "biopharmaceutical", "gmp", "diagnostics",
]

REMOTE_TERMS = ["remote", "work from home", "distributed team"]
LOCAL_TERMS = ["savannah"]
SOUTHEAST_TERMS = ["georgia", "savannah", "atlanta", "south carolina", "florida",
                   "north carolina", "tennessee", "alabama"]
RELOCATION_TERMS = ["relocation assistance", "relocation package", "sign-on bonus",
                     "signing bonus", "relocation bonus"]

BANDWIDTH_RED_FLAGS = [
    "24/7", "on-call", "rotating shift", "night shift", "weekend availability",
    "wear many hats", "fast-paced startup", "unlimited hours", "whatever it takes",
]
BANDWIDTH_GREEN_FLAGS = [
    "standard business hours", "monday-friday", "monday to friday", "m-f",
    "work-life balance", "flexible schedule",
]

COMPLIANCE_TERMS = ["clia", "cola", "cgmp", "gmp", "fda", "iso 13485", "21 cfr"]

# --- Mode weight tables (must each sum to 100 across the six categories) ---

MODES = {
    "strategic": {
        "title": {"high": 30, "med": 20, "low": 12, "none": 4},
        "industry": {"full": 20, "adjacent": 12, "none": 3},
        "location": {"remote": 20, "local": 14, "southeast": 14, "relocation": 10, "other": 4},
        "bandwidth": {"green": 15, "red": 3, "neutral": 8},
        "comp": {"high": 10, "floor": 6, "low": 2, "unlisted": 5,
                 "high_threshold": 150000, "floor_threshold": 100000},
        "compliance": 5,
    },
    "bridge": {
        # Any real management-level title counts fully - level/industry don't matter for a bridge job.
        "title": {"high": 15, "med": 15, "low": 15, "none": 6},
        "industry": {"full": 5, "adjacent": 5, "none": 5},
        # Location and workload carry most of the weight - the actual point of bridge mode.
        "location": {"remote": 26, "local": 30, "southeast": 18, "relocation": 8, "other": 6},
        "bandwidth": {"green": 30, "red": 4, "neutral": 15},
        "comp": {"high": 20, "floor": 20, "low": 5, "unlisted": 14,
                 "high_threshold": 90000, "floor_threshold": 60000},
        "compliance": 0,
    },
}


def _search_any(text: str, terms) -> bool:
    return any(re.search(t, text) for t in terms)


def score_job(job: dict, mode: str = "strategic") -> dict:
    if mode not in MODES:
        raise ValueError(f"Unknown mode {mode!r}, expected one of {list(MODES)}")
    w = MODES[mode]

    title = (job.get("title") or "").lower()
    location = (job.get("location") or "").lower()
    desc = (job.get("description") or "").lower()
    salary = (job.get("salary_text") or "").lower()
    combined = f"{title} {desc}"

    notes = [f"Mode: {mode}"]

    # 1. Title Alignment
    if _search_any(title, TITLE_HIGH):
        title_score = w["title"]["high"]
        notes.append(f"Title: strong Director/VP Ops or Quality/Regulatory match (+{title_score})")
    elif _search_any(title, TITLE_MED):
        title_score = w["title"]["med"]
        notes.append(f"Title: senior ops/plant/site leadership match (+{title_score})")
    elif _search_any(title, TITLE_LOW):
        title_score = w["title"]["low"]
        notes.append(f"Title: general Operations Manager match (+{title_score})")
    elif mode == "bridge" and _search_any(title, TITLE_ANY_MANAGEMENT):
        title_score = w["title"]["low"]
        notes.append(f"Title: general management-level role, acceptable for a bridge job (+{title_score})")
    else:
        title_score = w["title"]["none"]
        notes.append(f"Title: no strong keyword match (+{title_score})")

    # 2. Industry Fit
    if _search_any(combined, INDUSTRY_FULL):
        industry_score = w["industry"]["full"]
        notes.append(f"Industry: cell/gene therapy or biomanufacturing core match (+{industry_score})")
    elif _search_any(combined, INDUSTRY_ADJACENT):
        industry_score = w["industry"]["adjacent"]
        notes.append(f"Industry: adjacent regulated sector (+{industry_score})")
    else:
        industry_score = w["industry"]["none"]
        notes.append(f"Industry: unrelated to target sector (+{industry_score})")

    # 3. Location/Remote Fit
    if _search_any(location, REMOTE_TERMS) or _search_any(combined, REMOTE_TERMS):
        loc_score = w["location"]["remote"]
        notes.append(f"Location: remote (+{loc_score})")
    elif _search_any(location, LOCAL_TERMS):
        loc_score = w["location"]["local"]
        notes.append(f"Location: Savannah (local, no relocation/commute) (+{loc_score})")
    elif _search_any(location, SOUTHEAST_TERMS):
        loc_score = w["location"]["southeast"]
        notes.append(f"Location: Southeast on-site (+{loc_score})")
    elif _search_any(combined, RELOCATION_TERMS):
        loc_score = w["location"]["relocation"]
        notes.append(f"Location: other hub, relocation incentive present (+{loc_score})")
    else:
        loc_score = w["location"]["other"]
        notes.append(f"Location: other on-site, no relocation signal (+{loc_score})")

    # 4. Bandwidth/Workload Signal
    red = _search_any(combined, BANDWIDTH_RED_FLAGS)
    green = _search_any(combined, BANDWIDTH_GREEN_FLAGS)
    if green and not red:
        band_score = w["bandwidth"]["green"]
        notes.append(f"Workload: standard-hours language, no red flags (+{band_score})")
    elif red:
        band_score = w["bandwidth"]["red"]
        notes.append(f"Workload: shift/on-call/24-7 red flags present (+{band_score})")
    else:
        band_score = w["bandwidth"]["neutral"]
        notes.append(f"Workload: no signal either way, neutral (+{band_score})")

    # 5. Compensation Signal
    nums = [int(n.replace(",", "")) for n in re.findall(r"(\d{2,3},\d{3})", salary)]
    if nums:
        top = max(nums)
        if top >= w["comp"]["high_threshold"]:
            comp_score = w["comp"]["high"]
            notes.append(f"Comp: listed salary (${top:,}) clears the top comp threshold (+{comp_score})")
        elif top >= w["comp"]["floor_threshold"]:
            comp_score = w["comp"]["floor"]
            notes.append(f"Comp: listed salary (${top:,}) clears the floor (+{comp_score})")
        else:
            comp_score = w["comp"]["low"]
            notes.append(f"Comp: listed salary (${top:,}) below floor (+{comp_score})")
    else:
        comp_score = w["comp"]["unlisted"]
        notes.append(f"Comp: not listed, neutral (+{comp_score})")

    # 6. Regulatory/Compliance Match
    if w["compliance"] and _search_any(combined, COMPLIANCE_TERMS):
        reg_score = w["compliance"]
        notes.append(f"Compliance: explicit CLIA/COLA/cGMP/GMP mention (+{reg_score})")
    else:
        reg_score = 0

    total = title_score + industry_score + loc_score + band_score + comp_score + reg_score
    tier = "High" if total >= 70 else "Medium" if total >= 45 else "Low"

    return {
        "title": job.get("title", ""),
        "company": job.get("company", ""),
        "location": job.get("location", ""),
        "url": job.get("url", ""),
        "mode": mode,
        "total": total,
        "tier": tier,
        "subscores": {
            "title": title_score, "industry": industry_score, "location": loc_score,
            "bandwidth": band_score, "comp": comp_score, "compliance": reg_score,
        },
        "notes": notes,
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(1)

    args = sys.argv[2:]
    jobs_path = Path(sys.argv[1])
    append = "--append" in args
    mode = "strategic"
    if "--mode" in args:
        mode = args[args.index("--mode") + 1]

    jobs = json.loads(jobs_path.read_text(encoding="utf-8"))
    results = sorted((score_job(j, mode=mode) for j in jobs), key=lambda r: r["total"], reverse=True)

    print(f"Mode: {mode}\n")
    print(f"{'Score':>5}  {'Tier':<6}  {'Title':<45}  {'Company':<25}  Location")
    print("-" * 120)
    for r in results:
        print(f"{r['total']:>5}  {r['tier']:<6}  {r['title'][:45]:<45}  {r['company'][:25]:<25}  {r['location']}")

    if append:
        lines = [f"\n## Scan — {date.today().isoformat()} ({mode} mode)\n"]
        for r in results:
            lines.append(f"### [{r['tier']}] {r['total']}/100 — {r['title']} @ {r['company']}")
            lines.append(f"- Location: {r['location']}")
            if r["url"]:
                lines.append(f"- Link: {r['url']}")
            for n in r["notes"]:
                lines.append(f"  - {n}")
            lines.append("")
        with open(MATCHES_FILE, "a", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"\nAppended {len(results)} results to {MATCHES_FILE}")


if __name__ == "__main__":
    main()
