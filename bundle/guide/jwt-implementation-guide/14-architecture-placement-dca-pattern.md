---
type: Section
title: "14. Architecture Placement (DCA Pattern)"
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

New ports and use cases consistent with existing patterns:

```
account/application/shared/
├── LoginAttemptRepository.java      -- NEW output port; extends OutputPort
└── RefreshTokenRepository.java      -- NEW output port; extends OutputPort

account/application/refreshsession/
├── RefreshSessionInputPort.java     -- extends UseCase<RefreshSessionCommand, RefreshSessionResult>
├── RefreshSessionCommand.java       -- contains raw refresh token + client IP
├── RefreshSessionResult.java        -- contains new access token + new refresh token
└── RefreshSessionUseCase.java       -- implements RefreshSessionInputPort

account/application/revokeallsessions/
├── RevokeAllSessionsInputPort.java  -- extends UseCase<RevokeAllSessionsCommand, Void>
├── RevokeAllSessionsCommand.java    -- userId + reason
└── RevokeAllSessionsUseCase.java    -- implements RevokeAllSessionsInputPort
```

**Files to modify if implementing:**

| File | Change |
|------|--------|
| `JwtTokenService.java` | Switch to ES256; add `jti`, `aud`, `kid` to access token; separate visitor and access token generation |
| `JwtIdentitySession.java` | Three-cookie management; env-driven `Secure` flag; `clearAuthenticatedSession()` method |
| `JwtAuthenticationFilter.java` | Read from `shop-session` cookie; silent refresh on expired token |
| `AuthenticateAccountUseCase.java` | Integrate `LoginAttemptRepository` before and after credential check |

### Shared Auth Module Pattern

All three reference implementations (see [`jwt-analysis-c1.md`](jwt-analysis-c1.md), [`jwt-analysis-c2.md`](jwt-analysis-c2.md), [`jwt-analysis-c3.md`](jwt-analysis-c3.md)) encapsulate JWT parsing and validation in a **shared internal library** — consuming services never call the JWT library directly. The consuming service:

1. Passes the raw cookie value (plus environment and rotation configuration) to the library
2. Receives a typed result object (e.g. `AccountInfo`) back
3. Accesses the user identity via a single method call (e.g. `.accountId()`)

This pattern provides:
- A single place to update validation logic (key rotation, skew settings, new claim extraction) simultaneously across all services
- Consuming services never import the JWT library directly — no accidental bypass of validation rules
- Token parsing behaviour is consistent and cannot drift between services
- Easier key rotation: update the shared library once, redeploy all consuming services

In DCA terms, a shared auth module belongs in `sharedkernel/` or as a separate internal library published to an internal artifact registry. It should expose only a typed result API — never raw JWT objects or JWT library types.

**Keep the library framework-free.** The shared auth module should carry no DI-container or web-framework dependencies, so both the issuing service and every consuming service can reuse it regardless of their stack. Expose it through a small factory, and route all I/O through a single SPI interface that the consuming service implements with its own HTTP client:

```java
// Factory — the only public entry points
SharedAuth.jwtValidator(jwksEndpointClient);       // → JwtValidator
SharedAuth.claimDecryptor(activeKeyId, keyMap);    // → ClaimDecryptor

// SPI — the caller supplies the HTTP transport
interface JwksEndpointClient {
    String fetchJwksJson();
}
```

Each consuming service wires these into beans and provides its own `JwksEndpointClient` (pointed at the issuer's JWKS endpoint, with sane connect/read timeouts). The library decides *what* to fetch and *how* to validate; the service decides *how* to talk HTTP — the same dependency-inversion move DCA applies to output ports.

### Principal Modeling: Adapter View vs Domain View

Model the authenticated principal as a **sealed type** so anonymous vs. authenticated is exhaustive and type-checked, rather than a nullable user object (the `ai-architecture-sample` already follows this with its sealed `JwtIdentity`):

```java
sealed interface User permits Guest, Registered {
    record Guest() implements User {}
    record Registered(UserId userId) implements User {}
}
```

Keep the **transport view** separate from the **domain view**:

- **Adapter model** (request-scoped): the validated/decrypted token content — subject plus optional claims. Lives in the adapter layer; produced by the authentication filter.
- **Domain model**: `Guest | Registered`, referenced by the relevant aggregate.

Controllers receive the adapter model (absent → guest) and map it into the domain model in the application layer. Token-shaped types never leak into the domain.

---

## Related markers

- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Factory](/marker/tactical/factory.md)
