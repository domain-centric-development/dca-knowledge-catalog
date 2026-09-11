---
type: Recipe
title: Add a store
tags: [recipe, application, port-out, persistence]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/hexagonal/dca-hex-009.md, /rule/tactical/dca-tac-018.md, /rule/tactical/dca-tac-019.md, /rule/tactical/dca-tac-020.md, /rule/tactical/dca-tac-021.md, /marker/port-out/store.md, /marker/port-out/outputport.md, /marker/port-out/repository.md]
---

Give a context a persistence port for operational data that has **no aggregate of its own** — login attempts, an audit trail, metric snapshots, an event log. A Store is the sibling of a Repository: both `extend OutputPort` and keep persistence out of the domain (interface in the application layer, implementation in an outgoing adapter), but a Store *records and queries* rather than *loads, mutates and saves* a managed Aggregate Root. Reach for it when the data is a `record`/Value by nature and there is no identity-based lifecycle to manage. Compare with [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md), which is the aggregate-root counterpart.

## Steps

1. **Confirm it is a Store, not a Repository.** Run [Repository vs Store](/decision/repository-vs-store.md). Rule of thumb: need `findById()` / `save()` on a managed root → **Repository**; need `record()` / `count()` / `exists()` on appended operational data → **Store**. If the thing has no identity-based load/mutate/save lifecycle, it must be a Store — you cannot correctly model non-aggregate data as a Repository.
2. **Define the interface** `{Name}Store extends Store` in `application/shared/` — an output port, so interfaces only. Name the methods for the operational role in the ubiquitous language: `record(...)`, `count(...)`, `findAll()`, `exists(...)`. Do **not** expose aggregate-lifecycle methods (`findById`, `save`, `deleteById`) — that shape belongs to a Repository.
3. **Implement in an outgoing adapter** — e.g. `InMemory{Name}Store` or `Jdbc{Name}Store` in `adapter/outgoing/persistence/`, generated from the [store + in-memory adapter template](/template/store-with-in-memory-adapter.md). The implementation may use framework/persistence types; the interface must not.
4. **Wire by inversion** — use cases depend on the `{Name}Store` interface (constructor injection); only the adapter knows the store technology. Controllers and resources never touch it directly — they go through an input port.
5. **Verify** — the project's architecture suite (`./gradlew test-architecture`, or `dotnet test -c Debug` against the architecture-test project). Four rules govern Store, so a violation of steps 2 and 3 fails the build rather than surviving review.

## Rules to satisfy (build-time checklist)

- [Output ports in application.shared must extend OutputPort](/rule/hexagonal/dca-hex-009.md) *(a Store satisfies this transitively — `Store extends OutputPort`)*
- [Store interfaces must extend the Store marker, not Repository](/rule/tactical/dca-tac-018.md)
- [Store interfaces must reside in the application layer's shared output-port package](/rule/tactical/dca-tac-019.md)
- [Store implementations must reside in the adapter.outgoing package](/rule/tactical/dca-tac-020.md)
- [Store interfaces must not declare findById or save methods](/rule/tactical/dca-tac-021.md)

## Anchors

- Template: [Store + in-memory adapter skeleton](/template/store-with-in-memory-adapter.md)
- Markers: [Store](/marker/port-out/store.md) · [OutputPort](/marker/port-out/outputport.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md)
- Decision: [Repository or Store: which output port persists this](/decision/repository-vs-store.md)
- Guide: [Deviations from the literature](/guide/readme/deviations-from-the-literature.md) · [Layer rules](/guide/rules.md) · [Layer elements](/guide/elements.md) · [Port placement](/guide/quick-reference/port-placement.md)
- Sibling recipe: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
- Pitfall: [A Repository for a non-aggregate](/pitfall/repository-for-non-aggregate.md)
