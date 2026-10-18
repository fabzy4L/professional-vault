---
PROJECT: AppScriptFXNS
WHAT IT ACTUALLY DOES: A suite of Google Apps Script (JavaScript) tools that automate Amazon fulfillment center (Ship Dock) operations. It parses "Return to Baseline" (RTB) performance data, generates "Thrive" reports, and manages dock staffing/roles by treating Google Sheets as a relational database.

PERSONA 1 VIEW — RECRUITER: This signals a candidate who has operated in high-volume, high-pressure logistics and understands the importance of performance metrics. While not GxP-validated, it demonstrates the ability to build "Shadow IT" solutions that bridge gaps in enterprise software, a common need in pre-commercial biotech ops.

PERSONA 2 VIEW — CLIENT: This is a turnkey workflow automation package for a small warehouse or lab manager. It takes messy, manual spreadsheets and turns them into a structured dashboard with automated reporting and role-clearing functions.

TECH STACK VERIFIED: Google Apps Script (JavaScript), Google Workspace APIs (Sheets, Drive).

IMPACT SIGNAL: The complexity of `RTBV3.0.gs.txt` (12KB+ of logic) shows deep domain knowledge of labor-intensive operations and the ability to maintain complex state in a low-code environment.

GAPS OR CAVEATS: Lacks a modern CI/CD pipeline (e.g., Clasp/GitHub Actions) and relies on the "gs.txt" naming convention, which is a legacy way to version control Apps Script.
---

---
PROJECT: biotech-intel
WHAT IT ACTUALLY DOES: A multi-source intelligence scraper that pulls data from bioRxiv, ClinicalTrials.gov, FDA CDER, PubMed, and SEC Edgar. It then uses OpenAI (GPT-4o-mini) to synthesize these disparate data points into a concise markdown report for biotech investors.

PERSONA 1 VIEW — RECRUITER: This demonstrates a "scientific librarian" capability coupled with modern data engineering. It shows the candidate understands the key regulatory and clinical data sources required for competitive intelligence in drug development.

PERSONA 2 VIEW — CLIENT: This is a "Biotech News-as-a-Service" deliverable. It replaces the 2-3 hours a day spent checking RSS feeds and government websites with a single, high-quality automated briefing.

TECH STACK VERIFIED: Python 3.x, pandas, requests, OpenAI API, lxml, python-dateutil.

IMPACT SIGNAL: The inclusion of `sec_edgar.py` alongside `pubmed.py` shows a rare bridge between financial/regulatory filings and scientific publication tracking.

GAPS OR CAVEATS: The error handling in the main loop is basic (`try-except` pass), which could lead to silent data gaps if an API schema changes.
---

---
PROJECT: BLKPHXLABS (Dissertation RAG)
WHAT IT ACTUALLY DOES: A local Retrieval-Augmented Generation (RAG) application that allows users to chat with a specific PhD dissertation PDF. It handles the full pipeline from font-aware PDF extraction to vector storage in ChromaDB and conversational synthesis via Gemini 1.5 Flash.

PERSONA 1 VIEW — RECRUITER: This is a "Proof of Concept" for a specialized Knowledge Management System. It suggests the candidate could build similar tools for chatting with Internal Standard Operating Procedures (SOPs) or Regulatory Submission documents.

PERSONA 2 VIEW — CLIENT: This is a "Consultant-in-a-Box" for complex documents. A client would pay for this to quickly digest 200+ page technical reports without reading every line.

TECH STACK VERIFIED: Python, Streamlit, chromadb, google-genai, SentenceTransformer (all-MiniLM-L6-v2), PyMuPDF.

IMPACT SIGNAL: The `extraction.py` script identifies headings based on font size/metadata, showing a level of document-parsing sophistication beyond standard text-stripping.

GAPS OR CAVEATS: The vector store is local and non-distributed, limiting its use to single-user or small-team local deployments.
---

---
PROJECT: BLKPHXLABS.AI_BRIEFING
WHAT IT ACTUALLY DOES: An autonomous pipeline that generates a daily video briefing from Google Alerts. It uses Apps Script to dispatch Gmail threads to a Google Cloud Function, which scrapes the articles, scores relevance, synthesizes a script with Gemini, and produces a video using MoviePy.

PERSONA 1 VIEW — RECRUITER: This is a high-level cloud architecture signal. It demonstrates competency in serverless computing (GCP Functions), cloud storage, and automated media production—skills applicable to large-scale data monitoring in clinical trials.

PERSONA 2 VIEW — CLIENT: This is a "Viral Intelligence" generator. It doesn't just give you text; it gives you a video or audio briefing you can listen to while commuting, automating the entire workflow from news alert to media consumption.

TECH STACK VERIFIED: Google Cloud Functions, Python, Google Apps Script, MoviePy, Google Cloud TTS, Gemini API.

IMPACT SIGNAL: The orchestration between Google Apps Script (as the scheduler/trigger) and GCP (as the heavy-lifter) is a very clever, low-cost architectural pattern.

GAPS OR CAVEATS: The reliance on Google Alerts as the primary source makes it vulnerable to the noise and latency issues inherent in Google's indexing.
---

---
PROJECT: DATA_ANALYTICS
WHAT IT ACTUALLY DOES: A massive repository of academic and professional labs. It contains everything from qPCR gene expression analysis in R to COVID-19 dashboards and a Streamlit-based performance analyzer (rtb_app) for operational data.

PERSONA 1 VIEW — RECRUITER: This repo is a "technical transcript." The `nicotine_gene_expression` and `biostats_course_projects` folders provide the necessary scientific evidence of statistical literacy in a biological context (R, bioconductor, biostats).

PERSONA 2 VIEW — CLIENT: This looks like a portfolio of "Problem Solved" vignettes. A client with a specific data problem (e.g., "my gene expression data is a mess") can see a direct precedent for their project here.

TECH STACK VERIFIED: R (Tidyverse, Shiny), Python (Pandas, Scikit-Learn, PyTorch, Streamlit), SQL, Power BI.

IMPACT SIGNAL: The breadth is the signal here—it covers the entire spectrum from wet-lab data processing (qPCR) to high-level business intelligence.

GAPS OR CAVEATS: It is disorganized (a "mono-repo" style); a reviewer might get lost trying to find the "production" code among the homework assignments.
---

---
PROJECT: email-digest-scheduler
WHAT IT ACTUALLY DOES: A Python-based automation tool that polls an IMAP inbox for specific biotech keywords, uses GPT-4o-mini to summarize the matches, and sends a formatted HTML/PDF digest via SMTP.

PERSONA 1 VIEW — RECRUITER: This demonstrates a practical use of AI to solve information overload. It shows the candidate can handle secure credentials (SSL/TLS) and sensitive data (email) responsibly.

PERSONA 2 VIEW — CLIENT: This is a custom "Personal Assistant" bot. For a CEO who gets 500 emails a day, this script extracts the 5 that actually matter for their business and sends them a summary.

TECH STACK VERIFIED: Python, imaplib, smtplib, openai (v1), beautifulsoup4, zoneinfo.

IMPACT SIGNAL: The regex keyword filter is highly tuned for biotech (`scRNA-seq`, `CRISPR`, `organoid`), showing a specialized domain focus.

GAPS OR CAVEATS: The code is a single script (`email_sweep_summarizer.py`); for professional deployment, it would benefit from being broken into a more modular package structure.
---

---
PROJECT: LabOps.AI
WHAT IT ACTUALLY DOES: A sophisticated "Literature Intelligence" platform for biomanufacturing. It continuously ingests papers from bioRxiv/PubMed, resolves PDFs using Unpaywall, parses them into structured Markdown, and uses Gemini to extract specific bioprocess parameters like Critical Quality Attributes (CQAs) and Critical Process Parameters (CPPs).

PERSONA 1 VIEW — RECRUITER: This is the strongest signal for a Biotech Director role. It explicitly references CQAs and CPPs—the language of the FDA and GMP manufacturing—and shows the candidate can build tools to automate regulatory compliance and process development research.

PERSONA 2 VIEW — CLIENT: This is a "Research Accelerator." It turns a library of thousands of PDFs into a searchable, queryable database that can answer technical manufacturing questions in seconds.

TECH STACK VERIFIED: Python 3.13, SQLite (WAL mode), ChromaDB, Gemini 2.5 Flash, PyMuPDF, Unpaywall API, bioRxiv API.

IMPACT SIGNAL: The `summarizer.py` file uses a JSON schema that specifically extracts `cqa_refs` and `cpp_refs`, demonstrating high-level domain alignment with biopharma manufacturing.

GAPS OR CAVEATS: The "Phase 4 - Process Data Layer" is still in the "Planned" stage, meaning it currently only handles public literature, not actual private manufacturing batch records.
---

---
PROJECT: rtb-comment-generator
WHAT IT ACTUALLY DOES: A specialized data-to-text tool that ingests Ship Dock performance CSVs and uses pandas logic to generate natural-language coaching comments for management. It calculates weighted Units Per Hour (UPH) and identifies specific groups (like "new hires" in LC4-LC5) that need intervention.

PERSONA 1 VIEW — RECRUITER: Signals a candidate who can translate raw metrics into actionable management narratives. This is critical for Director-level roles where technical data must be communicated to non-technical stakeholders.

PERSONA 2 VIEW — CLIENT: This is a "Management Automator." It takes a task that usually takes a manager 30 minutes every morning (reviewing data and writing a summary) and does it in 1 second.

TECH STACK VERIFIED: Python, pandas, argparse, re.

IMPACT SIGNAL: The `RTB_Analysis_Script_V2.0.py` includes "rate dilution" logic for short-hour associates, showing a nuanced understanding of how labor statistics can be misleading.

GAPS OR CAVEATS: No unit tests are visible for the metric calculations, which is risky for a tool used to judge employee performance.
---

PORTFOLIO SUMMARY:
- Total projects reviewed: 8
- Strongest signal for biopharma hiring: LabOps.AI. It uses the specific language of the industry (CQAs/CPPs) and demonstrates a production-grade data pipeline for regulated environments.
- Strongest signal for Upwork freelance clients: AppScriptFXNS / rtb-comment-generator. These solve "messy spreadsheet" and "manual reporting" problems that plague operationally heavy startups.
- Most deployable/demo-ready project: LabOps.AI (Literature Chat). It has a clear CLI and query interface that works out of the box with a Gemini API key.
- Biggest portfolio gap relative to target audience: Lack of explicit GxP validation evidence or Software Quality Assurance (SQA) documentation (e.g., IQ/OQ/PQ protocols) which would be the "final boss" for a Biotech VP hire.
- Recommended GitHub pinned repos (max 6):
  1. LabOps.AI (Flagship)
  2. BLKPHXLABS.AI_BRIEFING (Cloud Architecture)
  3. biotech-intel (Data Engineering)
  4. DATA_ANALYTICS (Scientific Depth)
  5. rtb-comment-generator (Operational Impact)
  6. BLKPHXLABS - Dissertation Chat (NLP/RAG PoC)
