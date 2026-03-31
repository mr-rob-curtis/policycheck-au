# SOP-PC-001: Prospect Identification & Scraping

**Owner:** Head of Research (Sable)
**Last Updated:** 2026-04-01
**Status:** Active
**Audience:** Operations, Compliance Analysis Team

---

## Purpose

This SOP defines the end-to-end process for identifying target businesses and extracting privacy policy data using Artemis infrastructure. It ensures compliance with ethical scraping standards, legal obligations, and data privacy while maintaining operational efficiency.

---

## 1. Prospect Identification

### 1.1 Sector-Based Targeting via Artemis

**Process:**
1. Define target sectors aligned with Australian Privacy Act (APP) applicability
2. Use Artemis prospect discovery module to identify businesses by:
   - Industry classification (ANZSIC codes)
   - Business size (employee count, revenue thresholds)
   - Geographic scope (Australian-based operations)
   - APP obligation trigger (handles personal information, not exempted)

**Target Sectors (Priority Order):**
- Health services (highest compliance burden)
- Financial services (banking, insurance, lending)
- Retail and e-commerce (customer data collection)
- SaaS and software (user data handling)
- Professional services (legal, accounting, recruitment)
- Real estate (tenant/buyer personal information)
- Education (student records)
- Media and communications

**Quality Criteria:**
- Minimum 10 employees (sole traders/micro-businesses not economically viable)
- Online presence with discoverable website
- Active in last 12 months
- Not government agencies (public sector different requirements)

### 1.2 Data Sources for Prospect Discovery

**Primary Sources:**

| Source | Data Type | Update Frequency | Coverage | Notes |
|--------|-----------|------------------|----------|-------|
| **Australian Business Register (ABR)** | ABN, company name, registration date | Real-time | 2.5M+ active entities | Filter by ANZSIC, employee count estimates |
| **Google Maps** | Business listings, contact, categories | Weekly | ~80% of target businesses | Scrape carefully; use official API where possible |
| **ASIC** | Company directors, financial data | Monthly | 2M+ companies | Track director changes (compliance officer indicator) |
| **Industry Directories** | Sector-specific listings | Quarterly | Varies by sector | E.g., RACGP for health, RECA for real estate |
| **Chamber of Commerce** | Member directories | Quarterly | 50K+ SMEs | Often public, with email/phone |
| **LinkedIn** | Employee size, industry, hiring | Real-time | 800K+ AU companies | Enrich company data only, no employee scraping |
| **Domain registration** | Website ownership, contact | Real-time | Verify legitimacy | Check Whois data; flag privacy-protected owners |

**Prohibited Sources:**
- Scraped employee contact lists (LinkedIn email farming)
- Leaked customer databases
- Illegally obtained prospect data
- Sources requiring authentication bypass

### 1.3 Artemis Integration

**Artemis Output Format for PolicyCheck:**
```
{
  "prospect_id": "ARTxxx",
  "company_name": "Acme Corp AU",
  "abn": "12345678901",
  "industry": "Professional Services",
  "website_url": "https://acme.example.com.au",
  "primary_contact_email": null,  # discovered later
  "estimated_employees": 45,
  "last_verified": "2026-04-01",
  "data_sources": ["ABR", "Google Maps"],
  "confidence_score": 0.85  # likelihood they handle personal information
}
```

**Gate:** Minimum confidence score of 0.70 to proceed to scraping phase.

---

## 2. Website Scraping Workflow

### 2.1 Pre-Scrape Checks

Before initiating any scrape:

1. **Verify Business Legitimacy**
   - Domain registration matches company name (or legitimate variants)
   - Website has current content (not parked/abandoned)
   - Contact information present (email, phone, address)
   - No explicit "do not scrape" notices

2. **Check robots.txt and Terms of Service**
   - Respect robots.txt privacy rules
   - Read ToS for scraping restrictions
   - Flag for manual review if restrictions conflict with business model

3. **Rate Limit Planning**
   - Maximum 5 requests per domain per minute
   - Identify policy URL patterns (common: /privacy, /privacy-policy, /legal)
   - Plan request sequence to minimize load

### 2.2 Policy Discovery & Scraping

**Standard Workflow:**

```
Input: website_url
  │
  ├─ Attempt standard policy paths:
  │  ├─ /privacy-policy
  │  ├─ /privacy
  │  ├─ /policies
  │  ├─ /legal
  │  ├─ /terms-and-privacy
  │  └─ Custom patterns (footer links, sitemap)
  │
  ├─ If not found → Mark as "POLICY_ABSENT"
  │                 Escalate for manual verification
  │
  └─ If found → Scrape & Extract
     ├─ Full HTML → PDF conversion
     ├─ Extract text content
     ├─ Identify policy version/date
     └─ Log metadata (URL, fetch time, status code)
```

**Scraping Implementation:**
- Use Artemis internal scraper with anti-detection headers
- Browser user-agent rotation (daily)
- JavaScript rendering for dynamic content (Selenium/Playwright)
- Timeout: 30 seconds per page
- Retry logic: 3 attempts with exponential backoff (2s, 5s, 10s)

### 2.3 Quality Checks on Scraped Data

| Check | Pass Criteria | Failure Action |
|-------|--------------|-----------------|
| **Content Length** | >500 words | Flag as template/incomplete; manual review |
| **Key Sections Present** | Covers: collection, use, disclosure, security, rights | Flag gaps; proceed with caution |
| **Language** | Primarily English (>80%) | Include language identifier in report |
| **Date Extracted** | Policy date ≤2 years old | Flag as potentially outdated |
| **Legal Indicators** | References "privacy", "personal information", "disclosure" | May be false positive; manual review |
| **Duplicate Detection** | Not identical to existing scraped policies | Check MD5 hash against 5K+ policy database |

**Outcome:**
- **PASS**: Proceed to analysis phase
- **FAIL (Low Confidence)**: Route to analyst for manual review
- **FAIL (Absent Policy)**: Mark in prospect record; include in outreach as gap

### 2.4 Data Storage & Privacy Considerations

**Storage Architecture:**
```
Raw Policy Files:
  └─ /data/raw-policies/[PROSPECT_ID]/
     ├─ policy.html        (original scraped content)
     ├─ policy.txt         (text extraction)
     ├─ metadata.json      (timestamp, source, status)
     └─ screenshots/       (visual backup for disputes)

Processed Data:
  └─ /data/processed/[PROSPECT_ID]/
     ├─ analysis.json      (structured compliance assessment)
     └─ risk-flags.json    (identified gaps/risks)

Retention:
  - Raw files: 2 years (legal defensibility)
  - Processed data: 5 years (customer deliverables)
  - Access: Restricted to PolicyCheck AU team only
```

**Security Controls:**
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3+)
- No storage on local machines; cloud-only (Vercel infrastructure)
- Automated purge of policies when prospect record deleted
- Audit logging of all access (who, when, what)

**The Irony:** We are scraping privacy policies to assess compliance with the Australian Privacy Act. All scraped data is:
- Not personal information (published business policies)
- Publicly available (no hacking/unauthorized access)
- Used solely for compliance analysis service
- Subject to same APP principles we're auditing (only used for stated purpose, secured appropriately)

**Compliance Note:** While the scraped policies are public, treat the **association between prospect and policy assessment** as sensitive (competitive advantage data). Do not disclose client identity in policy storage.

### 2.5 Rate Limiting & Ethical Scraping Guidelines

**Global Rate Limits:**
- Max 500 policies scraped per day (resource constraints)
- No more than 10 requests to single domain per day
- Scraping window: 6 AM - 6 PM AEST (avoid peak business hours)
- User-agent identifies as: "PolicyCheck-AU-Bot/1.0 (+https://policycheck.au/bot)"

**Ethical Standards:**
1. **Transparency:** If domain owner complains, immediately halt scraping; provide opt-out mechanism
2. **Minimization:** Scrape only policy content (no sitemap harvesting, email harvesting, etc.)
3. **Respect:** Honor robots.txt; respond to take-down requests within 48 hours
4. **Load Management:** Stagger requests; implement backoff if 429 received
5. **No Impersonation:** Clearly identify as bot; do not mimic human user

**Escalation Triggers:**
- Multiple 403/429 responses from domain → pause; manual review before retry
- Domain blocks PolicyCheck-AU-Bot → escalate to Rob; consider DMCA risk
- Any cease-and-desist notice → immediately halt; legal review required

---

## 3. Data Quality Assurance

### 3.1 Post-Scrape Validation

**Automated Checks (in order):**
1. File integrity (not corrupted; valid HTML/text)
2. Content freshness (policy timestamp extracted)
3. Relevance (policy mentions personal information)
4. Completeness (all key sections identifiable)
5. Language (primarily English)

**Manual Review Triggers:**
- Any automated check fails
- Policy appears to be legal template (generic language)
- Policy conflicts with industry norms (unreasonably permissive/restrictive)
- Duplicate policy detected (indicates shared/white-label provider)

### 3.2 Duplicate & Derived Policy Detection

**Mechanism:**
- Compute MD5 hash of full policy text
- Store in centralized hash database
- Flag if >95% text match with existing policy
- Log: which company is original, which is copy (indicator of vendor use)

**Action:**
- If duplicate: note original source in metadata
- If derived: attempt to identify vendor (e.g., "This policy generated by LawTech XYZ")
- Reduce outreach to duplicates (less value to client)

---

## 4. Key Performance Indicators

| KPI | Target | Measurement |
|-----|--------|-------------|
| **Scrape Success Rate** | >85% of identified prospects | Policies found / prospects identified |
| **Policy Absence Rate** | <15% of target segments | Flag for outreach opportunity |
| **Data Quality Pass Rate** | >90% first attempt | Pass automated checks without manual review |
| **Processing Time** | <2 min per prospect | From discovery to analysis ready |
| **Bounce Rate** | <5% | Domains rejecting scraper / total requests |

---

## 5. Escalation Path

| Issue | Escalation | Timeline |
|-------|-----------|----------|
| **Scrape failure on >10 sites same domain pattern** | Sable (Head of Research) | Immediate |
| **Ethical concern (cease-and-desist, aggressive blocking)** | Rob (Product Lead) + Legal | Same day |
| **Data breach or unauthorized policy access suspected** | Pythia CISO | Immediate |
| **Quality assurance failure (>20% fail rate)** | Sable + Data Quality Lead | Daily standup |

---

## 6. Appendices

### 6.1 Standard Policy Path Templates

```
Common patterns observed:
- Example: https://example.com.au/privacy-policy
- Example: https://example.com.au/en/privacy
- Example: https://example.com.au/legal/privacy-policy
- Example: https://example.com.au/#/privacy
- Meta tag: <link rel="privacy-policy" href="..." />
```

### 6.2 robots.txt Respect Template

```
# Example: respecting robots.txt
User-agent: PolicyCheck-AU-Bot
Disallow: /admin
Disallow: /private

# Interpreted as: OK to scrape policies in public areas
```

### 6.3 Legal Precedent Notes

- High Court *Telstra v Phone Directories Co* (2010): Public data scraping can be lawful if no contractual breach
- ACCC Guidance: Scraping ToS restrictions may not be enforceable; respect demonstrated intent
- Australian Consumer Law: Transparent bot identification prevents misleading conduct
- Privacy Act: Scraped public policies not "personal information" under APP

---

**Document Version:** 1.0
**Next Review:** 2026-10-01
**Approved By:** [Rob/Product Lead] | [Sable/Head of Research]
