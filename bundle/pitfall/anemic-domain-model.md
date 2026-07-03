---
type: Pitfall
title: "Anemic domain model"
tags: [pitfall, tactical, aggregate, domain]
---

Aggregates and entities reduced to bags of getters and setters, with all the business rules living in application-layer services that reach in, read fields, compute, and write them back. The domain classes hold data; the "logic" lives outside them. This is the most common way a rich domain model quietly decays into a database-row-with-accessors.

## Why it is wrong

- Invariants can't be protected. If any caller can `setStatus(...)` or `setBalance(...)`, the aggregate can't guarantee it is ever in a valid state — the whole point of an aggregate boundary is lost.
- Business rules scatter. The same rule gets re-implemented in every service that touches the data, so behaviour drifts and Shotgun Surgery sets in.
- The ubiquitous language disappears from the model. `order.setStatus(SHIPPED)` says nothing; `order.ship()` names a domain operation and can enforce that only a paid order ships.
- It defeats the layering: application services become fat transaction scripts operating on dumb structs, and the domain layer carries no value.

## What forbids it

- [Domain model classes must not have public setter methods](/rule/tactical/domain-model-classes-must-not-have-public-setter-methods.md) — mechanically blocks the setter-driven mutation this anti-pattern depends on.
- [Value Objects must not have setter methods](/rule/tactical/value-objects-must-not-have-setter-methods.md) — value objects are immutable; you replace them, not mutate them.
- [Aggregate Roots must not hold references to repositories or other output ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md) — behaviour belongs on the aggregate, but it operates on its own state, not by calling out.

## Do instead

Put the behaviour where the data is. Expose intention-revealing methods that mutate state through guarded operations and enforce invariants internally; let the application service merely load the aggregate, invoke one behaviour, and save it.

`order.ship()` (validates, mutates, raises `OrderShipped`) — **not** `order.setStatus(SHIPPED)` in a service.

- [Recipe: add an aggregate](/recipe/add-an-aggregate.md) · [Template: aggregate root](/template/aggregate-root.md)

## Anchors

- ADRs: [ADR-021 Enriched Domain Model Pattern](/adr/adr-021-enriched-domain-model-pattern.md)
- Markers: [AggregateRoot&lt;T, ID&gt;](/marker/tactical/aggregateroot.md) · [Entity&lt;T, ID&gt;](/marker/tactical/entity.md)
- Book: [Domain Layer — Common Mistakes](/book/05-domain-layer/common-mistakes.md) · [Tactical Building Blocks](/book/05-domain-layer/tactical-building-blocks.md)
- Related decision: [Entity vs Value Object](/decision/entity-vs-value-object.md)
