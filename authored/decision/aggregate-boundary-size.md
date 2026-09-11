---
type: Decision
title: "Aggregate boundary: one big aggregate or several small ones"
tags: [decision, tactical, aggregate, entity]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/aggregateroot.md, /marker/tactical/entity.md, /marker/tactical/id.md, /marker/port-out/repository.md, /rule/tactical/dca-tac-003.md, /rule/tactical/dca-tac-007.md, /rule/tactical/dca-tac-016.md, /rule/tactical/dca-tac-017.md]
---

Once you know a concept is an Aggregate Root, the next fork is how much to pull *inside* its boundary. Everything inside an aggregate is loaded, saved, and kept consistent as one unit in one transaction — so the boundary is a design decision about **consistency and transaction scope**, not about how objects happen to relate on a diagram. Draw it too wide and every change locks a large object graph; draw it right and each aggregate stays small, loadable, and independently consistent.

## The discriminator

Ask, in order:

1. **What is the true invariant?** An invariant is a rule that must hold *at every commit*. The aggregate boundary must be exactly wide enough to enforce it and no wider. If two pieces of data must always agree the instant a transaction ends (an order total must equal the sum of its lines), they belong in the **same** aggregate. If they may be briefly inconsistent and reconciled later, they belong in **separate** aggregates linked by an event.
2. **Would this other thing have its own lifecycle?** If a contained object is created, changed, and retired on its *own* schedule — and other parts of the system need to load it directly — it is a separate Aggregate Root, not an inner Entity. Inner Entities have no independent life; they are reached only through the root.
3. **Does anyone need a repository for it?** Only Aggregate Roots get a repository. If you find yourself wanting `findById` for an inner part, that part is really its own aggregate.
4. **How big does it get at runtime?** A boundary that grows an unbounded collection (all a customer's orders inside `Customer`) forces you to load thousands of rows to touch one. Prefer small — reference the many by ID.

## Options

| | One larger aggregate | Several small aggregates |
|---|---|---|
| Use when | pieces share a real must-hold-now invariant and are always changed together | pieces have separate lifecycles or only need eventual consistency |
| Consistency | strong, inside one transaction | strong *within* each; eventual *between* them (via domain events) |
| Cross reference | inner Entities held by object, guarded by the root | other aggregates referenced **by Id only**, never by object |
| Repository | one, on the root | one per root |
| Risk | large load/lock footprint, contention | must design for eventual consistency between them |

**Default: prefer small aggregates.** Keep the boundary to the smallest cluster that still enforces one true invariant, and reference every other aggregate by its `Id`. This is Vernon's "reference other aggregates by identity" rule, and it is mechanically enforced: an Aggregate Root may not hold a field of another Aggregate Root type. When two small aggregates must stay in step, connect them with a domain event and accept eventual consistency between them rather than fusing them into one.

## Consequences

- Cross-aggregate references go by `Id` — an `Order` holds a `CustomerId`, never a `Customer` — so the two are persisted, loaded, and versioned independently. This is checked by an ArchUnit rule (see anchors).
- One transaction should modify one aggregate. Coordinating a change across two aggregates means raising a domain event and letting the second react, not saving both in the same call.
- Only the root gets a repository, and repository methods return the root. Wanting a repository for an inner Entity is the signal that your boundary is drawn wrong.

## Anchors

- Markers: [AggregateRoot&lt;T, ID&gt;](/marker/tactical/aggregateroot.md) · [Entity&lt;T, ID&gt;](/marker/tactical/entity.md) · [Id](/marker/tactical/id.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md)
- Rules: [Aggregate Roots must not have fields with other Aggregate Root types](/rule/tactical/dca-tac-003.md) · [Entities must not have fields with Aggregate Root types](/rule/tactical/dca-tac-007.md) · [Repositories must only exist for Aggregate Roots](/rule/tactical/dca-tac-016.md) · [Repository methods must not return non-root Entities](/rule/tactical/dca-tac-017.md)
- Guide: [Layer elements](/guide/elements.md) · [Layer rules](/guide/rules.md)
- Recipes: [Add an aggregate](/recipe/add-an-aggregate.md) · [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
- Related decision: [Entity vs Value Object](/decision/entity-vs-value-object.md)
