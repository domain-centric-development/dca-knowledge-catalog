---
type: ADR
title: "ADR-030: Separate Cookies for Identity, Session and Renewal"
adr: 30
status: accepted
pattern: "Split by lifetime and by purpose. Four identifiers, three of them in the auth subsystem."
resource: ai-architecture-sample/docs/architecture/adr/adr-030-three-cookie-session-design.md
tags: [adr]
---

Split by lifetime and by purpose. Four identifiers, three of them in the auth subsystem.

**Consequences:** [ADR-029](adr-029-expiry-is-not-logout.md) becomes implementable · The cart is consent-independent · Rotation on logout costs nothing · Blast radius is bounded by path scope · No revocation until `shop-refresh` exists · A logout on device A does not end a session on device B

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
