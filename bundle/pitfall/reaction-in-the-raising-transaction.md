---
type: Pitfall
title: A reaction in the raising transaction
tags: [pitfall, events, adapter, aggregate]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/integration-patterns/reacting-to-an-event.md, /guide/rules.md, /marker/port-in/inputport.md, /marker/tactical/domainevent.md, /rule/layered/dca-lay-004.md, /rule/hexagonal/dca-hex-017.md]
---

A listener for a domain event calls an input port, and it runs synchronously: Spring's `@EventListener`, a
subscriber the in-process dispatcher calls before the use case returns, a handler dispatched from `SaveChanges`. The
reaction looks decoupled — the publishing use case does not know it — and every test is green, because the reaction
happens before the request ends.

A quieter variant: the listener runs after the commit, but nothing recorded that it was due —
`@TransactionalEventListener(AFTER_COMMIT)` on its own, a callback registered on the commit, a fire-and-forget task.

## Why it is wrong

- **Synchronous:** the reaction's use case changes a second aggregate inside the first one's transaction. The
  boundary of both aggregates is gone. A failure in the reaction rolls back the fact that caused it, and a retry of
  the request runs the reaction again.
- **After commit without an outbox:** a process that stops between commit and callback loses the reaction for good. No
  status, no retry, no trace. A failure inside the callback is logged and forgotten.
- Both read as "event-driven" in review. The difference is in an annotation or a registration line.

## What forbids it

- [Event listeners that drive an input port must run after the commit in their own transaction](/rule/hexagonal/dca-hex-017.md)
  — experimental: a listener that calls an input port must be of the configured transactional-listener kind and run
  in a transaction. The rule reads the listener's kind, not whether an outbox backs it; the quieter variant is a
  review duty.

## Do instead

Make the listener a **transactional listener**: delivered after the commit, in a transaction of its own, from a
publication captured in the raising transaction — a framework registry (`@ApplicationModuleListener` with the event
publication registry), an own outbox table with a worker, or a library with durable local queues. Keep the
synchronous kind for what calls only output ports: the translator that captures an integration event, a metric. An
after-commit callback without an outbox fits a log line, never a reaction.

## Anchors

- Decision: [Reacting to an event: one path, two listener kinds](/decision/reacting-to-an-event.md)
- Guide: [Reacting to an event](/guide/integration-patterns/reacting-to-an-event.md) · [Layer rules](/guide/rules.md)
- Rules: [Transaction boundaries belong to the application layer](/rule/layered/dca-lay-004.md) · [Event listeners that drive an input port must run after the commit in their own transaction](/rule/hexagonal/dca-hex-017.md)
- Markers: [InputPort](/marker/port-in/inputport.md) · [DomainEvent](/marker/tactical/domainevent.md)
- Sibling pitfalls: [Modifying two aggregates in one transaction](/pitfall/modifying-two-aggregates-in-one-transaction.md) · [Declarative transaction without a transaction manager](/pitfall/declarative-transaction-without-a-transaction-manager.md)
