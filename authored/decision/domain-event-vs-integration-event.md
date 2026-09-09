---
type: Decision
title: "Domain event or integration event: which one to raise"
tags: [decision, events, integration-event]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domainevent.md, /marker/tactical/integrationevent.md, /rule/advanced/dca-adv-007.md, /rule/advanced/dca-adv-005.md, /rule/strategic/dca-str-007.md, /guide/readme/rules.md, /guide/readme/integration-patterns.md]
---

An event is either an **internal domain fact** or a **published cross-context contract** — and the two are different types in different layers, not one type reused. Confusing them leaks your model across a boundary or, conversely, over-engineers a purely in-context notification.

## The discriminator

1. **Who consumes it?** If every consumer lives *inside the same bounded context*, it is a **Domain Event**. If a *foreign context* (or external system) subscribes, you need an **Integration Event**.
2. **Must the payload be a stable, versioned wire contract?** Cross-context consumers depend on shape stability → Integration Event (version declared via `@IntegrationEventType`). Internal listeners can evolve with the model → Domain Event (no version, by rule).
3. **Which layer raises it?** Aggregates raise Domain Events from the **domain layer**. Integration Events are **adapter-layer** DTOs, produced by translating a domain event in an Anti-Corruption Layer at the outgoing edge.

## Options

| | Domain Event | Integration Event |
|---|---|---|
| Scope | inside one bounded context | across contexts / external |
| Naming | past tense, no suffix (`OrderPlaced`) | past tense + `Event` suffix (`OrderPlacedEvent`) |
| Layer | domain | adapter outgoing / `events` package |
| Versioning | forbidden (`version` field not allowed) | required — as class property `@IntegrationEventType(name, version)`, never a data field |
| Marker | [DomainEvent](/marker/tactical/domainevent.md) | [IntegrationEvent](/marker/tactical/integrationevent.md) |
| Build it | [Recipe: add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md) · [Template: domain event](/template/domain-event.md) | [Recipe: publish a cross-context event](/recipe/publish-a-cross-context-event.md) · [Template: integration event](/template/integration-event.md) |

**Default:** raise a **Domain Event**. Only promote to an Integration Event when a concrete cross-context consumer exists — never publish an integration contract "just in case". A domain event is *always* the origin; the integration event is a translation of it, produced at the boundary.

## The flow across the boundary

`aggregate raises DomainEvent` → in-context listeners react directly → an ACL translator maps it to a `@IntegrationEventType`-annotated `IntegrationEvent` → published to the outside. The domain type never crosses the wire; the versioned contract does.

Delivery (sync vs async, and whether you need an outbox) is a **separate** question — see [Event delivery](/decision/event-delivery-sync-async-and-outbox.md).

## Anchors

- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [IntegrationEvent](/marker/tactical/integrationevent.md)
- Rules: [Domain Events that are not Integration Events must not have a version field](/rule/advanced/dca-adv-007.md) · [Integration Events must be annotated with IntegrationEventType](/rule/advanced/dca-adv-005.md) · [Integration Events must be in events or adapter outgoing event packages](/rule/strategic/dca-str-007.md)
- Guide: [Layer rules](/guide/readme/rules.md) · [Integration patterns](/guide/readme/integration-patterns.md)
- Related: [Event delivery: sync, async, and outbox](/decision/event-delivery-sync-async-and-outbox.md) · [Pitfall: storing raw domain events in an external outbox](/pitfall/storing-domain-events-in-an-external-outbox.md)
