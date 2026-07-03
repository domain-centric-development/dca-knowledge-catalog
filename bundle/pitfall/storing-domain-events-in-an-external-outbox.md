---
type: Pitfall
title: "Storing raw domain events in an external (broker) outbox"
tags: [pitfall, events, outbox]
---

Serializing raw `DomainEvent` objects into an outbox that relays to a message broker. The tempting shortcut — "I already have the domain events, just persist and send them" — leaks the internal model across the bounded-context boundary.

## Why it is wrong

- A `DomainEvent` is internal and **may reference domain objects**; serializing it externally couples foreign consumers (and your durable replay log) to your internal model.
- It is **unversioned** by design (it can evolve freely). External consumers need a stable, versioned contract — that is exactly what an `IntegrationEvent` with `@IntegrationEventType(name, version)` provides.
- It makes the relay own business policy ("which domain event means which outbound action") instead of staying a dumb pipe.
- It pulls a domain type into the adapter/transport layer, violating the boundary the architecture enforces.

## Do instead

Translate in an Anti-Corruption Layer adapter, **inside the publishing transaction**, then store the **integration event**:

`DomainEvent` → (ACL translator) → `IntegrationEvent` (versioned) → outbox row → relay → broker.

The outbox stores *our* published language (channel-neutral, auditable); the foreign wire payload is built at delivery time by the outbound adapter.

## Inverse mistake

Forcing every domain event through an external outbox at all. Most domain events stay in-process; if an async in-process listener must not lose them, use the **internal** event-publication registry — not a broker outbox. See the [decision guide](/decision/event-delivery-sync-async-and-outbox.md).

## Anchors

- Forbidden by intent of: [Integration Events must be in events or adapter outgoing event packages](/rule/strategic/integration-events-must-be-in-events-or-adapter-outgoing-event-packages.md) · [Integration Events must be annotated with IntegrationEventType](/rule/advanced/integration-events-must-be-annotated-with-integrationeventtype.md)
- Decision recorded in: [ADR-026 Transactional Outbox for Integration Events](/adr/adr-026-transactional-outbox-integration-events.md)
- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [IntegrationEvent](/marker/tactical/integrationevent.md)
- Book: [Transactional Outbox Pattern](/book/14-events-integration/common-patterns.md) · [Domain Events vs Integration Events](/book/14-events-integration/domain-events-vs-integration-events.md)
- Note: [Domain vs integration events in an outbox](/note/outbox-domain-vs-integration-events.md)
