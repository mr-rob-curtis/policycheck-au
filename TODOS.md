# TODOS

## Deferred work tracked for future sprints.

### Dashboard backend
- **What:** Wire up public/dashboard.html with scan history data from Redis
- **Why:** Dashboard UI exists (200 lines) but has no backend. Currently a dead page.
- **Depends on:** Redis/Upstash setup (Stripe sprint), user auth
- **Context:** Dashboard was built as part of the Flask server prototype. The HTML shell is there (scan history table, stats grid, countdown timer) but needs an API endpoint to serve scan data. When Redis is added for paid report storage, the same scan data can feed the dashboard. Consider whether dashboard needs auth or is tied to a session/email.
- **Added:** 2026-04-01 (eng review)

### Scoring calibration tests
- **What:** Test suite specifically for compliance scoring accuracy and edge cases
- **Why:** The rule-based engine gives partial credit for keyword matches. A policy mentioning "personal information" once could get partial credit across multiple APPs, inflating scores. Inflated scores reduce the urgency that drives lead conversion.
- **Depends on:** WS3 test infrastructure (pytest + CI)
- **Context:** Key functions to test: `_apply_scoring_floor`, `_get_expanded_phrases_for_app`, `_calculate_coverage_percentage`, `_detect_topic_presence`. Test with real AU privacy policies (CBA, Westpac, small business examples) and verify scores match manual assessment. Consider creating a "golden set" of 10 policies with manually verified scores as regression baseline.
- **Added:** 2026-04-01 (eng review, outside voice finding)

### SSL certificate warning in scan results
- **What:** When a site has SSL issues, note it in the scan result
- **Why:** SSL problems are a signal of poor security hygiene, relevant to privacy compliance
- **Depends on:** WS2 security hardening (verify=False fallback removal)
- **Context:** After removing the verify=False fallback, SSL errors will cause fetch failures. The scan result should indicate "SSL certificate error" so the user understands why certain pages couldn't be scanned, rather than just "policy not found."
- **Added:** 2026-04-01 (CEO review)

### Rate limiting infrastructure
- **What:** IP-based rate limiting for the scan API
- **Why:** Without rate limiting, the scanner can be used as an HTTP proxy/amplifier
- **Depends on:** Redis/Upstash or Vercel KV setup
- **Context:** Accepted risk at current traffic levels (near zero). When adding Stripe/Redis, add rate limiting (10 scans/min/IP). In-memory won't work on Vercel (stateless functions). Vercel Pro plan has built-in WAF rate limiting as an alternative.
- **Added:** 2026-04-01 (eng review, outside voice finding)
