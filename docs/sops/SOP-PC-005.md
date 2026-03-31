# SOP-PC-005: Quality Assurance

**Owner:** Head of Research (Sable)
**Last Updated:** 2026-04-01
**Status:** Active
**Audience:** QA Team, Compliance Analysts, Outreach Team, Rob (Product Lead)

---

## Purpose

This SOP defines quality assurance processes across the entire PolicyCheck AU workflow, including pre-send email checks, report accuracy verification, complaint handling, compliance self-audits, and feedback loops for continuous improvement.

---

## 1. Email Quality Assurance (Pre-Send)

### 1.1 Three-Layer Email QA Process

Every PolicyCheck AU email goes through three sequential QA gates before sending:

#### **Layer 1: Automated System Checks (Pass/Fail)**

System automatically validates every email before it enters the queue:

| Check | Pass Criteria | Failure Action |
|-------|---|---|
| **Recipient Email Format** | Valid email syntax (RFC 5322) | Quarantine; manual review |
| **Subject Line Present** | Subject not blank, <100 characters | Quarantine; require subject |
| **Footer Complete** | Contains ABN, address, unsubscribe link | Quarantine; add footer |
| **No Spam Keywords** | Does not match spam trigger list | Flag; manual review |
| **From/Reply-To Set** | Valid SMTP headers | Quarantine; fix headers |
| **Links Functional** | All URLs return HTTP 200-399 | Flag unsubscribe link specifically; fail if broken |
| **Personalization Complete** | No mail-merge tokens unfilled (e.g., {{name}} still in text) | Quarantine; populate variables |
| **Recipient Not Opted Out** | Email not in do-not-contact list | Quarantine; skip contact |
| **No Duplicate Send** | Recipient hasn't received this email in past 14 days | Quarantine; check CRM history |
| **File Size** | Email body <100KB | Flag; review for bloat |

**Gate Decision:**
- All checks pass → Proceed to Layer 2
- Any check fails → Quarantine; notify analyst; require manual fix before retry

#### **Layer 2: Manual Sample Review (Professional Judgment)**

For each campaign, QA analyst randomly reviews 5 emails from the batch:

**Checklist:**
- [ ] Personalization accurate (correct prospect name, company)
- [ ] Tone professional & appropriate (not aggressive, not generic)
- [ ] Sector-specific variant applied correctly
- [ ] CTA clear and actionable
- [ ] No typos or grammatical errors
- [ ] Brand voice consistent with Pythia
- [ ] Footer formatting clean (no rendering issues)
- [ ] Spam Act elements present (sender ID, address, unsubscribe)
- [ ] Subject line honest (no misleading language)
- [ ] No sensitive data exposed (no account numbers, API keys, etc.)

**Sample Size Rules:**
- Batch <500 emails: review 5 samples
- Batch 500-5,000 emails: review 10 samples
- Batch >5,000 emails: review 15 samples (split across different segments)

**Gate Decision:**
- All samples pass → Proceed to Layer 3
- Any sample fails → Hold entire batch; analyst fixes issue; restart sampling

#### **Layer 3: Compliance Officer Sign-Off**

Before delivery, Compliance Officer performs final gate:

**Final Checks:**
- [ ] No complaints in system for this sender domain (past 30 days)
- [ ] Bounce rate acceptable (<2% on similar segments)
- [ ] Campaign aligns with Spam Act requirements (recheck footer, unsubscribe, subject)
- [ ] Delivery schedule complies with rate limits (max 200/hour pacing)
- [ ] No other campaigns sent to same segment in past 7 days (cadence)
- [ ] Prospect list deduped (no duplicates within batch)

**Gate Decision:**
- All checks pass → APPROVED for delivery
- Any check fails → REJECTED; return to analyst with remediation steps

**Sign-Off Record:**
```json
{
  "campaign_id": "CAMP-20260401-001",
  "qa_layer_1": { "status": "PASS", "timestamp": "2026-04-01T08:00:00Z" },
  "qa_layer_2": { "status": "PASS", "reviewer": "Analyst Name", "timestamp": "2026-04-01T08:15:00Z" },
  "qa_layer_3": { "status": "APPROVED", "officer": "Compliance Officer", "timestamp": "2026-04-01T08:30:00Z" },
  "delivery_authorized_at": "2026-04-01T09:00:00Z"
}
```

---

## 2. Report Accuracy Verification (Sample Audits)

### 2.1 Audit Frequency & Scope

**Weekly Spot Audits:**
- **Frequency:** Every Friday
- **Sample Size:** 5% of reports generated that week (or minimum 3 reports)
- **Scope:** Mix of teaser, standard, and premium reports

**Monthly Deeper Audits:**
- **Frequency:** First Monday of month
- **Sample Size:** 10% of reports (or minimum 10 reports)
- **Scope:** Focus on sectors with lowest client satisfaction scores

### 2.2 Report Accuracy Audit Checklist

For each sampled report, QA auditor performs deep-dive verification:

#### **Policy Extraction Verification**
- [ ] Policy text used in report matches original policy (spot-check 3 excerpts)
- [ ] Policy date/version correct (if policy has version marker)
- [ ] Scraped date/URL correct (metadata matches source)
- [ ] No text corruptions (encoding errors, missing sections)

#### **Rule-Based Analysis Validation**
- [ ] APP scores defensible (if policy scores 0.9, does it actually mention all 13 APPs?)
- [ ] Each APP score justified (recommendation text supports score)
- [ ] Contradictions flagged (if policy says "no sharing" but also "shares with partners", is this caught?)
- [ ] Recommendations specific (not generic; tied to policy excerpts)

#### **LLM Analysis Validation**
- [ ] Gaps identified are real (auditor can verify in policy)
- [ ] Recommendations actionable (not vague)
- [ ] Tone appropriate (not judgmental, not alarmist)
- [ ] Confidence score matches output quality (high confidence = clear analysis; low confidence = ambiguous policy)

#### **Sector Context Validation**
- [ ] Industry classification correct (health, finance, etc.)
- [ ] Industry norms accurate (checked against sector database)
- [ ] Comparison percentiles reasonable (not obviously wrong)

#### **Formatting & Compliance**
- [ ] Report ID unique (no duplicates)
- [ ] Disclaimer language exact (no modifications)
- [ ] Analyst name & date present
- [ ] No sensitive data in filename or metadata
- [ ] PDF rendering correct (all text readable, no corruption)

### 2.3 Audit Resolution

**If audit finds issue:**

1. **Critical (Accuracy Impact):** Report pulled from client; analyst re-reviews; client notified of correction
2. **Major (Interpretation):** Report flagged in system; note added to client; offered v1.1 update
3. **Minor (Formatting):** Logged; analyst training; no client notification

**Resolution Tracking:**
```json
{
  "audit_id": "AUD-20260401-001",
  "report_id": "PC-20260401-00012-S",
  "issue": "APP 6 score 0.8 but policy silent on third-party sharing",
  "severity": "CRITICAL",
  "resolution": "Re-analysis; score downgraded to 0.5; client notified",
  "closed_date": "2026-04-02"
}
```

### 2.4 Audit Summary Reporting

**Weekly Audit Report:**
```
Week of: 2026-04-01
Reports generated: 47
Reports audited: 3 (5%)
Issues found: 1
  ├─ Critical: 0
  ├─ Major: 1
  └─ Minor: 0
Pass rate: 99%
Trend: ✓ Stable
Notes: [Specific issue & resolution]
Approved: Sable
```

---

## 3. Customer Complaint Handling

### 3.1 Complaint Categories & Response Protocols

| Complaint Type | Response Criteria | Timeline | Owner |
|---|---|---|---|
| **Report Accuracy** | Acknowledge; offer immediate re-review; provide corrected report v1.1 | 24 hours | Analyst + Sable |
| **Missing Analysis** | Acknowledge; re-run LLM analysis; escalate to expert if needed | 48 hours | Analyst |
| **Delivery Issue** | Resend report; verify recipient access; troubleshoot delivery | 4 hours | Ops team |
| **Tone/Judgment** | Acknowledge; re-frame findings; offer phone consultation | 24 hours | Sable + Sales |
| **Billing Dispute** | Verify order; honor refund if within 14 days; investigate if older | 72 hours | Finance |
| **Spam Complaint** | Acknowledge; apologize; immediately unsubscribe; document feedback | 2 hours | Compliance |

### 3.2 Complaint Intake & Logging

**All complaints logged in complaint tracking system:**

```
Complaint Record:
├─ Complaint ID: COMP-20260401-001
├─ Date/Time Received: 2026-04-01 14:30 UTC
├─ Complaint Channel: Email (support@policycheck.au)
├─ Complainant: [Name, email]
├─ Report ID: PC-20260401-00012-S
├─ Category: Report Accuracy
├─ Severity: High
├─ Description: "APP 11 score too high; policy doesn't mention encryption"
├─ Assigned To: [Analyst]
├─ Status: OPEN
├─ Assigned Date: 2026-04-01
├─ SLA Resolution: 2026-04-02 14:30 UTC
└─ Notes: Customer may have legal background; technical complaint
```

### 3.3 Complaint Resolution Workflow

```
Complaint Received
  ├─ Log in system
  ├─ Send acknowledgment email (within 2 hours)
  │  └─ Thank for feedback; commit to timeline
  │
  ├─ Investigate (by category)
  │  ├─ Report accuracy: Analyst re-reviews; verifies claim
  │  ├─ Missing analysis: Rerun analysis; compare to original
  │  ├─ Delivery: Check logs; resend if needed
  │  └─ Tone: Discuss with analyst; understand concern
  │
  ├─ Decide on resolution
  │  ├─ If valid: apologize; offer correction or refund
  │  ├─ If partial credit: explain; offer partial refund or free upgrade
  │  └─ If disputed: explain reasoning; offer phone call
  │
  ├─ Implement resolution
  │  ├─ Issue v1.1 of report if needed
  │  ├─ Process refund if warranted
  │  └─ Send detailed response email
  │
  └─ Close & Document
     ├─ Mark complaint CLOSED
     ├─ Log resolution in system
     ├─ Extract learning for process improvement
     └─ Share pattern in monthly QA report
```

### 3.4 Complaint Patterns & Root Cause Analysis

**Monthly, Sable analyzes complaint patterns:**

- Count by category (accuracy, tone, delivery, etc.)
- Identify if pattern points to systemic issue (e.g., LLM over-scoring in health sector)
- Root cause analysis (e.g., sector guidance outdated? Analyst bias? Scraper issue?)
- Action items (process update, analyst retraining, system fix)

**Example Pattern Analysis:**
```
Month: March 2026
Total complaints: 5
Accuracy complaints: 3 (60%)
  ├─ All health sector
  ├─ All about APP 11 (security) score
  ├─ Complaint: "We use encryption; policy doesn't say it clearly"
  └─ Root cause: LLM expecting explicit "encryption" keyword; patient language not recognized

Action Items:
1. Update APP 11 keyword list to include proxies ("secure", "protected")
2. Retrain LLM prompt to recognize intent-based language in health sector
3. Retrain analyst on health sector policy language patterns
```

---

## 4. Monthly Compliance Self-Audit

### 4.1 Monthly Audit Scope

**Every month, Sable leads comprehensive compliance audit covering:**

#### **Legal Compliance**
- [ ] All outreach emails contained required Spam Act elements (sample check: 20 emails)
- [ ] Unsubscribe requests honored within 5 business days (check backlog)
- [ ] No complaints to ACMA or spam authorities (search public registry)
- [ ] No legal notices received (check email/legal inbox)
- [ ] Privacy policy updated for any regulatory changes (check OAIC guidance)

#### **Analysis Quality**
- [ ] Analyst calibration stable (rule-based vs. LLM score alignment; audit 10 reports)
- [ ] Confidence thresholds met (reports meeting minimum confidence for tier)
- [ ] Peer review completion rate 100% (spot check CRM)
- [ ] LLM drift detected (GPT-4 output consistency; run 5 test policies twice)
- [ ] Sector-specific adjustments appropriate (check for over/under-application)

#### **Report Delivery**
- [ ] Report IDs unique (no duplicates; check database)
- [ ] Disclaimer language unmodified (exact match; 10-report sample)
- [ ] PDFs rendering correctly (check for corruption; test on 3 devices)
- [ ] Delivery links functional (test unsubscribe, portal access, PDF download)
- [ ] No sensitive data exposure (scan for emails, passwords, account numbers)

#### **Outreach Quality**
- [ ] Email bounce rate <2% (check SendGrid metrics)
- [ ] Spam complaint rate <0.3% (check SendGrid metrics)
- [ ] Unsubscribe requests processed <5 days (check CRM timestamps)
- [ ] No cadence violations (sample 20 prospects; verify ≤3/quarter)
- [ ] Pre-send QA pass rate >98% (check gate logs)

#### **Process Compliance**
- [ ] All SOPs current & followed (spot check 3 workflows)
- [ ] Escalation paths invoked appropriately (check logs for missed escalations)
- [ ] KPI targets met or exceeded (review dashboard)
- [ ] Training/certification current for all staff (check training records)
- [ ] Tools/systems security maintained (check access logs)

### 4.2 Monthly Audit Report Template

**Sable produces formal audit report by 5th of following month:**

```
POLICYCHECK AU MONTHLY COMPLIANCE AUDIT
Month: March 2026
Audit Date: 2026-04-01
Auditor: Sable (Head of Research)

EXECUTIVE SUMMARY
Overall Compliance: PASS / CONDITIONAL PASS / FAIL
Critical Issues: [Count]
Action Items: [Count]

LEGAL COMPLIANCE
Spam Act Compliance: PASS
  ├─ Sample checked: 20 emails
  ├─ Issues found: 0
  └─ Status: All emails met requirements

Privacy Act Compliance: PASS
  ├─ OAIC guidance reviewed: Yes
  ├─ Updates needed: None
  └─ Status: Current

Complaint Volume: 5 complaints
  ├─ Spam-related: 0
  ├─ Accuracy-related: 3
  ├─ Delivery-related: 2
  └─ Resolution rate: 100% within SLA

ANALYSIS QUALITY
Report Accuracy: PASS
  ├─ Audit sample: 5 reports
  ├─ Issues found: 1 (minor formatting)
  ├─ Client impact: None
  └─ Resolution: Logged for training

Analyst Calibration: PASS
  ├─ Score alignment: 94% (target: >90%)
  ├─ Confidence score drift: Minimal
  └─ Peer review completion: 100%

Quality Metrics:
  ├─ Pass rate (automated QA): 99%
  ├─ Pass rate (manual QA): 100%
  └─ Client satisfaction: 4.3/5.0 (target: >4.0)

OUTREACH QUALITY
Email Metrics:
  ├─ Bounce rate: 1.2% (target: <2%)
  ├─ Spam complaint rate: 0.1% (target: <0.3%)
  ├─ Unsubscribe rate: 0.8% (target: <1%)
  └─ Open rate (teaser): 18% (benchmark: 15%)

Cadence Compliance: PASS
  ├─ Violations detected: 0
  ├─ Sample checked: 20 prospects
  └─ Status: All within limits

PROCESS COMPLIANCE
SOP Adherence:
  ├─ SOP-PC-001 (Scraping): Followed 100%
  ├─ SOP-PC-002 (Analysis): Followed 95% (minor analyst deviation)
  ├─ SOP-PC-003 (Reports): Followed 100%
  ├─ SOP-PC-004 (Outreach): Followed 100%
  └─ SOP-PC-005 (QA): Followed 100%

Escalation Path:
  ├─ Total escalations: 2
  ├─ Appropriate: 2 (100%)
  ├─ Missed escalations: 0
  └─ Resolution time: 1.5 days average

KPI Performance:
  ├─ Scrape success: 87% (target: >85%) ✓
  ├─ Analysis confidence: 84% avg (target: >80%) ✓
  ├─ Report QA pass rate: 99% (target: >98%) ✓
  ├─ Outreach deliverability: 98.8% (target: >95%) ✓
  └─ Customer satisfaction: 4.3/5.0 (target: >4.0) ✓

FINDINGS & RECOMMENDATIONS

Critical Issues: None

Major Issues:
1. APP 11 complaints in health sector (see complaint pattern analysis)
   - Action: Update keyword list + retrain analyst (Due: 2026-04-15)

Minor Issues:
1. One PDF rendering issue on Safari (not critical)
   - Action: Test on wider browser set (Due: 2026-04-10)

Observations:
- Analyst X has higher complaint rate than peer (3 vs. 0.5 average)
- Recommend 1:1 review of recent reports
- Teaser-to-Standard conversion rate trending up (5% → 7%)

RECOMMENDATIONS

For Next Month:
1. Implement health sector APP 11 keyword updates
2. Conduct 1:1 calibration session with analyst X
3. Expand browser compatibility testing
4. Monitor conversion rate trend; may indicate improved messaging

APPROVAL

Audit completed by: Sable, Head of Research
Reviewed by: [Rob/Product Lead]
Date: 2026-04-01
Status: APPROVED
Next audit: 2026-05-01
```

---

## 5. Feedback Loop & Continuous Improvement

### 5.1 Feedback Sources

PolicyCheck AU collects feedback from multiple sources to improve analysis quality:

| Source | Cadence | Input | Owner |
|--------|---------|-------|-------|
| **Customer Surveys** | Post-delivery (7 days) | Report clarity, accuracy, value | Marketing |
| **Complaint Analysis** | Monthly | Patterns in complaints; root causes | Sable |
| **Analyst Feedback** | Weekly standups | Tool limitations, workflow friction | Sable |
| **LLM Performance Audit** | Monthly | Confidence score drift, accuracy changes | Analyst + ML |
| **Sector Experts** | Quarterly | Industry guidance changes, norms updates | Sable |
| **Legal/Compliance** | As-needed | Regulatory changes; legal precedent shifts | Legal |
| **Sales/Customer Success** | Weekly | Customer success stories, unmet needs | Rob |

### 5.2 Feedback Integration Process

```
Feedback Collected
  │
  ├─ Review & Categorize
  │  ├─ Process improvement (SOP change)
  │  ├─ Training need (analyst retraining)
  │  ├─ System change (tool/LLM tuning)
  │  └─ Data update (sector guidance, APP definitions)
  │
  ├─ Prioritize
  │  ├─ Critical (regulatory, safety): Immediate
  │  ├─ High (affects accuracy/compliance): Within 2 weeks
  │  ├─ Medium (process improvement): Within 1 month
  │  └─ Low (nice-to-have): Quarterly review
  │
  ├─ Implement
  │  ├─ Document change (update relevant SOP)
  │  ├─ Test (validate change doesn't break existing processes)
  │  ├─ Roll out (communicate to team)
  │  └─ Train (ensure team understands change)
  │
  └─ Measure Impact
     ├─ Track KPI effect (improved accuracy? Faster turnaround?)
     ├─ Document learning (log in feedback ledger)
     └─ Adjust if needed (pivot if change doesn't achieve goal)
```

### 5.3 Continuous Improvement Examples

**Example 1: LLM Confidence Drift**
```
Feedback: LLM confidence scores trending lower in March (-3% vs. Feb)
Root Cause: OpenAI updated GPT-4 behavior (or system temperature changed)
Action: Ran 10 test policies through both old/new model; found 15% score variance
Implementation: Recalibrated confidence thresholds (>85% still high confidence; 75-85% medium)
Measurement: Confidence scores now stable; no change to report quality
Status: CLOSED
```

**Example 2: Health Sector APP 11 Complaints**
```
Feedback: 3 complaints about APP 11 scoring in health sector
Root Cause: Policy says "secure" not "encrypt"; LLM not recognizing synonym
Action: Added "secure", "protected", "safeguard" to APP 11 keyword list
Implementation: Updated system; retrained analyst on health language patterns
Measurement: Zero APP 11 complaints in April; customer satisfaction +0.5 points
Status: CLOSED
```

**Example 3: Report Clarity**
```
Feedback: Customers asking "What do I do with this report?" (survey feedback)
Root Cause: Recommendations present but not prioritized; no action plan
Action: Added "Priority Fix" section; ranked by severity + ease
Implementation: Updated report template; analyst training on prioritization
Measurement: Follow-up satisfaction improved 4.1 → 4.4 / 5.0
Status: CLOSED
```

---

## 6. Quality KPIs & Dashboards

### 6.1 Quality Scorecard

**Real-time dashboard (updated daily) tracking all QA KPIs:**

```
POLICYCHECK AU QUALITY SCORECARD
Updated: 2026-04-01 17:00 UTC

═══════════════════════════════════════════════════════════════════

OUTREACH QUALITY
  Email Deliverability:           98.8% (Target: >95%) ✓
  Bounce Rate:                    1.2% (Target: <2%) ✓
  Spam Complaint Rate:            0.1% (Target: <0.3%) ✓
  Unsubscribe Rate:               0.8% (Target: <1%) ✓

ANALYSIS QUALITY
  Rule-Based Confidence:          87% (Target: >80%) ✓
  LLM Confidence (avg):           83% (Target: >80%) ✓
  Peer Review Pass Rate:          100% (Target: >95%) ✓
  Analyst Agreement Rate:         94% (Target: >90%) ✓

REPORT QUALITY
  Pre-Send QA Pass Rate:          99% (Target: >98%) ✓
  Report Accuracy (audits):       99% (Target: >98%) ✓
  Disclaimer Compliance:          100% (Target: 100%) ✓
  Delivery Success Rate:          99.7% (Target: >99%) ✓

CUSTOMER SATISFACTION
  Post-Delivery NPS:              +42 (Target: >35) ✓
  Support Resolution Time:        18 hours (Target: <24h) ✓
  Complaint Rate:                 0.8% (Target: <1%) ✓
  Satisfaction Score:             4.3/5.0 (Target: >4.0) ✓

PROCESS COMPLIANCE
  SOP Adherence:                  99% (Target: >95%) ✓
  Escalation Path Success:        100% (Target: 100%) ✓
  Training Current:               100% (Target: 100%) ✓

═══════════════════════════════════════════════════════════════════

TREND: Stable across all metrics. No critical issues.
Last Updated: 2026-04-01 17:00 UTC
Next Update: 2026-04-02 17:00 UTC
```

### 6.2 Analyst Calibration Dashboard

**Tracks individual analyst performance:**

```
ANALYST PERFORMANCE SCORECARD

Analyst: John Smith
Month: March 2026

Coverage:
  Reports analyzed: 42
  Share of total: 28%

Quality Metrics:
  Avg confidence score: 82% (team avg: 83%) -1
  Complaint rate: 2.4% (team avg: 0.8%) ⚠️
  Peer review pass rate: 95% (team avg: 100%) ⚠️
  Client satisfaction: 4.0/5.0 (team avg: 4.3) ⚠️

Issues:
  ├─ Health sector complaints: 3/3 total (APP 11 scoring)
  ├─ Generic recommendations flagged: 2
  └─ Missed escalation: 1

Trend:
  Complaint rate trending UP (Feb: 1.2% → Mar: 2.4%)
  Confidence score stable

Action:
  1:1 calibration session scheduled 2026-04-05
  Focus: Health sector APP 11 analysis; recommendation specificity
```

---

## 7. Escalation Matrix

| Issue | Severity | Owner | Timeline | Approval |
|-------|----------|-------|----------|----------|
| **Report accuracy issue** | Critical | Sable | 4 hours | Rob |
| **Spam complaint** | Critical | Compliance | 2 hours | Sable |
| **Legal notice/cease-and-desist** | Critical | Legal | Immediate | Legal Counsel |
| **Analyst calibration drift** | Major | Sable | 5 days | Sable |
| **Process violation** | Major | Sable | Same day | Sable |
| **LLM performance degradation** | Major | ML Eng | 2 days | Sable |
| **Customer complaint** | Medium | Support Lead | 24 hours | Sable |
| **Feedback for improvement** | Low | Sable | Quarterly review | Rob |

---

## 8. Documentation & Audit Trail

### 8.1 QA Records Retention

All QA records archived with full audit trail:

```
/data/qa-records/
├─ email-qa/[CAMPAIGN_ID]/
│  ├─ layer1-automated.json
│  ├─ layer2-manual-review.json
│  ├─ layer3-compliance-approval.json
│  └─ delivery-log.json
│
├─ report-qa/[REPORT_ID]/
│  ├─ analysis-validation.json
│  ├─ accuracy-audit.json
│  └─ delivery-confirmation.json
│
├─ complaints/[COMPLAINT_ID]/
│  ├─ intake-record.json
│  ├─ investigation.json
│  ├─ resolution.json
│  └─ resolution-communication.json
│
└─ monthly-audits/
   └─ [YYYYMM]
      ├─ audit-report.pdf
      ├─ findings.json
      ├─ remediation-actions.json
      └─ approval-sign-off.json
```

**Retention:** 5 years (statute of limitations on complaints + regulatory audit needs)

---

**Document Version:** 1.0
**Next Review:** 2026-10-01
**Approved By:** [Rob/Product Lead] | [Sable/Head of Research]
