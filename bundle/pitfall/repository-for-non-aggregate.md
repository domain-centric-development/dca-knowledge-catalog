---
type: Pitfall
title: "A Repository for something that is not an aggregate root"
tags: [pitfall, tactical, repository, aggregate, port-out, persistence]
---

Declaring a `Repository` for an entity that lives inside an aggregate, for a value object, or for read-only projection data — `OrderLineRepository`, `MoneyRepository`, `OrderSummaryRepository`. The shape is seductive: it persists, so it "must" be a repository. But a Repository is the collection-like access point for an **aggregate root**, not a generic persistence interface.

## Why it is wrong

- It breaks the aggregate boundary. An entity inside an aggregate (an order line) must be reached *through* its root; a dedicated repository lets callers load and mutate it independently, so the root can no longer guarantee its invariants.
- It confers a false identity and lifecycle. Repositories model `findById`/`save`/`delete` — aggregate-lifecycle operations. A value object has no independent identity to find by; giving it one is a category error.
- `repository.save(entity)` on a non-root creates two write paths to the same data (through the root and around it), inviting inconsistency.
- Read-model access dressed as a Repository blurs the command/query line: a projection is not an aggregate you load-mutate-save.

## What forbids it

- [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md) — mechanically the constraint: a `Repository<T, ID>` is legal only when `T` is an aggregate root.
- [Repository methods must return Aggregate Roots](/rule/tactical/repository-methods-must-return-aggregate-roots.md) — so a repository over lines, values, or summaries can't honour its own method contracts.

## Do instead

Reach entities and value objects through their aggregate root's repository. For persistence-shaped needs that are *not* an aggregate — recording an event, counting, checking existence, storing operational or projection data — use a **Store** (an `OutputPort`) instead: `record`/`count`/`exists`, no identity, no lifecycle.

`OrderRepository` (root only); order lines loaded via the `Order`. `AuditEntryStore extends Store` for append-only records — not `AuditEntryRepository`.

- [Template: repository with in-memory adapter](/template/repository-with-in-memory-adapter.md) · [Recipe: add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
- Decisions: [Repository vs Store](/decision/repository-vs-store.md) · [Read model vs domain query](/decision/read-model-vs-domain-query.md)

## Anchors

- Rules: [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md) · [Repository methods must return Aggregate Roots](/rule/tactical/repository-methods-must-return-aggregate-roots.md)
- Markers: [Repository&lt;T, ID&gt;](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md) · [AggregateRoot&lt;T, ID&gt;](/marker/tactical/aggregateroot.md)
- Guide: [Layer elements](/guide/readme/elements.md) · [Layer rules](/guide/readme/rules.md)
