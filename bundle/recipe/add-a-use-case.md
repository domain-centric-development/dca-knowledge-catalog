---
type: Recipe
title: "Add a use case"
tags: [recipe, application, use-case]
---

Add one application-layer use case (a single intention: place an order, add an item, get a product). Self-contained folder, four files, framework only in the implementation.

## Steps

1. **Create the folder** `application/{usecasename}/` — lowercase, no separators (e.g. `additemtocart`).
2. **Pick write or read** — a write takes a `{Name}Command`; a read takes a `{Name}Query`.
3. **Generate the four files** from the [use-case template](/template/use-case.md): `{Name}InputPort`, `{Name}Command`/`{Name}Query`, `{Name}Result`, `{Name}UseCase`.
4. **Declare output ports** the use case needs (repositories, publishers) as constructor parameters — interfaces only, defined in `application/shared/` or the marker package; never reference adapters.
5. **Implement `execute`** — load aggregate(s) via ports, run business logic *on the aggregate* (not in the service), persist, then publish + clear domain events for writes, map to `{Name}Result`.
6. **Expose it** from an incoming adapter (`*Resource`/`*PageController`) that maps `{Name}Result` → a `*Response` DTO at the edge.
7. **Verify** — run `./gradlew test-architecture`; the rules below are checked.

## Rules to satisfy (build-time checklist)

- [Input port extends UseCase and the impl is the InputPort](/marker/port-in/usecase.md)
- [Use case classes must be annotated with @Service](/rule/naming/use-case-classes-must-be-annotated-with-service.md)
- [Commands must end with `Command` and reside in the application package](/rule/usecase/use-case-commands-must-end-with-command-and-reside-in-application-package.md)
- [Queries must end with `Query` and reside in the application package](/rule/usecase/use-case-queries-must-end-with-query-and-reside-in-application-package.md)
- [Result models must end with `Result` and reside in the application package](/rule/usecase/use-case-result-models-must-end-with-result-and-reside-in-application-package.md)
- [Commands/Queries/Results should be immutable (records)](/rule/usecase/use-case-result-models-should-be-immutable-final-or-records.md)
- [DTOs must not be used in the application layer](/rule/usecase/dtos-must-not-be-used-in-the-application-layer.md)

## Anchors

- Template: [Use case skeleton](/template/use-case.md)
- Markers: [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md) · [InputPort](/marker/port-in/inputport.md)
- Guide: [Layer rules](/guide/readme/rules.md) · [Deviations from the literature](/guide/readme/deviations-from-the-literature.md) · [Layer elements](/guide/readme/elements.md)
- If the use case must notify another context: [Publish a cross-context event](/recipe/publish-a-cross-context-event.md)
- Pitfall: [The god port](/pitfall/god-port.md) — one InputPort per use case, never one fat interface for many
