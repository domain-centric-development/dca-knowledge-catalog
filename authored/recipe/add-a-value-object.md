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

1. **Model it as a record** implementing `Value`, in the domain model package `domain/model/`, beside the aggregate that owns it (or the shared kernel if it is genuinely universal — [Shared kernel](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)). Generate from the [value-object template](/template/value-object.md). A final class is a permitted alternative if the team prefers it — it must then override `equals`/`hashCode` for attribute equality.
2. **Validate in the compact constructor** — reject invalid state at construction so an instance is always valid; throw on bad input rather than storing it. Give it **one factory per origin**: a value built from input and one rebuilt from storage run different checks, so each has its own named factory (`fromInput(...)`, `fromStored(...)`) and no neutral `of(...)` stands beside them. A value with one origin keeps its one factory.
3. **Keep it immutable** — records give you final fields and value equality for free; a class must be final, hold only final fields, and implement `equals`/`hashCode` itself. No setters; derive new values by returning new instances.
4. **Name from the ubiquitous language** — no technical suffixes (`Helper`, `Util`, `Utils`, `Impl`, `Implementation`) and no primitive obsession (wrap the primitive, don't pass a bare `String`). A value from a fixed set — a role, a status, a kind — is an enum when its members are names and nothing more, and a value object with one instance per member as soon as a member carries data of its own (a code, a label, a rule); a class of string constants still lets every other string through. Its operations take and return its own kind — a quantity reduced by a quantity, not by a bare number.
5. **Never embed an aggregate root or entity** inside a value object; hold their `Id` if a reference is needed.
6. **Verify** — the project's architecture suite (`./gradlew test-architecture`, or `dotnet test -c Debug` against the architecture-test project).

## Rules to satisfy (build-time checklist)

- [Value object classes should be final (immutability)](/rule/tactical/dca-tac-009.md)
- [Value object fields must be final (deep immutability)](/rule/tactical/dca-tac-010.md)
- [Value objects must not have setter methods](/rule/tactical/dca-tac-011.md)
- [Value objects must not contain aggregate roots or entities](/rule/tactical/dca-tac-008.md)
- [Value Objects must be records or immutable classes with attribute equality](/rule/tactical/dca-tac-012.md)
- [Domain classes must not use technical suffixes (Helper, Util, Utils, Impl, Implementation)](/rule/naming/dca-nam-010.md)

## Anchors

- Template: [Value object skeleton](/template/value-object.md)
- Decision: [Entity vs. value object](/decision/entity-vs-value-object.md)
- Marker: [Value](/marker/tactical/value.md)
- Guide: [Layer elements](/guide/elements.md) · [Shared kernel](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)
- Used inside an [aggregate](/recipe/add-an-aggregate.md)
