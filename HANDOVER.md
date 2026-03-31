# PolicyCheck AU -- Claude Code Handover

**Date:** 1 April 2026
**Repo:** `mr-rob-curtis/policycheck-au` (created, currently empty)
**Status:** Core engine built and tested. Frontend prototype built. Not yet deployed.
**Deadline pressure:** Small business exemption removal hits 1 July 2026 (91 days)

---

## 1. WHAT THIS IS

PolicyCheck AU scans Australian business websites for privacy policy compliance against the 13 Australian Privacy Principles (APPs). It generates gap analysis reports showing what's missing, scores compliance 0-100, and packages this as a lead-gen tool: free teaser report locked behind a paywall (A$149 Professional / A$499 Enterprise) with cold email outreach to affected sectors.

The regulatory trigger: the Privacy Act small business exemption is being removed for AML-CTF reporting entities from 1 July 2026, and ADM transparency rules land 10 December 2026. This affects 100,000+ businesses who currently have zero privacy compliance infrastructure.

Wave 1 target sectors: Real Estate (8,200 businesses), Chemists/Pharmacies (5,200), Lawyers/Conveyancers (12,900).

---

## 2. ARCHITECTURE

```
policycheck-au/
|-- api/                          # Vercel serverless functions
|   |-- scan.py                   # GET/POST - scrape URL, run analysis, return JSON
|   |-- report.py                 # POST - take analysis JSON, return HTML report
|
|-- lib/                          # Shared Python modules
|   |-- __init__.py
|   |-- policy_scraper.py         # PrivacyPolicyScraper class - finds & extracts policy text
|   |-- compliance_engine.py      # ComplianceEngine class - rule-based APP analysis
|   |-- app_requirements.py       # 13 APP definitions, critical phrases, scoring rules
|   |-- sector_notes.py           # Sector-specific language, gap recommendations, risk profiles
|   |-- report_generator.py       # HTMLReportGenerator - teaser and full HTML reports
|
|-- public/                       # Static frontend
|   |-- index.html                # Self-contained SPA (55KB) with full JS compliance engine
|
|-- server/                       # Flask development server (local testing only)
|   |-- app.py                    # Flask app with SSE streaming, scan management
|   |-- static/app.js             # Dashboard JS
|   |-- static/style.css          # Dashboard CSS
|   |-- templates/index.html      # Dashboard HTML
|   |-- data/scans.json           # Persisted scan results
|
|-- pipeline.py                   # CLI orchestrator for single/batch scans
|-- requirements.txt              # requests, beautifulsoup4
|-- vercel.json                   # Vercel deployment config
|-- .gitignore
```

### Data flow

1. User enters URL on frontend
2. Frontend JS uses CORS proxy (allorigins.win) to fetch the target page
3. JS compliance engine (port of Python engine) analyses policy text client-side
4. Results displayed with animated SVG gauge, expandable APP rows
5. Teaser report generated (locked sections prompt upgrade)

For the server-side path (Vercel functions):
1. `api/scan.py` receives URL, calls `PrivacyPolicyScraper` then `ComplianceEngine`
2. Returns structured JSON with scores, APP results, sector risk profile
3. `api/report.py` takes that JSON, generates HTML via `HTMLReportGenerator`

---

## 3. SOURCE FILES -- WHAT GOES WHERE

### Core engine (production code -- push to repo)

| Source location | Repo destination | Notes |
|---|---|---|
| `policycheck-vercel/lib/policy_scraper.py` | `lib/policy_scraper.py` | Uses requests + BeautifulSoup. 12s timeout. |
| `policycheck-vercel/lib/compliance_engine.py` | `lib/compliance_engine.py` | Rule-based keyword matching with semantic expansion. Has try/except import pattern for Vercel compatibility. |
| `policycheck-vercel/lib/app_requirements.py` | `lib/app_requirements.py` | APPRequirements dataclass, ComplianceScoringRules, SectorSpecificGuidance |
| `policycheck-vercel/lib/sector_notes.py` | `lib/sector_notes.py` | SectorSpecificLanguage, GAP_RECOMMENDATIONS, SectorRiskAssessment, ADM_TRANSPARENCY_DETAILS |
| `policycheck-vercel/lib/report_generator.py` | `lib/report_generator.py` | HTMLReportGenerator with teaser (locked) and full report methods |
| `policycheck-vercel/lib/__init__.py` | `lib/__init__.py` | Empty |
| `policycheck-vercel/api/scan.py` | `api/scan.py` | Vercel serverless handler |
| `policycheck-vercel/api/report.py` | `api/report.py` | Vercel serverless handler |
| `policycheck-vercel/public/index.html` | `public/index.html` | Self-contained 55KB SPA. This IS the deployable frontend. |
| `policycheck-vercel/vercel.json` | `vercel.json` | Vercel config |
| `policycheck-vercel/requirements.txt` | `requirements.txt` | Python deps |
| `policycheck-vercel/.gitignore` | `.gitignore` | Standard Python ignores |

### Reference/development files (keep locally, don't deploy)

| Source location | Purpose |
|---|---|
| `compliance-product/server/` | Flask dev server for local testing |
| `compliance-product/pipeline.py` | CLI batch processor |
| `compliance-product/engine/` | Original engine files (pre-Vercel refactor) |
| `compliance-product/scraper/` | Original scraper with tests |
| `compliance-product/reports/` | Report generator with samples |
| `compliance-product/final_test_reports/` | Test output from 8 real businesses |
| `compliance-product/test_results/` | Earlier test run |
| `compliance-product/mock_policies.json` | Synthetic test data |

### GTM & strategy files (keep in repo under /docs or /gtm)

| Source location | Purpose |
|---|---|
| `compliance-product/gtm/emails-real-estate.md` | 3-email cadence for real estate sector |
| `compliance-product/gtm/emails-chemists.md` | 3-email cadence for pharmacy sector |
| `compliance-product/gtm/emails-lawyers.md` | 3-email cadence for legal sector |
| `compliance-product/gtm/subject-lines.md` | A/B test subject line variants |
| `compliance-product/gtm/sector-hooks.md` | Sector-specific pain points and hooks |
| `compliance-product/gtm/cadence-rules.md` | Timing and follow-up rules |
| `compliance-product/gtm/email-compliance-checklist.md` | AU spam act compliance checklist |
| `compliance-product/landing/index.html` | Marketing landing page with countdown timer |
| `compliance-product/strategist-sector-analysis.md` | Sector prioritisation analysis |

### Research & SOPs

| Source location | Purpose |
|---|---|
| `compliance-product/pythia-study/stage-2 through 7` | Full Pythia study on GTM approach. Verdict: REFINE. Cold email creates credibility debt with this audience. |
| `compliance-product/sable/SOP-PC-001 through 005` | Standard operating procedures |
| `compliance-product/sable/risk-register.md` | Risk register |
| `compliance-product/sable/policycheck-skill.md` | Skill definition for future automation |

---

## 4. KNOWN BUGS & TECHNICAL DEBT

### Bugs to fix

1. **Import pattern is fragile.** `compliance_engine.py` uses try/except to handle `from app_requirements import ...` vs `from lib.app_requirements import ...`. This works but is brittle. Should use relative imports or a proper package structure.

2. **CORS proxy dependency.** The frontend uses `api.allorigins.win` as a CORS proxy to fetch target websites. This is a free third-party service that could go down, rate-limit, or disappear. Need a server-side proxy endpoint.

3. **No error handling for proxy failures.** If allorigins.win is down, the scan silently fails.

4. **Report generator expects specific dict shape.** `HTMLReportGenerator._parse_analysis()` expects `business_name` and `sector` at the top level of the analysis dict. The Flask server was passing them at a different level, causing HTTP 500s. Fixed in Flask, but the contract between scan.py and report.py needs formal validation.

5. **Scoring floor logic is crude.** Policies >500 chars covering 2+ APPs get a minimum score of 15. This was a quick fix to avoid scoring legitimate policies at 0. Needs proper calibration.

### Technical debt

1. **No tests.** Zero unit tests for the compliance engine, scraper, or report generator. The engine has ~1,500 lines of keyword matching logic that could drift.

2. **Rule-based only.** The engine uses keyword/phrase matching with semantic expansion. No NLP, no LLM analysis. This was intentional for v1 (deterministic, fast, no API costs) but limits accuracy.

3. **Duplicate test output folders.** `test_results/`, `test_results_final/`, `final_test_reports/` are three copies of essentially the same test run. Clean up.

4. **No rate limiting.** Both the API endpoints and the scraper have no rate limiting. A bot could hammer the scan endpoint.

5. **No caching.** Every scan re-scrapes the target URL. Should cache results for at least 24 hours.

6. **Reports look "vibe coded."** Rob's words. The HTML reports have poor information hierarchy and need professional design work.

7. **No Stripe/payment integration.** The teaser-to-paid upgrade flow is conceptual only. No actual payment processing.

8. **No email sending infrastructure.** Cold email templates exist but there's no integration with any email service (Mailgun, SendGrid, etc.) or Apollo sequences.

---

## 5. DEPLOYMENT INSTRUCTIONS

### Step 1: Push to GitHub

```bash
cd policycheck-vercel
git remote add origin https://github.com/mr-rob-curtis/policycheck-au.git
git branch -M main
git push -u origin main
```

The policycheck-vercel directory already has a git repo initialised with all files committed. The remote repo exists but is empty.

### Step 2: Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy from project root
cd policycheck-au
vercel --yes

# For production deployment
vercel --prod
```

Or connect via Vercel dashboard: Import Git Repository > select mr-rob-curtis/policycheck-au > Framework Preset: Other > Deploy.

### Step 3: Verify

Once deployed, the public/index.html should serve at the root URL. The API endpoints will be at /api/scan and /api/report. The frontend currently operates entirely client-side (JS engine + CORS proxy), so even if the Python serverless functions have issues, the core scan functionality works.

---

## 6. DEVELOPMENT BACKLOG

Format: GitHub Issues ready to create. Priority is P0 (do now), P1 (do this week), P2 (do before launch), P3 (nice to have).

### P0 -- Ship blockers

**ISSUE-001: Push code to GitHub and deploy to Vercel**
Labels: `infra`, `P0`
The repo exists at mr-rob-curtis/policycheck-au but is empty. Push the policycheck-vercel codebase and connect to Vercel for auto-deploy. Verify scan works end-to-end on production URL.
Acceptance: Live URL that accepts a website URL and returns a compliance score.

**ISSUE-002: Add server-side scan proxy**
Labels: `backend`, `P0`
The frontend relies on allorigins.win (free CORS proxy) to fetch target websites. This is unreliable. Add a `/api/proxy` Vercel function that fetches the target URL server-side and returns the HTML. Update frontend to use this instead.
Acceptance: Scans work without any third-party proxy dependency.

**ISSUE-003: End-to-end smoke test suite**
Labels: `testing`, `P0`
Create pytest suite covering: scraper finds policy on known URLs, engine scores known policy text deterministically, report generator produces valid HTML from known input, API endpoints return correct shapes.
Acceptance: `pytest` passes with 10+ test cases.

### P1 -- This week

**ISSUE-004: Proper Python package structure**
Labels: `refactor`, `P1`
Replace the try/except import hack in compliance_engine.py with proper relative imports. Add `__init__.py` files, use `from .app_requirements import ...` pattern. Ensure it works both locally and on Vercel.
Acceptance: No try/except import blocks remain.

**ISSUE-005: Scan result caching**
Labels: `backend`, `P1`
Cache scan results by URL hash. Return cached result if URL was scanned within last 24 hours. Use Vercel KV or a simple JSON store.
Acceptance: Second scan of same URL returns instantly from cache.

**ISSUE-006: Rate limiting on API endpoints**
Labels: `backend`, `P1`
Add basic rate limiting: 10 scans per IP per hour on free tier. Return 429 with retry-after header.
Acceptance: 11th scan from same IP within an hour returns 429.

**ISSUE-007: Error handling and user feedback**
Labels: `frontend`, `P1`
Currently scan failures are silent or show generic errors. Add specific error states: URL unreachable, no privacy policy found, policy too short to analyse, proxy timeout. Show actionable messages.
Acceptance: Each error case shows a distinct, helpful message.

### P2 -- Before launch (by mid-June)

**ISSUE-008: Report design overhaul**
Labels: `frontend`, `design`, `P2`
Current reports look generic. Redesign with proper information hierarchy: executive summary card at top, traffic-light indicators per APP, expandable detail sections, professional typography, PolicyCheck branding.
Acceptance: Rob signs off on visual quality.

**ISSUE-009: Stripe payment integration**
Labels: `backend`, `payments`, `P2`
Wire up Stripe Checkout for the two paid tiers: Professional (A$149) and Enterprise (A$499). Teaser report shows locked sections with upgrade CTA. Successful payment unlocks full report via unique token/link.
Acceptance: Test purchase on Stripe test mode unlocks full report.

**ISSUE-010: Email capture on free scan**
Labels: `frontend`, `growth`, `P2`
After the free teaser scan, gate the downloadable report behind an email capture form. This builds the prospect list without requiring payment.
Acceptance: Email captured and stored (Vercel KV or external CRM) before report download.

**ISSUE-011: Apollo/CRM integration for prospect lists**
Labels: `growth`, `P2`
Connect Apollo (or alternative) for Wave 1 sector prospect lists. Pull real estate agents, pharmacies, and conveyancers. Map to cold email sequences.
Acceptance: Can pull 100+ prospects per sector with email addresses.

**ISSUE-012: Email sending pipeline**
Labels: `growth`, `P2`
Integrate with SendGrid or Mailgun. Implement the 3-email cadence sequences (already written in /gtm). Include unsubscribe, AU Spam Act compliance (sender ID, ABN, physical address).
Acceptance: Can send a test cadence to Rob's email with proper compliance headers.

**ISSUE-013: ADM transparency module**
Labels: `engine`, `P2`
The ADM (Automated Decision-Making) transparency rules land 10 December 2026. The engine has basic ADM detection but needs the full assessment: does the business use automated profiling, credit scoring, algorithmic hiring, etc. This is the second wave of compliance pressure.
Acceptance: ADM section in report shows specific transparency obligations based on sector.

**ISSUE-014: Landing page with countdown timer**
Labels: `frontend`, `marketing`, `P2`
The marketing landing page exists at compliance-product/landing/index.html but is separate from the app. Integrate or deploy as the homepage, with live countdown to 1 July 2026, sector-specific messaging, social proof, and CTA to free scan.
Acceptance: Live landing page with working countdown and scan CTA.

### P3 -- Post-launch

**ISSUE-015: LLM-enhanced analysis mode**
Labels: `engine`, `P3`
Add optional Claude API analysis for deeper policy review. Run the rule-based engine first, then send ambiguous sections to Claude for nuanced assessment. Charge this as part of the Enterprise tier.
Acceptance: LLM mode produces richer, more accurate analysis with cited reasoning.

**ISSUE-016: Batch scan dashboard**
Labels: `frontend`, `P3`
Admin dashboard for running batch scans across prospect lists. Upload CSV of URLs, run all, download results. For internal use to pre-scan prospects before outreach.
Acceptance: Upload 50 URLs, get 50 results in a downloadable report.

**ISSUE-017: Scheduled re-scan and monitoring**
Labels: `backend`, `P3`
Enterprise tier feature: re-scan client URLs monthly, alert on score changes, track compliance improvement over time.
Acceptance: Automated monthly re-scan with email notification on score change.

**ISSUE-018: Multi-jurisdiction support**
Labels: `engine`, `P3`
Extend beyond AU Privacy Act to GDPR, UK GDPR, NZ Privacy Act. Each jurisdiction gets its own rule set and report section.
Acceptance: Can select jurisdiction and get jurisdiction-specific compliance report.

**ISSUE-019: White-label partner programme**
Labels: `business`, `P3`
Allow accounting firms, legal practices, and IT consultancies to white-label PolicyCheck for their clients. Custom branding, bulk pricing, API access.
Acceptance: Partner can run scans under their own brand with co-branded reports.

---

## 7. KEY DECISIONS & CONTEXT

**Pythia study verdict: REFINE.** The synthetic qual study found that cold email to small business owners creates credibility debt. The audience trusts advisors (accountants, lawyers, IT consultants) more than direct outreach from unknown compliance tools. Rob overrode this for v1 because cold email is fastest to market, but the medium-term play is advisor partnerships.

**Rule-based engine was deliberate.** No LLM dependency means deterministic results, zero per-scan cost, and sub-second analysis. The trade-off is lower accuracy on ambiguous policies. LLM enhancement is P3.

**Self-contained HTML was the pragmatic call.** The 55KB public/index.html contains the entire JS compliance engine, so the frontend works without any backend. The Python serverless functions exist for programmatic access and future features, but the core product is the static page.

**Pricing.** Free scan (teaser, locked sections) / A$149 Professional (full report, remediation checklist) / A$499 Enterprise (full report + ADM assessment + quarterly re-scan). These are untested price points. The Pythia study suggested A$99-149 is the sweet spot for impulse purchase by small business owners.

---

## 8. FIRST SESSION INSTRUCTIONS FOR CLAUDE CODE

```
1. Clone the repo: git clone https://github.com/mr-rob-curtis/policycheck-au.git
2. The repo will be empty. Copy files from the policycheck-vercel/ directory structure above.
3. Push initial commit with all source files.
4. Connect repo to Vercel (vercel link, then vercel --prod).
5. Verify: visit the production URL, enter any Australian business URL, confirm scan completes.
6. Create GitHub Issues from the backlog above (Section 6).
7. Start with ISSUE-002 (server-side proxy) as it's the highest-risk dependency.
```

---

## 9. FILES TO COPY

All deployable code is in: `/sessions/loving-gifted-keller/policycheck-vercel/`

This directory has a git repo already initialised. The cleanest path is:
1. Add the GitHub remote
2. Push to main
3. Connect Vercel to the GitHub repo

All reference files (GTM emails, Pythia study, SOPs, test reports) are in: `/sessions/loving-gifted-keller/mnt/outputs/compliance-product/`

These should go into a `/docs` directory in the repo or stay as local reference material.
