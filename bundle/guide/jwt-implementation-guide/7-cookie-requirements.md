---
type: Section
title: 7. Cookie Requirements
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

| Attribute | Access Token (`shop-session`) | Refresh Token (`shop-refresh`) | Visitor Token (`shop-identity`) |
|-----------|------------------------------|-------------------------------|--------------------------------|
| `HttpOnly` | `true` | `true` | `true` |
| `Secure` | `true` (env-driven) | `true` (env-driven) | `true` (env-driven) |
| `SameSite` | `Strict` | `Strict` | `Lax` |
| `Path` | `/` | `/auth/refresh` | `/` |
| `MaxAge` | 900 s | 2 592 000 s (30 days) | 2 592 000 s (30 days) |

**Three-cookie design:**
- `shop-identity` — visitor JWT (existing; survives session expiry, rotated on explicit logout — see §13)
- `shop-session` — access token JWT (replaces current all-in-one cookie)
- `shop-refresh` — opaque refresh token (**path-scoped to `/auth/refresh`**)

Path-scoping `shop-refresh` to `/auth/refresh` means the browser only sends it to the refresh endpoint. The cookie is never visible to product, cart, or checkout services — even if those services share the same origin.

**`Secure` flag must be environment-driven, never hardcoded:**

```java
boolean secure = environment.acceptsProfiles(Profiles.of("prod", "staging"));
ResponseCookie.from("shop-session", token)
    .httpOnly(true)
    .secure(secure)
    .sameSite("Strict")
    .path("/")
    .maxAge(Duration.ofMinutes(15))
    .build();
```

**Status in `ai-architecture-sample`:**

| | |
|---|---|
| `shop-identity` / `shop-session` split | ✅ done |
| Session expiry keeps the visitor identity | ✅ done |
| Logout rotates the identity, clears the session | ✅ done |
| `Secure` from configuration instead of hardcoded `false` | ✅ done (`app.security.jwt.secure-cookies`) |
| `SameSite` on every cookie the subsystem writes | ✅ done (`Lax`) |
| Path-scoped `shop-refresh` and the renewal flow | ❌ **deferred** — no refresh token exists |

The deferral is deliberate, and it has a price worth naming: without a refresh token there is no
revocation and no theft detection, so **the session cookie's lifetime is the blast radius of a
stolen token**.
A renewal flow needs a persistent token store, rotation with reuse detection, and an endpoint to
scope the cookie to — larger than everything above combined.

---
