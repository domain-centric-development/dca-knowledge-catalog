---
type: Section
title: 17. Related Documents
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

- [`spring-modulith.md`](spring-modulith.md) — Spring Boot integration patterns
- [`archunit-governance.md`](archunit-governance.md) — Enforcing architectural rules
- [`ai-architecture-sample/docs/architecture/adr/`](../ai-architecture-sample/docs/architecture/adr/) — ADRs for the reference implementation, in particular
  **ADR-029** (session expiry ends the session, not the identity) and **ADR-030** (separate cookies
  for identity, session and renewal)

> This guide was distilled from analyses of three production JWT implementations. Those analyses
> described third-party systems and are deliberately not part of this repository; what they taught is
> in the sections above.

## Related ADRs

- [ADR-029: Session Expiry Ends the Session, Not the Identity](/adr/adr-029-expiry-is-not-logout.md)
- [ADR-030: Separate Cookies for Identity, Session and Renewal](/adr/adr-030-three-cookie-session-design.md)
