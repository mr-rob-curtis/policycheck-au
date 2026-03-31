# PolicyCheck AU - Operational Documentation & Skill Architecture

**Prepared by:** Sable, Head of Research at Pythia
**Date:** 2026-04-01
**Status:** Ready for Implementation
**Product Owner:** Rob (Product Lead)

---

## Overview

This documentation package provides complete operational guidelines and skill architecture for PolicyCheck AU, an automated Australian Privacy Act compliance tool built on Pythia infrastructure. The package includes five Standard Operating Procedures (SOPs), a skill definition, and a comprehensive risk register.

---

## Document Index

### 1. Standard Operating Procedures (SOPs)

#### **SOP-PC-001: Prospect Identification & Scraping** (12 KB)
- Prospect discovery via Artemis + Australian Business Register
- Website scraping workflow with quality gates
- Data sources (ABR, Google Maps, ASIC, industry directories)
- Privacy & security considerations for scraped policies
- Rate limiting & ethical scraping guidelines
- Key metrics: Scrape success rate (>85%), data quality pass rate (>90%)

#### **SOP-PC-002: Compliance Analysis** (18 KB)
- Two-mode analysis architecture: Rule-based (Mode A) + LLM (Mode B)
- Australian Privacy Principles (13 APPs) assessment framework
- Rule-based checks for deterministic compliance scoring
- LLM analysis for gap identification & recommendations
- Confidence thresholds by delivery tier (teaser >70%, standard ≥80%, premium ≥85%)
- Sector-specific adjustments (health, finance, retail, SaaS)
- Human review triggers & analyst calibration
- Version control for APP requirement definitions
- Key metrics: Analyst agreement >90%, average confidence >80%

#### **SOP-PC-003: Report Generation & Delivery** (18 KB)
- Report structure & content standards
- Three-tier delivery: Teaser (free), Standard ($299), Premium ($799)
- Mandatory disclaimer language (non-negotiable)
- Sector-specific report customization
- Report quality checks (3-layer QA)
- Email delivery, portal hosting, PDF generation
- Report versioning & update protocol
- Key metrics: QA pass rate >98%, delivery success >99.5%

#### **SOP-PC-004: Outreach & Email Compliance** (19 KB)
- Australian Spam Act 2003 compliance requirements
- Mandatory email elements (sender ID, footer, unsubscribe)
- Email cadence limits (max 3/quarter per prospect)
- Sector-specific outreach messaging variants
- 3-email sequence workflow (initial, follow-up, final)
- Pre-send quality checklist (automated + manual)
- Response handling & escalation
- Weekly email audits & monthly compliance reports
- Key metrics: Deliverability >95%, spam complaint rate <0.3%

#### **SOP-PC-005: Quality Assurance** (23 KB)
- Three-layer email QA: Automated system checks → Manual review → Compliance approval
- Report accuracy verification via spot audits (5-10% monthly sample)
- Customer complaint handling & resolution workflow
- Monthly compliance self-audit (legal, analysis, delivery, process)
- Feedback loop for continuous improvement
- Analyst calibration dashboards
- Key metrics: Report accuracy >98%, customer satisfaction >4.0/5.0

### 2. Skill Definition

#### **policycheck-skill.md** (32 KB)
Complete orchestration skill for end-to-end PolicyCheck workflow:

**Five Sequential Stages:**
1. **Stage 0: Input Validation & Prospection** — Validate inputs; enrich via Artemis
2. **Stage 1: Policy Scraping & Extraction** — Discover, scrape, validate policies
3. **Stage 2: Compliance Analysis** — Rule-based + LLM analysis; sector adjustments
4. **Stage 3: Report Generation** — Create PDF report; apply tier template; QA validate
5. **Stage 4: Outreach Preparation** — Draft email; Spam Act checks; schedule delivery
6. **Stage 5: Completion & Logging** — Archive; audit trail; trigger follow-ups

**Operating Modes:**
- Single prospect: Analyze one company
- Batch: Process 50-500 prospects per batch; auto-deduplication; paced scraping/email

**Quality Gates at Each Stage:** Ensures confidence thresholds met, analyst review completed, compliance checks passed

**Integration Points:** Artemis (prospect enrichment), Vercel (hosting), SendGrid (email), OpenAI (LLM), CRM (record management)

### 3. Risk Register

#### **risk-register.md** (26 KB)
Comprehensive operational risk assessment with 11 identified risks:

**CRITICAL Risks (Likelihood × Impact ≥ 2.0 / 5.0):**
1. **R-001: Analysis Accuracy Liability** (2.0/5.0)
   - Risk: Inaccurate analysis could lead to client liability/OAIC action
   - Mitigations: Multi-layer QA, disclaimers, E&O insurance

2. **R-002: Privacy Breach of Scraped Data** (2.0/5.0)
   - Risk: Breach of stored policies; major reputational damage ("privacy tool fails to protect data")
   - Mitigations: AES-256 encryption, MFA, security audit, cyber insurance

3. **R-004: Spam Complaint Reputational Damage** (3.0/5.0)
   - Risk: Email compliance violations → domain blacklist → revenue loss
   - Mitigations: 3-layer email QA, Spam Act compliance, separate sending domain

**HIGH Risks (1.5-2.4 / 5.0):**
4. **R-003: Brand Dilution** (2.4/5.0) — PolicyCheck ≠ Research brand confusion
5. **R-005: Competitive Market Saturation** (2.4/5.0) — Incumbents entering AU market
6. **R-008: Data Center Downtime** (1.2/5.0) — Vercel outage impacts report access

**MEDIUM Risks (1.2 / 5.0):**
7. **R-006: Scraper Blocking** — Domains detect/block scraping bot
8. **R-007: LLM Model Degradation** — OpenAI behavior/pricing changes
9. **R-010: Scope Creep** — Privacy regulations expanding beyond 13 APPs

**LOW Risks (<0.8 / 5.0):**
10. **R-011: Key Personnel Departure** — Sable or Rob leaves

**Total Estimated Mitigation Cost (Y1):** ~$186K (18-37% of projected revenue)

---

## Quick Reference: Key Dependencies

### Artemis Integration
- Prospect discovery, enrichment, CRM sync
- API: `artemis.api/v1/prospects/enrich`

### Vercel Deployment
- Report hosting, portal, email templates
- Environment: Pythia infrastructure

### SendGrid Email
- Campaign delivery, bounce/complaint tracking
- API: `sendgrid.api/v3/mail/send`

### OpenAI (GPT-4)
- LLM analysis (Mode B)
- API: `api.openai.com/v1/chat/completions`

### CRM System
- Prospect record management, outreach tracking
- Internal: Pythia CRM

---

## Implementation Roadmap

### Phase 1: Week 1-2 (Go-Live Preparation)
- [ ] Legal review of all SOPs + disclaimer language
- [ ] Finalize Spam Act compliance checklist
- [ ] Set up Vercel infrastructure + SendGrid domain
- [ ] Train initial team (analysts, outreach)

### Phase 2: Week 3-4 (Pilot)
- [ ] Launch with 100 test prospects (internal + trusted partners)
- [ ] Validate all QA gates (Stage 0-5)
- [ ] Run first email campaign; monitor metrics
- [ ] Collect feedback; iterate SOPs

### Phase 3: Week 5-8 (Ramp)
- [ ] Scale to 500 prospects/week
- [ ] Monitor compliance (Spam Act, OAIC guidance, complaints)
- [ ] Conduct first accuracy audit (R-001 mitigation)
- [ ] Establish monthly risk review cadence

### Phase 4: Month 2-3 (Optimization)
- [ ] Implement R-002 mitigations (MFA, external security audit)
- [ ] Deploy R-005 mitigations (Compliance Benchmark feature)
- [ ] Add R-008 mitigation (secondary hosting failover)
- [ ] Target: 5,000 prospects analyzed; >5% teaser-to-paid conversion

---

## KPI Dashboard Targets

| KPI | Target | Owner | Cadence |
|-----|--------|-------|---------|
| **Scrape Success Rate** | >85% | Artemis team | Daily |
| **Analysis Confidence (avg)** | >80% | Sable | Daily |
| **Report QA Pass Rate** | >98% first attempt | QA team | Daily |
| **Email Deliverability** | >95% | Outreach team | Daily |
| **Spam Complaint Rate** | <0.3% | Compliance | Weekly |
| **Customer Satisfaction (NPS)** | >+35 | Marketing | Monthly |
| **Report Accuracy (audits)** | >98% | Sable | Monthly |
| **Analyst Agreement Rate** | >90% | Sable | Monthly |
| **Revenue/Customer** | $299-799 | Rob | Monthly |
| **Gross Margin** | >70% | Finance | Monthly |

---

## Risk Governance

**Monthly Risk Review:** First Wednesday, 2 PM AEST
- Attendees: Sable, Rob, Legal (as needed)
- Agenda: Risk score updates, mitigation progress, escalations
- Output: Risk status report (distributed to leadership)

**Escalation Thresholds:**
- CRITICAL (score ≥3.5): Immediate mitigation plan; daily standup
- HIGH (score 2.5-3.4): Weekly tracking; Rob notified
- MEDIUM (score 1.5-2.4): Monthly review; document mitigations
- LOW (score <1.5): Quarterly review; maintain monitoring

---

## Document Governance

**SOP Updates:**
- Quarterly review minimum (or triggered by regulatory change)
- Changes require: Owner sign-off + Rob approval
- Version control: Major updates = v2.0; minor fixes = v1.1

**Risk Register Updates:**
- Monthly (as part of risk review)
- New risks added as discovered
- Scores updated based on evidence

**Skill Definition Updates:**
- As product features evolve
- Backward compatibility maintained
- Version control in code repository

---

## Contact & Support

**Sable (Head of Research, Owner)**
- Email: sable@pythia.com
- Role: Methodology integrity, SOP compliance, QA oversight

**Rob (Product Lead)**
- Email: rob@pythia.com
- Role: Product vision, go-to-market, escalations

**Compliance Officer**
- Email: compliance@policycheck.au
- Role: Email QA, Spam Act checks, regulatory monitoring

**Support Channel (General)**
- Email: support@policycheck.au
- URL: https://policycheck.au/support

---

## Appendix: File Structure

```
/compliance-product/sable/
├─ README.md                 (this file; overview & quick reference)
├─ SOP-PC-001.md             (Prospect Identification & Scraping)
├─ SOP-PC-002.md             (Compliance Analysis)
├─ SOP-PC-003.md             (Report Generation & Delivery)
├─ SOP-PC-004.md             (Outreach & Email Compliance)
├─ SOP-PC-005.md             (Quality Assurance)
├─ policycheck-skill.md      (Skill Definition & Orchestration)
└─ risk-register.md          (Risk Assessment & Mitigations)
```

**Total Documentation:** ~148 KB; ~12,000 lines; comprehensive coverage of ops, product, compliance, QA, and risk

---

## Approval Sign-Off

**Prepared by:** Sable, Head of Research
**Date:** 2026-04-01
**Status:** Ready for Rob approval & implementation

**Approvals (Required):**
- [ ] Rob (Product Lead) — Product & go-to-market alignment
- [ ] Legal Counsel — Spam Act & liability compliance
- [ ] Pythia CISO — Data security & privacy practices
- [ ] Finance (CFO) — Cost & revenue projections

---

**Version:** 1.0
**Last Updated:** 2026-04-01
**Next Review:** 2026-10-01
