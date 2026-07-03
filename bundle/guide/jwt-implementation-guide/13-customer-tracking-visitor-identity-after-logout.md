---
type: Section
title: "13. Customer Tracking: Visitor Identity After Logout"
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

### Two Strategies

| Strategy | On Logout | Next Visit | Cart Survives? |
|----------|-----------|------------|----------------|
| Preserve visitor identity | Clear session + refresh cookies; keep visitor cookie | Same `UserId` | Yes |
| Reset visitor identity | Clear all three cookies | New `UserId` | No |

### Recommendation: Preserve Visitor Identity

Cart loss on logout is a significant UX friction point in e-commerce. The visitor token contains only a random UUID — no PII — so the privacy risk is minimal.

**Implementation:** Logout clears `shop-session` and `shop-refresh` only. `shop-identity` is left intact.

```
logout:
  clear: shop-session (MaxAge=0), shop-refresh (MaxAge=0)
  keep:  shop-identity
```

`IdentitySession.clearIdentity()` should be renamed or supplemented with `clearAuthenticatedSession()` to make this distinction explicit.

### GDPR / Right to Erasure

If a "right to be forgotten" request is received, purge the `UserId` from:
- `refresh_tokens` table (`DELETE WHERE user_id = ?`)
- Shopping Cart bounded context
- Checkout history
- Account bounded context
- `login_attempts` table (`DELETE WHERE email = ?`)
- Any analytics or event store that references the `UserId`

The visitor cookie on the client device cannot be actively deleted, but the UUID it contains will no longer resolve to any stored data.

---
