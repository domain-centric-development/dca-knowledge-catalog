---
type: Note
title: "Domain vs integration events in an outbox / event store"
tags: [note, events, outbox]
---

Should an outbox store domain events or integration events? The short answer: an **external** (broker) outbox stores **integration events**; an **internal** event-publication registry stores **domain events**. They are the same transactional-outbox pattern at two scopes. This note compounds a longer Q&A — see the [decision guide](/decision/event-delivery-sync-async-and-outbox.md) for the table.

## Three things people conflate

**1. Event store ≠ outbox.** An event-sourcing *event store* keys by aggregate, is append-only, never "completes" — events are the source of truth. An *outbox* keys by delivery, tracks completion/retry, and is a relay buffer over a DB that is itself the truth. The Spring Modulith `EVENT_PUBLICATION` table is an outbox (per-listener completion + redelivery), **not** an event store.

**2. Internal registry vs external outbox.** Both persist the event in the publishing transaction and relay at-least-once. The internal registry redelivers to **in-process** listeners and stores the **domain event** (it never leaves the context). The external outbox relays to a **broker** and stores the **integration event** (versioned, serializable, channel-neutral — the foreign wire payload is built later by the delivery adapter, which is the ACL).

**3. Delivery mode, not event type, decides outbox need.** Sync listener → atomic, no outbox. Async + must-not-lose → durable capture. A domain event delivered async in-process still needs the registry; "domain events never need an outbox" is wrong for that case.

## State of the reference implementation

The sample implements the **internal** registry only — surfaced read-only as `EventPublicationLogStore` / `JdbcEventPublicationLogStore` in the `backoffice` context (reads Spring Modulith's `EVENT_PUBLICATION` table). The **external** broker outbox is documented as the target pattern ([ADR-026](/adr/adr-026-transactional-outbox-integration-events.md)) but not yet built — no `@Externalized` / broker config. So storing **domain** events in the sample is correct: it is the internal registry, not a boundary-crossing outbox.

## Anchors

- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [IntegrationEvent](/marker/tactical/integrationevent.md)
- ADRs: [ADR-026 Transactional Outbox](/adr/adr-026-transactional-outbox-integration-events.md) · [ADR-024 Interface Inversion](/adr/adr-024-interface-inversion-spring-modulith.md) · [ADR-005 Domain Events Publishing](/adr/adr-005-domain-events-publishing.md)
- Book: [Domain Events vs Integration Events](/book/14-events-integration/domain-events-vs-integration-events.md) · [Transactional Outbox Pattern](/book/14-events-integration/common-patterns.md)
- Guide: [Event-driven architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
- Decision: [Event delivery: sync, async, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md)
- Pitfall: [Storing domain events in an external outbox](/pitfall/storing-domain-events-in-an-external-outbox.md)
