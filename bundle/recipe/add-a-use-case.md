---
type: Recipe
title: "Add a use case"
tags: [recipe, application, use-case]
---

Add one application-layer use case (a single intention: place an order, add an item, get a product). Self-contained folder, four files, framework only in the implementation.

## Steps

1. **Find the context's form, then create the folder.** Look at the packages directly below `application/` (ignore `shared`). If they are use cases, the context is *flat*: create `application/{usecasename}/`. If they are features — domain-named groups such as `session` or `cartrecovery` that themselves contain use-case folders — the context is *grouped*: pick the feature the new use case belongs to (or add one, named from the ubiquitous language, never `commands`/`queries`/`handlers`) and create `application/{feature}/{usecasename}/`. Never add a flat use case to a grouped context or a grouped one to a flat context — the mixed form is a rule violation. The folder name is lowercase, no separators (e.g. `additemtocart`). When to introduce features at all: [Group use cases into features or split the bounded context](/decision/group-use-cases-vs-split-context.md).
2. **Pick write or read** — a write takes a `{Name}Command`; a read takes a `{Name}Query`.
3. **Generate the four files** from the [use-case template](/template/use-case.md): `{Name}InputPort`, `{Name}Command`/`{Name}Query`, `{Name}Result`, `{Name}UseCase`.
4. **Declare output ports** the use case needs (repositories, publishers) as constructor parameters — interfaces only, defined in `application/shared/` or the marker package; never reference adapters.
5. **Implement `execute`** — load aggregate(s) via ports, run business logic *on the aggregate* (not in the service), persist, then publish + clear domain events for writes (in that order — `save` first), then assemble `{Name}Result`: values only — ids, value objects, nested part records named by content, read models — never the aggregate or an entity, also not inside a `List`/`Optional`. A command answers small (ids, status, what the caller needs next); a query answers with the read model or snapshot. Assemble in the application layer: static `from(...)` on the result, the use-case body when several ports feed it, a `*Assembler` when it grows or is shared. See [Result shape and assembly](/decision/result-shape-and-assembly.md).
6. **Draw the transaction boundary** — class-level `@Transactional` when every port is local; when the use case also reads from a remote-capable port (another context's API, a payment provider), do the remote reads first and wrap load–mutate–save–publish in `transactionBoundary.inTransaction(...)` instead. Read-only use cases get neither. See [Declarative or explicit transaction boundary](/decision/declarative-vs-explicit-transaction-boundary.md).
7. **Expose it** from an incoming adapter (`*Resource`/`*PageController`) that maps `{Name}Result` → a `*Response` DTO at the edge.
8. **Verify** — run `./gradlew test-architecture`; the rules below are checked.

## Rules to satisfy (build-time checklist)

- [Input port extends UseCase and the impl is the InputPort](/marker/port-in/usecase.md)
- [Use case classes must be annotated with @Service](/rule/naming/use-case-classes-must-be-annotated-with-service.md)
- [Commands must end with `Command` and reside in the application package](/rule/usecase/use-case-commands-must-end-with-command-and-reside-in-application-package.md)
- [Queries must end with `Query` and reside in the application package](/rule/usecase/use-case-queries-must-end-with-query-and-reside-in-application-package.md)
- [Result models must end with `Result` and reside in the application package](/rule/usecase/use-case-result-models-must-end-with-result-and-reside-in-application-package.md)
- [Commands/Queries/Results should be immutable (records)](/rule/usecase/use-case-result-models-should-be-immutable-final-or-records.md)
- [Results must not expose aggregate roots or entities](/rule/usecase/use-case-result-models-must-not-expose-aggregate-roots-or-entities.md)
- [DTOs must not be used in the application layer](/rule/usecase/dtos-must-not-be-used-in-the-application-layer.md)
- [Use cases that publish domain events must have a transaction boundary](/rule/usecase/use-cases-that-publish-domain-events-must-have-a-transaction-boundary.md)
- [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md)
- [Use case packages within a module must use one consistent depth — flat or grouped by feature](/rule/usecase/use-case-packages-within-a-module-must-use-one-consistent-depth-flat-or-grouped-by-feature.md)
- [Feature and use case packages within a module's application layer must not have cyclic dependencies](/rule/cycles/feature-and-use-case-packages-within-a-module-s-application-layer-must-not-have-cyclic-dependencies.md)

## Anchors

- Template: [Use case skeleton](/template/use-case.md)
- Markers: [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md) · [InputPort](/marker/port-in/inputport.md)
- Guide: [Layer rules](/guide/readme/rules.md) · [Deviations from the literature](/guide/readme/deviations-from-the-literature.md) · [Layer elements](/guide/readme/elements.md)
- If the use case must notify another context: [Publish a cross-context event](/recipe/publish-a-cross-context-event.md)
- Shaping the answer: [Result shape and assembly](/decision/result-shape-and-assembly.md)
- If the flat list has grown long: [Group use cases into features or split the bounded context](/decision/group-use-cases-vs-split-context.md) — migrate the whole context in one move, never one use case at a time
- Pitfall: [The god port](/pitfall/god-port.md) — one InputPort per use case, never one fat interface for many
- Pitfalls: [Remote call inside a transaction](/pitfall/remote-call-inside-a-transaction.md) · [Publishing domain events without a transaction](/pitfall/publishing-domain-events-without-a-transaction.md) · [Clearing domain events before dispatch](/pitfall/clearing-domain-events-before-dispatch.md)
