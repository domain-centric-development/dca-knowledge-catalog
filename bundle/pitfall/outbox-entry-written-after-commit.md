---
type: Pitfall
title: Outbox entry written after the commit
tags: [pitfall, events, integration-event, outbox, application, infrastructure]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/readme/rules.md, /rule/usecase/dca-use-012.md, /marker/port-out/integrationeventpublisher.md, /marker/port-out/domaineventpublisher.md, /guide/spring-modulith/event-driven-architecture-in-spring-modulith.md]
---

An integration-event publisher that registers the outbox publication in an *after-commit* hook — "so a rolled-back use case publishes nothing". The intent is right, the mechanism is wrong: the publication is created in a second step after the aggregate is already durable.

## Why it is wrong

- Between the aggregate's commit and the outbox write there is a window in which the process can die. The state change survives, the event is lost — exactly the failure the outbox pattern exists to rule out.
- A database-backed outbox cannot be dropped in later: with after-commit registration it would have to open a second transaction, keeping the window. The *shape* has to be right before the store is.
- It hides the intent of the pattern from readers: "written in the same transaction as the aggregate" is the whole point of a transactional outbox.

## What forbids it

- [Layer rules](/guide/readme/rules.md) — event publishing rules: the publication is written *inside* the aggregate's transaction, released to the dispatcher after commit, discarded on rollback.
- [Use cases that save an aggregate or publish domain events must have a transaction boundary](/rule/usecase/dca-use-012.md) — the publishing use case has a transaction for the outbox row to join.

## Do instead

Register **inside** the transaction; use the commit hook only to *wake the dispatcher*; use a rollback hook only where the store cannot roll back by itself (an in-memory stand-in — a database rolls the row back on its own):

```text
inTransaction:
    repository.save(aggregate)
    outbox.register(event)        // same transaction — pending, not yet due
afterCommit:
    outbox.release(id)            // dispatcher may deliver now
afterRollback:
    outbox.discard(id)            // in-memory only
```

Spring Modulith's event publication registry does exactly this; the guide's Modulith section describes it. Consumers stay idempotent: delivery is at least once.

- Decision: [Event delivery: sync, async, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md)

## Anchors

- Markers: [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md) · [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- Rules: [Use cases that save an aggregate or publish domain events must have a transaction boundary](/rule/usecase/dca-use-012.md)
- Guide: [Layer rules](/guide/readme/rules.md) · [Event-driven architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
- Related pitfall: [Storing raw domain events in an external outbox](/pitfall/storing-domain-events-in-an-external-outbox.md)
