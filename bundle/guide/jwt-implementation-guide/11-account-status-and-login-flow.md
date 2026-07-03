---
type: Section
title: 11. Account Status and Login Flow
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

| AccountStatus | Credentials Checked | Outcome | Tokens Issued | Cookie Action |
|---------------|--------------------|---------|-----------|-----------------------|
| ACTIVE | Yes, valid | Success | Both | Set all three cookies |
| ACTIVE | Yes, invalid | Failure | None | No change |
| SUSPENDED | No | Failure | None | Clear session + refresh |
| CLOSED | No | Failure | None | Clear session + refresh (permanent) |
| Not found | No | Failure (generic) | None | No change |
| Rate limited | No | 429 Too Many Requests | None | No change |

### Generic Error Message Rule

Always return the same generic message for unauthenticated failures:

- Unknown email → "Invalid email or password" (do not confirm whether the email exists)
- Wrong password → "Invalid email or password" (same message; prevents timing-based account enumeration)
- SUSPENDED/CLOSED → Specific message, but **only after** valid credentials are confirmed. The user already knows their account exists; a specific message helps them understand next steps. An attacker who cannot authenticate cannot reach this message path.

### Session Revocation on Status Change

`AccountSuspended` domain event (already modeled in the sample) → event listener calls `refreshTokenRepository.revokeAllForUser(userId, "ACCOUNT_SUSPENDED")`.

Access tokens expire naturally within 15 minutes — this is the accepted tradeoff for stateless design. For immediate revocation, an optional Redis denylist on the `jti` claim can be added (see Section 16, Optional Enhancements).

---
