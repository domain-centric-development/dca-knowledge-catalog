---
type: Pitfall
title: Reconstitution raises the creation event
tags: [pitfall, domain, aggregate, domain-event, events, repository, persistence, adapter]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-009.md, /guide/rules.md, /marker/tactical/aggregateroot.md, /marker/tactical/baseaggregateroot.md, /marker/tactical/factory.md, /marker/port-out/repository.md]
---

A repository adapter — in-memory, JDBC or JPA — rebuilds a loaded aggregate through the same factory that creates a new one: `Task.create(id, title, …)` in the row mapper, in the entity-to-domain mapper, or in the in-memory adapter's copy on read. `create` registers `TaskCreated`, because that is its job. The aggregate now returns from `findById` carrying a creation event for something that has existed for months; the next `save` plus `publishAndClearEvents` publishes it, and every listener re-runs its side effect — a welcome mail per edit, a second stock initialisation, a duplicate projection row.

## Why it is wrong

- Creation is a business fact that happened once. Publishing it on every reload turns one fact into as many as there are edits, and no listener can tell the phantom from the original.
- The bug hides in tests: an in-memory adapter that returns the stored instance never reconstitutes, so the suite passes; the first database adapter, or an in-memory adapter that copies on read as it should, surfaces it in production.
- Registered-but-unpublished events are state the aggregate carries between calls. A load is supposed to hand back a fact, not to add one — re-reading must not replay what the writer already published.

## What forbids it

No rule catches it statically. [Use cases that save an aggregate must publish its domain events](/rule/usecase/dca-use-009.md) sees a use case that saves and publishes and is satisfied; which events sit on the aggregate at that moment is runtime state. The guide's contract is explicit — [A repository hands out copies](/guide/rules.md): every adapter maps back through the aggregate's `reconstitute` factory, and registered-but-unpublished events are not carried over. The contract test on the port is what makes the rule testable: assert that an aggregate loaded from the repository has an empty event list.

## Do instead

Give the aggregate two factories for two moments in its life: `create(...)` for the birth of a new fact, which validates and registers `{Name}Created`; `reconstitute(...)` for a repository handing back what it stored, which takes the persisted state as-is and registers nothing. Adapters call only `reconstitute` — the JDBC row mapper, the JPA entity mapper, the in-memory copy. Clearing the events after calling `create` is the wrong cure: it runs the creation validation against already-valid state and still hides that the factory was misused.

- Skeleton with both factories: [Aggregate root skeleton](/template/aggregate-root.md)
- Adapters that reconstitute: [JDBC repository adapter](/template/jdbc-repository-adapter.md) · [JPA repository adapter](/template/jpa-repository-adapter.md) · [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md)

## Anchors

- Markers: [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md) · [BaseAggregateRoot](/marker/tactical/baseaggregateroot.md) · [Factory](/marker/tactical/factory.md) · [Repository<T, ID>](/marker/port-out/repository.md)
- Rules: [Use cases that save an aggregate must publish its domain events](/rule/usecase/dca-use-009.md)
- Guide: [Layer rules](/guide/rules.md)
- Related pitfall: [Clearing domain events before they are dispatched](/pitfall/clearing-domain-events-before-dispatch.md) · Decision: [Factory or constructor](/decision/factory-vs-constructor.md)
