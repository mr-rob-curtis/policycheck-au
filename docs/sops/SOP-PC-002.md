# SOP-PC-002: Compliance Analysis

**Owner:** Head of Research (Sable)
**Last Updated:** 2026-04-01
**Status:** Active
**Audience:** Compliance Analysis Team, QA, Rob (Product Lead)

---

## Purpose

This SOP defines the analytical process for assessing Australian Privacy Act compliance. It establishes quality thresholds, mode selection (rule-based vs. LLM), sector-specific adjustments, human review triggers, and version control for evolving legal requirements.

---

## 1. Analysis Overview

### 1.1 Two-Mode Architecture

PolicyCheck AU operates in two complementary modes:

**Mode A: Rule-Based Analysis (Deterministic)**
- Checks policy against explicit APP requirements
- Output: Yes/No/Unclear for each APP principle
- Confidence: 95%+ (predictable, auditable)
- Time: <10 seconds per policy
- Best for: Simple, clearly structured policies

**Mode B: LLM Analysis (Interpretive)**
- GPT-4-based semantic understanding
- Output: Risk assessment, gaps, recommendations
- Confidence: 70-85% (requires human review)
- Time: 20-60 seconds per policy
- Best for: Complex, nuanced policy language

### 1.2 Analysis Workflow

```
Policy Input → Rule-Based Scan → LLM Synthesis → Confidence Assessment → Quality Gate
                    │                  │                    │                   │
                    └─→ Pass all rules  ├─→ High confidence (>85%) ─→ Auto-approve
                    │                  │
                    └─→ Gaps detected   └─→ Medium confidence (70-84%) ─→ Analyst review
                                       │
                                       └─→ Low confidence (<70%) ─→ Human analysis

```

---

## 2. Rule-Based Analysis (Mode A)

### 2.1 Australian Privacy Act Structure

The APP is enforced through 13 Australian Privacy Principles:

| APP | Requirement | PolicyCheck Check |
|-----|-------------|-------------------|
| **APP 1** | Management of personal information | Policy discloses governance/accountability |
| **APP 2** | Anonymity & pseudonymity | Option to avoid ID? Stated & honored? |
| **APP 3** | Collection of solicited information | Stated collection practices clear? |
| **APP 4** | Dealing with unsolicited information | Protocol for unrequested data? |
| **APP 5** | Notification about personal information | Notified at/before collection? How? |
| **APP 6** | Use or disclosure | Uses stated? Limitations clear? |
| **APP 7** | Direct marketing | Unsubscribe mechanism present? |
| **APP 8** | Credit reporting | (If applicable) Credit data handling disclosed? |
| **APP 9** | Government related ID | (If applicable) Tax file number handling stated? |
| **APP 10** | Quality of personal information | Update mechanism or statement re: accuracy? |
| **APP 11** | Security of personal information | Encryption/security measures disclosed? |
| **APP 12** | Access and correction | Right to request, view, update personal data? |
| **APP 13** | Complaints handling | Complaint mechanism & timeline stated? |

### 2.2 Rule-Based Check Implementation

**For Each APP Principle:**

1. **Keyword Search** (initial gate)
   - Scan policy for explicit mentions (e.g., APP 6: "disclosure", "share", "third parties")
   - If found: score 1 (present); if not: score 0 (absent)

2. **Semantic Pattern Matching**
   - Check for reasonable proxies (e.g., "we will not sell data" = APP 6 compliance indication)
   - Score: +0.5 if proxy language detected

3. **Specificity Assessment**
   - Generic statement ("We care about privacy") ≠ specific APP compliance claim
   - Specific statement ("We encrypt data in transit using TLS 1.3") = compliance signal
   - Adjust score based on specificity (0 = generic only; 1 = specific details provided)

4. **Contradiction Detection**
   - Flag if policy claims "no data sharing" but also "shares with marketing partners"
   - Score: -1 (fails APP 6 unless justified)

**Output per APP:**
```json
{
  "app_principle": 6,
  "title": "Use or Disclosure",
  "policy_score": 0.8,
  "rule_matches": [
    "Policy explicitly discloses sharing with third parties",
    "Limitation: 'Only for direct purpose or related purposes'",
    "No mention of security of disclosed data"
  ],
  "gaps": [
    "Does not specify retention period before deletion"
  ],
  "recommendation": "Add data retention policy to strengthen APP 6 compliance"
}
```

### 2.3 Aggregation to Overall Score

**Rule-Based Compliance Score = (Sum of APP scores) / 13**

| Score | Assessment | Interpretation |
|-------|-----------|-----------------|
| **0.9-1.0** | Excellent | Policy explicitly addresses all 13 APPs |
| **0.7-0.89** | Good | Most APPs clear; minor gaps |
| **0.5-0.69** | Fair | Several gaps; at-risk for complaints |
| **0.3-0.49** | Poor | Major gaps; significant compliance exposure |
| **<0.3** | Very Poor | Policy inadequate; legal liability risk |

---

## 3. LLM Analysis (Mode B)

### 3.1 Prompt Architecture

**System Prompt (Fixed):**
```
You are a compliance analyst for Australian Privacy Act (APP) assessment.
You assess privacy policies against the 13 Australian Privacy Principles.
Your output is a JSON structured analysis with:
- Gap identification (specific risks)
- Recommendations (specific fixes)
- Confidence score (70-100)
- Risk severity (CRITICAL, HIGH, MEDIUM, LOW)

Do NOT make legal conclusions ("this violates the law").
DO identify "this policy does not clearly disclose X, which APP Y requires".

Respond ONLY in valid JSON format.
```

**User Prompt (Policy-Specific):**
```
Analyze this privacy policy for APP compliance.

[POLICY TEXT]

For each of these gaps identified by rule-based analysis, explain:
1. Why it's a gap
2. Likelihood of regulatory concern (% chance OAIC investigation)
3. Specific recommended fix

Identified gaps:
{rule_based_gaps}

Output JSON with structure:
{
  "gap_analysis": [
    {
      "app_principle": 6,
      "gap_description": "Policy does not specify retention period",
      "risk_severity": "MEDIUM",
      "regulatory_concern_pct": 45,
      "recommended_fix": "Add: 'We retain customer data for X years, then delete'",
      "fix_complexity": "TRIVIAL"
    }
  ],
  "overall_risk_assessment": "MEDIUM",
  "confidence_score": 82,
  "key_strengths": ["..."],
  "critical_weaknesses": ["..."]
}
```

### 3.2 LLM-Specific Confidence Thresholds

**High Confidence (85-100):**
- Policy is well-structured, explicit, detailed
- All major APPs clearly addressed
- LLM assessment aligns with rule-based score
- Clear recommendation pathway

**Medium Confidence (70-84):**
- Policy ambiguous on some APPs
- LLM detects nuance beyond rule-based (e.g., implicit vs. explicit)
- Recommendation requires interpretation
- Analyst review recommended

**Low Confidence (<70):**
- Policy highly ambiguous, contradictory, or poorly written
- LLM unable to assess specific APP(s) due to unclear policy
- Requires domain expert (lawyer) review
- Flag for manual analysis before delivery to client

### 3.3 Integration: Rule-Based + LLM

**When Mode A (Rule-Based) completes:**
- If score ≥ 0.85 AND all gaps minor: **Confidence PASS** → proceed to report generation
- If score 0.65-0.84 OR gaps found: **Confidence MEDIUM** → run Mode B
- If score < 0.65 OR critical gaps: **Confidence LOW** → escalate for human review

**When Mode B (LLM) completes:**
- If LLM confidence ≥ 85%: **Approve** → report generation
- If LLM confidence 70-84%: **Analyst Review Required** (below)
- If LLM confidence < 70%: **Escalate to Expert** (legal review)

---

## 4. Quality Thresholds for Analysis Output

### 4.1 Minimum Confidence Scores by Delivery Tier

| Pricing Tier | Min LLM Confidence | Min APP Coverage | Action if Not Met |
|--------------|-------------------|------------------|-------------------|
| **Teaser** (free) | 70% | 8/13 APPs | Rerun LLM; if still fails, do not deliver |
| **Standard** (paid) | 80% | 11/13 APPs | Analyst review; may reword but do not deliver without review |
| **Premium** (paid) | 85% | All 13 APPs | Expert review required; may require policy amendment suggestions |

### 4.2 Output Quality Checklist

**Before releasing analysis to client, verify:**

- [ ] Rule-based score ≤ LLM score (LLM should not inflate score)
- [ ] All flagged gaps are explained with specific policy references
- [ ] Recommendations are actionable (not vague: "improve your privacy" is vague)
- [ ] Risk severity assessments are internally consistent (gaps don't increase severity arbitrarily)
- [ ] No legal conclusions ("You are in violation"); only factual gaps
- [ ] Analyst name and review date present on report
- [ ] Disclaimer language included (see SOP-PC-003)

---

## 5. Sector-Specific Analysis Adjustments

### 5.1 Sector Override Rules

Certain sectors have different regulatory expectations. Adjust analysis accordingly:

#### **Health Sector (Highest Standard)**
- **Additional Requirements:** National Privacy Code for health (not statutory but expected)
- **APP 11 Sensitivity:** Medical data = heightened security expectations
- **Adjustment:** If APP 11 score <0.8, risk severity auto-escalates to HIGH
- **APP 8 Check:** Health credit reporting (if applicable) must be explicit

#### **Financial Services (High Standard)**
- **Additional Requirements:** Australian Securities and Investments Commission (ASIC) expectations
- **APP 6 Sensitivity:** Customer data sharing with affiliates = common; must be explicit
- **Adjustment:** If APP 6 vague, automatically flag as MEDIUM risk (not LOW)
- **APP 8:** Credit reporting practices must be detailed (common for banks/lenders)

#### **Retail/E-Commerce (Medium Standard)**
- **Additional Requirement:** Australian Consumer Law (marketing practices)
- **APP 7 Sensitivity:** Direct marketing opt-out must be easy/free
- **Adjustment:** If APP 7 missing, automatic MEDIUM risk; if opt-out is paid/hard, HIGH risk

#### **SaaS/Software (Medium Standard)**
- **Additional Requirement:** Cloud data residency (Australian/non-Australian disclosure)
- **APP 11 Sensitivity:** Data encryption in transit and at rest = expected standard
- **Adjustment:** If policy silent on encryption, automatic LOW risk (may be acceptable for non-personal-data)

#### **Education (Medium-High Standard)**
- **Additional Requirement:** Duty of care to minors
- **APP 3 Sensitivity:** Collection from minors must disclose to parent/guardian
- **Adjustment:** If accepts student data but no disclosure of minor data handling, MEDIUM+ risk

#### **Real Estate (Low-Medium Standard)**
- **Additional Requirement:** Anti-money laundering (AML) data requirements
- **APP 6:** May share with government agencies (AML); must disclose
- **Adjustment:** If policy doesn't mention AML compliance, add note but don't penalize

### 5.2 Sector Lookup & Application

**In LLM analysis, inject sector context:**
```
Industry classification: {sector}
Regulatory guidance: {sector_guidance}
APP sensitivity overrides: {sector_specific_checks}

Reassess any ambiguous APPs with these sector norms in mind.
```

**Sector Database (version controlled; see Section 5.4):**
- Maintained in `/data/sector-guidance/sector-guidance.json`
- Updated quarterly or on regulatory change
- Includes: sector name, ANZSIC code, key regulators, APP sensitivity map

---

## 6. Human Review Triggers

### 6.1 Automatic Escalation Criteria

**Analysis is escalated to analyst for manual review if ANY of:**

1. **Confidence Score Low:** LLM confidence < 70%
2. **Rule-Based Low:** Rule-based APP coverage < 8/13 APPs
3. **Critical Gaps:** LLM identifies CRITICAL risk (e.g., no security disclosure, no consent mechanism)
4. **Contradiction Detected:** Policy contradicts itself on key APP(s)
5. **Ambiguous Language:** >3 APPs use hedging language ("may", "in some cases") without clarity
6. **Sector-Specific Failure:** Sector-specific check flags CRITICAL or HIGH (see 5.1)
7. **Regulatory News:** Within 48h of regulatory guidance change, all policies in affected APP area re-reviewed
8. **Client Tier Premium:** All Premium tier reports manually reviewed regardless of confidence

### 6.2 Analyst Review Workflow

**Analyst action upon escalation:**

1. **Re-Read Original Policy** (full, not just extracted text)
2. **Validate LLM Assessment:** Does LLM output match policy content?
3. **Assess Benefit-of-Doubt:** Is policy *trying* to be compliant but unclear? (May recommend rewording vs. rejecting)
4. **Check Sector Context:** Is this policy normal for its sector?
5. **Decision:**
   - **Approve:** Generate report with analyst notes
   - **Request Rewording:** Suggest specific policy amendments; hold pending client decision
   - **Reject:** Policy inadequate; recommend full privacy overhaul

**Analyst Sign-Off:**
```json
{
  "analyst_name": "Name",
  "analyst_email": "name@pythia.com.au",
  "review_date": "2026-04-01",
  "decision": "APPROVE | REQUEST_REWORDING | REJECT",
  "notes": "Specific concerns or recommendations",
  "confidence_adjustment": 0  // -10 to +10 adjustment to LLM score
}
```

---

## 7. Version Control for APP Requirements

### 7.1 APP Definition Evolution

Australian Privacy Act requirements may change due to:
- Federal legislation amendments (e.g., *Privacy Legislation Amendment (Enforcement and Other Measures) Bill 2022*)
- OAIC Regulatory guidance updates
- Court precedent shifts
- Industry guidance (e.g., updated health privacy code)

### 7.2 Version Control System

**File:** `/data/app-definitions/app-requirements-v[VERSION].json`

**Content:**
```json
{
  "version": "1.0",
  "effective_date": "2026-04-01",
  "source": "Australian Privacy Act 1988 as amended; OAIC Guidance 2026",
  "apps": {
    "1": {
      "title": "Management of Personal Information",
      "key_elements": [
        "Personal information handling policy exists",
        "Privacy contact details disclosed",
        "Accountability mechanism stated"
      ],
      "rule_based_keywords": ["privacy", "management", "governance"],
      "minimum_policy_coverage": 0.7,
      "sector_overrides": {}
    },
    // ... 2-13
  }
}
```

### 7.3 Update Protocol

**When APP requirements change:**

1. **Notification:** Legal/Sable receives notification of regulatory change
2. **Assessment:** Impact on existing policies? (Most changes = re-assessment of subset)
3. **Version Bump:** Create new `/app-requirements-v[N+1].json`
4. **Re-Analysis Flag:** Mark all existing analyses as "requires re-assessment under v[N+1]"
5. **Client Notification:** If change impacts delivered reports, notify clients of updated assessment
6. **Cutover:** New analyses use new version; old analyses tagged with legacy version

**Example Change Log:**
```
v1.0 (2026-04-01): Initial release
v1.1 (2026-06-15): APP 11 security updated; now requires "encryption" explicit mention
v2.0 (2026-09-01): Major legislative amendment; all APPs re-assessed
```

---

## 8. Quality Assurance for Analysis Output

### 8.1 Peer Review

**Before delivery, analysis peer-reviewed by another analyst:**
- [ ] Rule-based score is defensible (policy actually covers stated APPs)
- [ ] LLM gaps are specific, not generic
- [ ] Recommendations are actionable and proportionate
- [ ] Disclaimer language present and accurate
- [ ] No legal opinions (only factual gaps)
- [ ] Tone is professional and non-judgmental

### 8.2 Spot Audits (Weekly)

**Randomly select 5% of completed analyses:**
- [ ] Re-run Mode B (LLM) independently; compare output
- [ ] Calculate agreement rate (should be >90%)
- [ ] If disagreement: discuss with analyst; adjust if needed
- [ ] Track analyst calibration (some over-rate, under-rate)

### 8.3 Feedback Loop

**Incorporate into analysis refinement:**
- Calibration drift: If analyst tends to over/under-score, adjust expectations
- LLM drift: If GPT-4 behavior changes (new version), re-validate confidence thresholds
- Sector adjustments: If sector-specific checks prove inaccurate, update per 5.2

---

## 9. Key Performance Indicators

| KPI | Target | Measurement |
|-----|--------|-------------|
| **Analysis Confidence (>80%)** | >85% of analyses | LLM score ≥80 without human review |
| **Analyst Agreement** | >90% | Peer review spot-check alignment |
| **Human Review Rate** | <15% of analyses | Escalations / total analyses |
| **Turnaround Time** | <10 min (automated) | Complete analysis cycle for Mode A/B |
| **Client Satisfaction** | >4.0/5.0 | Post-delivery survey (gap recommendations) |

---

## 10. Escalation Path

| Issue | Escalation | Timeline |
|--------|-----------|----------|
| **LLM confidence anomaly (>5 in a row <70%)** | Sable (Head of Research) | Daily standup |
| **Analyst calibration drift** | Sable + analyst 1:1 | Weekly |
| **APP guidance change identified** | Rob (Product Lead) + Sable | Same day |
| **Regulatory complaint re: analysis accuracy** | Legal + Rob | Immediate |
| **Sector adjustment needed** | Sable + subject-matter expert | Within 5 days |

---

## 11. Appendices

### 11.1 Rule-Based Check Examples

**Example 1: APP 7 (Direct Marketing)**
```
Policy text: "We send marketing emails to customers who have opted in."

Rule checks:
1. Keyword: "marketing", "email", "opted in" → PRESENT
2. Semantic: Explicit opt-in mentioned → Score +1.0
3. Specificity: Clear opt-in mechanism → +0.0
4. Contradiction: None → +0.0

APP 7 Score = 1.0 (Excellent)
```

**Example 2: APP 11 (Security)**
```
Policy text: "We are committed to protecting your data."

Rule checks:
1. Keyword: "security", "encrypt", "protect" → PRESENT (but generic)
2. Semantic: No specific security measures → Score +0.3
3. Specificity: Only generic statement → -0.5
4. Contradiction: None → +0.0

APP 11 Score = 0.3 (Poor - needs specifics)
```

### 11.2 Sector Sensitivity Map

```json
{
  "Health": {
    "critical_apps": [11, 8],
    "override_rules": "If APP 11 score < 0.8, escalate to HIGH risk"
  },
  "Finance": {
    "critical_apps": [6, 8],
    "override_rules": "If APP 6/8 vague, escalate to MEDIUM risk"
  },
  "Retail": {
    "critical_apps": [7],
    "override_rules": "If APP 7 missing, escalate to MEDIUM risk"
  },
  "SaaS": {
    "critical_apps": [11],
    "override_rules": "If APP 11 silent on encryption, acceptable for non-PII"
  }
}
```

---

**Document Version:** 1.0
**Next Review:** 2026-10-01
**Approved By:** [Rob/Product Lead] | [Sable/Head of Research]
