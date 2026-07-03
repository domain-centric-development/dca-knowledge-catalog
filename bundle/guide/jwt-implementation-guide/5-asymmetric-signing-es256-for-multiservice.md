---
type: Section
title: "5. Asymmetric Signing (ES256) for Multiservice"
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

### The HS256 Problem

With a shared symmetric key, any service that can verify tokens can also mint them. A compromised service exposes the entire platform.

### ES256 / RS256 Approach

- Auth service holds the **private key** (sign only)
- All other services hold the **public key** (verify only, cannot mint)
- Key material never appears in `application.yml` — loaded from vault or secret manager at startup

**Prefer ES256 over RS256:** smaller tokens (64 bytes vs 256 bytes for the signature), same security level, faster operations.

### JWKS Endpoint

Publish public keys at `GET /.well-known/jwks.json`:

```json
{
  "keys": [
    {
      "kty": "EC",
      "crv": "P-256",
      "kid": "2024-01",
      "use": "sig",
      "alg": "ES256",
      "x": "...",
      "y": "..."
    }
  ]
}
```

Services fetch and cache the JWKS on startup; refresh on cache miss for unknown `kid`.

### Consumer-Side JWKS Caching

Verifying services should resolve the public key for a token's `kid` against a local in-memory cache rather than fetching the JWKS per request:

```
getPublicKey(kid):
    if cache.has(kid): return cache[kid]          // fast path, no lock
    synchronized:
        if cache.has(kid): return cache[kid]      // double-check
        refreshFromJwksEndpoint()                 // one fetch, not N
        if cache.has(kid): return cache[kid]
        throw UnknownKeyId                        // token fails verification
```

- **Cache hit** — return immediately, no lock, no network call. Token verification stays purely local.
- **Cache miss** — a single thread fetches and parses the JWKS document inside a synchronized block with a double-check; concurrent requests for a new `kid` trigger one fetch, not a thundering herd.
- **Still missing after refresh** — the `kid` is unknown to the issuer; that token's verification fails.

The cache is **lazy, accumulative, and has no TTL**: keys are only ever added. A new `kid` is discovered on the first token that carries it; a retired `kid` lingers harmlessly until process restart. This works because possessing a retired *public* key is not a risk — it can verify old tokens (which have expired anyway) but never forge new ones.

### Key Rotation Procedure

The rotation uses explicit modes to eliminate the validation gap during transition:

| Mode | JWKS contains | Services verify against |
|------|--------------|-------------------------|
| `OLD` | Old public key only | Old key only |
| `BOTH` | Old + new public key | Either key (try new first, fall back to old) |
| `NEW` | New public key only | New key only |

**Step-by-step:**
1. Start in `OLD` mode — only the current key is published
2. Generate new key pair; assign a new `kid`
3. Switch to `BOTH` mode — publish both keys in JWKS; start signing new tokens with the new private key
4. Wait for all tokens signed by the old key to expire (maximum = access token lifetime = 15 min)
5. Switch to `NEW` mode — remove the old public key from JWKS; decommission the old private key

The `BOTH` mode eliminates the risk of in-flight tokens (signed by the old key) failing validation during the transition window. The `kid` claim in the JWT header identifies which key to use; services in `BOTH` mode try the matching key by `kid`, then fall back to the other.

---
