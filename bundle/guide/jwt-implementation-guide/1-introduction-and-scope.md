---
type: Section
title: 1. Introduction and Scope
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

Two concerns that must be kept separate:

- **JWT Session Token (access token):** Stateless, short-lived, validated by signature + `exp` only — no DB lookup per request.
- **Login State Management (refresh token):** Stateful, DB-backed, revocable by deleting a row.

**What the `ai-architecture-sample` has today:**
- `JwtTokenService` — signs/verifies tokens using **HS256** (symmetric)
- `JwtIdentitySession` — manages a visitor cookie (`shop-identity`) and access cookie; `Secure=false` hardcoded
- `JwtAuthenticationFilter` — validates the access token per request
- No refresh token, no brute-force protection, no attempt tracking, no cookie path-scoping

**What changes in a multiservice platform vs a monolith:**
With HS256, every verifying service must share the signing secret. One leaked service secret compromises all services. The solution is asymmetric signing (ES256/RS256) — only the auth service holds the private key; all other services verify using the public key.

---
