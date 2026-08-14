---
type: Recipe
title: "Publish a cross-context event"
tags: [recipe, events, integration-event, outbox]
---

Make one bounded context react to something that happened in another, or notify an external system. The event **crosses a boundary**, so it must become an `IntegrationEvent` — never a raw domain event. First decide the delivery mode; the wrong choice is the most common event mistake.

## Step 0 — decide (do this first)

Read [Event delivery: sync, async, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md). Outcome:

- **In-process** reaction, same app → stays a `DomainEvent`; an async `@ApplicationModuleListener` + the publication registry gives durable at-least-once. **No broker, no integration event.** Stop here.
- **Cross-context to a broker / external system** → continue below.

## Steps (cross-context)

1. **Raise the domain event** in the aggregate as usual ([Add an aggregate](/recipe/add-an-aggregate.md)).
2. **Define the integration event** in `adapter/outgoing/messaging/event/` — a serializable record of primitives only, implementing `IntegrationEvent` and annotated with `@IntegrationEventType(name, version)` — the contract identity as a class property ([Integration patterns](/guide/readme/integration-patterns.md)).
3. **Translate in an ACL adapter, inside the transaction** — a synchronous listener on the domain event maps it to the integration event and writes the transactional-outbox row in the publishing transaction. Never translate after commit.
4. **Relay out of band** — a poller (plus an after-commit fast path) claims rows, sends to the broker, marks processed; retry with backoff. The outbox stores *your* integration event; the foreign wire payload is built at delivery by the outbound adapter (the ACL to the foreign contract).
5. **Consume** on the other side in `adapter/incoming/messaging/`, translate back through that context's ACL, invoke its use case.
6. **Verify** — `./gradlew test-architecture`.

## Rules to satisfy (build-time checklist)

- [Integration events must be in events or adapter-outgoing event packages](/rule/strategic/integration-events-must-be-in-events-or-adapter-outgoing-event-packages.md)
- [Integration Events must be annotated with IntegrationEventType](/rule/advanced/integration-events-must-be-annotated-with-integrationeventtype.md)
- [Integration Events must not have a version field](/rule/advanced/integration-events-must-not-have-a-version-field.md)
- Do **not** serialize raw domain events across the boundary — see the [pitfall](/pitfall/storing-domain-events-in-an-external-outbox.md)

## Anchors

- Decision: [Event delivery: sync, async, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md)
- Note: [Domain vs integration events in an outbox](/note/outbox-domain-vs-integration-events.md)
- Pitfall: [Storing domain events in an external outbox](/pitfall/storing-domain-events-in-an-external-outbox.md)
- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [IntegrationEvent](/marker/tactical/integrationevent.md)
- Guide: [Integration patterns](/guide/readme/integration-patterns.md) · [Layer rules](/guide/readme/rules.md)
