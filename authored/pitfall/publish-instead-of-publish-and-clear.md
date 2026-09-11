---
type: Pitfall
title: Publishing events one by one instead of publishAndClearEvents
tags: [pitfall, application, use-case, domain-event, events, port-out]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-009.md, /marker/port-out/domaineventpublisher.md, /marker/tactical/baseaggregateroot.md, /rule/usecase/dca-use-012.md, /guide/rules.md]
---

A use case that saves the aggregate and then dispatches its events by hand:

```java
repository.save(task);
for (DomainEvent event : task.domainEvents()) {
    publisher.publish(event);
}
task.clearDomainEvents();   // or forgotten
```

It reads like the long form of the same thing. It is not: the sanctioned form is one call, `publisher.publishAndClearEvents(task)`, and the rule accepts nothing else.

## Why it is wrong

- The loop separates *dispatch* from *clear* and makes the use case responsible for the order. If the third listener throws, the loop aborts: with the clear at the end, the aggregate keeps all events including the two already dispatched, and a retry publishes them twice; with the clear inside the loop, the aggregate is cleared before every listener returned. `publishAndClearEvents` dispatches all events and clears only after every listener has returned — the clear is the acknowledgement that the events were seen.
- Forgetting `clearDomainEvents()` keeps the events on the instance; a later save on the same object in the same request publishes them again.
- The publisher's contract — save, dispatch, clear, inside one transaction — is a single unit that must be implemented once, in the publisher, not re-derived per use case.
- The rule counts only `publishAndClearEvents` as a publication, so the manual loop fails `DCA-USE-009` on every entry path that reaches the save, even when the code happens to be correct.

## What forbids it

- [Use cases that save an aggregate must publish its domain events](/rule/usecase/dca-use-009.md) — `publish(event)`, even followed by `clearDomainEvents()`, does not count as publishing the aggregate's events.
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md) — the marker's contract names `publishAndClearEvents(aggregate)` as the one operation a use case calls after `save`.

## Do instead

Replace the loop and the clear with one line:

```java
repository.save(task);
publisher.publishAndClearEvents(task);
```

The publisher iterates, dispatches and clears; a throwing listener propagates, the events stay on the aggregate and the surrounding transaction rolls back. `publish(event)` remains for events that are not registered on an aggregate — which in this architecture is the exception, not the pattern.

- Related pitfall: [Clearing domain events before they are dispatched](/pitfall/clearing-domain-events-before-dispatch.md) — the same separation of dispatch and clear, seen from inside the publisher.

## Anchors

- Markers: [DomainEventPublisher](/marker/port-out/domaineventpublisher.md) · [BaseAggregateRoot](/marker/tactical/baseaggregateroot.md)
- Rules: [Use cases that save an aggregate must publish its domain events](/rule/usecase/dca-use-009.md) · [Use cases that save an aggregate or publish domain events must have a transaction boundary](/rule/usecase/dca-use-012.md)
- Guide: [Layer rules](/guide/rules.md)
- Template: [Use case skeleton](/template/use-case.md)
