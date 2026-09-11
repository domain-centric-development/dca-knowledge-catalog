---
type: Pitfall
title: CSRF-exempt API that accepts cookie authentication
tags: [pitfall, adapter, rest, security, infrastructure]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/jwt-implementation-guide/8-csrf-protection.md, /guide/rules.md]
---

The security configuration ignores CSRF for `/api/**` ("APIs are token-based") while the authentication filter still reads the session cookie for every path — first the cookie, then the `Authorization` header as fallback. Often accompanied by `/api/auth/login` *setting* that cookie.

## Why it is wrong

- The exemption is only sound if a browser cannot authenticate a request to the API by attaching cookies. Here it can: a cross-site form post to `/api/carts/{id}/checkout` arrives with the victim's session cookie and is never challenged. It is the worst of both worlds — no token, but cookie auth.
- A login endpoint that sets a session cookie without CSRF protection is a login-CSRF vector: the attacker logs the victim's browser into an account the attacker controls.
- Global `csrf.disable()` "because we use JWT" is the same mistake at larger scale; `SameSite=Lax` is defence in depth, not a strategy — `Lax` still sends the cookie on top-level navigations.

## What forbids it

- [CSRF protection](/guide/jwt-implementation-guide/8-csrf-protection.md) — an API may be exempt only if it neither reads nor issues cookies; browser sessions are established through CSRF-protected web forms.
- [Layer rules](/guide/rules.md) — input adapter rules: every state-changing browser form carries a CSRF token.

## Do instead

Make the token-only paths truly token-only in the authentication filter: on `/api/**` read the identity from `Authorization: Bearer` alone and never write a cookie; the API login returns the token in the body, logout is a stateless acknowledgement. Everything browser-facing keeps the CSRF filter with a cookie-backed token repository (stateless) and a hidden `_csrf` field in every writing form — the same mechanism as ASP.NET Core's antiforgery token. One place decides what "token-only endpoint" means, and the CSRF exemption list mirrors it.

- Related pitfall: [State-changing GET endpoint](/pitfall/state-changing-get-endpoint.md)

## Anchors

- Guide: [CSRF protection](/guide/jwt-implementation-guide/8-csrf-protection.md) · [Layer rules](/guide/rules.md)
