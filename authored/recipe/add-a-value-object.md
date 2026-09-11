---
type: Recipe
title: Add a value object
tags: [recipe, domain, value-object]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/spring-modulith/shared-kernel-in-spring-modulith.md, /rule/tactical/dca-tac-009.md, /rule/tactical/dca-tac-010.md, /rule/tactical/dca-tac-011.md, /rule/tactical/dca-tac-008.md, /rule/tactical/dca-tac-012.md, /rule/naming/dca-nam-010.md, /marker/tactical/value.md]
---

Add an immutable value object — a concept defined by its attributes, with no identity (`Money`, `EmailAddress`, a quantity). A Java record implementing the `Value` marker, validated on construction, is the default. When in doubt whether it should be an entity, decide first.

## Step 0 — decide (do this first)

If the concept has a lifecycle and identity that must be tracked over time, it is an entity, not a value object — see [Entity vs. value object](/decision/entity-vs-value-object.md).

## Steps

1. **Model it as a record** implementing `Value`, in the owning aggregate's `domain/{concept}/` package (or the shared kernel if it is genuinely universal — [Shared kernel](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)). Generate from the [value-object template](/template/value-object.md). A final class is a permitted alternative if the team prefers it — it must then override `equals`/`hashCode` for attribute equality.
2. **Validate in the compact constructor** — reject invalid state at construction so an instance is always valid; throw on bad input rather than storing it.
3. **Keep it immutable** — records give you final fields and value equality for free; a class must be final, hold only final fields, and implement `equals`/`hashCode` itself. No setters; derive new values by returning new instances.
4. **Name from the ubiquitous language** — no technical suffixes (`Manager`, `Helper`, `Util`, `Impl`) and no primitive obsession (wrap the primitive, don't pass a bare `String`).
5. **Never embed an aggregate root or entity** inside a value object; hold their `Id` if a reference is needed.
6. **Verify** — the project's architecture suite (`./gradlew test-architecture`, or `dotnet test -c Debug` against the architecture-test project).

## Rules to satisfy (build-time checklist)

- [Value object classes should be final (immutability)](/rule/tactical/dca-tac-009.md)
- [Value object fields must be final (deep immutability)](/rule/tactical/dca-tac-010.md)
- [Value objects must not have setter methods](/rule/tactical/dca-tac-011.md)
- [Value objects must not contain aggregate roots or entities](/rule/tactical/dca-tac-008.md)
- [Value Objects must be records or immutable classes with attribute equality](/rule/tactical/dca-tac-012.md)
- [Domain classes must not use technical suffixes (Manager, Helper, Util, Impl, Implementation)](/rule/naming/dca-nam-010.md)

## Anchors

- Template: [Value object skeleton](/template/value-object.md)
- Decision: [Entity vs. value object](/decision/entity-vs-value-object.md)
- Marker: [Value](/marker/tactical/value.md)
- Guide: [Layer elements](/guide/elements.md) · [Shared kernel](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)
- Used inside an [aggregate](/recipe/add-an-aggregate.md)
