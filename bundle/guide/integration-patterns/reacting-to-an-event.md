---
type: Section
title: Reacting to an event
chapter: Integration Patterns
source: guide
resource: dca-guide/architecture/integration-patterns.md
tags: [guide, section]
---

A reaction to an event goes **adapter → command → use case**. That holds for a contract from another context
and for a fact this context raised itself. The adapter subscribes, translates the event into a command and calls an
input port. The use case decides, changes one aggregate or calls an output port, and returns a result. A context
that reacts to its own domain event still drives a use case, and that use case runs in a transaction of its own.

### Two listener kinds

Every listener is one of two kinds. The kind decides what it may call.

| | Synchronous listener | Transactional listener |
|---|---|---|
| Runs | inside the transaction that raised the event | after that transaction committed, in a transaction of its own |
| Receives | the event object from the in-process dispatcher | a publication captured in the raising transaction, from the outbox |
| May call | output ports only: the translator that captures an integration event, a metrics port | an input port |
| After a crash | nothing is lost: it ran before the commit or rolled back with it | nothing is lost: the publication is still due and is delivered again |
| Use it for | the translator of path B; anything that needs the request — tenant, locale | every reaction that changes state or performs an external effect |

**A listener that drives an input port is a transactional listener.** A synchronous listener that drives a use case
changes a second aggregate inside the first one's transaction. The boundary of both aggregates is gone, a failure in
the reaction rolls back the fact that caused it, and the reaction runs again on every retry of the request.

Between the two sits an after-commit callback without an outbox: Spring's
`@TransactionalEventListener(AFTER_COMMIT)` on its own, or a hook registered on the commit. It runs after the commit,
but nothing records that it is due. A process that stops between commit and callback loses the reaction. It fits a log
line or a metric. It does not fit a reaction.

### Whose job is the consistency

Whether a second change belongs in the same transaction or in a reaction is a domain question. Evans' tie-breaker,
as Vernon reports it in *Implementing Domain-Driven Design*: if making the data consistent is the job of the user who
runs the use case, keep it transactional — one use case, within the aggregate rules. If it is another user's job, or
the system's, let a reaction do it. The question shows which invariants must hold at once. Most rules that span
aggregates tolerate seconds or minutes; ask the people who know the domain before assuming they do not.

### The outbox, in any form

The guarantee does not depend on a framework. Every outbox has the same parts:

1. **Capture.** The publication is written in the transaction that saves the aggregate. A rollback removes it.
2. **Status per publication and consumer.** Published, processing, completed, failed — per consumer, because two
   reactions to one event succeed and fail independently.
3. **Claim and mark.** A worker claims due publications atomically. A claim older than a threshold counts as stale
   and is claimed again, so a worker that died mid-reaction does not leave the publication stuck.
4. **Wakeup and poll.** The commit wakes the worker; a periodic poll finds what a lost wakeup left behind.
5. **Bounded retry.** Retry with backoff up to a limit. A terminal failure stays in the outbox for inspection and a
   deliberate replay.
6. **At least once.** The same publication can arrive twice. The reaction is idempotent per event id and consumer.

Three forms carry these parts:

- **A framework registry.** Spring Modulith's event publication registry with `@ApplicationModuleListener`, which is
  `@Async` + `@Transactional(REQUIRES_NEW)` + `@TransactionalEventListener`. Its staleness monitor is off by default;
  configure it, or a reaction that hung stays in processing for good.
- **An own table and a worker.** An outbox table beside the aggregates, written by the domain-event publisher, and
  a scheduled worker per consumer that claims rows and drives the input port. No framework needed.
- **A messaging library with durable local queues.** In .NET, Wolverine's durable local queues with its outbox, or the
  outbox of a service bus.

An in-memory outbox has the status machine but not the guarantee. It suits tests and samples, not production.


### A stored event is a format

"Domain events need no versioning" assumes in-process delivery that completes before the transaction ends. Once a
domain event is stored, it is persisted data, and the next deployment reads what the previous one wrote. It needs no
version number — it is read by the same code base, and only until it is delivered — but it needs what a database
migration needs:

- **Tolerant reading.** Unknown fields are ignored, missing ones defaulted. Adding a field is always safe.
- **Two steps for a rename or removal.** Add the new field and keep reading the old one; drop the old one a
  deployment later. Or deploy on an empty outbox: drain it first and check for failed publications.
- **The type name.** Many outboxes record the event's fully qualified class name and the listener's identity. Moving
  the event to another package or renaming the listener method then breaks every pending publication. Drain the outbox
  before such a refactoring, or record a logical name where the outbox lets you.

The less an event carries, the less of its format can change. Ids practically never do.

### An integration event to yourself

An integration event that only its own context consumes, published to make a reaction to an own fact durable, is a
detour. It buys a contract, a version and compatibility rules for a reader that ships with the writer. That is what
domain events are for: capture the domain event in the outbox and subscribe with a transactional listener.
