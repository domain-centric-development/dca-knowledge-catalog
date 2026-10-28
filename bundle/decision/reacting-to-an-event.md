---
type: Decision
title: "Reacting to an event: one path, two listener kinds"
tags: [decision, events, adapter, application]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/integration-patterns/reacting-to-an-event.md, /guide/integration-patterns/optional-events-and-reliable-delivery.md, /guide/rules.md, /guide/spring-modulith/event-driven-architecture-in-spring-modulith.md, /marker/port-in/inputport.md, /marker/port-out/domaineventpublisher.md, /marker/tactical/domainevent.md]
---

## The question

Something happened — a domain event of this context, or an integration event from another — and something else has
to follow. Where does the reaction run, and what does the listener call?

## The decision

**One path for every reaction: adapter → command → use case.** It holds for a contract from another context and for
a fact this context raised itself. The listener is an incoming adapter: it translates the event into a command and
calls an input port. The use case decides, changes one aggregate or calls an output port, and returns a result. No
reaction lives in the listener, and none in a second kind of input port beside the use case.

**Every listener is one of two kinds, and the kind decides what it may call:**

| | Synchronous listener | Transactional listener |
|---|---|---|
| Runs | inside the transaction that raised the event | after that transaction committed, in a transaction of its own |
| Receives | the event object from the in-process dispatcher | a publication captured in the raising transaction |
| May call | output ports only | an input port |
| Use it for | a translator that captures an integration event; a metric; anything that needs the request (tenant, locale) | every reaction that changes state or performs an external effect |

**A listener that drives an input port is a transactional listener.** Both kinds can sit on the same event: the
translator captures the contract synchronously, the reaction runs after the commit.

## Choosing between a reaction and one transaction

Whether a second change belongs in the same use case or in a reaction is a domain question. Ask whose job the
consistency is (Evans, as Vernon reports it): the user who runs the use case — one use case, one transaction, within
the aggregate rules; another user, or the system — a reaction, eventually consistent. Most rules that span aggregates
tolerate seconds or minutes; the people who know the domain decide, not the developer's habit.

## What the transactional listener needs underneath

An outbox, in any form: captured in the raising transaction, status per publication and consumer,
claim-and-mark with a stale threshold, a wakeup after commit and a poll as the net, bounded retry, terminal failures
kept for replay, delivery at least once. Three forms carry it:

- a framework registry — Spring Modulith's event publication registry with `@ApplicationModuleListener`; configure its
  staleness monitor, which is off by default;
- an own table and a worker — an outbox table written by the domain-event publisher and a scheduled worker per
  consumer; no framework needed;
- a messaging library with durable local queues — Wolverine in .NET, or a service bus outbox.

An in-memory outbox has the status machine but not the guarantee. Without any outbox, there is no transactional
listener — only the after-commit callback, which loses the reaction when the process stops (see the pitfall below).

## Alternatives considered

- **A derived notification type per domain event**, stored in the outbox instead of the domain event (Grzybek's
  "domain event notification"). Works; it doubles the types for an internal reaction. Capture the domain event itself;
  derive a type only for what leaves the context — that is the integration event.
- **An event handler as a second input-port kind** (`on(Event)` beside `execute(Command)`). Two ways to change state
  for the same trigger; rejected.
- **All listeners synchronous.** Reactions then change a second aggregate in the first one's transaction — rejected.
- **All listeners after commit.** The translator then captures the integration event outside the aggregate's
  transaction — rejected.

## Anchors

- Guide: [Reacting to an event](/guide/integration-patterns/reacting-to-an-event.md) · [Optional events and reliable delivery](/guide/integration-patterns/optional-events-and-reliable-delivery.md) · [Layer rules](/guide/rules.md) · [Event-driven architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
- Markers: [InputPort](/marker/port-in/inputport.md) · [DomainEventPublisher](/marker/port-out/domaineventpublisher.md) · [DomainEvent](/marker/tactical/domainevent.md)
- Pitfalls: [A reaction in the raising transaction](/pitfall/reaction-in-the-raising-transaction.md) · [A stored domain event changed like code](/pitfall/stored-domain-event-changed-like-code.md) · [An integration event to yourself](/pitfall/integration-event-to-yourself.md) · [Modifying two aggregates in one transaction](/pitfall/modifying-two-aggregates-in-one-transaction.md)
- Recipe: [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md) · Template: [Event consumer skeleton](/template/event-consumer.md)
- Related decision: [Event delivery: synchronous, asynchronous, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md)
