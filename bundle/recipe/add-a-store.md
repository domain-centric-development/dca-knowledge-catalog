---
type: Recipe
title: "Add a store"
tags: [recipe, application, port-out, persistence]
---

Give a context a persistence port for operational data that has **no aggregate of its own** — login attempts, an audit trail, metric snapshots, an event log. A Store is the sibling of a Repository: both `extend OutputPort` and keep persistence out of the domain (interface in the application layer, implementation in an outgoing adapter), but a Store *records and queries* rather than *loads, mutates and saves* a managed Aggregate Root. Reach for it when the data is a `record`/Value by nature and there is no identity-based lifecycle to manage. Compare with [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md), which is the aggregate-root counterpart.

## Steps

1. **Confirm it is a Store, not a Repository.** Run [Repository vs Store](/decision/repository-vs-store.md). Rule of thumb: need `findById()` / `save()` on a managed root → **Repository**; need `record()` / `count()` / `exists()` on appended operational data → **Store**. If the thing has no identity-based load/mutate/save lifecycle, it must be a Store — you cannot correctly model non-aggregate data as a Repository.
2. **Define the interface** `{Name}Store extends Store` in `application/shared/` — an output port, so interfaces only. Name the methods for the operational role in the ubiquitous language: `record(...)`, `count(...)`, `findAll()`, `exists(...)`. Do **not** expose aggregate-lifecycle methods (`findById`, `save`, `deleteById`) — that shape belongs to a Repository.
3. **Implement in an outgoing adapter** — e.g. `InMemory{Name}Store` or `Jdbc{Name}Store` in `adapter/outgoing/persistence/`, generated from the [store + in-memory adapter template](/template/store-with-in-memory-adapter.md). The implementation may use framework/persistence types; the interface must not.
4. **Wire by inversion** — use cases depend on the `{Name}Store` interface (constructor injection); only the adapter knows the store technology. Controllers and resources never touch it directly — they go through an input port.
5. **Mind the governance gap.** Unlike Repository, **no ArchUnit rule governs Store today** — see [The Store marker has no governing rules](/note/store-marker-has-no-governing-rules.md). Nothing mechanically enforces that `*Store` extends the `Store` marker, avoids aggregate-lifecycle methods, or places the interface vs. implementation correctly. Hold the discipline by hand; `./gradlew test-architecture` will not catch a violation.
6. **Verify** — `./gradlew test-architecture` (still run it: the generic output-port rule below is enforced).

## Rules to satisfy (build-time checklist)

- [Output ports in application.shared must extend OutputPort](/rule/hexagonal/output-ports-in-application-shared-must-extend-outputport.md) *(a Store satisfies this transitively — `Store extends OutputPort`)*
- Store-specific placement and naming are **not enforced** — see [The Store marker has no governing rules](/note/store-marker-has-no-governing-rules.md). Keep the interface in `application/shared/` and the implementation in `adapter/outgoing/` by discipline.

## Anchors

- Template: [Store + in-memory adapter skeleton](/template/store-with-in-memory-adapter.md)
- Markers: [Store](/marker/port-out/store.md) · [OutputPort](/marker/port-out/outputport.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md)
- Decision: [Repository or Store: which output port persists this](/decision/repository-vs-store.md)
- Note: [The Store marker has no governing ArchUnit rules](/note/store-marker-has-no-governing-rules.md)
- ADRs: [ADR-008 Repository Interfaces as Output Ports](/adr/adr-008-repository-interfaces-as-output-ports.md) · [ADR-004 Persistence-Oriented Repository Pattern](/adr/adr-004-persistence-oriented-repository.md)
- Book: [Stores: persistence for non-aggregate data](/book/06-application-layer/stores-persistence-for-non-aggregate-data.md) · [Outgoing Adapters](/book/07-adapter-layer/outgoing-adapters.md)
- Sibling recipe: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
- Pitfall: [A Repository for a non-aggregate](/pitfall/repository-for-non-aggregate.md)
