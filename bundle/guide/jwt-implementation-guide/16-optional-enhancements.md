---
type: Section
title: 16. Optional Enhancements
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

```
[ ] Multi-level authentication (soft login / full login) with loginTyp claim
[ ] Multi-country / multi-tenant support with tenant claim and per-tenant validation
[ ] Field-level AES encryption of sensitive claims (alternative to full JWE — see below)
[ ] "Manage active sessions" UI (list + revoke individual refresh_tokens rows by device_hint)
[ ] Remember-me vs regular session (different refresh token TTL chosen at login time)
[ ] Email notification on login from new IP address or unrecognised device_hint
[ ] Step-up authentication for high-risk operations (re-prompt password before checkout)
[ ] IP/country anomaly detection (flag logins from unusual geographies)
[ ] CAPTCHA or proof-of-work challenge after N consecutive failures
[ ] JWE (payload encryption) if access token claims contain sensitive data
[ ] Redis jti denylist for immediate access token revocation (before natural expiry)
[ ] Per-user "valid-after" watermark as a lightweight revocation alternative (see below)
[ ] Append-only auth_events audit table (login, logout, refresh, soft-lock, suspend, close)
[ ] Magic link tokens for passwordless login or account recovery flow
[ ] Shared auth library published to internal artifact registry (encapsulates all JWT parsing)
```

### Per-User Valid-After Watermark

A lightweight revocation alternative for topologies that deliberately run **without refresh tokens** (longer-lived access token, e.g. 30 minutes, as the only credential): store one **"valid-after" timestamp per user**, updated on logout, password change, or suspension. On verification, reject any token issued before the watermark:

```
tokenValid = token.iat >= user.tokenValidAfter
```

One indexed timestamp per user buys forced revocation without a token blacklist or denylist infrastructure.

**Trade-offs:**
- Enforcing the watermark requires a per-user lookup at verification time — it re-introduces state exactly where the stateless JWT was supposed to avoid it. Typically only the auth/issuer service enforces it; whether downstream resource services also check the watermark (vs. trusting `exp` alone) is an explicit design decision. Trusting `exp` alone means a logged-out user's unexpired token still passes at resource services — acceptable only if the TTL is short.
- Compared to the refresh-token approach in this guide (Sections 2 and 12): the refresh-token design keeps revocation checks off the per-request path entirely (revocation bites at the next rotation, at most 15 minutes out), at the cost of the refresh infrastructure. The watermark suits simpler topologies that accept a DB hit on verification or a short revocation lag.

### Field-Level AES Encryption

A practical middle ground between an unprotected payload (standard JWS) and full payload encryption (JWE): encrypt only the sensitive claim value before embedding it in the JWT.

```
1. AES-encrypt rawUserId  →  encryptedValue
2. Embed encryptedValue as the claim (e.g. "uniqueUserId": "<AES_ENCRYPTED>")
3. Sign the JWT normally (JWS)
4. Verifier: verify signature → AES-decrypt the claim value
```

The token is human-readable except for the encrypted field. This protects the sensitive identifier from log scrapers and intermediaries that can base64-decode the payload, without the complexity of a full JWE implementation.

**Recommended cipher construction — AES-256-GCM:**

- 12-byte random IV per encryption; 128-bit authentication tag
- Pass the encryption key ID as **AAD** (additional authenticated data) — this binds the ciphertext to its key, so tampering with the key prefix fails the GCM tag
- Wire format: `keyId:base64(IV ‖ ciphertext ‖ tag)`
- Decryption failures should degrade to an **absent value**, never an exception — consistent with the rule that invalid token material means anonymous, not 5xx

**Key versioning for rotation:** prefix the encrypted value with the key ID (as above) so the decryption side can select the correct key from a key map and fall back to older keys for in-flight tokens:

```
V2:<base64(AES_V2_encrypt(rawUserId))>
```

Decommission old key versions only after the maximum token lifetime has elapsed (i.e. after all tokens encrypted with the old key have expired). The same `OLD → BOTH → NEW` rotation pattern from Section 5 applies: accept both key versions during the transition window, then drop the old version.

**Two independent key systems:** the signing key pair (ES256) and the claim-encryption key (AES) must not be conflated — different algorithms, different rotation lifecycles, different secrets. The encrypted claim is protected twice: GCM auth tag inside, ES256 signature outside.

---
