---
type: ADR
title: "ADR-007: Hexagonal Architecture with Explicit Port/Adapter Separation"
adr: 7
status: accepted
pattern: "We will implement strict Hexagonal Architecture with explicit separation between:."
resource: ai-architecture-sample/docs/architecture/adr/adr-007-hexagonal-architecture.md
tags: [adr, hexagonal]
---

We will implement strict Hexagonal Architecture with explicit separation between:.

**Consequences:** Framework Independence · Testability · Swappable Adapters · Clear Boundaries · Maintainability · Flexibility · Team Organization · None identified

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md)

## Enforced by

- [Application Services should not access port adapters](/rule/hexagonal/application-services-should-not-access-port-adapters.md)
- [Classes from the domain should not access port adapters](/rule/hexagonal/classes-from-the-domain-should-not-access-port-adapters.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
