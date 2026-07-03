---
type: ADR
title: "ADR-006: Domain Events as Immutable Records"
adr: 6
status: accepted
pattern: All Domain Events MUST be implemented as Java records with immutable data.
resource: ai-architecture-sample/docs/architecture/adr/adr-006-domain-events-immutable-records.md
tags: [adr, domain, events]
---

All Domain Events MUST be implemented as Java records with immutable data.

**Consequences:** Immutability Guaranteed · Thread-Safe · Concise · Value Equality · Clear Intent · Validation Support · Modern Java · Pattern Matching

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)

## Enforced by

- [Domain Events should be immutable (final or records)](/rule/advanced/domain-events-should-be-immutable-final-or-records.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
