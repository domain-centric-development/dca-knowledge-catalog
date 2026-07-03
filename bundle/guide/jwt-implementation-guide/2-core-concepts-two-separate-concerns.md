---
type: Section
title: "2. Core Concepts: Two Separate Concerns"
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

### 2.1 The Session Token (Access Token)

- Stateless — services validate by signature + `exp`, no DB lookup
- Short-lived (15 min) — limits blast radius if stolen; invisible to user with silent refresh
- Asymmetrically signed — services verify with public key, cannot mint new tokens
- Contains: `sub` (userId), `email`, `roles`, `jti` (UUID, unique per token), `aud`, `exp`

### 2.2 The Login Gate (Refresh Token + Login State)

- Stateful — every use requires a DB row lookup
- Opaque random bytes (256-bit) — claims live in the DB row, not the token
- Revocable by deleting or marking the row revoked
- Scoped by cookie path so it is never sent to product/cart/checkout services

### 2.3 Why They Must Never Be Merged

| Approach | Risk |
|----------|------|
| Long-lived JWT (7+ days) | No revocation without a denylist — cancels the stateless benefit |
| HS256 with shared secret | One compromised service exposes all services |
| Short access token + DB-backed refresh | Revocation cost is always O(1) regardless of service count |

---
