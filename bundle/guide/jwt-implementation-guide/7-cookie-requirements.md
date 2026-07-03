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
- `shop-identity` — visitor JWT (existing; preserved through login/logout)
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

**Current gaps in `ai-architecture-sample`:**
- `Secure=false` hardcoded in `JwtIdentitySession` and `JwtAuthenticationFilter`
- No `SameSite` attribute on authenticated cookies
- No path-scoped refresh cookie (no refresh token exists yet)
- `clearIdentity()` clears only the visitor cookie; logout should also clear `shop-session` and `shop-refresh`

---
