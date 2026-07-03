---
type: Section
title: 8. CSRF Protection
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

### Why Cookie Transport Requires CSRF Mitigation

When authentication credentials are stored in cookies, browsers automatically attach them to every request — including cross-origin requests initiated by a malicious page. This enables Cross-Site Request Forgery (CSRF): an attacker tricks an authenticated user's browser into making a state-changing request to your service without the user's intent.

### Primary Defence: `SameSite=Strict`

Section 7 specifies `SameSite=Strict` for both the access token (`shop-session`) and refresh token (`shop-refresh`) cookies. With `Strict`, the browser never sends these cookies on any cross-site request — not on top-level navigations, not on form submissions, not on fetch/XHR calls from third-party origins.

`SameSite=Strict` is sufficient CSRF protection when:
- All state-changing endpoints are protected by the `shop-session` cookie
- The session and refresh cookies consistently use `SameSite=Strict`
- The application does not rely on cross-site navigations that must carry authentication (e.g. OAuth redirect flows where cookies need to be sent on the redirect)

### Supplementary Defence: Double Submit Cookie (for `SameSite=Lax` cookies)

**The visitor cookie (`shop-identity`) uses `SameSite=Lax`.** Lax allows the cookie to be sent on top-level cross-site navigations (e.g. clicking a link from another site). If the visitor cookie is ever used to authorize a state-changing operation, a CSRF token is required.

The Double Submit Cookie pattern provides CSRF protection without server-side token state:

1. Server sets a random CSRF token in a **separate, non-HttpOnly cookie** (so JavaScript can read it)
2. Client-side JavaScript reads this cookie and echoes its value as a custom request header (e.g. `X-CSRF-Token`)
3. Server validates that the header value matches the cookie value

A cross-site attacker cannot read the cookie (same-origin policy on JS), so cannot forge the matching header.

```java
// Setting the CSRF cookie (not HttpOnly — must be readable by JavaScript)
ResponseCookie.from("csrf-token", UUID.randomUUID().toString())
    .sameSite("Lax")
    .secure(secure)
    .path("/")
    .build();

// Validating in the filter
String cookieValue = request.getCookieValue("csrf-token");
String headerValue = request.getHeader("X-CSRF-Token");
if (cookieValue == null || !cookieValue.equals(headerValue)) {
    throw new CsrfException("CSRF token mismatch");
}
```

Spring Security provides `CookieCsrfTokenRepository` for cookie-based CSRF token management, which handles token generation, storage, and validation automatically.

### Recommendation Summary

| Cookie | SameSite | CSRF mitigation needed? |
|--------|----------|-------------------------|
| `shop-session` (access token) | `Strict` | No — `SameSite=Strict` is sufficient |
| `shop-refresh` (refresh token) | `Strict` | No — `SameSite=Strict` is sufficient |
| `shop-identity` (visitor token) | `Lax` | Yes if used for state changes — use Double Submit Cookie |

---
