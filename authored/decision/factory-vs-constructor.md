---
type: Decision
title: "Factory or constructor: how an aggregate gets created"
tags: [decision, tactical, factory, aggregate]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/factory.md, /marker/tactical/aggregateroot.md, /marker/tactical/id.md, /rule/advanced/dca-adv-013.md, /rule/advanced/dca-adv-014.md, /rule/advanced/dca-adv-016.md, /rule/advanced/dca-adv-015.md, /rule/tactical/dca-tac-005.md]
---

Every aggregate needs a way to come into existence. The fork is how elaborate that creation is: a plain **constructor** (or a static factory method on the aggregate itself) covers the common case, while a dedicated **Factory** (its own domain class) earns its place only when creation is genuinely complex. Reaching for a Factory too early adds a class that does nothing a static method wouldn't; skipping it when creation is complex scatters that logic across use cases.

## The discriminator

Ask, in order:

1. **Is construction trivial** — assign the fields, validate invariants, done? Then a **constructor** or a **static factory method on the aggregate** (`Order.create(customerId)`) is enough. This is the default; most aggregates never need more.
2. **Does creation involve real work** — generating IDs, raising a creation event, assembling from another aggregate or a collection of inputs? A static `create(...)` on the aggregate still handles most of this cleanly. Use it until it stops fitting.
3. **Does the creation logic itself deserve a name and a home** — because it is complex, reused, or builds one aggregate *from another* (an `Order` from a `Cart`)? Then extract a dedicated **Factory**: a stateless domain class implementing the `Factory` marker.

A quick tell: if you are copy-pasting the same multi-step assembly into several use cases, that assembly is a Factory waiting to be named.

## Options

| | Constructor / static factory method | Factory (marker) |
|---|---|---|
| Use when | fields + invariant checks; simple `create` | complex creation, ID generation, creation events, building one aggregate from another |
| Lives where | on the aggregate itself | its own class in the **domain** package |
| State | n/a | stateless — only final fields for dependencies |
| Framework | none | none — no Spring annotations |
| Signals intent | "this is how you make one" | "creation is a first-class domain operation" |

**Default: constructor or a static factory method on the aggregate.** A separate Factory is the exception — use it when aggregate creation is complex, involves ID generation, raises creation events, or assembles the aggregate from other domain objects. Even then, the Factory typically delegates to the aggregate's own `create` for the final step; it orchestrates the assembly, it does not bypass the aggregate's invariants.

## Consequences

- A Factory is a domain citizen: it must reside in the domain package, carry no Spring annotations, and stay stateless (only final fields for dependencies). These are ArchUnit-enforced (see anchors).
- A Factory should implement the `Factory` marker so it is discoverable and governed as a tactical pattern.
- Whichever route you pick, the aggregate remains the guardian of its invariants — entities are not instantiated from outside the aggregate, so the Factory works *with* the root, not around it.

## Anchors

- Markers: [Factory](/marker/tactical/factory.md) · [AggregateRoot&lt;T, ID&gt;](/marker/tactical/aggregateroot.md) · [Id](/marker/tactical/id.md)
- Rules: [Factories should implement Factory Marker Interface](/rule/advanced/dca-adv-013.md) · [Factories must reside in domain package](/rule/advanced/dca-adv-014.md) · [Factories should be stateless (only final fields for dependencies)](/rule/advanced/dca-adv-016.md) · [Factories must not have Spring annotations](/rule/advanced/dca-adv-015.md) · [Entities must not be instantiated directly from outside the aggregate](/rule/tactical/dca-tac-005.md)
- Guide: [Layer elements](/guide/readme/elements.md) · [Framework annotation rules](/guide/architecture-reference-guide/framework-annotations-rules.md) · [Java package structure](/guide/readme/java-package-structure.md)
- Recipes: [Add an aggregate](/recipe/add-an-aggregate.md)
- Template: [Factory skeleton](/template/factory.md)
- Related decision: [Entity vs Value Object](/decision/entity-vs-value-object.md)
