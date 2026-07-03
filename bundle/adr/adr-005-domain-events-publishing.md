---
type: ADR
title: "ADR-005: Domain Events Publishing Strategy"
adr: 5
status: accepted
pattern: "Domain aggregates REGISTER events during mutations, but events are PUBLISHED only after successful persistence."
resource: ai-architecture-sample/docs/architecture/adr/adr-005-domain-events-publishing.md
tags: [adr, domain, events]
---

Domain aggregates REGISTER events during mutations, but events are PUBLISHED only after successful persistence.

**Consequences:** No Ghost Events · Framework Independence · Transactional Consistency · Easy Testing · Clear Responsibility · Reliable · Flexible · None identified

## Applies to markers

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Id](/marker/tactical/id.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
