---
type: ADR
title: "ADR-026: Transactional Outbox for Integration Events"
adr: 26
status: accepted
pattern: "Boundary-crossing events are captured as integration events in a transactional outbox written in the same transaction as the aggregate change, then relayed to the broker out of band with at-least-once delivery."
resource: ai-architecture-sample/docs/architecture/adr/adr-026-transactional-outbox-integration-events.md
tags: [adr, events]
---

Boundary-crossing events are captured as integration events in a transactional outbox written in the same transaction as the aggregate change, then relayed to the broker out of band with at-least-once delivery.

**Consequences:** No lost outbound messages · Transport independence · Operational visibility · Layer purity · More moving parts · At-least-once · Payload at rest

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
