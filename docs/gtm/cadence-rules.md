# PolicyCheck AU: Outreach Cadence & Operations Rules

---

## EMAIL SENDING CADENCE

### Wave 1 Sector Campaign Timeline

**Email 1: The Gift**
- Day 0 (Campaign launch)
- Send time: 9:00 AM AEST (Australia Eastern Standard Time)
- Volume: Send all Wave 1 lists in single batch
- Timing rationale: Business hours, end of night for US contacts (if any B2B include US partners)

**Email 2: The Deadline**
- Day 4 (4 days after Email 1)
- Send time: 9:00 AM AEST
- Send ONLY to contacts who opened Email 1
- Volume: Approximately 35%+ of Email 1 recipients (open rate)
- Timing rationale: People who opened Email 1 are engaged; secondary offer likely to convert

**Email 3: The Peer Pressure**
- Day 10 (6 days after Email 2)
- Send time: 9:00 AM AEST
- Send ONLY to contacts who clicked Email 2 link OR opened Email 2
- Volume: Approximately 10%+ of Email 1 recipients (click + open rate)
- Timing rationale: Final nurture before moving to sales cadence

**Total campaign duration:** 10 days per prospect (from Email 1 to Email 3)

---

## MAXIMUM EMAILS & COOL-DOWN PERIODS

### Hard Limits

**Maximum emails per prospect per calendar month:** 3 (Email 1, Email 2, Email 3)

**Maximum emails per prospect across all campaigns:** 6 (Wave 1 only)

**Cool-down after Email 3:** 30 days minimum

**Cool-down if prospect unsubscribes:** Permanent (never contact again)

**Cool-down if prospect replies:** Escalate to sales; do NOT send Email 3 if Email 2 generated a reply

### Rationale

- 3+ emails per month = high unsubscribe risk + spam folder risk
- 6+ emails total = reputational damage
- 30-day cool-down = avoids fatigue, respects recipient inbox
- Replies = engagement signal; move to sales immediately

---

## SEGMENTATION & SEND STRATEGY

### Segment 1: Email 1 Recipients
**Definition:** All Wave 1 list prospects (real estate agencies, chemists, lawyers)
**Email 1 send:** Day 0, all recipients simultaneously
**Expected open rate:** 30-38%
**Action after Day 1:** Artemis flags opens automatically

### Segment 2: Email 1 Openers
**Definition:** Contacts who opened Email 1 (within 5 days of send)
**Email 2 send:** Day 4, ONLY to Email 1 openers
**Expected response:** 8-12% click through to full report
**Action:** Artemis flags clicks automatically

### Segment 3: Email 2 Engagers
**Definition:** Contacts who opened Email 2 OR clicked Email 2 link
**Email 3 send:** Day 10, ONLY to Email 2 engagers
**Expected response:** 5-7% soft conversion (click or reply)
**Action:** If reply, escalate to sales; otherwise mark as "nurture" or "cold" depending on response

### Non-Responders
**Definition:** Contacts who did not open Email 1
**Action:** Do NOT send Email 2 or Email 3
**Future cadence:** Move to retargeting pool (see below)

---

## ENGAGEMENT TRIGGERS & SALES ESCALATION

### Email Reply Triggers Immediate Sales Escalation

**If prospect replies to Email 1:**
- Do NOT send Email 2
- Sales team logs response in CRM
- Sales team follows up within 24 hours (phone or email)
- Email template: `sales-follow-up-reply-email1.txt`

**If prospect replies to Email 2:**
- Do NOT send Email 3
- Sales team logs response in CRM
- Sales team follows up within 24 hours
- Email template: `sales-follow-up-reply-email2.txt`

**If prospect replies to Email 3:**
- Sales team logs response in CRM
- Sales team follows up within 24 hours
- Email template: `sales-follow-up-reply-email3.txt`

### Click Triggers Secondary Offer

**If prospect clicks Email 1 teaser report link:**
- Email 2 goes to them on Day 4 (as scheduled)
- Artemis tracks that they viewed teaser report (valuable signal)
- Sales team can reference this in Email 2 follow-up

**If prospect clicks Email 2 full report link:**
- Email 3 goes to them on Day 10 (as scheduled)
- If they purchase A$149 report: sales team logs as "customer"
- If they view but don't purchase: sales team logs as "warm lead"
- Sales team follows up within 48 hours with special offer or help

**If prospect clicks Email 3 checklist link:**
- They've engaged with soft CTA
- Sales team logs as "warm lead"
- Move to sales cadence (see below)

---

## REPLY HANDLING WORKFLOW

### Auto-Reply System

**For all PolicyCheck emails, enable auto-reply:**
```
Thanks for getting in touch. We'll respond within 24 business hours.

In the meantime, here's your compliance score:
[TEASER_REPORT_LINK]

Best,
[PolicyCheck AU team]
```

**Why:** Confirms receipt, shows responsiveness, keeps them engaged.

### Manual Reply Review (24-hour SLA)

**Daily task (9:00 AM AEST):**
1. Check inbox for Email 1 / Email 2 / Email 3 replies
2. Categorize replies:
   - **"Interested"** (asks for report, pricing, demo): escalate to sales immediately
   - **"Not interested"** (declines or objects): add to unsubscribe list + send optional nurture email
   - **"Out of office"** (auto-reply): log in CRM, re-contact in 7 days
   - **"Wrong person"** (forwarded to someone else): add new contact, re-send Email 1 to correct person
   - **"Unsubscribe"** (any variation): add to global unsubscribe list immediately

### Reply Categories & Actions

**"Interested" replies (e.g., "Can you send me the full report?"):**
- Action: Send sales follow-up email with payment link for A$149 report
- Tone: Match their enthusiasm, offer help
- Timeline: Within 24 hours
- Template: `sales-follow-up-interested.txt`

**"Not interested" replies (e.g., "We don't need this" or "Not relevant"):**
- Action: Send optional nurture email (see below)
- Tone: Professional, non-pushy, helpful
- Timeline: Within 24 hours
- Template: `sales-follow-up-decline.txt`
- Offer: Free 13-point Privacy Act checklist (no cost, no friction)

**"Out of office" replies:**
- Action: Log in CRM, wait 7-10 days, send Email 1 again to same contact
- Reasoning: They didn't opt out; they were temporarily unavailable
- Timeline: Re-send 7-10 days after out-of-office ends

**"Wrong person" replies (e.g., "Try [Name] instead"):**
- Action: Extract new contact name and send Email 1 to them
- Note: Do NOT mark original contact as unsubscribed (they helped; respect that)
- Timeline: Within 24 hours
- New email: Use original Email 1 template + note: "Referral from [Original Contact Name]" (builds credibility)

**"Unsubscribe" requests (any form):**
- Action: Add to global unsubscribe list IMMEDIATELY
- Timeline: Same day
- Follow-up: Send optional unsubscribe confirmation email
- Template: `unsubscribe-confirmation.txt`
- Future action: Never contact again

---

## BOUNCE & INVALID EMAIL HANDLING

### Hard Bounce (Invalid Email Address)

**Definition:** Email address does not exist or domain is invalid

**Action:**
1. Artemis flags automatically
2. Do NOT retry to that address
3. Research valid contact email (check company website, LinkedIn, phone)
4. If valid email found: restart at Email 1
5. If no valid email found: mark as "no contact info" and skip

**Timeline:** Same day

### Soft Bounce (Temporary Delivery Issue)

**Definition:** Email bounced due to full inbox, server down, or temporary issue

**Action:**
1. Artemis retries automatically (3 attempts over 5 days)
2. If still bouncing after 5 days: treat as hard bounce
3. Research alternative contact email
4. Restart at Email 1 if new email found

**Timeline:** 5 days, then same as hard bounce

### Domain-Level Rejection

**Definition:** Email server rejects all emails from PolicyCheck domain

**Action:**
1. Artemis logs as domain issue (not email-specific)
2. Contact Artemis support to investigate
3. May indicate domain reputation issue (spam filtering, block list)
4. Pause outreach to that domain until resolved

**Timeline:** Same day investigation

---

## UNSUBSCRIBE PROCESSING

### Unsubscribe Request Processing (Spam Act 5-Business-Day Requirement)

**Definition:** Any request to remove email address from all future contact

**Forms of unsubscribe request:**
- Clicking "Unsubscribe" link in email footer
- Replying with "Unsubscribe"
- Replying with "Remove me"
- Any explicit request to stop contact

**Processing timeline:** Within 5 business days (Spam Act requirement)

**Action:**
1. Artemis logs unsubscribe automatically (if via unsubscribe link)
2. If via email reply, log manually in same day
3. Remove from ALL future outreach (not just this campaign)
4. Add to global unsubscribe list (shared across all PolicyCheck campaigns)
5. Send unsubscribe confirmation email (optional but recommended)

**Unsubscribe confirmation email template:**
```
We've removed [Email] from all PolicyCheck AU outreach.

If this was a mistake, or if you'd like to re-enable contact in the future,
just reply to this email and we'll be happy to help.

Thanks,
PolicyCheck AU team
```

**Record-keeping:** Keep unsubscribe record for 5+ years (proof of compliance if audited)

---

## RETARGETING & WARM LEAD NURTURE

### Non-Opener Retargeting (30+ Days Later)

**Definition:** Contacts who did not open Email 1

**Action after 30 days:**
1. Create new email sequence (separate from Wave 1)
2. Send retargeting Email 1 (similar to original, but fresh angle)
3. Treat as fresh campaign (new Email 1, Email 2, Email 3 cadence)

**Retargeting Email 1 variant subjects (increased curiosity focus):**
- "We scanned [Company Name]'s privacy policy—here's what we found"
- "[Company Name]: one privacy gap that could cost you A$5,000+"
- "Quick question: is your [sector] privacy policy July 1 ready?"

**Why separate campaign?** Avoids perception of spam (same message over and over); treats them as fresh lead.

### Warm Lead Nurture (Engaged but Didn't Buy)

**Definition:** Contacts who clicked Email 2 or Email 3 but didn't purchase

**Action:**
1. Log in CRM as "Warm lead"
2. Move to monthly nurture cadence (see below)
3. Sales team assigned (not marketing)
4. Sales team reaches out personally within 1 week

**Monthly nurture cadence:**
- Week 1: Sales call or phone outreach
- Week 2: If no response, email with free resource (checklist or webinar link)
- Week 3: If still no response, send one final email with "still available if useful" tone
- Week 4: If still no response, move to yearly re-engagement (contact again in 6 months)

**Warm lead email template:**
```
Hi [First Name],

I noticed you looked at our full Privacy Act compliance report. A few quick questions:

1. Did the report have what you needed?
2. Is timing just not right now?
3. Or is there something I can clarify?

No pressure at all—just want to make sure we're being helpful.

[Sales contact details]

Best,
[Sales rep name]
```

---

## SALES CADENCE (Post-Email 3)

### Warm Lead Path (Clicked Email 2 or Email 3)

**Day 1 (after Email 3 is sent or after engagement):**
- Sales team logs in CRM as "warm lead"
- Sales team sends personal outreach email or calls

**Day 2-3:**
- If no response to Email 3, send sales follow-up email
- Offer: "Can I help clarify the report?" or "Let's do a 15-minute walkthrough"

**Day 7:**
- If still no response, send second sales follow-up (phone call preferred)
- Tone: "Just checking in—is July 1 on your radar?"

**Day 14:**
- If still no response, send final follow-up with free resource
- Offer: Free checklist or webinar registration

**Day 30:**
- Move to monthly nurture (see above)

### Cold Lead Path (Did Not Open Any Email)

**Action:** Do NOT escalate to sales

**Instead:** Add to retargeting pool (see above), contact again in 30+ days with fresh angle

---

## COMPLIANCE REVIEW CADENCE

### Weekly Compliance Check (Tuesdays, 10:00 AM AEST)

**Checklist:**
- [ ] All unsubscribe requests processed within 5 days?
- [ ] All bounces flagged and researched?
- [ ] All replies logged in CRM?
- [ ] Artemis campaign settings still correct?
- [ ] Subject lines still truthful/compliant?
- [ ] Email footers include sender ID, address, unsubscribe?

**Responsible party:** Compliance lead or operations manager

### Monthly Compliance Audit (First Monday of month)

**Checklist:**
- [ ] Email templates reviewed for Spam Act compliance?
- [ ] Unsubscribe list maintained and shared across campaigns?
- [ ] Campaign records backed up (for ACMA audit-readiness)?
- [ ] No complaints from ACMA or recipients?
- [ ] Open/click rates within expected ranges?

**Responsible party:** Compliance lead

**If issues found:**
- [ ] Document issue
- [ ] Implement corrective action within 5 business days
- [ ] Update this document
- [ ] Brief team on changes

---

## CAMPAIGN PAUSE/RESUME RULES

### Pause Campaign If:

1. **Unsubscribe rate exceeds 5%** (indicates messaging mismatch)
   - Action: Review subject lines and Email 1 opening
   - Fix: Adjust messaging based on feedback
   - Resume: After fixes tested on small segment (50 people)

2. **Bounce rate exceeds 10%** (indicates list quality issue)
   - Action: Review list source and validation
   - Fix: Use cleaner list or validate current list
   - Resume: After list validation

3. **Click-through rate below 5% in Email 2** (indicates weak offer)
   - Action: Review A$149 report offer and messaging
   - Fix: Adjust Email 2 messaging or offer
   - Resume: After fixes tested on small segment

4. **Complaint from ACMA or recipient** (potential compliance issue)
   - Action: Investigate compliance immediately
   - Fix: Address issue and update templates
   - Resume: Only after compliance review

5. **Email domain blocked by major providers** (deliverability issue)
   - Action: Check domain reputation, review for spam complaints
   - Fix: Work with email provider to resolve
   - Resume: After domain reputation restored

### How to Pause:
- In Artemis, set campaign status to "Paused"
- Stop all Email 2 and Email 3 sends immediately
- Notify team via Slack/email
- Document reason and pause duration

### How to Resume:
- Review root cause and fix
- Test fix on small segment (50-100 people)
- Confirm fix is working
- In Artemis, set campaign status to "Active"
- Resume sends in next batch

---

## FREQUENCY CAPPING (GLOBAL)

### Maximum Contact Frequency per Prospect

**Per campaign:** 3 emails (Email 1, 2, 3)

**Across all campaigns:** 6 emails per 30 days (Wave 1 limit)

**Per year:** 12 emails maximum (includes retargeting)

**Implementation:**
- Artemis tracks all outreach (auto-captured)
- Suppress lists prevent duplicate sends
- Manual review monthly to catch edge cases

---

## SUCCESS METRICS & MONITORING

### Daily Metrics Check

**Track in Artemis dashboard:**
- Emails sent (by sector)
- Open rate (target: 30-38%)
- Click rate (target: 8-14%)
- Reply rate (target: 2-5%)
- Unsubscribe rate (target: <2%)
- Bounce rate (target: <5%)

### Weekly Reporting

**Email to team (Tuesdays, 2:00 PM AEST):**
- Total emails sent this week
- Cumulative open/click/reply rates (by sector)
- Top-performing subject line variants
- Any issues or pauses
- Next week's schedule

### Monthly Deep Dive

**Full campaign analysis (1st of month):**
- Email 1 performance (by sector)
- Email 2 performance (by sector)
- Email 3 performance (by sector)
- Conversion rates (report purchases)
- Cost per acquisition (divide email cost by purchases)
- Retention rate (reply + no unsubscribe)

**Targets:**
- Real Estate: 3-5% conversion to A$149 report
- Chemists: 4-6% conversion to A$149 report
- Lawyers: 2-3% conversion to A$149 report

---

## CRISIS PROTOCOLS

### If Major Complaint Received

**Definition:** Multiple complaints from single sector or organization

**Action:**
1. Pause all outreach immediately
2. Investigate complaint (what triggered it?)
3. Review affected email template
4. Conduct compliance audit (see above)
5. Brief leadership
6. Only resume after root cause fixed + compliance confirmed

### If Domain Reputation Damaged

**Definition:** Emails being marked as spam by major providers, or domain blocked

**Action:**
1. Pause all outreach immediately
2. Contact email provider (Artemis support)
3. Check for spam complaints (may be external sabotage or accidental)
4. Review recent campaigns for compliance issues
5. If domain is compromised, consider new domain for outreach
6. Only resume after reputation restored (confirmed by email provider)

### If ACMA Inquiry Received

**Definition:** Australian Communications and Media Authority contacts PolicyCheck

**Action:**
1. Do NOT ignore (this is a legal inquiry)
2. Document everything immediately
3. Compile all campaign records (templates, dates, list sources)
4. Gather evidence of compliance (unsubscribe handling, record-keeping)
5. Respond within 30 days with full explanation + evidence
6. Pause new outreach until inquiry resolved
7. Brief leadership and legal counsel

---

## HANDOFF TO SALES

### When to Escalate to Sales

1. **Email reply** (any email in sequence)
2. **Report purchase** (Email 2 or Email 3 link clicked + purchase)
3. **Phone inquiry** (prospect calls or replies with phone number)
4. **LinkedIn connection request** (prospect reaches out on LinkedIn)
5. **Warm lead** (clicked 2+ links but didn't purchase)

### Sales Handoff Email Template

```
Hi [Sales rep name],

New lead from PolicyCheck outreach:

Prospect: [Company Name]
Contact: [First Name] [Last Name]
Email: [Email]
Phone: [Phone if available]
Sector: [Real Estate / Chemist / Lawyer]
Engagement: [Email X open, Email Y click, Report view, Reply]
Stage: [Hot / Warm / Cold]

Email sequence background: [Brief summary of what we sent and why]

Next steps: [Suggest cold call, send product demo, etc.]

Best,
Marketing team
```

### SLA for Sales Follow-up

- Hot leads (replied to email): Contact within 4 business hours
- Warm leads (clicked, didn't purchase): Contact within 24 business hours
- Cold leads (opened email, didn't click): Contact within 5 business days

---

## FINAL SIGN-OFF

Before launching PolicyCheck campaigns, confirm:

- [ ] All cadence timing is set in Artemis (Day 0, 4, 10)
- [ ] Unsubscribe handling is automated
- [ ] Reply routing to sales is confirmed
- [ ] Bounce handling is automated
- [ ] Compliance review schedule is calendared
- [ ] Sales SLA is documented and communicated
- [ ] Campaign pause triggers are understood by team
- [ ] Monthly metrics targets are clear

**Campaign readiness: CONFIRMED**

