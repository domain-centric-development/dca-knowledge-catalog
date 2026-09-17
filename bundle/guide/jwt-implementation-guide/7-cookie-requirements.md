---
type: Section
title: 7. Cookie Requirements
chapter: JWT Implementation Guide
source: guide
resource: dca-guide/topics/jwt-implementation-guide.md
tags: [guide, section]
---

| Attribute | Access Token (`shop-session`) | Refresh Token (`shop-refresh`) | Visitor Token (`shop-identity`) | CSRF Token |
|-----------|------------------------------|-------------------------------|--------------------------------|------------|
| `HttpOnly` | `true` | `true` | `true` | `false` — the form script reads it |
| `Secure` | `true` (env-driven) | `true` (env-driven) | `true` (env-driven) | `true` (env-driven) |
| `SameSite` | `Strict` | `Strict` | `Lax` | follows the cookie it protects |
| `Path` | `/` | `/auth/refresh` | `/` | `/` |
| `MaxAge` | 900 s | 2 592 000 s (30 days) | 2 592 000 s (30 days) | session |

**The CSRF token cookie belongs in this table.** It is easy to leave out, because no framework asks
you to configure it: Spring Security and ASP.NET Core both write it themselves, with a default that
is *not* the one you chose for your own cookies — no `SameSite` attribute at all in one case,
`Strict` in the other. That difference only surfaces where the policies diverge, and then it looks
like a broken form rather than a cookie problem: the identity cookie arrives, the token cookie does
not, and every state-changing request fails as a *missing* token rather than a refused one.

> **Rule:** cookies that have to survive the same journey carry the same policy. A request that
> needs both an identity and a form token is refused unless both cookies reach the server. Set the
> CSRF cookie's `SameSite` and `Secure` from the same configuration as the identity cookie instead
> of accepting the framework's default.

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

**Status in `dca-ecommerce-sample-java`:**

| | |
|---|---|
| `shop-identity` / `shop-session` split | ✅ done |
| Session expiry keeps the visitor identity | ✅ done |
| Logout rotates the identity, clears the session | ✅ done |
| `Secure` from configuration instead of hardcoded `false` | ✅ done (`app.security.jwt.secure-cookies`) |
| `SameSite` on every cookie the subsystem writes, the CSRF cookie included | ✅ done (`Lax`; the token cookie follows the identity cookie) |
| Path-scoped `shop-refresh` and the renewal flow | ❌ **deferred** — no refresh token exists |

The deferral is deliberate, and it has a price worth naming: without a refresh token there is no
revocation and no theft detection, so **the session cookie's lifetime is the blast radius of a
stolen token**.
A renewal flow needs a persistent token store, rotation with reuse detection, and an endpoint to
scope the cookie to — larger than everything above combined.

---
