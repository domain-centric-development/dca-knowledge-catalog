---
type: Pitfall
title: Clearing domain events before they are dispatched
tags: [pitfall, events, domain-event, application, infrastructure]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-009.md, /marker/port-out/domaineventpublisher.md, /rule/usecase/dca-use-012.md, /guide/readme/rules.md]
---

A `DomainEventPublisher` implementation that snapshots the aggregate's events, calls `clearDomainEvents()`, and then dispatches the snapshot — or a use case that publishes before it saves. Both look like tidy bookkeeping; both change what a failure means.

## Why it is wrong

- Clear-then-dispatch: the first listener that throws aborts the loop with the events already gone from the aggregate. The use case fails, but nothing records which events were never seen; a retry starts from an aggregate with an empty event list.
- Publish-before-save: a listener reacts to a state change that may never be persisted (the save can still fail). Downstream contexts learn about an order that does not exist.
- Both break the contract that domain-event listeners run *inside* the publishing transaction and either all succeed with the state change or none do.

## What forbids it

- [Use cases that save an aggregate must publish its domain events](/rule/usecase/dca-use-009.md) — the use case saves, then publishes; the rule anchors the order.
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md) — the marker's contract: save → dispatch → clear; clearing is the acknowledgement that every listener saw the event.

## Do instead

Order inside the use case: `save`, then `publishAndClearEvents`, inside the same transaction. Inside the publisher: dispatch every collected event; only when all listeners returned, clear the aggregate. A throwing listener propagates, the events stay on the aggregate, the surrounding transaction rolls back. Asynchronous or cross-context listeners are not reached this way — they receive an integration event through the outbox.

- Decision: [Event delivery: sync, async, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md)

## Anchors

- Markers: [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- Rules: [Use cases that save an aggregate must publish its domain events](/rule/usecase/dca-use-009.md) · [Use cases that save an aggregate or publish domain events must have a transaction boundary](/rule/usecase/dca-use-012.md)
- Guide: [Layer rules](/guide/readme/rules.md)
