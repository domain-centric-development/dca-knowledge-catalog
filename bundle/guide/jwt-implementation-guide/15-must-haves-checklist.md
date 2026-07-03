---
type: Section
title: 15. Must-Haves Checklist
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

```
[ ] Switch from HS256 to ES256 (asymmetric signing)
[ ] Publish JWKS endpoint (GET /.well-known/jwks.json) for public key distribution
[ ] Add kid claim to JWT header; support key rotation
[ ] Split into three token types: visitor JWT, access JWT, opaque refresh token
[ ] Store refresh tokens as SHA-256 hash in PostgreSQL; never store raw value
[ ] Implement refresh token rotation with reuse/theft detection
[ ] Absolute expiry on refresh tokens (90-day hard limit; never updated on rotation)
[ ] Reduce access token lifetime to 15 minutes
[ ] Set Secure=true on all cookies in production (env-driven, not hardcoded false)
[ ] SameSite=Strict for access + refresh cookies; SameSite=Lax for visitor cookie
[ ] Path=/auth/refresh on the refresh token cookie
[ ] login_attempts table with per-email + per-IP rate limiting
[ ] Configurable lockout thresholds via application.yml
[ ] Revoke all refresh tokens on AccountSuspended and AccountClosed domain events
[ ] On logout: clear session + refresh cookies; preserve visitor cookie
[ ] Generic error messages for all unauthenticated failures (no account enumeration)
[ ] jti claim (UUID) in every access token
[ ] aud claim per service or service group in every access token
[ ] Never log raw token values; never return refresh token in response body
[ ] Private key loaded from vault/secret manager, never from application.yml
[ ] clockSkewSeconds = 0 for self-issued token validation
[ ] Expired access token + no valid refresh cookie → treat as anonymous, not 401
```

---
