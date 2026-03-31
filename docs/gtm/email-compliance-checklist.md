# Australian Spam Act 2003: Email Compliance Checklist

## CRITICAL COMPLIANCE REQUIREMENTS

### 1. SENDER IDENTIFICATION (Spam Act Section 17)

**Every email MUST include:**

- Sender's name (individual or business name)
- Sender's physical business address
- Valid sender email address or phone number

**Implementation in PolicyCheck AU emails:**

```
Best,

[Sender Name]
PolicyCheck AU
[Phone: +61 2 XXXX XXXX]
[Address: Street, Suburb, State, Postcode]
[Email: sender@policycheck.au]
```

**Why:** Recipients must be able to identify who sent the email and contact them. This is non-negotiable.

**Red flags:**
- Using personal email only (non-compliant)
- Using fake/unverifiable business address (non-compliant)
- Omitting phone number (risky, borderline non-compliant)

---

### 2. UNSOLICITED COMMERCIAL ELECTRONIC MESSAGES (Spam Act Section 16)

**PolicyCheck emails are B2B (business-to-business).**

**Under the Spam Act:**
- B2B emails to established business relationships are EXEMPT from consent requirements
- B2B emails to new contacts are subject to consent OR recipient-activated consent
- Recipient-activated consent means: the email includes a clear opt-out, and the recipient can unsubscribe anytime

**PolicyCheck outreach strategy:**
- Emails to real estate agencies, chemists, lawyers = B2B cold outreach
- Requires clear, easy opt-out in EVERY email
- Implies implied consent can be established AFTER first email IF they engage

**Implementation:**

Include at the bottom of every email:

```
[Company name] sends these emails because your business may benefit from
Australian Privacy Act compliance preparation. If you prefer not to receive
further emails, you can unsubscribe here: [UNSUBSCRIBE_LINK]

To manage your preferences, visit: [PREFERENCE_CENTER_LINK]
```

**Why:** This establishes good faith and compliance. Even cold B2B outreach is legal IF recipients can easily opt out.

---

### 3. SUBJECT LINE COMPLIANCE

**Spam Act Section 19: Subject lines must not be misleading or deceptive.**

**PolicyCheck compliance:**
- Subject lines must be truthful about email content
- Subject lines must not trick recipients into opening

**Compliant:**
- "We found a gap in [Agency Name]'s privacy policy"
- "Your consent language is missing something (fixable in 30 secs)"
- "Real estate + Privacy Act: A$5,000+ per breach from July 1"

**Non-compliant (do NOT use):**
- "URGENT: Your account is at risk" (misleading, suggests account compromise)
- "ACTION REQUIRED: Click here immediately" (misleading urgency, suggests legal demand)
- "Re: Your inquiry" (deceptive—suggests previous conversation that didn't happen)

**Why:** Deceptive subject lines trigger spam folder flagging and may violate Spam Act Section 19.

---

### 4. PRICING & PROMOTION COMPLIANCE

**Spam Act Section 18: Commercial electronic messages (emails selling something) must:**
- Clearly identify the commercial nature of the message
- Include information about any goods/services being promoted
- Include pricing (if applicable)

**PolicyCheck implementation:**

In Email 1:
- "I've fixed that one gap as proof of concept. You can see your score and the corrected clause here: [TEASER_REPORT_LINK]"
- No pricing mentioned (first email is informational, not promotional)

In Email 2:
- "Your full report analyses all 13 APPs and tells you which gaps matter most. It's A$149 to unlock."
- Pricing is clear and upfront

In Email 3:
- "Some are adding the A$499 policy draft option"
- Pricing is clear and upfront

**Why:** Transparency about commercial nature and pricing avoids spam folder and maintains trust.

---

### 5. RECORD KEEPING REQUIREMENTS (Spam Act Section 20)

**PolicyCheck must keep records of:**
- Every email sent (date, time, recipient)
- Subject line
- Sender identification
- Unsubscribe requests and when they were processed
- Evidence of compliance with Spam Act

**Implementation:**
- Artemis platform logs all outreach automatically
- Unsubscribe requests must be processed within 5 business days
- Keep records for 5+ years (safer than 12 months, given Privacy Act alignment)

**Why:** Regulators (ACMA—Australian Communications and Media Authority) can audit records. Poor record-keeping = penalties even if emails were otherwise compliant.

---

### 6. HEADER COMPLIANCE

**Every email header must include:**
- Valid "From:" field with sender identification
- Valid "Reply-To:" field (should match From: or be business contact)
- Valid "Return-Path:" (should be business domain, not Gmail/Outlook personal accounts)

**Implementation:**
- Use PolicyCheck AU domain for all outreach (not personal email accounts)
- Artemis handles this automatically

**Why:** Invalid headers are spam indicators and reduce deliverability.

---

### 7. CONSENT ELEVATION (IMPLIED TO EXPRESS)

**PolicyCheck consent pathway:**

**Email 1 (Day 0):**
- "Implied consent" to contact (B2B, legitimate business interest)
- Includes clear unsubscribe
- No explicit consent required yet

**Email 2 (Day 4):**
- Still "implied consent" (follow-up to Email 1 engagement interest)
- Include unsubscribe again
- Recipient may have clicked Email 1 link (establishing engagement)

**Email 3 (Day 10):**
- If recipient engaged with Email 1 or 2: "express consent" has been established
- If recipient did NOT engage: this is final email before marking as uninterested
- Include unsubscribe prominently

**If recipient unsubscribes:**
- Remove from ALL future outreach immediately (not just this campaign)
- Do not re-add without explicit permission
- Keep unsubscribe record for 5+ years

---

### 8. SPECIAL COMPLIANCE REQUIREMENTS FOR AUSTRALIA

**Spam Act is administered by ACMA (Australian Communications and Media Authority)**

**Current enforcement priorities:**
- Misleading subject lines
- Deceptive commercial identification
- Ignored unsubscribe requests
- Spoofed sender information

**PolicyCheck risk assessment:**
- Low risk if all above requirements are met
- Medium risk if subject lines are too aggressive or deceptive
- High risk if unsubscribe requests are ignored

**ACMA penalties:**
- Civil penalties: up to A$1.1 million per company
- Criminal penalties: up to A$555,000 or 5 years imprisonment (egregious cases)

For PolicyCheck's volume and messaging (truthful, permission-based, easy opt-out), ACMA enforcement risk is minimal if compliance checklist is followed.

---

### 9. EMAIL CONTENT COMPLIANCE: REAL ESTATE EXAMPLE

**Email 1 compliance audit:**

```
SENDER IDENTIFICATION: ✓
"Best, [Sender Name], PolicyCheck AU, [Phone], [Address]"

SUBJECT LINE: ✓
"We found a gap in [Agency Name]'s privacy policy"
(Truthful, not misleading, accurately describes content)

COMMERCIAL IDENTIFICATION: ✓
Email is informational (not promotional). No Spam Act Section 18 trigger yet.
Unsubscribe included.

BODY: ✓
- Addresses recipient (real estate agency) ✓
- Provides genuine value (one fixed gap as proof) ✓
- No false claims or deceptive language ✓
- Includes teaser report link ✓
- Deadline is real (July 1 is accurate) ✓

UNSUBSCRIBE: ✓
Clear opt-out mechanism in footer

HEADERS: ✓
(Handled by Artemis platform)

COMPLIANCE RATING: COMPLIANT
```

**Email 2 compliance audit:**

```
SENDER IDENTIFICATION: ✓
Same as Email 1

SUBJECT LINE: ✓
"What happens when the Privacy Commissioner finds that gap"
(Truthful, references real process)

COMMERCIAL IDENTIFICATION: ✓
"Your full report analyses all 13 APPs. It's A$149 to unlock."
(Clear pricing and promotion)

BODY: ✓
- Addresses follow-up ✓
- Emphasises deadline (July 1) ✓
- Quantifies penalties (A$5,000 per breach) ✓
- Positions A$149 report as insurance ✓
- No false claims ✓

UNSUBSCRIBE: ✓
Clear opt-out mechanism in footer

COMPLIANCE RATING: COMPLIANT
```

---

### 10. COMMON COMPLIANCE PITFALLS (DO NOT DO)

**1. Using personal email for outreach**
- PROBLEM: Violates Spam Act Section 17 (sender identification)
- SOLUTION: Use PolicyCheck AU domain

**2. Misleading subject lines**
- PROBLEM: "URGENT: Your business is at risk" (deceptive)
- SOLUTION: Use truthful subject lines (see subject-lines.md)

**3. Ignoring unsubscribe requests**
- PROBLEM: Violates Spam Act Section 16 (opt-out rights)
- SOLUTION: Process all unsubscribes within 5 business days

**4. No sender address or phone**
- PROBLEM: Violates Spam Act Section 17 (sender identification)
- SOLUTION: Always include address and phone in footer

**5. Impersonating someone else**
- PROBLEM: Violates Spam Act Section 17 (sender must be truthfully identified)
- SOLUTION: Use real sender name and contact details

**6. Hidden unsubscribe link**
- PROBLEM: ACMA flags suspicious/hard-to-find unsubscribe
- SOLUTION: Make unsubscribe link visible and prominent

**7. Sending to purchased lists without verification**
- PROBLEM: Lists may contain people who never consented to contact
- SOLUTION: Use verified B2B lists (Real Estate Institute, Law Society directories, etc.)

**8. No record-keeping**
- PROBLEM: Can't prove compliance if audited
- SOLUTION: Use Artemis to log all outreach

---

## ARTEMIS CONFIGURATION CHECKLIST

**Before running PolicyCheck campaigns on Artemis, verify:**

- [ ] All email templates include sender name, phone, address
- [ ] All subject lines are truthful and not misleading
- [ ] All emails include unsubscribe link
- [ ] Unsubscribe link goes to working preference center
- [ ] Artemis is configured to remove unsubscribes within 5 business days
- [ ] Email headers use PolicyCheck AU domain (not personal emails)
- [ ] No imported lists are used without verification (use only Real Estate Institute, PBS, Law Society, etc.)
- [ ] Campaign tracking is enabled (for record-keeping)
- [ ] Reply-to email is monitored and responded to
- [ ] Bounce management is active (invalid addresses are flagged)

---

## IF CONTACTED BY ACMA

**ACMA (Australian Communications and Media Authority) may contact PolicyCheck if:**
- Someone files a complaint about spam
- ACMA runs a spot-check on outreach
- Unsubscribe requests are ignored

**Response protocol:**

1. Do not ignore the letter (this is a legal inquiry)
2. Compile all records:
   - Email templates sent
   - Unsubscribe requests and responses
   - Campaign dates and recipient counts
   - Subject lines used
   - Any feedback received

3. Respond within 30 days with:
   - Explanation of compliance approach
   - Evidence of Spam Act compliance
   - Any corrective actions taken

4. If PolicyCheck is fully compliant (all checklist items met), ACMA will likely close the inquiry

**Note:** For PolicyCheck's volume and messaging, ACMA enforcement risk is low if this checklist is followed.

---

## FINAL SIGN-OFF

**Before launching PolicyCheck campaigns:**

Confirm:
- "All emails include sender name, phone, address: ✓"
- "All subject lines are truthful: ✓"
- "All emails include unsubscribe: ✓"
- "Artemis record-keeping is active: ✓"
- "List sources are verified (Real Estate Institute, etc.): ✓"

**If all checkboxes are ticked, campaigns are SPAM ACT COMPLIANT.**

