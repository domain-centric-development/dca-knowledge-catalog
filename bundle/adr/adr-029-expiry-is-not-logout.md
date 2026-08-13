---
type: ADR
title: "ADR-029: Session Expiry Ends the Session, Not the Identity"
adr: 29
status: accepted
pattern: "Expiry ends the *session*. Only an explicit logout ends the *identity*."
resource: ai-architecture-sample/docs/architecture/adr/adr-029-expiry-is-not-logout.md
tags: [adr]
---

Expiry ends the *session*. Only an explicit logout ends the *identity*.

**Consequences:** No silent cart loss · Signing in no longer shortens continuity · Attack signal restored · Predictable rule · Two cookies to reason about instead of one

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
