---
type: Section
title: 12. Refresh Token Rotation Flow
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

```
1. POST /auth/refresh  →  Browser sends Cookie: shop-refresh=<raw>
2. Compute SHA-256(raw) → token_hash; query refresh_tokens table
3. Not found / revoked / expires_at < NOW() → 401; clear all cookies; force re-login
4. absolute_expires_at < NOW() → 401; clear all cookies; force re-login
5. AccountStatus check → SUSPENDED or CLOSED → 401; revoke row; clear cookies
6. Generate new access token (JWT, 15 min, ES256, includes jti + aud)
7. Generate new refresh token (SecureRandom 256-bit, Base64-encoded)
8. Update DB row:
     token_hash         = SHA-256(newRawToken)
     last_rotated_at    = NOW()
     expires_at         = NOW() + 30 days     (sliding reset)
     -- absolute_expires_at is NOT updated --
9. Set cookies: shop-session (MaxAge=900) + shop-refresh (MaxAge=2592000, Path=/auth/refresh)
10. Return 200 OK  (no body needed; tokens are in cookies)
```

### Theft Detection (Rotation Reuse)

If a replaced (already-rotated) token hash is presented:
1. The old hash is not found (it was overwritten in step 8)
2. Revoke **all** tokens for this `user_id` (set `revoked=true`, `revoked_reason='SUSPICIOUS'`)
3. Log a `SUSPICIOUS_REUSE` security event
4. Return 401; clear all cookies on the client

The user is forced to re-login on all devices. This is the correct tradeoff — if a token was reused, either the legitimate session was stolen, or the legitimate client has a bug. Either way, revoking everything protects the account.

### Silent Refresh for Server-Side Rendered Pages

`JwtAuthenticationFilter` detects an expired access token (valid signature, `exp` in the past) and triggers a server-side call to the refresh logic before passing the request to controllers. The user never sees a redirect or 401 during normal browsing.

### Token Expiry UX Contract

If the access token is expired **and** no valid refresh cookie is present (cookie missing, revoked, or past absolute expiry), the request MUST be treated as anonymous — not as an error. The user sees the experience an anonymous visitor would see, not a 401 error page or an error modal.

Implementation: catch `ExpiredJwtException` in the authentication filter, log at DEBUG level (this is expected behaviour, not a fault), and proceed with a null/anonymous principal. Reserve WARN-level logging and 401 responses for unexpected validation failures such as an invalid signature or a malformed token.

The general principle is **enrichment, not gating**: the authentication filter/interceptor never blocks a request. It either attaches an authenticated principal or attaches nothing — the request always proceeds. Authorization for protected actions is enforced per action in the application layer, not at the token-extraction boundary.

### Clock Skew

For self-issued tokens (tokens your own auth service signs and all other services verify), set clock skew tolerance to **0 seconds**. With a 15-minute access token lifetime, even 60 seconds of skew tolerance extends the effective blast radius of a stolen token. Enforce NTP synchronisation across all services instead of relying on token parser tolerance.

```java
// JJWT example
Jwts.parser()
    .clockSkewSeconds(0)  // strict — no tolerance for self-issued tokens
    .verifyWith(publicKey)
    .build()
    .parseSignedClaims(token);
```

---
