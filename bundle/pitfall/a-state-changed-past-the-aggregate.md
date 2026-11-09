---
type: Pitfall
title: A state changed past the aggregate
tags: [pitfall, aggregate, adapter, persistence, domain-event, domain]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/hexagonal/dca-hex-021.md, /guide/rules/domain-layer-rules.md, /guide/rules/adapter-layer-rules.md, /marker/tactical/aggregateroot.md, /marker/port-out/repository.md, /marker/port-out/store.md, /decision/repository-vs-store.md, /pitfall/anemic-domain-model.md]
---

An outgoing adapter changes a lifecycle field itself. The repository adapter gains `markShipped(orderId)` that runs `UPDATE orders SET status = 'SHIPPED'`; an export job sets `exported = true` on the rows it wrote; a cleanup step rewrites `status: done` in a stored file. The aggregate has `ship()` with its guard and its `OrderShipped` event — and nobody calls it on this path.

```java
// the transition lives in the adapter
jdbc.update("UPDATE orders SET status = 'SHIPPED' WHERE id = ?", orderId.value());
```

## Why it is wrong

- **The transition has no guard.** `ship()` refuses an order that is not paid. The update does not ask; a cancelled order ships.
- **No event is raised.** Whoever reacts to `OrderShipped` — a notice, a projection, another context — never hears of this one.
- **The state has two ways in.** One path through the root, one past it. Undoing a state now has two answers as well, and the next change to the rule is made in one of them.
- **The same shape hides behind a store.** A port marked `Store` whose method takes the state to set (`save(entry, status=…)`, `setStatus(id, …)`) is a lifecycle without its aggregate: the transitions are written by every caller, none of them guarded.

## How to spot it

- An adapter or a store method with a state word in its name or its arguments: `mark…`, `set…Status`, `status=`, `delivered=`, `applied=`.
- An aggregate whose transition method is never called outside its tests.
- An event the model raises in one path and that is missing in a log of the other.

## What catches it

[Outgoing adapters must not call state-changing methods of aggregate roots](/rule/hexagonal/dca-hex-021.md) (experimental) holds the first form: an outgoing adapter calls no method of an aggregate root that changes its state. The direct write into storage and the store with a state argument stay a review question — a status column is an ordinary field to any static check.

## Do instead

Every transition is a method of the root, named after what it means (`ship()`, `complete()`, `reopen()`), with its guard and its event. A use case loads the aggregate, calls the method and saves. The repository's adapter is the only writer of the aggregate's fields, and it writes what the aggregate holds — never a state it decided. Where a store is about to carry a status, the thing with a status is an aggregate: give it its root and a repository ([Repository vs. Store](/decision/repository-vs-store.md)).

## Anchors

- Guide: [Domain layer rules](/guide/rules/domain-layer-rules.md) · [Adapter layer rules](/guide/rules/adapter-layer-rules.md)
- Rule: [Outgoing adapters must not call state-changing methods of aggregate roots](/rule/hexagonal/dca-hex-021.md)
- Markers: [AggregateRoot](/marker/tactical/aggregateroot.md) · [Repository](/marker/port-out/repository.md) · [Store](/marker/port-out/store.md)
- Decision: [Repository vs. Store](/decision/repository-vs-store.md)
- Related pitfalls: [A copy of the aggregate decides](/pitfall/a-copy-of-the-aggregate-decides.md) · [Anemic domain model](/pitfall/anemic-domain-model.md)
