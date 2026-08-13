---
type: Section
title: 3. Token Types and Their Roles
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

| Token | Type | Signed | Stored | Lifetime | Revocable | Purpose |
|-------|------|--------|--------|----------|-----------|---------|
| Visitor token | JWT (anonymous) | ES256 | Cookie only | 30 days | No | Cart persistence for anonymous shoppers |
| Access token | JWT (registered) | ES256 | Cookie only | 15 min | No | Authenticate requests to all services |
| Refresh token | Opaque random | N/A | PostgreSQL | 30 days sliding | Yes (delete row) | Issue new access tokens; tracks login sessions |

### Visitor Token (`shop-identity`)

Purpose: persists an anonymous `UserId` so the shopping cart survives browser restarts without requiring an account. Preserved through login and through session expiry; rotated on explicit logout (see Section 13).

Contains: `sub` (random UUID), `iat`, `exp`. No PII.

### Access Token (`shop-session`)

Purpose: proves identity to every service on every request. Validated locally by each service using the JWKS public key — no auth service round-trip.

Contains: `sub`, `email`, `given_name`, `family_name`, `cid`, `roles`, `jti`, `aud`, `iat`, `exp` — see Section 6 for full claims reference.

### Refresh Token (`shop-refresh`)

Purpose: issues new access tokens after the 15-minute window expires; tracks active login sessions per device.

Raw value: 256-bit `SecureRandom` bytes, Base64-encoded. Stored in PostgreSQL as SHA-256 hash only. The raw value lives only in memory and in the `HttpOnly` cookie.

### Authentication Levels

Real ecommerce platforms commonly operate with three authentication levels rather than a simple binary anonymous/authenticated split:

| Level | Token present | `loginTyp` claim | User identifier claim | Description |
|-------|--------------|------------------|-----------------------|-------------|
| Anonymous | Visitor token only | — | `sub` (visitor UUID) | No account; cart persists via visitor cookie |
| Soft login | Access token with `loginTyp: "SOFT"` | `"SOFT"` | `softLoginId` | Remembered device; no password re-entry; limited capabilities |
| Full login | Access token with `loginTyp: "FULL"` | `"FULL"` | `sub` (user UUID) | Password verified this session; full capabilities |

**Key structural differences between soft and full login tokens:**
- Soft login token: **no `sub` claim**; the effective user identifier is carried in `softLoginId`
- Full login token: has `sub` claim; `softLoginId` is absent

Services that require full authentication (e.g. order placement, payment) MUST reject tokens where `loginTyp == "SOFT"`. Services that accept soft login MUST read the user identity from `softLoginId` when `loginTyp == "SOFT"` and from `sub` when `loginTyp == "FULL"`.

**Capability matrix:**

| Capability | Anonymous | Soft Login | Full Login |
|------------|:---------:|:----------:|:----------:|
| Browse catalogue | Yes | Yes | Yes |
| Add to cart | Yes | Yes | Yes |
| View saved addresses | No | Yes | Yes |
| Initiate checkout | No | Yes (limited) | Yes |
| Place order / pay | No | No | Yes |
| Manage account settings | No | No | Yes |
| Access order history | No | Read-only | Full |

---
