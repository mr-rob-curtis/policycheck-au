# SOP-PC-004: Outreach & Email Compliance

**Owner:** Head of Research (Sable)
**Last Updated:** 2026-04-01
**Status:** Active
**Audience:** Outreach/Sales Team, Compliance Team, Rob (Product Lead)

---

## Purpose

This SOP ensures that all PolicyCheck AU cold email outreach complies with Australian Spam Act 2003 and industry best practices, while maintaining brand integrity and maximizing deliverability and response rates.

---

## 1. Australian Spam Act 2003 Compliance Overview

### 1.1 Regulatory Framework

**The Australian Spam Act 2003** regulates commercial electronic messages sent to/from Australia. Key requirements:

| Requirement | Our Obligation | PolicyCheck Implementation |
|-------------|---|---|
| **Sender Identification** | Must clearly identify sender | From: name identifies company & department |
| **Subject Line** | Must not mislead about content | Honest, no clickbait (e.g., not "URGENT: ACT NOW") |
| **Business Address** | Must include physical address | Footer includes registered office address |
| **Unsubscribe Mechanism** | Easy, free, prompt opt-out | One-click link; honored within 5 business days |
| **Consent** | B2B email has lighter requirements; B2C stricter | Focus: B2B (businesses, not consumers) |
| **No Automated Harvesting** | Must not spider/harvest emails without consent | Pre-existing relationships or legitimate discovery |

**Exceptions:**
- The Spam Act primarily targets **commercial messages** (selling/promoting goods/services)
- PolicyCheck AU emails ARE commercial (promoting compliance service)
- PolicyCheck AU prospects are primarily **businesses** (lighter regulatory burden than consumers)

### 1.2 Penalties for Non-Compliance

- ACMA (Australian Communications & Media Authority) enforcement
- Civil penalties: Up to $555,000 AUD per breach
- Criminal penalties (egregious cases): Up to $111,000 AUD + imprisonment
- Reputational damage & blacklisting

---

## 2. Required Email Elements

### 2.1 Mandatory Email Header & Footer

**Every PolicyCheck AU outreach email MUST include:**

#### **From Line:**
```
From: PolicyCheck AU <noreply@policycheck.au>
Reply-To: support@policycheck.au
```
- Must identify company clearly
- Use no-reply address only if reply-to is set (otherwise unreachable)
- Alternate: `From: Rob Smith, PolicyCheck AU <rob@policycheck.au>` (personalized)

#### **Subject Line:**
- Must be honest & accurate
- Avoid: ALL CAPS, urgency triggers ("URGENT", "ACT NOW"), misleading claims
- Examples (GOOD):
  - "Your Privacy Policy Assessment: Free Compliance Check"
  - "Australian Privacy Act Compliance Report - [Company Name]"
  - "Your Business Privacy Policy Analyzed Against APP"
- Examples (BAD):
  - "URGENT: Privacy Violation Detected at Your Company" (misleading)
  - "COMPLIANCE ALERT" (alarmist)
  - "Act Now to Avoid Legal Liability" (pressure tactic)

#### **Email Body:**
Minimum 300 characters; professional business tone
- No aggressive sales language
- Focus on value (assessment = help with compliance, not "gotcha" inspection)
- Example opening:
  ```
  Hi [Name],

  We analyzed your privacy policy against Australian Privacy Act requirements
  and identified potential compliance gaps. Here's what we found—and how to fix them.

  [Teaser report findings]

  [CTA to view full report]
  ```

#### **Footer (Required by Spam Act):**
```
---

PolicyCheck AU
Powered by Pythia

Pythia Intelligence Pty Ltd (ABN: [ABN])
535 Mission Street, Suite 1100
San Francisco, CA 94105
Australia Office: [Address to be confirmed]

Email: support@policycheck.au
Phone: [Number]

If you no longer wish to receive emails from PolicyCheck AU,
unsubscribe here: [One-click unsubscribe link]

Privacy: https://policycheck.au/privacy
Terms: https://policycheck.au/terms
```

**Why This Format:**
- Clear identification (company name, not obfuscated)
- Physical address (legal requirement)
- Easy unsubscribe (clear, actionable)
- Contact method (demonstrates legitimacy)

---

## 3. Email Cadence & Frequency Limits

### 3.1 Global Rate Limits

**Per prospect:**
- Maximum 3 emails per quarter (12 weeks)
- Minimum 2 weeks between first and second email
- Minimum 3 weeks between second and third email
- After 3rd email: pause for 12 weeks before restart (if no response)

**Per prospect domain (same company):**
- Maximum 5 separate email addresses contacted per quarter
- Stagger contacts (don't email entire company leadership in same day)

**Per outreach campaign:**
- Maximum 5,000 emails per day (resource constraints + deliverability)
- Pace: ~200 emails/hour (not burst delivery which triggers spam filters)

### 3.2 Sequence Rules

**Standard 3-Email Sequence:**

**Email 1: Initial Outreach (Teaser)**
- Content: Free compliance assessment + findings
- Tone: Informative, no pressure
- CTA: "See full report" (upgrade offer)
- Timing: Day 1

**Email 2: Follow-Up (Value Add)**
- Content: If no response after 14 days; include short tip or regulatory update relevant to their sector
- Tone: Helpful, not pushy
- CTA: "View report + get free consultation" (sweetener)
- Timing: Day 14 (if no response)

**Email 3: Final Outreach (Last Attempt)**
- Content: If no response after 35 days; final offer
- Tone: Professional, accepting of "no"
- CTA: "Expired offer; contact us if interested later"
- Timing: Day 35 (if no response)

### 3.3 Cadence Exemptions

**Suspend outreach if:**
- Prospect explicitly opts out (honored immediately, logged in CRM)
- Prospect's company details suggest they've exited the market
- Bounce/delivery failure (email invalid or domain doesn't exist)
- Prospect asks to be added to "do not contact" list (honored for 24 months)
- Company acquired/merged (requires re-qualification with new owners)

---

## 4. Segment-Specific Outreach Rules

### 4.1 Sector-Specific Messaging

Each sector receives customized email variant tailored to their compliance pain points:

#### **Health Sector (Highest Sensitivity)**
- Messaging: "App compliance gap = patient data at risk"
- Emphasis: Security, patient trust, regulatory audit preparedness
- Regulatory angle: OAIC, health regulator trends
- Example subject: "Health Privacy Compliance Assessment: [Clinic Name]"
- Avoid: Alarmism ("You are likely in breach")

#### **Financial Services**
- Messaging: "APP 6 (disclosure) & APP 8 (credit reporting) gaps"
- Emphasis: Customer trust, ASIC expectations, affiliate data sharing
- Regulatory angle: RBA guidance, ASIC expectations
- Example subject: "Your Privacy Policy vs Financial Services Standards"
- Avoid: "You're exposing customer data"

#### **Retail/E-Commerce**
- Messaging: "APP 7 (marketing) & APP 3 (collection) compliance"
- Emphasis: Customer experience, unsubscribe ease, ACCC expectations
- Regulatory angle: Australian Consumer Law, ACCC guidance
- Example subject: "Privacy Compliance for Online Retailers"
- Avoid: Scaring about data breaches

#### **SaaS/Software**
- Messaging: "APP 11 (security) and data residency transparency"
- Emphasis: Cloud data handling, customer trust, vendor due diligence
- Regulatory angle: IRAP alignment (if govt customers)
- Example subject: "SaaS Privacy Compliance Assessment"
- Avoid: Over-technical language (they know encryption)

#### **Small/Micro Business (<10 employees)**
- Messaging: "Simplified APP compliance for startups"
- Emphasis: Cost-effective fixes, not overwhelming
- Regulatory angle: OAIC often lenient with SMEs
- Example subject: "Free Privacy Policy Review for [Business]"
- Avoid: Enterprise-level complexity

### 4.2 Sector Targeting Rules

**Target:**
- Health: >10 employees (compliance investment justified)
- Finance: >15 employees (handles customer data at scale)
- Retail: >20 employees (e-commerce/POS systems)
- SaaS: >5 employees (often tech-savvy, care about compliance)
- Other: >10 employees (general threshold)

**Do Not Target:**
- Government agencies (different compliance regime)
- Non-profit/charity (non-commercial)
- Sole traders/sole proprietorships (cost-benefit unfavorable)
- Businesses in insolvency/liquidation
- Explicit "do not contact" reputation (via ASIC/ACMA blacklist)

---

## 5. Outreach Workflow & Pre-Send Checks

### 5.1 Campaign Creation Workflow

```
Step 1: Define Segment
  ├─ Select sector(s)
  ├─ Define company size
  ├─ Select geographic scope (AU only)
  └─ Confirm prospect count (<5,000/day max)

Step 2: Prospect Deduplication
  ├─ Check CRM for existing contacts
  ├─ Remove opted-out addresses
  ├─ Remove known bad emails (bounces)
  └─ Remove competitors/irrelevant companies

Step 3: Personalization
  ├─ Enrich with company name, contact name
  ├─ Generate sector-specific email variant
  ├─ Customize subject line (avoid mail-merge artifacts)
  └─ Verify all variables populated correctly

Step 4: Pre-Send QA (see 5.2)
  ├─ Run automated checks
  ├─ Manual review of sample (n=5)
  └─ Approve/return for revision

Step 5: Delivery
  ├─ Schedule via email service (Vercel/SendGrid)
  ├─ Pace delivery (200/hour max)
  ├─ Monitor bounce/complaint rates
  └─ Log in CRM with timestamp
```

### 5.2 Pre-Send Quality Checklist

**Automated Checks (in system):**
- [ ] All emails have subject line (not blank)
- [ ] All emails have footer with ABN, address, unsubscribe link
- [ ] All emails have from/reply-to headers
- [ ] Subject line not ALL CAPS (spam indicator)
- [ ] No phishing indicators (URL shorteners, suspicious links)
- [ ] Unsubscribe link functional (not dummy)
- [ ] No personal data in email body (e.g., employee salary)
- [ ] File size <100KB (compliance with email standards)
- [ ] No executable attachments (security)

**Manual Review (Sampling):**
For each campaign, review sample of 5 random emails:
- [ ] Personalization accurate (correct prospect name/company)
- [ ] Tone professional (not aggressive, not generic)
- [ ] CTA clear and actionable
- [ ] Footer formatting consistent
- [ ] No typos or grammatical errors
- [ ] Sector-specific variant appropriate for recipient
- [ ] No misleading claims in subject line

**Compliance Review (Sample):**
- [ ] Spam Act elements present (sender ID, address, unsubscribe)
- [ ] Subject line honest (not misleading)
- [ ] Sender identity clear (not spoofed)
- [ ] Unsubscribe mechanism clearly stated

**If Any Check Fails:** Campaign paused; returned for correction. Do not send.

---

## 6. Outreach Email Templates

### 6.1 Template: Health Sector Outreach

```
Subject: Free Privacy Compliance Assessment: [Clinic/Hospital Name]

Dear [Contact Name],

Healthcare providers in Australia handle sensitive patient data daily—and
the Australian Privacy Act sets strict requirements for how that data
must be protected and disclosed.

We analyzed [Clinic Name]'s privacy policy against the 13 Australian
Privacy Principles and identified [X] areas for improvement. Here's what
we found:

• APP 11 (Security): Policy doesn't explicitly disclose encryption measures
• APP 12 (Access): No clear process for patients to request their records
• APP 5 (Notification): Limited disclosure about what data is collected

These gaps could expose your clinic to regulatory complaints and erode
patient trust. The good news: they're fixable.

[View Your Free Assessment →]

In the attached teaser report, you'll see:
- Your privacy compliance score (APP scoring)
- The top gaps we identified
- Quick recommendations to improve

Questions? Reply to this email or contact us at support@policycheck.au.

---

PolicyCheck AU
Powered by Pythia

Pythia Intelligence Pty Ltd (ABN: [ABN])
[Address]

support@policycheck.au
[Phone]

Unsubscribe: [Link]
```

### 6.2 Template: Financial Services Outreach

```
Subject: Your Bank/Insurer's Privacy Policy vs App Standards

Dear [Contact Name],

Financial services in Australia are held to high privacy standards.
Customers expect their financial data to be handled transparently—and
regulators (ASIC, RBA) increasingly expect that too.

We analyzed [Company Name]'s privacy policy against the 13 Australian
Privacy Principles and found areas where clarity could improve:

• APP 6 (Use/Disclosure): Sharing with "affiliated companies"—but list unclear
• APP 8 (Credit Reporting): If you handle credit data, this needs specifics
• APP 13 (Complaints): Complaint resolution timeline not mentioned

For financial services, these are standard audit questions. We can help
you get ahead of them.

[See Your Free Compliance Assessment →]

What you'll get:
- Score on each of the 13 APPs
- Specific gaps that regulators care about
- Recommendations aligned with industry standards

[View Report]

---

PolicyCheck AU
Powered by Pythia

Pythia Intelligence Pty Ltd (ABN: [ABN])
[Address]

support@policycheck.au
[Phone]

Unsubscribe: [Link]
```

### 6.3 Template: Follow-Up (Email 2)

```
Subject: Regulatory Update: Privacy Act & Your Sector

Dear [Contact Name],

Following up on the privacy assessment we sent earlier this week.

Thought you might find this useful: The OAIC released updated guidance
on APP 6 (disclosure) for [Sector]. Key takeaway: regulators expect
companies to be explicit about third-party data sharing. If your policy
is vague on this, now is the time to clarify.

Your assessment identified a gap here. Want to see the specific
recommendations?

[View Your Report + Get Free 15-min Consultation →]

No pressure—just want to make sure you have the tools to stay compliant.

---

PolicyCheck AU
Powered by Pythia

[Rest of footer]
```

### 6.4 Template: Final Outreach (Email 3)

```
Subject: Last Chance: Your Free Privacy Compliance Review

Dear [Contact Name],

This is our last outreach—I promise.

If you haven't already, here's your complimentary privacy assessment.
No strings attached, no sales call required.

[Access Report (expires end of week)]

If you'd rather not hear from us again, just let us know and we'll
remove you from our list.

Either way, we're here if you need us.

---

PolicyCheck AU
Powered by Pythia

[Rest of footer]
```

---

## 7. Response Handling & Escalation

### 7.1 Prospect Response Scenarios

**If prospect replies to email:**

| Response Type | Action | Escalation |
|---|---|---|
| **"Unsubscribe me"** | Immediately remove from list; log in CRM | None |
| **"We already have a lawyer"** | Acknowledge; note in CRM; no further outreach | None |
| **Question about report** | Sales team answers; offer call | Sales |
| **Interest in report** | Offer Standard or Premium tier; route to sales | Sales |
| **Complaint about email** | Apologize; offer opt-out; log in compliance log | Sable (Head of Research) |
| **Cease-and-desist** | Immediately halt; escalate to legal | Legal |
| **Out of office/auto-reply** | Pause sequence; retry after 2 weeks | None |

### 7.2 Spam Complaint Handling

**If prospect marks email as spam (complaint rate >0.5%):**
1. **Immediate:** Stop sending to that domain's email provider
2. **Review:** Analyze last 5 emails sent to that provider for issues
3. **Investigation:** Check:
   - Was footer present? (compliance)
   - Was unsubscribe easy? (compliance)
   - Was subject line honest? (tone)
   - Were we violating cadence rules? (frequency)
4. **Action:**
   - If compliance issue found: Fix, document, implement across all campaigns
   - If false positive (prospect angry, not real spam complaint): Note in CRM
   - If systematic (>3 complaints from same provider): Pause that segment

### 7.3 Escalation Path

| Trigger | Owner | Timeline |
|---------|-------|----------|
| **Prospect complaint about marketing** | Sable + Sales Lead | Same day |
| **Spam complaint rate >1%** | Sable | Immediate |
| **Cease-and-desist from prospect's lawyer** | Legal | Immediate |
| **Unsubscribe request not honored within 5 days** | Compliance Officer | Urgent |
| **Email bounce rate >5%** | Ops team | Daily standup |

---

## 8. Compliance Audit & Monitoring

### 8.1 Weekly Email Audit

**Every Friday, audit random sample of 10 sent emails:**
- [ ] Footer present & complete (address, unsubscribe, ABN)
- [ ] From/reply-to headers correct
- [ ] Subject line honest (not misleading)
- [ ] Cadence rules followed (no more than 3/quarter to same prospect)
- [ ] Unsubscribe link tested & functional
- [ ] No spam indicators (urgency language, all caps, phishing)

### 8.2 Monthly Compliance Report

**Sable produces monthly report:**
```
Month: [Month]
Total emails sent: [Count]
Bounce rate: [%]
Spam complaint rate: [%]
Unsubscribe rate: [%]
Compliance violations: [Count]
  ├─ Missing footer: [Count]
  ├─ Misleading subject line: [Count]
  ├─ Cadence violation: [Count]
  └─ Other: [Count]

Corrective actions:
├─ [Action 1]
└─ [Action 2]

Audit: [Pass/Fail]
Approved by: Sable
```

### 8.3 Regulatory Alignment Check

**Quarterly check against latest Spam Act guidance:**
- [ ] ACMA updated enforcement guidance? (review)
- [ ] Industry best practices changed? (review)
- [ ] Case law on Spam Act? (legal review)
- [ ] Update SOP if needed

---

## 9. Key Performance Indicators

| KPI | Target | Measurement |
|-----|--------|-------------|
| **Email Deliverability** | >95% | Emails delivered / sent |
| **Bounce Rate** | <2% | Invalid addresses / total sent |
| **Spam Complaint Rate** | <0.3% | Complaints / total sent |
| **Unsubscribe Rate** | <1% | Unsubscribes / delivered |
| **Open Rate (Teaser)** | >15% | Opens / delivered |
| **Click Rate (Teaser)** | >3% | Clicks / delivered |
| **Conversion Rate (Teaser→Paid)** | >5% | Paid reports / teaser sent |
| **Compliance Violations** | 0 per month | Spam Act breaches |

---

## 10. Appendices

### 10.1 Spam Act Checklist

**Before sending ANY campaign, confirm:**
```
☐ Sender identity clear (company name, not spoofed)
☐ From/reply-to headers populated
☐ Subject line honest (not misleading or all caps)
☐ Business address in footer (physical address, not PO box)
☐ Unsubscribe link functional & easy
☐ Unsubscribe honored within 5 business days
☐ No harvested email addresses (all opted in or business relevance)
☐ No automated scraping of contacts
☐ No image-only emails (bypass filters illegally)
☐ No misleading headers/routing
```

### 10.2 Subject Line Dos & Don'ts

**DO:**
- "Your Privacy Policy Assessment: [Company Name]"
- "Australian Privacy Act Compliance Report - Free"
- "Privacy Compliance Gap: 3 Easy Fixes for [Sector]"

**DON'T:**
- "URGENT: PRIVACY VIOLATION FOUND" (alarm/misleading)
- "ACT NOW OR FACE LEGAL LIABILITY" (pressure)
- "FREE MONEY—CLAIM YOUR PRIVACY REWARD" (misleading)
- "Your Company is Not Compliant" (negative, unproven)
- All caps (spam filter trigger)

### 10.3 Unsubscribe Link Implementation

**Unsubscribe link must:**
- Work with single click (no confirmation page)
- Be honored within 5 business days
- Log unsubscribe in CRM with timestamp
- Remove from all future campaigns (not just current)

**Example implementation:**
```
[Unsubscribe]: https://policycheck.au/unsubscribe?token=[UNIQUE_TOKEN]

Token = one-time use, expires after 7 days
```

---

**Document Version:** 1.0
**Next Review:** 2026-10-01
**Approved By:** [Rob/Product Lead] | [Sable/Head of Research] | [Legal/Compliance]
