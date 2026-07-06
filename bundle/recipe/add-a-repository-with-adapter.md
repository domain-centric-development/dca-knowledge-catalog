---
type: Recipe
title: "Add a repository with adapter"
tags: [recipe, adapter, repository]
---

Give an aggregate root a persistence port: an interface in the application layer, an implementation in an outgoing adapter. The interface belongs to the domain-facing side (an output port); the storage technology stays behind the boundary. One repository per aggregate root.

## Steps

1. **Define the interface** `{Name}Repository extends Repository<{Name}, {Name}Id>` in `application/shared/` — this is an output port, so it holds only interfaces. It inherits `findById`, `save`, `deleteById`; add finders that return the aggregate root (or collections of it).
2. **Only for aggregate roots** — no repositories for entities or value objects inside the aggregate; reach them through the root.
3. **Implement in an outgoing adapter** — e.g. `InMemory{Name}Repository` in `adapter/outgoing/`, generated from the [repository + in-memory adapter template](/template/repository-with-in-memory-adapter.md). The implementation may use framework/persistence types; the interface must not.
4. **Wire by inversion** — use cases depend on the interface (constructor injection); the adapter is the only thing that knows the store. Controllers and resources must never touch a repository directly — they go through the input port.
5. **Use explicit `save()`** — persistence-oriented style, not a live collection illusion ([ADR-004](/adr/adr-004-persistence-oriented-repository.md)). The use case calls `save` after mutating, then publishes domain events.
6. **Verify** — `./gradlew test-architecture`.

## Rules to satisfy (build-time checklist)

- [Repositories must only exist for aggregate roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md)
- [Repository interfaces should extend the Repository marker](/rule/tactical/repository-interfaces-should-extend-repository-marker-interface.md)
- [Repository interfaces must reside in the application output-port package](/rule/tactical/repository-interfaces-must-reside-in-application-output-port-package.md)
- [Repository implementations must reside in the adapter.outgoing package](/rule/tactical/repository-implementations-must-reside-in-adapter-outgoing-package.md)
- [Repository methods must return aggregate roots](/rule/tactical/repository-methods-must-return-aggregate-roots.md)
- [Repository interfaces must end with `Repository`](/rule/naming/repository-interfaces-must-end-with-repository.md)
- [Controllers and resources must never access repositories directly](/rule/hexagonal/controllers-and-resources-must-never-access-repositories-directly.md)
- [Output ports in application.shared must extend OutputPort](/rule/hexagonal/output-ports-in-application-shared-must-extend-outputport.md)

## Anchors

- Template: [Repository + in-memory adapter skeleton](/template/repository-with-in-memory-adapter.md) — JPA variant: [JPA repository adapter](/template/jpa-repository-adapter.md)
- Markers: [Repository<T, ID>](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md)
- ADRs: [ADR-004 Persistence-Oriented Repository](/adr/adr-004-persistence-oriented-repository.md) · [ADR-008 Repository Interfaces as Output Ports](/adr/adr-008-repository-interfaces-as-output-ports.md)
- Book: [Repository interfaces](/book/06-application-layer/repository-interfaces.md) · [Outgoing adapters](/book/07-adapter-layer/outgoing-adapters.md)
- The aggregate this repository serves: [Add an aggregate](/recipe/add-an-aggregate.md)
- Going to a database later: [Swap the in-memory adapter for JPA](/recipe/swap-in-memory-for-jpa.md)
- Pitfall: [A Repository for a non-aggregate](/pitfall/repository-for-non-aggregate.md) — non-aggregate data gets a Store ([Repository vs Store](/decision/repository-vs-store.md))
