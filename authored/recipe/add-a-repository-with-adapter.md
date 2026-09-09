---
type: Recipe
title: Add a repository with adapter
tags: [recipe, adapter, repository]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/readme/rules.md, /rule/tactical/dca-tac-016.md, /rule/tactical/dca-tac-013.md, /rule/tactical/dca-tac-014.md, /rule/tactical/dca-tac-015.md, /rule/tactical/dca-tac-017.md, /rule/naming/dca-nam-004.md, /rule/hexagonal/dca-hex-003.md]
---

Give an aggregate root a persistence port: an interface in the application layer, an implementation in an outgoing adapter. The interface belongs to the domain-facing side (an output port); the storage technology stays behind the boundary. One repository per aggregate root.

## Steps

1. **Define the interface** `{Name}Repository extends Repository<{Name}, {Name}Id>` in `application/shared/` — this is an output port, so it holds only interfaces. It inherits `findById`, `save`, `deleteById`; add finders that return the aggregate root (or collections of it).
2. **Only for aggregate roots** — no repositories for entities or value objects inside the aggregate; reach them through the root.
3. **Choose the persistence technique** — the port does not change with it; the adapter does:
   - **In-memory** ([repository + in-memory adapter](/template/repository-with-in-memory-adapter.md)) — start here: a `ConcurrentHashMap` behind the port, copying on write *and* on read, plus a contract test on the port that every later implementation runs.
   - **JDBC** ([JDBC repository adapter](/template/jdbc-repository-adapter.md)) — when you want explicit SQL and full control over the schema: a row mapper that calls the aggregate's `reconstitute` factory, no entity classes.
   - **JPA** ([JPA repository adapter](/template/jpa-repository-adapter.md)) — when the team's tooling is ORM-based: a separate `{Name}Entity` with the mapping annotations and a mapper between entity and aggregate, so the domain stays annotation-free.
4. **Implement in an outgoing adapter** — e.g. `InMemory{Name}Repository` in `adapter/outgoing/`. The implementation may use framework/persistence types; the interface must not. Every adapter hands out copies through `reconstitute`, never the stored instance ([Layer rules](/guide/readme/rules.md)).
5. **Wire by inversion** — use cases depend on the interface (constructor injection); the adapter is the only thing that knows the store. Controllers and resources must never touch a repository directly — they go through the input port.
6. **Use explicit `save()`** — persistence-oriented style, not a live collection illusion ([Layer rules](/guide/readme/rules.md)). The use case calls `save` after mutating, then `publishAndClearEvents` — one call, not a loop over `publish(event)` ([Publishing events one by one](/pitfall/publish-instead-of-publish-and-clear.md)).
7. **Verify** — `./gradlew test-architecture`.

## Rules to satisfy (build-time checklist)

- [Repositories must only exist for aggregate roots](/rule/tactical/dca-tac-016.md)
- [Repository interfaces should extend the Repository marker](/rule/tactical/dca-tac-013.md)
- [Repository interfaces must reside in the application output-port package](/rule/tactical/dca-tac-014.md)
- [Repository implementations must reside in the adapter.outgoing package](/rule/tactical/dca-tac-015.md)
- [Repository methods must not return non-root Entities](/rule/tactical/dca-tac-017.md)
- [Repository interfaces must end with `Repository`](/rule/naming/dca-nam-004.md)
- [Controllers and resources must never access repositories directly](/rule/hexagonal/dca-hex-003.md)
- [Output ports in application.shared must extend OutputPort](/rule/hexagonal/dca-hex-009.md)

## Anchors

- Templates: [Repository + in-memory adapter skeleton](/template/repository-with-in-memory-adapter.md) · [JDBC repository adapter](/template/jdbc-repository-adapter.md) · [JPA repository adapter](/template/jpa-repository-adapter.md)
- Markers: [Repository<T, ID>](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md)
- Guide: [Layer rules](/guide/readme/rules.md) · [Deviations from the literature](/guide/readme/deviations-from-the-literature.md) · [Layer elements](/guide/readme/elements.md) · [Ports and adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- The aggregate this repository serves: [Add an aggregate](/recipe/add-an-aggregate.md)
- Going to a database later: [Swap the in-memory adapter for JPA](/recipe/swap-in-memory-for-jpa.md)
- Bulk methods on the port: [Add a bulk operation](/recipe/add-a-bulk-operation.md)
- Pitfalls: [Repository name does not match the aggregate](/pitfall/repository-name-does-not-match-aggregate.md) · [Reconstitution raises the creation event](/pitfall/reconstitution-raises-creation-event.md) · [A Repository for a non-aggregate](/pitfall/repository-for-non-aggregate.md) — non-aggregate data gets a Store ([Repository vs Store](/decision/repository-vs-store.md))
