---
type: Decision
title: "Event delivery: synchronous, asynchronous, and when you need an outbox"
tags: [decision, events, outbox]
---

Choosing how to deliver an event reliably is two independent questions, not one. Answer both, then read the row off the table — most "do I need an outbox?" confusion comes from collapsing them.

## The two axes

1. **Boundary** — does the event stay **inside** the bounded context (a `DomainEvent`) or **cross** it to an external system (an `IntegrationEvent`)?
2. **Delivery** — is the listener **synchronous** (runs in the publishing transaction) or **asynchronous** (separate transaction/thread)?

Outbox need is driven by **delivery**, not by event type. Event type is driven by **boundary**.

## Decision table

| Listener delivery | Crosses boundary? | Stored payload | Needs durable capture (outbox)? | Mechanism |
|---|---|---|---|---|
| `DomainEvent`, **sync** | No | — | **No** — atomic with the transaction | plain in-tx listener |
| `DomainEvent`, **async**, must-not-lose | No | the domain event | **Yes** | **internal** event-publication registry |
| `DomainEvent`, **async**, best-effort (metrics/logging) | No | — | No — allowed to be lost | plain async publisher |
| `IntegrationEvent`, **async**, to a broker | Yes | the integration event (versioned) | **Yes** | **external** transactional outbox |

## Why it's the same pattern twice

The internal registry and the external outbox are **both transactional outboxes**: persist the event in the publishing transaction, relay out of band, at-least-once. They differ only in:

- **consumer** — in-process listener vs foreign system over a broker
- **stored payload** — `DomainEvent` (never leaves the context) vs `IntegrationEvent` (versioned published contract)

Crossing the boundary forces the translation: a cross-context consumer needs a stable, serializable, versioned contract, so an Anti-Corruption Layer translates `DomainEvent` → `IntegrationEvent` before it is captured.

## Common trap

"Domain events don't need an outbox" is only true for **synchronous** delivery. An **async, must-not-lose** in-process domain listener needs durable capture too — it just stores the domain event and delivers in-process. See the [pitfall](/pitfall/storing-domain-events-in-an-external-outbox.md) for the inverse mistake.

## Anchors

- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [IntegrationEvent](/marker/tactical/integrationevent.md)
- ADRs: [ADR-005 Domain Events Publishing](/adr/adr-005-domain-events-publishing.md) · [ADR-024 Interface Inversion (SM listeners)](/adr/adr-024-interface-inversion-spring-modulith.md) · [ADR-026 Transactional Outbox](/adr/adr-026-transactional-outbox-integration-events.md)
- Book: [Domain Events vs Integration Events](/book/14-events-integration/domain-events-vs-integration-events.md) · [Domain Events — when durable delivery is needed](/book/14-events-integration/domain-events.md) · [Transactional Outbox Pattern](/book/14-events-integration/common-patterns.md)
- Guide: [Event-driven architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
- Related: [Note: domain vs integration events in an outbox](/note/outbox-domain-vs-integration-events.md)
