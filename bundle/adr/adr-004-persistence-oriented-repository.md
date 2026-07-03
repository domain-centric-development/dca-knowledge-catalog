---
type: ADR
title: "ADR-004: Persistence-Oriented Repository Pattern"
adr: 4
status: accepted
pattern: "We will use the Persistence-Oriented repository style with explicit `save()` operations."
resource: ai-architecture-sample/docs/architecture/adr/adr-004-persistence-oriented-repository.md
tags: [adr, repository]
---

We will use the Persistence-Oriented repository style with explicit `save()` operations.

**Consequences:** Explicit Transactions · Framework Agnostic · Event Publishing · Testability · Clarity · Simplicity · Control · Not True Collection Illusion

## Applies to markers

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Id](/marker/tactical/id.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
