import subprocess
import os
import fitz  # PyMuPDF

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Fabian Alvarez-Primo, PhD - Resume</title>
<style>
  @page {
    size: letter;
    margin: 0.44in 0.5in 0.42in 0.5in;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #111827;
    background-color: #ffffff;
    font-size: 8.8pt;
    line-height: 1.36;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .header {
    text-align: center;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 8px;
    margin-bottom: 10px;
  }
  .header h1 {
    font-size: 20pt;
    font-weight: 800;
    letter-spacing: 0.04em;
    color: #0f172a;
    text-transform: uppercase;
    margin-bottom: 3px;
  }
  .header .tagline {
    font-size: 8.8pt;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #1e3a8a; /* Aerospace deep navy */
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .header .contact-bar {
    font-size: 8.4pt;
    color: #334155;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
  }
  .contact-bar span {
    display: inline-flex;
    align-items: center;
  }
  .contact-bar .separator {
    color: #94a3b8;
    font-weight: 600;
  }
  .contact-bar a {
    color: #0f172a;
    text-decoration: none;
    font-weight: 500;
  }
  .citizen-badge {
    background-color: #0f172a;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 7.6pt;
    padding: 1px 6px;
    border-radius: 3px;
    letter-spacing: 0.03em;
    text-transform: uppercase;
  }

  .section {
    margin-bottom: 9px;
  }
  .section-title {
    font-size: 9.5pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #0f172a;
    border-bottom: 1.2px solid #0f172a;
    padding-bottom: 2px;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }

  .summary-text {
    text-align: justify;
    color: #1f2937;
    font-size: 8.7pt;
    line-height: 1.38;
  }
  .summary-text strong {
    color: #0f172a;
    font-weight: 700;
  }

  /* Core Competencies Grid */
  .competencies-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 4px 10px;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 6px 10px;
  }
  .comp-item {
    font-size: 8.2pt;
    color: #1e293b;
    display: flex;
    align-items: flex-start;
    line-height: 1.25;
  }
  .comp-item::before {
    content: "▪";
    color: #1e3a8a;
    font-size: 8pt;
    margin-right: 5px;
    line-height: 1.2;
  }

  /* Experience Entries */
  .job {
    margin-bottom: 8px;
  }
  .job:last-child {
    margin-bottom: 0;
  }
  .job-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1px;
  }
  .job-title-company {
    font-size: 9.2pt;
  }
  .job-title {
    font-weight: 700;
    color: #0f172a;
  }
  .company {
    font-weight: 600;
    color: #1e3a8a;
  }
  .job-meta {
    font-size: 8.4pt;
    font-weight: 600;
    color: #475569;
    text-align: right;
    white-space: nowrap;
  }
  .job-scope {
    font-size: 8.3pt;
    color: #475569;
    font-style: italic;
    margin-bottom: 3px;
    line-height: 1.3;
  }
  ul.bullets {
    list-style: none;
    padding-left: 0;
  }
  ul.bullets li {
    position: relative;
    padding-left: 12px;
    margin-bottom: 2.5px;
    font-size: 8.5pt;
    color: #1f2937;
    line-height: 1.34;
  }
  ul.bullets li::before {
    content: "•";
    position: absolute;
    left: 1px;
    color: #1e3a8a;
    font-weight: bold;
    font-size: 9pt;
  }
  ul.bullets li strong {
    color: #0f172a;
    font-weight: 700;
  }

  /* Page Break styling */
  .page-break {
    page-break-before: always;
    break-before: page;
  }
  .page-break-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 3px;
    margin-bottom: 9px;
    font-size: 8pt;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .page-break-header span.name {
    font-weight: 700;
    color: #0f172a;
  }

  /* Education */
  .edu-item {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 3px;
    font-size: 8.6pt;
  }
  .edu-degree {
    font-weight: 700;
    color: #0f172a;
  }
  .edu-school {
    color: #334155;
    font-weight: 500;
  }
  .edu-meta {
    font-size: 8.4pt;
    color: #475569;
    font-weight: 600;
    text-align: right;
  }

  /* Technical Tools & Honors */
  .tech-tools {
    font-size: 8.5pt;
    color: #1e293b;
    line-height: 1.4;
  }
  .tech-tools strong {
    color: #0f172a;
  }
  .honors-text {
    font-size: 8.5pt;
    color: #1e293b;
    line-height: 1.4;
  }
  .honors-text strong {
    color: #0f172a;
  }
</style>
</head>
<body>

<!-- PAGE 1 -->
<div class="header">
  <h1>Fabian Alvarez-Primo, PhD</h1>
  <div class="tagline">Operations Manager | High-Volume Material Flow | Safety, Quality & Continuous Improvement</div>
  <div class="contact-bar">
    <span>Savannah, GA</span>
    <span class="separator">·</span>
    <span>+1 (915) 603-2117</span>
    <span class="separator">·</span>
    <span><a href="mailto:fpalvarez23@gmail.com">fpalvarez23@gmail.com</a></span>
    <span class="separator">·</span>
    <span><a href="https://linkedin.com/in/fpalvarez23">linkedin.com/in/fpalvarez23</a></span>
    <span class="separator">·</span>
    <span class="citizen-badge">U.S. Citizen (ITAR Compliant)</span>
  </div>
</div>

<div class="section">
  <div class="section-title">Professional Summary</div>
  <div class="summary-text">
    Operations Manager who takes extreme ownership of high-volume material flow. Currently runs a <strong>60+ associate</strong> outbound operation at Amazon at <strong>99.7% quality compliance</strong>, with a <strong>0.0% serious incident rate</strong> sustained for 9+ months and DPMO <strong>29% better than goal</strong>. Raised dock throughput <strong>82%</strong> by building custom data tooling (Python, SQL, browser automation, live dashboards) to find and remove bottlenecks. Brings a Ph.D. in Materials Science & Engineering and a B.S. in Metallurgical & Materials Engineering, plus prior supervision of a CLIA/COLA-regulated laboratory. Comfortable reading hardware, specs, and data alongside Engineering and Production.
  </div>
</div>

<div class="section">
  <div class="section-title">Core Competencies</div>
  <div class="competencies-grid">
    <div class="comp-item">Operations & Material Flow Management</div>
    <div class="comp-item">People Leadership (Supervisors, PAs, Associates)</div>
    <div class="comp-item">Safety Culture (0.0% SIR, OSHA Enforcement)</div>
    <div class="comp-item">KPI Design, Dashboards & Analytics (SQL, Python)</div>
    <div class="comp-item">Root Cause & Corrective Action / Lean</div>
    <div class="comp-item">Quality Systems (CLIA, COLA, cGMP, ISO 9001)</div>
    <div class="comp-item">Inventory & Location Accuracy</div>
    <div class="comp-item">Cross-functional Execution (Eng / Prod / Quality)</div>
    <div class="comp-item">Materials Engineering & Metallurgy (PhD)</div>
  </div>
</div>

<div class="section">
  <div class="section-title">Professional Experience</div>

  <div class="job">
    <div class="job-header">
      <div class="job-title-company">
        <span class="job-title">Operations Manager II (Area Manager, L5)</span> | <span class="company">Amazon</span>
      </div>
      <div class="job-meta">Savannah, GA &nbsp;|&nbsp; 2024 – Present</div>
    </div>
    <div class="job-scope">
      Owns outbound dock operations (on-time departures, shipping-sorter recirculation). Prior scope covered upper mezzanine, transship, vendor returns, and shipping sort.
    </div>
    <ul class="bullets">
      <li>Lead a <strong>60+ associate</strong> operation across a compressed 4-day schedule through Process Assistants and floor leads, holding <strong>99.7% quality compliance</strong>.</li>
      <li>Raised dock rate <strong>82% (220 → 400+ units/hr)</strong> and cut recirculation from <strong>5% to below 2%</strong> with data-driven staffing models, chute-level congestion diagnostics, and standardized material paths.</li>
      <li>Sustained a <strong>0.0% Serious Incident Rate for 9+ consecutive months</strong>; run daily barrier sweeps and safety-reporting mechanisms on shift.</li>
      <li>Beat the DPMO goal by <strong>29% (5,291 vs. 7,500, Jan–Apr 2026)</strong> and held AR COS penetration at <strong>92.6–94.4% vs. a 90% goal</strong>.</li>
      <li>Built a container-to-physical-location staging audit tool that maps material to its location, reducing missed packages and DPMO risk.</li>
      <li>Engineered a three-layer flow-visibility system: a browser-automation scraper of WIP data, a real-time analytics layer (root causes, staffing ratios, DPMO, hourly throughput), and a staffing/rate tool. It replaced manual workflows and enabled proactive labor deployment.</li>
      <li>Stood up Vendor Returns operations from scratch at site, with no prior operational structure.</li>
      <li>Developed <strong>15 Process Assistants</strong> (up to <strong>9 concurrently</strong>) and <strong>2 new leaders</strong> into full role ownership. Trained the Operations Manager and Area Managers on shift procedures, and ran Ship Dock and the DEA team while the Operations Manager was absent.</li>
      <li>Built a Python/statistical performance-review tool (curve-fit throughput by process path) that removes subjectivity from write-ups; in production use for ~8 months.</li>
    </ul>
  </div>

  <div class="job" style="margin-top: 6px;">
    <div class="job-header">
      <div class="job-title-company">
        <span class="job-title">Account Executive</span> | <span class="company">DISH Network</span>
      </div>
      <div class="job-meta">2023 – 2024</div>
    </div>
    <ul class="bullets">
      <li>Built Tableau analytics to drive customer-retention strategy.</li>
      <li>Won a company-wide award for the highest contracts sold during training; promoted to Account Executive, performing at <strong>&gt;95% of company average</strong>.</li>
    </ul>
  </div>
</div>

<!-- PAGE 2 -->
<div class="page-break"></div>

<div class="page-break-header">
  <span class="name">Fabian Alvarez-Primo, PhD</span>
  <span>Operations Manager &nbsp;•&nbsp; SpaceX Application &nbsp;•&nbsp; Page 2</span>
</div>

<div class="section">
  <div class="section-title">Professional Experience (Continued)</div>

  <div class="job">
    <div class="job-header">
      <div class="job-title-company">
        <span class="job-title">Post-doctoral Research Fellow</span> | <span class="company">Texas Tech University Health Sciences Center</span>
      </div>
      <div class="job-meta">El Paso, TX &nbsp;|&nbsp; 2022</div>
    </div>
    <ul class="bullets">
      <li>Ran biobanking operations covering sample intake, processing, controlled storage, and chain-of-custody documentation.</li>
      <li>Led a cell-reprogramming project under <strong>cGMP-compliant</strong> protocols. Coordinated timelines and deliverables across clinical, molecular, and neuroscience teams.</li>
    </ul>
  </div>

  <div class="job" style="margin-top: 6px;">
    <div class="job-header">
      <div class="job-title-company">
        <span class="job-title">Clinical Laboratory Scientist & Supervisor</span> | <span class="company">West Texas Pain Institute</span>
      </div>
      <div class="job-meta">El Paso, TX &nbsp;|&nbsp; 2021 – 2022</div>
    </div>
    <ul class="bullets">
      <li>Supervised a team of <strong>9</strong> processing <strong>1,300+ patient samples per month</strong>, with full <strong>CLIA and COLA</strong> compliance and audit readiness.</li>
      <li>Enforced OSHA protocols and documentation discipline. Operated and maintained LC/MS, immunoassay, and DNA sequencing instrumentation.</li>
      <li>Ran the LIS (Stratus DX) and EMR data systems, keeping records accurate and compliant.</li>
    </ul>
  </div>

  <div class="job" style="margin-top: 6px;">
    <div class="job-header">
      <div class="job-title-company">
        <span class="job-title">Doctoral Research Assistant</span> | <span class="company">Inspired Materials & Stem Cell Tissue Engineering Lab, UTEP</span>
      </div>
      <div class="job-meta">El Paso, TX &nbsp;|&nbsp; 2017 – 2020</div>
    </div>
    <ul class="bullets">
      <li>Ran lab operations across <strong>5+ concurrent projects</strong>: equipment scheduling, reagent procurement, SOPs, and data management.</li>
      <li>Mentored <strong>30+ students</strong> on scanning electron microscopy and 3D printing. Improved 3D printer manufacturing precision <strong>30%</strong> through hardware modifications.</li>
      <li>Developed and characterized a conductive composite following ASTM and <strong>ISO 9001</strong> standards. Co-authored a failure analysis study (<em>Journal of Failure Analysis and Prevention</em>, 2019).</li>
    </ul>
  </div>

  <div class="job" style="margin-top: 6px;">
    <div class="job-header">
      <div class="job-title-company">
        <span class="job-title">R&D Engineer Intern</span> | <span class="company">Climax Molybdenum</span>
      </div>
      <div class="job-meta">Sahuarita, AZ &nbsp;|&nbsp; 2015</div>
    </div>
    <ul class="bullets">
      <li>Developed ASTM test methods for a refractory ceramic in leaching-vessel service and wrote the material-handling SOP.</li>
    </ul>
  </div>
</div>

<div class="section" style="margin-top: 8px;">
  <div class="section-title">Education</div>
  <div class="edu-item">
    <div>
      <span class="edu-degree">Ph.D., Materials Science & Engineering</span> &nbsp;|&nbsp; <span class="edu-school">The University of Texas at El Paso</span>
    </div>
    <div class="edu-meta">2020 &nbsp;|&nbsp; GPA 3.91</div>
  </div>
  <div class="edu-item">
    <div>
      <span class="edu-degree">B.S., Metallurgical & Materials Engineering</span> &nbsp;|&nbsp; <span class="edu-school">The University of Texas at El Paso</span>
    </div>
    <div class="edu-meta">2015</div>
  </div>
</div>

<div class="section" style="margin-top: 8px;">
  <div class="section-title">Technical Tools & Methodologies</div>
  <div class="tech-tools">
    <strong>Data & Software:</strong> Python (pandas, scikit-learn, Streamlit), SQL, R, Excel / Google Sheets (advanced modeling), Google Apps Script, JavaScript (browser automation), MATLAB, Tableau<br>
    <strong>Hardware & Engineering:</strong> SolidWorks, AutoCAD, Scanning Electron Microscopy (SEM), X-ray Diffraction (XRD), Mechanical Testing (ASTM standards), 3D Printing / Additive Manufacturing<br>
    <strong>Quality & Compliance:</strong> Root Cause & Corrective Action (RCCA), Lean / Continuous Improvement, CLIA, COLA, cGMP, ISO 9001, OSHA
  </div>
</div>

<div class="section" style="margin-top: 8px;">
  <div class="section-title">Publications & Honors</div>
  <div class="honors-text">
    <strong>Publications:</strong> <strong>7</strong> peer-reviewed journal publications, including failure analysis and materials characterization.<br>
    <strong>Honors & Professional Societies:</strong> Tau Beta Pi (Engineering Honor Society) · Alpha Sigma Mu (Materials Science & Engineering Honor Society) · Alpha Chi · Society for Biomaterials (President, 2 terms)
  </div>
</div>

</body>
</html>
"""

html_path = r"C:\Users\f4l\iCloudDrive\iCloud~md~obsidian\Professional\Resumes\temp_resume.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

out_pdf = r"C:\Users\f4l\iCloudDrive\iCloud~md~obsidian\Professional\Resumes\FabianAlvarez_SpaceX_OperationsManager.pdf"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={out_pdf}",
    html_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome return code:", res.returncode)

if os.path.exists(out_pdf):
    doc = fitz.open(out_pdf)
    print("PDF Page Count:", len(doc))
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(dpi=150)
        pix.save(f"page_{i+1}.png")
        print(f"Saved page_{i+1}.png, dimensions: {pix.width}x{pix.height}")
    doc.close()
else:
    print("PDF was not created!")
