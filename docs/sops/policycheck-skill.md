# PolicyCheck AU Skill Definition

**Skill Name:** PolicyCheck
**Owner:** Sable (Head of Research) / Rob (Product Lead)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-01

---

## Skill Metadata

```yaml
name: PolicyCheck
description: "Orchestrate end-to-end Australian Privacy Act compliance analysis for business websites"
version: "1.0"
owner: "Sable"
owner_email: "sable@pythia.com"
created: "2026-04-01"
updated: "2026-04-01"
github_repo: "pythia/policycheck-au"
documentation_url: "https://docs.policycheck.au"
support_email: "support@policycheck.au"
```

---

## Purpose

The PolicyCheck skill orchestrates the complete PolicyCheck AU workflow: prospect discovery, policy scraping, compliance analysis (rule-based + LLM), report generation, and outreach campaign preparation. It handles single prospect analysis and batch processing.

---

## Skill Inputs

### Single Prospect Mode

```json
{
  "mode": "single",
  "input": {
    "company_name": "Acme Corp AU",
    "website_url": "https://acme.example.com.au",
    "industry_sector": "professional-services",
    "contact_email": "privacy@acme.example.com.au",
    "delivery_tier": "teaser|standard|premium",
    "run_analysis": true,
    "generate_report": true,
    "prepare_outreach": true,
    "priority": "normal|high"
  }
}
```

### Batch Mode (Prospect List)

```json
{
  "mode": "batch",
  "input": {
    "prospect_list_id": "LIST-20260401-001",
    "segment": "health|finance|retail|saas|other",
    "company_size_min": 10,
    "company_size_max": 5000,
    "delivery_tier": "teaser",
    "run_analysis": true,
    "generate_report": true,
    "prepare_outreach": true,
    "batch_size_limit": 500,
    "priority": "normal"
  }
}
```

### Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| **mode** | enum | Yes | "single" or "batch" | "single" |
| **company_name** | string | Yes (single) | Business name to analyze | "Acme Corp AU" |
| **website_url** | string | Yes (single) | Company website URL | "https://example.com.au" |
| **industry_sector** | enum | Yes | Industry classification | "health", "finance", "retail", "saas", "other" |
| **contact_email** | string | No | Primary contact for outreach | "privacy@acme.com.au" |
| **delivery_tier** | enum | Yes | Report detail level | "teaser", "standard", "premium" |
| **run_analysis** | boolean | Yes | Run compliance analysis | true |
| **generate_report** | boolean | Yes | Generate final report | true |
| **prepare_outreach** | boolean | Yes | Prepare outreach email | true |
| **batch_size_limit** | integer | No (batch) | Max records per batch | 500 |
| **priority** | enum | No | Processing priority | "normal" or "high" |

---

## Skill Execution Stages

The PolicyCheck skill executes through **5 sequential stages**, each with defined inputs, outputs, and quality gates:

```
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 0: INPUT VALIDATION & PROSPECTION                        │
├─────────────────────────────────────────────────────────────────┤
│  Input:   company_name, website_url, sector, mode               │
│  Process: Validate input; enrich via Artemis; check CRM records │
│  Output:  prospect_record_id, enriched_prospect_data            │
│  Gate:    ✓ Valid email format; ✓ Website responsive; ✓ Not on  │
│           do-not-contact list                                   │
│  Owner:   Artemis + Prospect Management                         │
│  SOP:     PC-001 (Section 1-2)                                  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 1: POLICY SCRAPING & EXTRACTION                          │
├─────────────────────────────────────────────────────────────────┤
│  Input:   prospect_record_id, website_url                       │
│  Process: Discover policy URL; scrape; extract text; validate   │
│  Output:  policy_html, policy_text, metadata                    │
│  Gate:    ✓ Policy found (or POLICY_ABSENT flagged); ✓ Content  │
│           >500 words; ✓ MD5 hash checked (duplicate)            │
│  Owner:   Artemis Scraper + Data Quality                        │
│  SOP:     PC-001 (Section 2-3)                                  │
│  KPI:     Success rate >85%; Quality pass rate >90%             │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 2: COMPLIANCE ANALYSIS                                   │
├─────────────────────────────────────────────────────────────────┤
│  Input:   policy_text, industry_sector, app_definitions v[N]    │
│  Process: Mode A (rule-based); Mode B (LLM) if needed; sector   │
│           adjustments; confidence assessment                    │
│  Output:  app_scores[], confidence_score, gaps[], recommendations│
│  Gate:    ✓ Confidence ≥ tier threshold; ✓ All 13 APPs scored   │
│           or N/A; ✓ Analyst sign-off if required                │
│  Owner:   Compliance Analysis Team                              │
│  SOP:     PC-002 (Sections 2-7)                                 │
│  KPI:     Avg confidence >80%; Analyst agreement >90%           │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 3: REPORT GENERATION                                     │
├─────────────────────────────────────────────────────────────────┤
│  Input:   app_scores, gaps, recommendations, tier, company_info │
│  Process: Generate report PDF; apply tier template; add         │
│           disclaimer; validate QA checks                        │
│  Output:  report_pdf, report_id, portal_url                     │
│  Gate:    ✓ 3-layer email QA passed; ✓ Disclaimer exact;        │
│           ✓ All 13 APPs present (or justified N/A)              │
│  Owner:   Report Generation & QA                                │
│  SOP:     PC-003 (Sections 2-5)                                 │
│  KPI:     QA pass rate >98%; Delivery success >99%              │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 4: OUTREACH PREPARATION                                  │
├─────────────────────────────────────────────────────────────────┤
│  Input:   prospect_record, report_id, tier, contact_email       │
│  Process: Render outreach email (sector-specific); apply Spam   │
│           Act checks; schedule delivery; log in CRM             │
│  Output:  outreach_email_draft, delivery_schedule, campaign_id  │
│  Gate:    ✓ All Spam Act elements present; ✓ Subject line       │
│           honest; ✓ Cadence rules met; ✓ Unsubscribe link works │
│  Owner:   Outreach & Compliance Team                            │
│  SOP:     PC-004 (Sections 2-5)                                 │
│  KPI:     Deliverability >95%; Bounce rate <2%                  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 5: COMPLETION & LOGGING                                  │
├─────────────────────────────────────────────────────────────────┤
│  Input:   All previous stage outputs                            │
│  Process: Log in CRM; archive records; trigger follow-up        │
│           sequence (if applicable)                              │
│  Output:  prospect_record_complete, audit_trail, next_actions   │
│  Gate:    ✓ All data persisted; ✓ Audit trail complete; ✓       │
│           Prospect status updated                               │
│  Owner:   CRM & Automation                                      │
│  SOP:     All (cross-cutting)                                   │
│  KPI:     Data integrity 100%; Audit trail complete             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Stage Details

### STAGE 0: Input Validation & Prospection

**Trigger Condition:** Skill invoked with valid mode & input parameters

**Input Validation:**
```python
def validate_input(mode, input_params):
    if mode == "single":
        assert input_params.company_name is not None
        assert input_params.website_url is not None
        assert validate_url_format(input_params.website_url)
        assert input_params.industry_sector in VALID_SECTORS
        assert input_params.delivery_tier in ["teaser", "standard", "premium"]
    elif mode == "batch":
        assert input_params.prospect_list_id is not None
        assert input_params.segment in VALID_SECTORS
        assert input_params.batch_size_limit > 0 and input_params.batch_size_limit <= 500
    return True
```

**Prospection (via Artemis):**
- Query Artemis with company name + domain
- Enrich with: ABN, employee count, contact info, industry classification
- Check CRM for existing records (avoid duplicate analysis)
- Verify business not on do-not-contact list

**Output:**
```json
{
  "stage": 0,
  "status": "COMPLETE",
  "prospect_record_id": "PRO-20260401-00001",
  "prospect_data": {
    "company_name": "Acme Corp AU",
    "abn": "12345678901",
    "website_url": "https://acme.example.com.au",
    "industry_sector": "professional-services",
    "estimated_employees": 45,
    "enriched_at": "2026-04-01T09:00:00Z",
    "crm_check": "NEW_PROSPECT",
    "ready_for_stage_1": true
  }
}
```

**Quality Gate Decision:**
- ✓ PASS: Proceed to Stage 1
- ✗ FAIL: Return error (invalid company, already analyzed, on do-not-contact list)

---

### STAGE 1: Policy Scraping & Extraction

**Trigger Condition:** Stage 0 PASS; prospect_record_id available

**Process Flow:**
1. Attempt to discover policy URL via standard paths
2. If not found → Mark as POLICY_ABSENT; flag for manual verification
3. If found → Scrape content; extract text
4. Run quality checks (see SOP-PC-001 Section 2.3)
5. Store in secure storage (encrypted)

**Implementation Detail:**
```python
def scrape_and_extract(prospect_record_id, website_url):
    policy_url = discover_policy_url(website_url)
    if not policy_url:
        return {
            "status": "POLICY_ABSENT",
            "policy_html": None,
            "policy_text": None,
            "metadata": {"discovery_attempted": True}
        }

    policy_html = scrape_with_retry(policy_url, max_retries=3)
    policy_text = extract_text(policy_html)

    # Quality checks
    if len(policy_text) < 500:
        raise QualityError("Policy too short (<500 words)")

    # Duplicate detection
    policy_hash = md5(policy_text)
    if exists_in_database(policy_hash):
        return {"status": "DUPLICATE", "original_prospect_id": "..."}

    return {
        "status": "SUCCESS",
        "policy_html": policy_html,
        "policy_text": policy_text,
        "metadata": {
            "policy_url": policy_url,
            "scrape_timestamp": now(),
            "content_length": len(policy_text),
            "hash": policy_hash
        }
    }
```

**Output:**
```json
{
  "stage": 1,
  "status": "COMPLETE",
  "prospect_record_id": "PRO-20260401-00001",
  "policy_data": {
    "policy_html": "[full HTML...]",
    "policy_text": "[extracted text...]",
    "metadata": {
      "policy_url": "https://acme.example.com.au/privacy-policy",
      "scrape_timestamp": "2026-04-01T09:15:00Z",
      "content_length": 3427,
      "quality_checks_passed": true
    }
  }
}
```

**Quality Gate Decision:**
- ✓ PASS: Policy found, >500 words, not duplicate → Proceed to Stage 2
- ✓ PASS_WITH_FLAG: Policy found, older than 2 years → Proceed to Stage 2; flag in report
- ✗ FAIL: Policy absent, <500 words, or duplicate → Stop; log reason; add to "requires manual review"

---

### STAGE 2: Compliance Analysis

**Trigger Condition:** Stage 1 PASS; policy_text available

**Workflow:**

```
A. Rule-Based Analysis (Mode A)
   ├─ For each APP 1-13:
   │  ├─ Keyword search
   │  ├─ Semantic pattern match
   │  ├─ Specificity assessment
   │  └─ Contradiction detection
   ├─ Output: app_scores[] (0-1 for each APP)
   └─ Confidence: 95% (deterministic)

B. Confidence Gate
   ├─ If app_coverage_rate > 80% AND confidence > 85%:
   │  └─ SKIP Mode B (LLM); proceed to reporting
   ├─ Else:
   │  └─ Proceed to Mode B

C. LLM Analysis (Mode B)
   ├─ Run GPT-4 with policy text
   ├─ Extract gaps, recommendations
   ├─ Assess regulatory risk
   └─ Output: gaps[], recommendations[], confidence_score (70-100)

D. Sector Adjustments
   ├─ Apply sector-specific APP sensitivity overrides
   ├─ Compare to industry norms
   └─ Adjust risk severity if needed

E. Human Review Gate
   ├─ If tier PREMIUM: Mandatory analyst + legal review
   ├─ If tier STANDARD & confidence 70-84%: Analyst review
   ├─ If tier TEASER & confidence < 70%: Do not deliver
```

**Code Pseudocode:**
```python
def analyze_compliance(prospect_record_id, policy_text, sector, tier):
    # Mode A: Rule-based
    mode_a_result = rule_based_analysis(policy_text)
    app_scores = mode_a_result['app_scores']
    app_coverage = mode_a_result['coverage_rate']

    # Confidence gate
    if app_coverage > 0.80 and confidence_score(mode_a_result) > 0.85:
        confidence_score = 0.90
        needs_llm = False
    else:
        needs_llm = True

    # Mode B: LLM (if needed)
    if needs_llm:
        mode_b_result = llm_analysis(policy_text, tier)
        gaps = mode_b_result['gaps']
        confidence_score = mode_b_result['confidence']
    else:
        gaps = []
        recommendations = []

    # Sector adjustments
    sector_context = load_sector_guidance(sector)
    app_scores = apply_sector_overrides(app_scores, sector_context)

    # Analyst review gate
    if tier == "PREMIUM":
        analyst_review_required = True
    elif confidence_score < 0.70:
        analyst_review_required = True
    elif tier == "STANDARD" and confidence_score < 0.80:
        analyst_review_required = True
    else:
        analyst_review_required = False

    return {
        "app_scores": app_scores,
        "gaps": gaps,
        "recommendations": recommendations,
        "confidence_score": confidence_score,
        "analyst_review_required": analyst_review_required
    }
```

**Output:**
```json
{
  "stage": 2,
  "status": "COMPLETE",
  "prospect_record_id": "PRO-20260401-00001",
  "analysis_data": {
    "app_scores": {
      "1": 0.8, "2": 0.9, "3": 0.7, "4": 0.6, "5": 0.8,
      "6": 0.5, "7": 0.9, "8": 0.0, "9": 0.0, "10": 0.7,
      "11": 0.4, "12": 0.8, "13": 0.6
    },
    "overall_score": 0.65,
    "confidence_score": 0.78,
    "gaps": [
      {
        "app_principle": 11,
        "description": "Policy does not mention encryption or security measures",
        "severity": "HIGH",
        "recommendation": "Add: 'We encrypt customer data in transit using TLS 1.3'"
      }
    ],
    "analyst_review_required": true,
    "analyst_assigned": "analyst-id-xyz",
    "analysis_timestamp": "2026-04-01T09:30:00Z"
  }
}
```

**Quality Gate Decision:**
- ✓ PASS (High Confidence): Confidence ≥ 85% & tier requirements met → Proceed to Stage 3
- ✓ PASS_WITH_REVIEW (Medium Confidence): Confidence 70-84%; analyst review complete → Proceed to Stage 3
- ✗ FAIL (Low Confidence): Confidence < 70%; cannot deliver (teaser only) → Stop; escalate

---

### STAGE 3: Report Generation

**Trigger Condition:** Stage 2 PASS; analysis_data available; analyst sign-off (if required)

**Report Template Application:**
```python
def generate_report(analysis_data, tier, prospect_record):
    if tier == "TEASER":
        template = load_template("teaser-report.html")
        sections = ["executive_summary", "top_gaps", "cta"]
    elif tier == "STANDARD":
        template = load_template("standard-report.html")
        sections = ["executive_summary", "app_details", "gaps", "recommendations", "sector_context"]
    elif tier == "PREMIUM":
        template = load_template("premium-report.html")
        sections = ["executive_summary", "app_details", "gaps", "recommendations", "legal_risk", "sector_context", "peer_comparison"]

    # Populate template
    report_html = template.render({
        "company_name": prospect_record.company_name,
        "overall_score": analysis_data.overall_score,
        "confidence_score": analysis_data.confidence_score,
        "app_scores": analysis_data.app_scores,
        "gaps": analysis_data.gaps,
        "recommendations": analysis_data.recommendations,
        "sector_context": load_sector_context(prospect_record.sector),
        "analyst_name": analysis_data.analyst_name,
        "analysis_date": analysis_data.analysis_timestamp,
        "disclaimer": DISCLAIMER_TEXT
    })

    # Generate PDF
    report_pdf = html_to_pdf(report_html, options={"page_size": "A4"})

    # QA Validation
    qc_result = validate_report_qa(report_pdf, tier)
    if not qc_result.pass:
        raise QAError(f"Report QA failed: {qc_result.errors}")

    # Generate unique report ID
    report_id = f"PC-{date.today().strftime('%Y%m%d')}-{sequence_counter()}-{tier[0].upper()}"

    # Store
    store_report_secure(report_id, report_pdf, prospect_record_id)

    return {
        "report_id": report_id,
        "report_pdf": report_pdf,
        "portal_url": f"https://policycheck.au/reports/{report_id}"
    }
```

**QA Validation (3-layer, per SOP-PC-005):**
1. Automated checks (report structure, disclaimer exact, etc.)
2. Manual sample review (tone, accuracy of excerpts)
3. Compliance officer sign-off (email readiness, Spam Act elements)

**Output:**
```json
{
  "stage": 3,
  "status": "COMPLETE",
  "prospect_record_id": "PRO-20260401-00001",
  "report_data": {
    "report_id": "PC-20260401-00001-T",
    "tier": "teaser",
    "report_url": "https://policycheck.au/reports/PC-20260401-00001-T",
    "report_pdf_path": "/secure-storage/reports/PC-20260401-00001-T.pdf",
    "generated_at": "2026-04-01T09:45:00Z",
    "qc_passed": true,
    "pages": 2
  }
}
```

**Quality Gate Decision:**
- ✓ PASS: QA 3-layer complete; all checks passed → Proceed to Stage 4
- ✗ FAIL: QA check failed → Return to analyst for correction; restart generation

---

### STAGE 4: Outreach Preparation

**Trigger Condition:** Stage 3 PASS; report_id available; prospect contact info available

**Process Flow:**
1. Retrieve sector-specific email template
2. Populate with prospect data, report URL, personalization
3. Run 3-layer email QA (automated, manual, compliance)
4. Schedule delivery via SendGrid
5. Log in CRM with delivery metadata

**Email Template Selection:**
```python
def select_email_template(sector, tier, prospect_response_history):
    if prospect_response_history is None:
        # First email
        if tier == "TEASER":
            return load_template(f"email-{sector}-teaser-1.html")
        else:
            return load_template(f"email-{sector}-standard-1.html")
    elif days_since_first_email < 14:
        # Too soon for follow-up
        raise OutreachError("Cadence rule violation: <14 days since first email")
    elif days_since_first_email < 35:
        # Second email
        return load_template(f"email-{sector}-followup-2.html")
    else:
        # Final email
        return load_template(f"email-{sector}-final-3.html")
```

**Email QA Validation (SOP-PC-004, SOP-PC-005):**
```python
def validate_email_qa(email_draft):
    # Layer 1: Automated
    automated_checks = {
        "recipient_format_valid": is_valid_email(email_draft.to),
        "subject_line_present": bool(email_draft.subject),
        "footer_complete": has_footer_elements(email_draft.body),
        "no_spam_keywords": not has_spam_keywords(email_draft.subject),
        "from_reply_to_set": bool(email_draft.from_addr and email_draft.reply_to),
        "links_functional": all_links_return_200(email_draft.body),
        "personalization_complete": not has_unfilled_tokens(email_draft.body),
        "recipient_not_opted_out": not is_opted_out(email_draft.to),
        "no_duplicate_send": not sent_in_last_14_days(email_draft.to, email_draft.campaign_id)
    }

    if not all(automated_checks.values()):
        raise QAError(f"Layer 1 failed: {[k for k,v in automated_checks.items() if not v]}")

    # Layer 2: Manual review (sample of 5 emails per campaign)
    # [performed by analyst]

    # Layer 3: Compliance officer sign-off
    # [performed by compliance officer]

    return True
```

**Delivery Scheduling:**
```python
def schedule_delivery(email_draft, priority="normal"):
    # Pace delivery: max 200/hour
    send_time = calculate_send_time_with_pacing(priority)

    # Log in CRM
    crm_entry = {
        "prospect_id": email_draft.prospect_id,
        "email_address": email_draft.to,
        "campaign_id": email_draft.campaign_id,
        "report_id": email_draft.report_id,
        "scheduled_send_time": send_time,
        "tier": email_draft.tier,
        "sequence_number": email_draft.sequence_number,
        "created_at": now()
    }
    log_to_crm(crm_entry)

    # Queue in SendGrid
    queue_email_for_delivery(email_draft, send_time)

    return {
        "email_queued": True,
        "scheduled_send_time": send_time,
        "crm_entry_id": crm_entry.id
    }
```

**Output:**
```json
{
  "stage": 4,
  "status": "COMPLETE",
  "prospect_record_id": "PRO-20260401-00001",
  "outreach_data": {
    "email_drafted": true,
    "campaign_id": "CAMP-20260401-001",
    "recipient": "privacy@acme.example.com.au",
    "scheduled_send_time": "2026-04-01T10:00:00Z",
    "tier": "teaser",
    "sequence": 1,
    "qc_passed": true,
    "crm_logged": true
  }
}
```

**Quality Gate Decision:**
- ✓ PASS: All QA layers passed; delivery scheduled → Proceed to Stage 5
- ✗ FAIL: QA failed (typically Layer 1) → Return to analyst; fix issue; re-validate

---

### STAGE 5: Completion & Logging

**Trigger Condition:** Stages 0-4 all COMPLETE

**Actions:**
1. Update prospect record status in CRM
2. Archive all analysis/report data
3. Create audit trail (full lineage from prospect → report → outreach)
4. Log KPIs (processing time, queue position)
5. Trigger follow-up automation (if applicable)

**Completion Record:**
```python
def complete_workflow(prospect_record_id, stage_outputs):
    # Update CRM
    crm_update = {
        "prospect_id": prospect_record_id,
        "status": "ANALYSIS_COMPLETE",
        "stage_0_output": stage_outputs[0],
        "stage_1_output": stage_outputs[1],
        "stage_2_output": stage_outputs[2],
        "stage_3_output": stage_outputs[3],
        "stage_4_output": stage_outputs[4],
        "completed_at": now(),
        "processing_time_minutes": calculate_processing_time()
    }
    update_crm(crm_update)

    # Archive
    archive_workflow_data(prospect_record_id, stage_outputs)

    # Audit trail
    audit_trail = {
        "prospect_id": prospect_record_id,
        "workflow_lineage": {
            "prospect_record_id": stage_outputs[0].prospect_record_id,
            "policy_content_hash": stage_outputs[1].metadata.hash,
            "analysis_id": stage_outputs[2].analyst_assigned,
            "report_id": stage_outputs[3].report_data.report_id,
            "campaign_id": stage_outputs[4].outreach_data.campaign_id
        },
        "checkpoints": [s.status for s in stage_outputs],
        "created_at": now()
    }
    log_audit_trail(audit_trail)
```

**Output:**
```json
{
  "stage": 5,
  "status": "COMPLETE",
  "prospect_record_id": "PRO-20260401-00001",
  "workflow_summary": {
    "overall_status": "SUCCESS",
    "stage_results": [
      {"stage": 0, "status": "COMPLETE"},
      {"stage": 1, "status": "COMPLETE"},
      {"stage": 2, "status": "COMPLETE"},
      {"stage": 3, "status": "COMPLETE"},
      {"stage": 4, "status": "COMPLETE"}
    ],
    "key_outputs": {
      "prospect_id": "PRO-20260401-00001",
      "report_id": "PC-20260401-00001-T",
      "report_url": "https://policycheck.au/reports/PC-20260401-00001-T",
      "campaign_id": "CAMP-20260401-001",
      "email_scheduled_for": "2026-04-01T10:00:00Z"
    },
    "processing_metrics": {
      "total_time_minutes": 45,
      "stages_completed": 5,
      "qc_gates_passed": 3,
      "analyst_interventions": 1
    },
    "next_actions": [
      "Monitor email delivery (scheduled for 2026-04-01T10:00:00Z)",
      "Schedule follow-up email if no response by 2026-04-14",
      "Track customer lifecycle (conversion to paid report)"
    ]
  }
}
```

---

## Batch Processing Workflow

For batch mode (multiple prospects), the skill:

1. **Loads prospect list** from CRM/CSV
2. **Deduplicates** (removes already-analyzed prospects, opted-out addresses)
3. **Processes in sequence** (not parallel, to manage rate limits):
   - Stages 0-5 per prospect
   - Paces scraping (max 500/day)
   - Paces email sends (max 200/hour)
4. **Reports progress** (prospects completed, status breakdown, errors)
5. **Returns summary** (analytics on batch completion)

**Batch Processing Output:**
```json
{
  "batch_id": "BATCH-20260401-001",
  "mode": "batch",
  "status": "COMPLETE",
  "segment": "health",
  "prospects_submitted": 427,
  "prospects_processed": 425,
  "processing_results": {
    "successful": 410,
    "policy_absent": 12,
    "already_analyzed": 3,
    "errors": 0
  },
  "reports_generated": 410,
  "emails_scheduled": 410,
  "processing_time_hours": 6.5,
  "estimates": {
    "email_deliverability_rate": "98.4%",
    "teaser_conversion_estimate": "5.2%",
    "conversion_to_paid_estimate": "8.1%"
  }
}
```

---

## Error Handling & Rollback

**If any stage fails:**
1. Stop execution (no silent failures)
2. Log error with full context
3. Escalate per SOP (critical = immediate; normal = daily standup)
4. Offer rollback (clear all partial data; return to initial state)

**Example Error Scenarios:**
```
Stage 1 Error: Policy scraping failed (website down)
  ├─ Action: Retry 3x with exponential backoff
  ├─ If still fails: Mark POLICY_ABSENT; continue to Stage 2 or stop
  └─ Escalation: If > 10 failures in batch, notify ops

Stage 2 Error: LLM API rate limit exceeded
  ├─ Action: Queue for retry; backoff 1 hour
  ├─ If persists: Degrade to rule-based only (Mode A)
  └─ Escalation: Notify ML eng team

Stage 4 Error: Email validation fails (Spam Act check)
  ├─ Action: Return to analyst for fix
  ├─ Analyst corrects email; revalidates
  └─ Escalation: Log as compliance issue; review SOP
```

---

## Integration Points

### Artemis Integration
- **Purpose:** Prospect discovery, enrichment, CRM synchronization
- **Data Exchanged:** Company name, ABN, employee count, contact info
- **API Endpoint:** `artemis.api/v1/prospects/enrich`

### Vercel Integration
- **Purpose:** Report hosting, portal, email template rendering
- **Data Exchanged:** Report PDFs, portal HTML
- **Deployment:** PolicyCheck reports deployed to Vercel infrastructure

### SendGrid Integration
- **Purpose:** Email delivery, bounce tracking, complaint logging
- **Data Exchanged:** Email drafts, delivery status, bounce/complaint data
- **API Endpoint:** `sendgrid.api/v3/mail/send`

### CRM Integration
- **Purpose:** Prospect record management, deal tracking, outreach history
- **Data Exchanged:** Prospect records, email logs, conversion data
- **API Endpoint:** `crm.pythia.internal/api/v1/prospects`

### GPT-4 Integration (OpenAI)
- **Purpose:** LLM analysis (Mode B)
- **Data Exchanged:** Policy text (no PII)
- **Model:** gpt-4-turbo-preview
- **API Endpoint:** `api.openai.com/v1/chat/completions`

---

## KPIs & Monitoring

The skill is monitored via daily dashboards:

| KPI | Target | Measurement |
|-----|--------|-------------|
| **End-to-End Processing Time** | <60 min (single) | Stage 0 start → Stage 5 completion |
| **Success Rate** | >95% | Successful workflows / total invocations |
| **Policy Scrape Success** | >85% | Policies found / prospects targeted |
| **Analysis Confidence** | >80% avg | LLM confidence score across all reports |
| **Email Deliverability** | >95% | Emails delivered / emails sent |
| **Report Accuracy** | >98% (audits) | Audits passing QA / total audits |

---

## Configuration & Versioning

### Environment Variables
```bash
ARTEMIS_API_KEY=...
OPENAI_API_KEY=...
SENDGRID_API_KEY=...
POLICYCHECK_MODE=production  # or staging, test
RATE_LIMIT_SCRAPE_PER_DAY=500
RATE_LIMIT_EMAIL_PER_HOUR=200
ANALYST_REVIEW_REQUIRED_CONFIDENCE_THRESHOLD=0.80
```

### Version History
```
v1.0 (2026-04-01): Initial release
  ├─ 5-stage workflow
  ├─ Single & batch modes
  ├─ Rule-based + LLM analysis
  ├─ 3-tier report delivery
  └─ Full Spam Act compliance

[Future versions will be tracked here]
```

---

## Support & Escalation

**Support Contact:** support@policycheck.au
**Owner:** Sable (Head of Research) - sable@pythia.com
**Product Lead:** Rob - rob@pythia.com
**Escalation Path:** See SOP-PC-001 through SOP-PC-005

---

**Document Version:** 1.0
**Next Review:** 2026-10-01
**Approved By:** [Rob/Product Lead] | [Sable/Head of Research]
