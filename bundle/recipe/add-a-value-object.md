---
type: Recipe
title: "Add a value object"
tags: [recipe, domain, value-object]
---

Add an immutable value object — a concept defined by its attributes, with no identity (`Money`, `EmailAddress`, a quantity). A Java record implementing the `Value` marker, validated on construction, is the default. When in doubt whether it should be an entity, decide first.

## Step 0 — decide (do this first)

If the concept has a lifecycle and identity that must be tracked over time, it is an entity, not a value object — see [Entity vs. value object](/decision/entity-vs-value-object.md).

## Steps

1. **Model it as a record** implementing `Value`, in the owning aggregate's `domain/{concept}/` package (or the shared kernel if it is genuinely universal — [ADR-016](/adr/adr-016-shared-kernel-pattern.md)). Generate from the [value-object template](/template/value-object.md).
2. **Validate in the compact constructor** — reject invalid state at construction so an instance is always valid; throw on bad input rather than storing it.
3. **Keep it immutable** — records give you final fields and value equality for free. No setters; derive new values by returning new instances.
4. **Name from the ubiquitous language** — no technical suffixes (`Manager`, `Helper`, `Util`, `Impl`) and no primitive obsession (wrap the primitive, don't pass a bare `String`).
5. **Never embed an aggregate root or entity** inside a value object; hold their `Id` if a reference is needed.
6. **Verify** — `./gradlew test-architecture`.

## Rules to satisfy (build-time checklist)

- [Value object classes should be final (immutability)](/rule/tactical/value-object-classes-should-be-final-immutability.md)
- [Value object fields must be final (deep immutability)](/rule/tactical/value-object-fields-must-be-final-deep-immutability.md)
- [Value objects must not have setter methods](/rule/tactical/value-objects-must-not-have-setter-methods.md)
- [Value objects must not contain aggregate roots or entities](/rule/tactical/value-objects-must-not-contain-aggregate-roots-or-entities.md)
- [Records for value objects are the preferred pattern](/rule/tactical/records-for-value-objects-are-allowed-preferred-pattern-for-simple-value-objects.md)
- [Domain classes must not use technical suffixes (Manager, Helper, Util, Impl)](/rule/naming/domain-classes-must-not-use-technical-suffixes-manager-helper-util-impl.md)

## Anchors

- Template: [Value object skeleton](/template/value-object.md)
- Decision: [Entity vs. value object](/decision/entity-vs-value-object.md)
- Marker: [Value](/marker/tactical/value.md)
- ADRs: [ADR-009 Value Objects as Records](/adr/adr-009-value-objects-as-records.md) · [ADR-016 Shared Kernel Pattern](/adr/adr-016-shared-kernel-pattern.md)
- Book: [Tactical building blocks](/book/05-domain-layer/tactical-building-blocks.md) · [Shared value objects](/book/11-shared-kernel/shared-value-objects.md)
- Used inside an [aggregate](/recipe/add-an-aggregate.md)
