---
type: ADR
title: "ADR-002: Framework-Independent Domain Layer"
adr: 2
status: accepted
pattern: The domain layer MUST have zero dependencies on infrastructure frameworks.
resource: ai-architecture-sample/docs/architecture/adr/adr-002-framework-independent-domain.md
tags: [adr, domain]
---

The domain layer MUST have zero dependencies on infrastructure frameworks.

**Consequences:** Long-lived Domain · Easy Testing · Portable · Focused Code · Clear Boundaries · Faster Tests · Team Efficiency · None identified

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainService](/marker/tactical/domainservice.md)
- [Factory](/marker/tactical/factory.md)
- [Specification<T>](/marker/tactical/specification.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
