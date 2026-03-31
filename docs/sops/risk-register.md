# PolicyCheck AU - Risk Register

**Owner:** Sable (Head of Research)
**Last Updated:** 2026-04-01
**Review Frequency:** Monthly
**Status:** Active

---

## Risk Register Overview

This register documents operational, legal, reputational, technical, and commercial risks specific to PolicyCheck AU. Each risk includes likelihood, impact, mitigations, and ownership for ongoing monitoring.

**Risk Heat Map (by severity):**
```
CRITICAL (Likelihood × Impact = 4+ / 5 scale)
├─ R-001: Analysis accuracy leading to liability
├─ R-002: Privacy breach of scraped data
├─ R-004: Reputational damage from spam complaints
└─ R-009: Regulatory action for Spam Act violations

HIGH (Likelihood × Impact = 3-3.9 / 5)
├─ R-003: Brand dilution (compliance product ≠ research)
├─ R-005: Competitor market saturation
└─ R-008: Data center downtime (Vercel)

MEDIUM (Likelihood × Impact = 2-2.9 / 5)
├─ R-006: Scraper block/throttling by target domains
├─ R-007: LLM model limitations/degradation
└─ R-010: Scope creep in regulatory compliance

LOW (Likelihood × Impact = <2 / 5)
└─ R-011: Key personnel departure
```

---

## CRITICAL RISKS

### R-001: Analysis Accuracy Leading to Liability

**Description:** PolicyCheck AU generates compliance assessments that could influence client decision-making. If analysis is inaccurate, clients may fail regulatory audits, face OAIC investigations, or suffer reputational damage. This could trigger product liability claims.

**Likelihood:** MEDIUM (2/5)
- Rule-based mode is deterministic (95% confidence)
- LLM analysis introduces variability (70-85% confidence)
- Human review mitigates errors but not eliminated

**Impact:** CRITICAL (5/5)
- Product liability lawsuit: Could claim $100K+ damages
- Regulatory liability: OAIC may view us as complicit in non-compliance
- Reputational: "PolicyCheck gave us false confidence" narrative
- Brand damage: Undermines Pythia research credibility

**Overall Risk Score:** 2/5 × 5/5 = **CRITICAL (2.0/5.0 on 10-pt scale = 40%)**

**Mitigations (Current):**
1. ✓ SOP-PC-002: Rule-based + LLM + analyst review gates
2. ✓ SOP-PC-003: Clear disclaimer on all reports ("not legal advice")
3. ✓ SOP-PC-005: Monthly accuracy audits (5% sample)
4. ✓ Insurance: Errors & Omissions (E&O) policy for product liability (TBD)

**Mitigations (Recommended):**
1. **Expand QA sampling** from 5% to 10% monthly (resource cost: +$2K/month)
2. **Add legal review** for all Premium reports (currently: analyst only)
3. **Implement confidence score disclosure** in every report (already done)
4. **Cap liability in ToS** ("Maximum liability = price paid for report")
5. **Establish reinsurance** for extreme claims (unlikely but catastrophic)

**Control Assurance Level:** MEDIUM
- Monthly audits + analyst review provide oversight
- But: No legal QA; audits only 5% sample; no external certification

**Owner:** Sable (Head of Research) + Legal
**Escalation Trigger:** Complaint involving client legal action
**Monitoring:** Monthly audit report; track complaint types

---

### R-002: Privacy Breach of Scraped Data

**Description:** PolicyCheck AU stores scraped privacy policies (3,000+ documents by Y1 end). While these are public documents, a breach could expose the prospect-policy association (competitive intelligence), or be weaponized as "Pythia doesn't protect data" irony.

**Likelihood:** MEDIUM (2/5)
- Vercel infrastructure is industry-standard secure
- But: High-value target (competes with incumbents)
- Data at rest: Encrypted; in transit: TLS 1.3
- Risk: Insider threat or zero-day vulnerability

**Impact:** CRITICAL (5/5)
- Reputational: "Privacy tool company suffered privacy breach" = PR nightmare
- Competitive: Prospect list + analysis leaked to competitors
- Trust: Undermines product credibility with privacy-conscious customers
- Legal: OAIC investigation into our own privacy practices

**Overall Risk Score:** 2/5 × 5/5 = **CRITICAL (2.0/5.0)**

**Mitigations (Current):**
1. ✓ SOP-PC-001: Encrypted storage (AES-256 at rest)
2. ✓ TLS 1.3 in transit
3. ✓ Access controls: Restricted to PolicyCheck AU team only
4. ✓ Audit logging: All access logged with timestamp/IP
5. ✓ Data retention: Purge after 2 years if prospect deleted

**Mitigations (Recommended):**
1. **Implement multi-factor authentication (MFA)** for all PolicyCheck access
2. **Segment data** from Pythia research (separate AWS VPC or third-party hosting)
3. **Conduct annual security audit** (third-party penetration test)
4. **Cyber insurance policy** (data breach coverage; $1M-5M limit)
5. **Incident response plan** (drafted; ready for immediate deployment)

**Control Assurance Level:** HIGH
- Encryption, TLS, access controls in place
- But: No external audit yet; no third-party segmentation

**Owner:** Pythia CISO + Vercel Ops
**Escalation Trigger:** Unauthorized access detected; data exfiltration attempt
**Monitoring:** Monthly access log review; quarterly security audit

---

### R-004: Reputational Damage from Spam Complaints

**Description:** PolicyCheck AU sends 5,000-10,000 cold emails monthly. If compliance practices slip (misleading subject lines, hard unsubscribe, ignoring complaints), ACMA complaints could escalate, ISPs may blacklist our sending domain, and Pythia brand association could suffer.

**Likelihood:** MEDIUM-HIGH (3/5)
- Operating under Spam Act 2003 (strict rules)
- Human error in outreach team: Template mistakes, missed opt-outs
- ISP filters tighten (spam feedback loops)

**Impact:** CRITICAL (5/5)
- Email domain blacklist: All outreach campaigns fail; ~$50K/month revenue impact
- Brand damage: "Pythia bought compliance startup that violated Spam Act"
- Regulatory penalty: ACMA fines up to $555K AUD (low probability, high cost)
- Opportunity loss: Can't scale outreach; stuck at 500 prospects/month

**Overall Risk Score:** 3/5 × 5/5 = **CRITICAL (3.0/5.0)**

**Mitigations (Current):**
1. ✓ SOP-PC-004: All emails include required footer, unsubscribe, business address
2. ✓ 3-layer email QA (automated, manual, compliance approval)
3. ✓ Cadence limits: Max 3 emails per prospect per quarter
4. ✓ Unsubscribe honored within 5 days
5. ✓ Weekly email audit (random sample of 10 emails)
6. ✓ SendGrid compliance (DKIM, SPF, DMARC)

**Mitigations (Recommended):**
1. **Dedicated sending domain** (policycheck-mail.au) separate from pythia.com
   - Cost: ~$100/year
   - Benefit: If PolicyCheck domain gets blacklisted, main Pythia brand protected
2. **Monthly ACMA complaint check** (query public ACMA register)
3. **Implement BIMI/ARC** (advanced email authentication; cost: $2K/year)
4. **Third-party email audit** (Validity/ReturnPath certification; cost: $5K)
5. **Insurance for regulatory fines** (cyber liability; covered under general policy)

**Control Assurance Level:** HIGH
- Multiple QA gates + regular audits in place
- But: Human error still possible; no proactive ISP monitoring

**Owner:** Sable (Compliance) + Outreach Team Lead
**Escalation Trigger:** >1% spam complaint rate; ACMA inquiry received
**Monitoring:** Daily SendGrid metrics; weekly audit; monthly compliance report

---

## HIGH RISKS

### R-003: Brand Dilution (Compliance Product ≠ Research)

**Description:** Pythia brand is research/synthesis (SyntheticQual). PolicyCheck is transactional (compliance tool). Prospect confusion ("Wait, is Pythia a research firm or a legal tech company?") could dilute brand positioning.

**Likelihood:** HIGH (4/5)
- Both products share "Pythia" branding
- Target market overlap: Enterprise clients doing research + compliance
- Risk: B2B buyers may view Pythia as unfocused

**Impact:** MEDIUM-HIGH (3/5)
- SyntheticQual pricing pressure (clients say "You also do compliance audit, why charge $150K for research?")
- Sales complexity: Longer sales cycles explaining brand architecture
- Talent attraction: Researchers may not want to work at "compliance startup"
- Limited upside from bundling (most clients want one or the other)

**Overall Risk Score:** 4/5 × 3/5 = **HIGH (2.4/5.0)**

**Mitigations (Current):**
1. ✓ Separate product name: "PolicyCheck AU" (not "Pythia Compliance")
2. ✓ Separate website: policycheck.au (not pythia.com subdomain)
3. ✓ Separate marketing: Messaging emphasizes tool, not Pythia research
4. ✓ CRM segmentation: PolicyCheck prospects tracked separately

**Mitigations (Recommended):**
1. **Create brand architecture document** (explain: "Pythia Ventures operates multiple brands")
   - Cost: Internal (1-2 days)
   - Benefit: Clear positioning; easier for sales to explain
2. **Rebrand as standalone** (if continued under Pythia; cost: $50K+)
   - Consider: Spin PolicyCheck as separate company if > $2M ARR
3. **Pricing/packaging clarity** (show no bundle discount; products independent)
4. **Sales training** on brand positioning and product distinction
5. **Monitor NPS** by customer segment (research vs. compliance vs. both)

**Control Assurance Level:** MEDIUM
- Branding separate but not fully differentiated
- Risk of confusion still present in market

**Owner:** Rob (Product Lead) + Marketing
**Escalation Trigger:** Sales loss attributed to brand confusion; NPS drop
**Monitoring:** Monthly brand perception survey (among target customers); sales feedback

---

### R-005: Competitor Market Saturation

**Description:** Privacy compliance tools market is growing ($2B+ globally). Incumbent competitors (LawTech firms, Big 4 consulting) could enter AU market with better distribution, lower prices, or integrated solutions. PolicyCheck's early-mover advantage may be eroded.

**Likelihood:** HIGH (4/5)
- AU privacy market small but growing (GDPR awareness spillover)
- Low barriers to entry: Scraping + LLM analysis are commoditized
- AI-powered competitors already exist (US/EU): Harvey, LawGeex, etc.

**Impact:** HIGH (3/5)
- Revenue cannibalization: Pricing pressure; conversion rate decline
- Market share loss: If competitor gets to 1,000+ customers first, becomes standard
- Exit strategy impaired: Less attractive acquisition target if commoditized
- Customer retention: Switching costs low; easy to move to competitor

**Overall Risk Score:** 4/5 × 3/5 = **HIGH (2.4/5.0)**

**Mitigations (Current):**
1. ✓ First-to-market in AU (no direct competitors identified as of Apr 2026)
2. ✓ Integrated with Pythia infrastructure (distribution advantage)
3. ✓ Quality focus: Rule-based + LLM analysis exceeds basic tools
4. ✓ SOP-PC-002: Version-controlled APP definitions (= compliance edge)

**Mitigations (Recommended):**
1. **Build moat via data** (3,000+ analyzed policies → proprietary dataset)
   - Action: Create "Compliance Benchmark" (how your policies compare to peers)
   - Cost: $20K data science work
   - Benefit: Stickiness (competitors can't replicate without 3K+ customer data)
2. **Vertical specialization** (become "THE compliance tool for health sector")
   - Action: Deep product focus on health + regulatory relationships
   - Cost: Analyst time for sector expertise
   - Benefit: Defensible position vs. horizontal competitors
3. **Speed to acquisition** (profitable by Y1 end; make acquisition attractive)
   - Action: Focus on ARR growth & unit economics
   - Cost: Already in plan
   - Benefit: Exit before market commoditizes
4. **IP/patents** (if novel analysis methodology exists, patent it)
   - Action: Legal review; consider non-provisional patent
   - Cost: $15K-30K
   - Benefit: 10-year protection if defensible
5. **Customer lock-in** (ongoing monitoring/reports; make switching painful)
   - Action: Add "Annual Compliance Check" feature
   - Cost: $50K engineering
   - Benefit: Subscription revenue; stickiness

**Control Assurance Level:** MEDIUM
- Early-mover advantage present but not defensible yet
- Commoditization risk real within 12-18 months

**Owner:** Rob (Product Lead) + Sable
**Escalation Trigger:** Competitor product launch in AU; pricing pressure
**Monitoring:** Quarterly competitive intelligence scan; customer churn analysis

---

### R-008: Data Center Downtime (Vercel)

**Description:** PolicyCheck reports hosted on Vercel. If Vercel experiences outage, prospect portal/report links become inaccessible, outreach emails lead to dead links, and customer frustration spikes.

**Likelihood:** MEDIUM (2/5)
- Vercel has 99.95% SLA (historical: ~0.05% downtime)
- But: Single point of failure if no redundancy
- Risk: During critical launch period or high-traffic events

**Impact:** HIGH (3/5)
- Revenue impact: Downtime during peak outreach period = lost conversions
- Customer frustration: "I paid $299 and can't access my report"
- Reputational: Compliance tool shouldn't have uptime issues (ironic)
- Escalation: Customers request refunds; churn risk

**Overall Risk Score:** 2/5 × 3/5 = **HIGH (1.2/5.0)**

**Mitigations (Current):**
1. ✓ Vercel SLA: 99.95% uptime (industry standard)
2. ✓ Geographic distribution: Vercel serves from multiple regions
3. ✓ Monitoring: Uptime monitoring via StatusPage
4. ✓ Incident response: Vercel provides 24/7 support

**Mitigations (Recommended):**
1. **Secondary hosting failover** (e.g., AWS S3 CloudFront as backup)
   - Cost: $500/month + engineering setup ($5K)
   - Benefit: Near-zero downtime risk; automatic failover
   - Feasibility: High (reports are static PDFs)
2. **CDN for reports** (CloudFlare or Fastly; already via Vercel)
3. **Health check & alerting** (Pythia ops gets notified within 60 sec of outage)
   - Cost: $100/month (UptimeRobot or similar)
4. **Incident response SLA** (commit to restore within 1 hour; provide discount if miss)
5. **Regular DR testing** (simulate outage; practice failover quarterly)

**Control Assurance Level:** MEDIUM-HIGH
- Vercel SLA provides baseline protection
- But: No secondary failover; dependent on single vendor

**Owner:** Vercel Ops + Pythia Infrastructure
**Escalation Trigger:** Vercel outage affecting report access; customer complaints
**Monitoring:** Uptime dashboard; incident logs

---

## MEDIUM RISKS

### R-006: Scraper Block/Throttling by Target Domains

**Description:** PolicyCheck scrapes 500+ company websites monthly. Target domains may detect scraping bot activity and implement blocking (CAPTCHA, IP ban, honeypot). This degrades scraping success rate.

**Likelihood:** MEDIUM (3/5)
- Current success rate: 87% (good, but 13% fails)
- Risk increases with scale (more requests = easier to detect)
- Some domains actively block (tech-savvy companies)

**Impact:** MEDIUM (2/5)
- Reduced coverage: Can't analyze companies whose sites block us
- Outreach effectiveness: Can't offer report for blocked prospects
- Workaround cost: Manual scraping increases analyst time (resource constraint)
- Reputational: Being labeled "bot" damages brand with targets

**Overall Risk Score:** 3/5 × 2/5 = **MEDIUM (1.2/5.0)**

**Mitigations (Current):**
1. ✓ SOP-PC-001: Rate limiting (max 10 requests/domain/day)
2. ✓ User-agent rotation (daily rotation to avoid detection)
3. ✓ Respect robots.txt (honor domain's stated preferences)
4. ✓ Manual fallback (escalate to analyst if auto-scrape fails)

**Mitigations (Recommended):**
1. **Proxy network** (rotate residential IPs to avoid IP-based blocking)
   - Cost: $300/month (BrightData, Oxylabs)
   - Benefit: 95%+ success rate even for blocking domains
   - Ethical?: Legally murky; adds layer of deception
2. **Headless browser** (Playwright; render JavaScript like human; harder to detect)
   - Cost: Already using; +$500/month for scale
   - Benefit: Bypasses basic bot detection
3. **CAPTCHA-solving service** (if honeypot encountered)
   - Cost: $0.001-0.05 per CAPTCHA (expensive at scale)
   - Benefit: Can bypass basic CAPTCHA; not reliable for reCAPTCHA v3
4. **Public records alternative** (if website unavailable, offer public domain search)
   - Cost: $2K for integration
   - Benefit: Fallback source for policy discovery
5. **Communicate with top blocking domains** (ask for consent/API access)
   - Cost: Relationship management time
   - Benefit: Ethical + potentially better data

**Control Assurance Level:** MEDIUM
- Rate limiting + robots.txt respect in place
- But: Success rate still 87% (13% fail); no proxy/bypass yet

**Owner:** Sable + Artemis Team
**Escalation Trigger:** Success rate drops below 80%; specific domain blocks PolicyCheck
**Monitoring:** Weekly scraping metrics; per-domain success rates

---

### R-007: LLM Model Limitations/Degradation

**Description:** PolicyCheck relies on GPT-4 for Mode B analysis (confidence scoring, gap identification). If OpenAI changes model behavior, pricing, or terms; or if better alternatives emerge, analysis quality could suffer.

**Likelihood:** MEDIUM (3/5)
- OpenAI actively updates models (behavior may shift with new versions)
- Pricing fluctuations possible (currently $0.03 per 1K tokens input)
- Competitors (Claude, Gemini) emerging with comparable capability

**Impact:** MEDIUM (2/5)
- Analysis quality degradation: Lower confidence scores; reduced accuracy
- Cost increase: If OpenAI raises prices; impact margin by 10-20%
- Lock-in: Hard to switch models mid-production; retraining required
- Regulatory: If new model has different privacy practices (data retention)

**Overall Risk Score:** 3/5 × 2/5 = **MEDIUM (1.2/5.0)**

**Mitigations (Current):**
1. ✓ SOP-PC-002: Rule-based analysis as primary (LLM is secondary)
2. ✓ Confidence gates: Only use LLM output if high confidence
3. ✓ Analyst override: Human review catches LLM errors
4. ✓ Model versioning: Track which GPT-4 version used per report

**Mitigations (Recommended):**
1. **Multi-model strategy** (run analysis on 2 models; average scores)
   - Cost: +$0.02 per report (Claude + GPT-4)
   - Benefit: Hedges against single-model failure; improves accuracy
2. **Monitor model drift** (monthly; rerun test set of 100 policies on GPT-4)
   - Cost: ~$2/month
   - Benefit: Early detection of behavior changes
3. **Price lock contract** (negotiate with OpenAI for rate stability; cost: negotiation)
4. **Alternative model integration** (add Claude 3.5 Sonnet as backup; cost: $5K engineering)
5. **Rule-based sufficiency analysis** (if LLM unavailable, can rule-based alone suffice?)
   - Cost: Analysis (1-2 days)
   - Benefit: Understand true dependency on LLM

**Control Assurance Level:** MEDIUM
- Rule-based foundation provides fallback
- But: Heavy reliance on GPT-4 for confidence scoring

**Owner:** Sable + ML Engineering
**Escalation Trigger:** GPT-4 price increase >20%; confidence score drift >10%
**Monitoring:** Monthly model testing; cost tracking; accuracy benchmarks

---

## LOW RISKS

### R-010: Scope Creep in Regulatory Compliance

**Description:** Australian Privacy Act constantly evolving (GDPR awareness, IRAP alignment, etc.). PolicyCheck's compliance scope may expand beyond initial 13 APPs, requiring more analysis, deeper legal expertise, and higher liability exposure.

**Likelihood:** MEDIUM (3/5)
- Privacy regulations globally trending toward stricter (GDPR model)
- AU Parliament considering amendments (Privacy Legislation Amendment Bill 2022, etc.)
- Sector-specific regulations (health, finance) adding complexity

**Impact:** LOW-MEDIUM (2/5)
- Effort increase: More APPs/sectors to analyze; longer development
- Expertise gap: May need legal staff (currently: analyst-driven)
- Liability expansion: Broader scope = broader liability exposure
- Margin compression: More work per report; lower profitability

**Overall Risk Score:** 3/5 × 2/5 = **MEDIUM-LOW (1.2/5.0)**

**Mitigations (Current):**
1. ✓ SOP-PC-002: Version control for APP definitions (can update)
2. ✓ Quarterly legal review (check for regulatory changes)
3. ✓ Sector-specific adjustments already in place

**Mitigations (Recommended):**
1. **Regulatory horizon scanning** (quarterly; dedicated analyst monitors OAIC, Parliament)
   - Cost: 4 hours/quarter analyst time
   - Benefit: Early warning; time to adjust before massive change
2. **Scope gate** (define: what is in scope for v1.0; what is out of scope)
   - Current: 13 APPs only (national level)
   - Out of scope: Sector-specific regs (health, finance), state-level privacy laws
3. **Modular design** (add sector-specific modules only if market demand warrants)
4. **Legal partnership** (retain privacy lawyer on retainer for regulatory changes)
   - Cost: $3K-5K/month
   - Benefit: Faster adaptation to new requirements

**Control Assurance Level:** MEDIUM
- Version control + quarterly review in place
- But: No dedicated regulatory scanning process yet

**Owner:** Sable + Legal
**Escalation Trigger:** Major legislative change affecting APP scope
**Monitoring:** Quarterly legal review; OAIC guidance scan

---

### R-011: Key Personnel Departure

**Description:** PolicyCheck heavily dependent on Sable (analysis methodology) and Rob (product vision). If either departs, product continuity and quality could suffer.

**Likelihood:** LOW (2/5)
- Sable: Head of Research; deep expertise; unlikely to leave
- Rob: Product visionary; built enthusiasm
- But: Key person risk always present; could be poached by competitors

**Impact:** MEDIUM (2/5)
- Product knowledge loss: Analysis approach embedded in their understanding
- Momentum loss: New leader needs ramp-up time
- Quality degradation: Reduced oversight during transition
- Morale: Team may lose confidence in product direction

**Overall Risk Score:** 2/5 × 2/5 = **LOW (0.8/5.0)**

**Mitigations (Current):**
1. ✓ Documentation: SOPs capture methodology
2. ✓ Team training: Analysts trained on analysis approach
3. ✓ Competitive compensation: Both well-compensated (equity + salary)

**Mitigations (Recommended):**
1. **Succession planning** (identify backup for each key role)
   - Cost: Internal (identify from team)
   - Benefit: Continuity if someone departs
2. **Knowledge capture** (quarterly: extract domain knowledge; document)
   - Cost: 4 hours/quarter per person
   - Benefit: Reduce bus factor
3. **Equity vesting over 4 years** (both Sable & Rob; incentivizes staying)
4. **Retention bonus** ($50K if stay through Y2)
5. **Team cross-training** (no single person critical to any process)

**Control Assurance Level:** MEDIUM-HIGH
- Documentation + training reduce risk
- But: Some tacit knowledge only in their heads

**Owner:** HR + Rob
**Escalation Trigger:** Key person indicates intent to leave
**Monitoring:** Annual retention check-ins

---

## RISK MONITORING & GOVERNANCE

### Monthly Risk Reviews

Sable leads monthly risk review (first Wednesday):
- [ ] Update risk scores based on recent events
- [ ] Review mitigations implemented (% complete)
- [ ] Identify new risks
- [ ] Escalate critical/high risks to Rob + Legal

**Risk Review Template:**
```
Month: April 2026
Reviewed by: Sable
Attendees: Rob, Legal

NEW RISKS IDENTIFIED:
- R-012: [new risk if discovered]

RISK STATUS CHANGES:
- R-001: CRITICAL (unchanged)
- R-003: HIGH → MEDIUM (brand confusion less likely due to marketing efforts)
- R-006: MEDIUM (unchanged; scraper success rate stable at 87%)

MITIGATION UPDATES:
- R-002 (Privacy Breach): Completed MFA rollout (4/5 items done)
- R-004 (Spam Complaints): Added dedicated sending domain (policycheck-mail.au)
- R-008 (Downtime): In progress - secondary hosting failover (design phase)

ESCALATIONS:
- None this month

ACTION ITEMS FOR NEXT MONTH:
1. R-002: Complete security audit (external vendor)
2. R-005: Finalize "Compliance Benchmark" feature spec
3. R-007: Test Claude 3.5 Sonnet as LLM backup

Next Review: 2026-05-01
```

### Escalation Thresholds

| Risk Level | Trigger | Escalation | Action |
|-----------|---------|-----------|--------|
| **CRITICAL (≥3.5/5)** | Any CRITICAL risk | Rob + Legal + CISO | Immediate mitigation plan; daily standup |
| **HIGH (2.5-3.4/5)** | Likelihood or Impact increase | Rob + Sable | Weekly tracking; mitigation progress |
| **MEDIUM (1.5-2.4/5)** | Consistent score or increasing | Sable | Monthly review; document mitigations |
| **LOW (<1.5/5)** | Stable or decreasing | Sable | Quarterly review; maintain monitoring |

---

## Risk Appendix

### A. Likelihood & Impact Definitions

**Likelihood (1-5 scale):**
- 1 (Very Low): <10% chance in next 12 months
- 2 (Low): 10-25% chance
- 3 (Medium): 25-50% chance
- 4 (High): 50-75% chance
- 5 (Very High): >75% chance

**Impact (1-5 scale):**
- 1 (Minimal): <$10K loss; no brand impact
- 2 (Low): $10K-50K loss; minimal brand impact
- 3 (Medium): $50K-250K loss; noticeable brand impact
- 4 (High): $250K-1M loss; significant brand damage
- 5 (Critical): >$1M loss; severe brand damage / existential threat

**Risk Score = Likelihood × Impact / 5 (normalized to 0-5 scale)**

### B. Mitigation Cost Estimates

| Risk | Current Annual Cost | Recommended Mitigations | Additional Cost |
|------|---|---|---|
| R-001 (Accuracy) | $0 (SOP + audit) | Legal QA ($30K/yr); expand audit ($2K/yr) | +$32K/yr |
| R-002 (Privacy) | $0 (encryption built-in) | MFA, audit, insurance ($25K/yr) | +$25K/yr |
| R-003 (Brand) | $0 (brand architecture) | Market research, training ($10K/yr) | +$10K/yr |
| R-004 (Spam) | $500 (audits + domain) | BIMI, third-party audit ($7K/yr) | +$7K/yr |
| R-005 (Competition) | $0 (first-mover) | Data moat building ($20K/yr); IP patents ($10K one-time) | +$20K/yr |
| R-006 (Scraper Block) | $0 (rate limiting) | Proxy network; headless browser scale ($5K/yr) | +$5K/yr |
| R-007 (LLM) | $0.02/report | Multi-model strategy; testing ($5K/yr) | +$5K/yr |
| R-008 (Downtime) | $0 (Vercel SLA) | Secondary hosting failover ($6K setup + $500/mo) | +$12K/yr |
| R-010 (Scope Creep) | $0 | Legal partnership ($50K/yr); horizon scanning | +$50K/yr |
| R-011 (Key Person) | $0 | Succession planning, retention bonus ($50K/yr) | +$50K/yr |
| | | **TOTAL FIRST-YEAR MITIGATION COST** | **~$186K** |

**ROI Rationale:** Year 1 revenue estimate = $500K-1M; $186K mitigation investment = 18-37% of revenue. Justified given existential risk profile.

---

**Document Version:** 1.0
**Next Review:** 2026-05-01
**Approved By:** [Rob/Product Lead] | [Sable/Head of Research] | [Legal]
