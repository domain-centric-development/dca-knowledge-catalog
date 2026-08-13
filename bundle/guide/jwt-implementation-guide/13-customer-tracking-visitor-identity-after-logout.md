---
type: Section
title: "13. Customer Tracking: Visitor Identity After Logout"
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

### Expiry and logout are different events

The visitor identity answers "whose cart is this", not "is this person authenticated". Those two
questions have different lifetimes, which is why they sit in different cookies (§7):

| Event | User intent | `shop-session` | `shop-identity` |
|-------|-------------|----------------|-----------------|
| Access token expires | none — a timer fired | gone | **kept** |
| Explicit logout | "end my session here" | cleared | **rotated to a new UserId** |

Expiry must never cost the cart: nobody asked for anything, the clock simply ran out. Losing a cart
because a tab sat open over lunch is pure harm with no security benefit.

### On logout: rotate, do not delete

An explicit logout is a request to leave — typically on a shared device, where the next person must
not inherit the cart. Rotating the visitor identity satisfies that **without deleting anything**:

| Case | Outcome |
|------|---------|
| Shared device, next person | fresh `UserId` → empty cart |
| Own device, logs back in | cart returns from the **account**, via cart recovery on login |
| Privacy | nothing from the previous session is reachable from this browser |

The cart of a registered user is keyed on their account, not on the browser. A reference
implementation that recovers and merges the cart on login (e.g. `RecoverCartOnLoginUseCase`) makes
rotation free: what looks like "losing the cart" is only "losing the anonymous path to it".

> **This reverses earlier advice in this guide,** which recommended preserving the visitor identity
> through logout on cart-continuity grounds. That rationale does not survive account-based cart
> recovery: continuity is provided by the account, so preserving the identity buys nothing and keeps
> a shared-device risk.

### Tracking is a separate identifier — not this one

A stable visitor id is tempting for analytics, and that is exactly the trap. Three reasons to keep
the measurement identifier out of `shop-identity`:

1. **Consent.** A cart identifier is *strictly necessary* under ePrivacy/GDPR — no consent needed. An
   analytics identifier is not. Merging them makes the whole cookie consent-dependent, so **a visitor
   who declines analytics loses their cart** — a functional guarantee they are entitled to either way.
2. **Opposite lifecycles.** Analytics wants long, stable identifiers; the cart identity wants to
   rotate on logout for shared devices. One value cannot satisfy both.
3. **After login, analytics does not need it.** Events attach to the account; the anonymous id only
   matters before login, and the usual answer there is identity stitching at login time.

So "rotating on logout is safer but worse for tracking" is true only while one identifier does both
jobs. Separated, rotation costs exactly one thing: linking this browser's *future* anonymous sessions
to its past ones — which is what someone who deliberately logs out is asking you not to do.

```
shop-session   session         short    expiry is harmless
shop-refresh   renewal         long     path-scoped, rotating
shop-identity  cart identity   long     rotates only on explicit logout
[analytics]    measurement     own      consent-governed, owned by the analytics tool
```

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
