---
type: Decision
title: "Entity or Value Object: modelling a domain concept"
tags: [decision, tactical, entity, value-object]
---

When you introduce a new domain concept, the first modelling fork is whether it is an **Entity** (has identity and a lifecycle) or a **Value Object** (defined entirely by its attributes). Getting this wrong is expensive: it decides equality, mutability, and whether the concept ever gets its own repository.

## The discriminator

Ask, in order:

1. **Does it need a stable identity that survives attribute changes?** If two instances with identical attributes must still be distinguishable — because each tracks *the same thing over time* — it is an **Entity**. If two instances with equal attributes are interchangeable, it is a **Value Object**.
2. **Does it have a lifecycle you track (created, changed, retired)?** A lifecycle implies identity → Entity. A snapshot of "what something is right now" → Value Object.
3. **Is equality by identity or by value?** Identity equality → Entity. Structural (all-fields) equality → Value Object.

A quick tell: if you find yourself wanting a setter, you probably reached for an Entity where a *new* Value Object would be cleaner — replace the whole value instead of mutating it.

## Options

| | Entity | Value Object |
|---|---|---|
| Identity | own `Id`, equality by identity | none, equality by all fields |
| Mutability | mutable state, guarded by behaviour | immutable — replace, never mutate |
| Persistence | reachable via a repository (only Aggregate Roots get one) | persisted *inside* an aggregate, never on its own |
| Marker | [Entity&lt;T, ID&gt;](/marker/tactical/entity.md) | [Value](/marker/tactical/value.md) |
| Build it | [Recipe: add an aggregate](/recipe/add-an-aggregate.md) · [Template: entity](/template/entity.md) | [Recipe: add a value object](/recipe/add-a-value-object.md) · [Template: value object](/template/value-object.md) |

Value Objects are the **default** — reach for a Value Object unless identity or lifecycle forces an Entity. Most "Entities" that turn out anemic were Value Objects in disguise. An Entity that is not the root of its aggregate must never be handed out or persisted on its own; only Aggregate Roots get repositories.

## Consequences

- A Value Object is `final`, its fields are `final`, and it exposes no setters — immutability is mechanically enforced (see anchors). If you need a "changed" value, construct a new one.
- An Entity must carry an `Id` and must not be instantiated from outside its aggregate — the Aggregate Root is the only factory.
- Neither may reference an Aggregate Root by object; cross-aggregate references go by `Id`.

## Anchors

- Markers: [Entity&lt;T, ID&gt;](/marker/tactical/entity.md) · [Value](/marker/tactical/value.md)
- Rules: [Value Object classes should be final](/rule/tactical/value-object-classes-should-be-final-immutability.md) · [Value Object fields must be final](/rule/tactical/value-object-fields-must-be-final-deep-immutability.md) · [Value Objects must not have setter methods](/rule/tactical/value-objects-must-not-have-setter-methods.md) · [Entities must have an ID field](/rule/tactical/entities-must-have-an-id-field.md) · [Entities must not be instantiated directly from outside the aggregate](/rule/tactical/entities-must-not-be-instantiated-directly-from-outside-the-aggregate.md)
- ADRs: [ADR-009 Value Objects as Records](/adr/adr-009-value-objects-as-records.md) · [ADR-003 Aggregate Reference by ID](/adr/adr-003-aggregate-reference-by-id.md)
- Book: [Tactical Building Blocks](/book/05-domain-layer/tactical-building-blocks.md) · [Common Patterns](/book/05-domain-layer/common-patterns.md)
- Related pitfall: [Anemic domain model](/pitfall/anemic-domain-model.md)
