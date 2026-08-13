---
type: Section
title: 6. JWT Claims Design
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

### Why OIDC Standard Claim Names Matter

Two standards define JWT claim names:
- **RFC 7519** — The JWT spec itself: `iss`, `sub`, `aud`, `exp`, `nbf`, `iat`, `jti`
- **OpenID Connect Core 1.0** — Profile claims: `given_name`, `family_name`, `email`, `email_verified`, `name`

Using these names instead of ad-hoc equivalents (`userId`, `firstName`, `customerId`) has concrete consequences:

| Benefit | Explanation |
|---------|-------------|
| **Framework auto-mapping** | Spring Security's `JwtAuthenticationConverter` maps `sub`, `given_name`, `email` to `Authentication` attributes automatically; custom names require explicit `claimSetConverter` configuration |
| **Library constants** | Nimbus JOSE+JWT, JJWT, and auth0-java-jwt ship with `JWTClaimNames` / `RegisteredClaimNames` constants — no string literals scattered across services |
| **IdP compatibility** | If you later add Keycloak, Auth0, Cognito, or Google as an identity provider, they all emit the same OIDC claim names — no mapping layer needed in each downstream service |
| **API gateway policies** | Kong, AWS API Gateway, and Nginx JWT modules extract `sub`, `email`, `given_name` without custom configuration |
| **Tooling** | `jwt.io`, security scanners, and log-analysis tools recognise OIDC claims and render them meaningfully |
| **Inter-team consistency** | `given_name` is unambiguous; `firstName` vs `first_name` vs `fname` creates divergence across service teams over time |

### Standard Claim Reference

**RFC 7519 registered claims — always include in access tokens:**

| Claim | Type | Description |
|-------|------|-------------|
| `iss` | String | Issuer — auth service base URL |
| `sub` | String | Subject — stable, immutable user identifier (`UserId`); absent in soft login tokens |
| `aud` | String[] | Audience — which services may accept this token |
| `exp` | NumericDate | Expiration — Unix timestamp |
| `iat` | NumericDate | Issued at — Unix timestamp |
| `jti` | String | JWT ID — UUID, unique per token (enables denylist lookups) |

**OIDC Core profile claims — embed selectively (see below):**

| Claim | Type | Example |
|-------|------|---------|
| `email` | String | `"jane@example.com"` |
| `email_verified` | Boolean | `true` |
| `given_name` | String | `"Jane"` |
| `family_name` | String | `"Doe"` |
| `name` | String | `"Jane Doe"` — only if services need the pre-computed full name |
| `preferred_username` | String | Handle or username if distinct from email |
| `locale` | String | `"en-GB"` |

**Application-specific custom claims — use short, lowercase names:**

| Claim | Type | Description |
|-------|------|-------------|
| `cid` | String | Customer ID — the business-facing identifier used on orders and invoices |
| `roles` | String[] | Coarse-grained roles: `CUSTOMER`, `BACKOFFICE_AGENT` |
| `loginTyp` | String | Authentication level: `"FULL"` (password verified this session) or `"SOFT"` (remembered device, no password re-entry) |
| `softLoginId` | String | Effective user identifier in soft login tokens — present only when `loginTyp == "SOFT"` |
| `tenant` | String | Tenant/country scope (e.g. `"DE"`, `"AT"`, `"CH"`). Required for multi-country platforms. Verifying services MUST reject tokens whose `tenant` value does not match the service's configured scope |

**`cid` vs `sub`:** `sub` is the immutable technical identity (a UUID that never changes, even if the email changes). `cid` is the customer-facing identifier that may appear on order confirmations and support tickets. In the `ai-architecture-sample`, `UserId` currently serves both roles; a production system may issue them separately.

**`tenant` / multi-country:** In platforms serving multiple countries or storefronts, the `tenant` claim (sometimes called `mandant`) prevents a token issued for one country's shop from being accepted by another country's services. Validation logic: `if (!token.tenant().equals(serviceConfig.tenant())) throw new InvalidTenantException()`.

### What to Embed

**Embed claims that are:** stable (rarely changes), non-sensitive (safe if logged or observed), and read-heavy (most services need it without a DB call).

| Claim | Embed? | Reason |
|-------|--------|--------|
| `sub` (userId) | Always (full login) | Required for all authorization decisions |
| `email` | Yes | Personalization, notification routing, support lookup |
| `given_name` | Yes | "Hello, Jane" — needed by most UI-facing services |
| `family_name` | Yes | Full name display, shipping label generation |
| `cid` (customerId) | Yes | Checkout, order management, account context |
| `roles` | Yes | Coarse-grained gatekeeping without a DB call |
| `email_verified` | Yes, if needed | Gate features (e.g., checkout) on verified email |
| `loginTyp` | Yes | Encoding the authentication level in the token |
| `tenant` | Yes, if multi-country | Required for tenant-scoped validation |
| Shipping address | No | Changes frequently; fetch from Account service on demand |
| Payment methods | No | Sensitive; never embed in a token |
| Loyalty points / balance | No | Changes too frequently; always stale |
| Fine-grained permissions | No | Services own their own authorization logic |

### Reference Access Token Payload

```json
{
  "iss": "https://auth.shop.example.com",
  "sub": "usr_01HXYZ123",
  "aud": ["shop-api"],
  "exp": 1704068100,
  "iat": 1704067200,
  "jti": "tok_01HABC456",
  "email": "jane@example.com",
  "email_verified": true,
  "given_name": "Jane",
  "family_name": "Doe",
  "cid": "cust_01HDEF789",
  "roles": ["CUSTOMER"],
  "loginTyp": "FULL",
  "tenant": "DE"
}
```

Total payload: ~350 bytes. With an ES256 signature (64 bytes) and a compact header, the full encoded token is well under 1 KB and fits comfortably in a cookie.

### Claim Freshness

Claims embedded in the token are valid for its lifetime (15 min). For most profile data this is the accepted tradeoff.

| Event | Staleness Risk | Required Action |
|-------|----------------|-----------------|
| Name change | Low — max 15 min stale | None; next rotation picks up the new value |
| Email change | Medium — affects notifications | Revoke all refresh tokens immediately; next login issues fresh claims |
| Role change (admin granted/revoked) | High — authorization impact | Revoke all refresh tokens; next rotation issues fresh claims |
| Account suspended | Critical | Revoke all refresh tokens; access tokens expire within 15 min (accepted tradeoff for stateless validation) |

Revocation on email/role change: the relevant use case raises a domain event → event listener calls `refreshTokenRepository.revokeAllForUser(userId, reason)`. The access token remains valid for up to 15 minutes — this is the cost of stateless validation. For zero-tolerance scenarios, add the `jti` denylist (see Section 16, Optional Enhancements).

---

### 6.4 Encrypting a Claim (defense in depth)

A signed JWT is integrity-protected but **not confidential**: anyone holding it can base64-decode
the payload. Where a claim carries an identifier that should not be readable by whoever obtains the
token, encrypt the value at application level and carry the ciphertext as a custom claim:

- **Cipher:** AES-256-GCM with a random 12-byte IV and a 128-bit auth tag
- **AAD:** the key id — this binds the ciphertext to the key that produced it, so tampering with the
  key prefix fails the GCM tag instead of silently decrypting under another key
- **Wire format:** `keyId:base64(IV ‖ ciphertext ‖ tag)`, so the reader learns which key to use
  without a lookup table on the wire
- **Rotation:** keep a key map (id → key); encrypt with the active key, decrypt with whichever key
  the prefix names. This is what makes rotation possible without a flag day
- **Failure mode:** a decryption failure degrades to an *absent value*, never an exception — a token
  encrypted under a retired key must not take down the request

Two **independent** key systems then coexist: the EC key pair signs the token, an AES key encrypts
the claim. Different algorithms, different rotation lifecycles, different secrets — the claim is
protected twice, by the GCM tag inside and the signature outside.

> Encrypt claims sparingly. Every encrypted claim is one a consumer cannot route or filter on
> without holding the key, and it moves a key-distribution problem into every service that needs
> the value.

### 6.5 Staff Tokens Are a Separate Token Type

Internal staff authentication does not belong in the customer token. A separate type keeps the
audiences apart — a customer token can never satisfy a staff endpoint even if roles were forged
into it — and lets the two evolve independently:

| Claim | Type | Purpose |
|-------|------|---------|
| `sub` | string | employee identifier |
| `exp` | date | expiry, typically much shorter than a customer session |
| `grp` | string[] | group memberships for authorization |

The same reasoning applies to admin and machine-to-machine access: prefer a distinct token type
with its own `aud` over adding privileged roles to the customer token.

---
