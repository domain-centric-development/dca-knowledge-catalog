---
type: Recipe
title: Add an aggregate
tags: [recipe, domain, aggregate]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/readme/deviations-from-the-literature.md, /rule/tactical/dca-tac-001.md, /rule/tactical/dca-tac-003.md, /rule/tactical/dca-tac-002.md, /rule/tactical/dca-tac-016.md, /rule/tactical/dca-tac-013.md, /rule/tactical/dca-tac-014.md, /marker/tactical/domainevent.md]
---

Add an aggregate root: the transactional consistency boundary that owns its invariants and emits domain events. Lives in the framework-free domain layer.

## Steps

1. **Model the boundary** — one aggregate = one consistency boundary. Keep it small; reference other aggregates by their `Id`, never by object.
2. **Create the package** `domain/{name}/` and generate from the [aggregate template](/template/aggregate-root.md): `{Name}Id` (typed identity), `{Name}` (root extends `BaseAggregateRoot`), `{Name}Created` (domain event).
3. **Enforce invariants in a factory** — `static {Name} create(...)` validates and registers the creation event. No public setters; mutate via intention-revealing methods that re-check invariants.
4. **Register domain events** on every meaningful state change; the use case publishes + clears them after save.
5. **Add the repository** — interface `{Name}Repository extends Repository<{Name}, {Name}Id>` in `application/shared/` (output port), implementation in `adapter/outgoing/` ([Deviations from the literature](/guide/readme/deviations-from-the-literature.md)). One repository per aggregate root only.
6. **Verify** — `./gradlew test-architecture`.

## Rules to satisfy (build-time checklist)

- [Aggregate roots must implement AggregateRoot<T, ID>](/rule/tactical/dca-tac-001.md)
- [Aggregate roots must not have fields with other aggregate-root types](/rule/tactical/dca-tac-003.md)
- [Aggregate roots must not hold references to repositories or other output ports](/rule/tactical/dca-tac-002.md)
- [Repositories must only exist for aggregate roots](/rule/tactical/dca-tac-016.md)
- [Repository interfaces should extend the Repository marker](/rule/tactical/dca-tac-013.md)
- [Repository interfaces must reside in the application output-port package](/rule/tactical/dca-tac-014.md)
- [Domain events must implement DomainEvent and be records](/marker/tactical/domainevent.md)

## Anchors

- Template: [Aggregate root skeleton](/template/aggregate-root.md)
- Markers: [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md) · [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md) · [DomainEvent](/marker/tactical/domainevent.md) · [Repository<T, ID>](/marker/port-out/repository.md)
- Guide: [Layer elements](/guide/readme/elements.md) · [Layer rules](/guide/readme/rules.md)
- Then expose behavior via [Add a use case](/recipe/add-a-use-case.md)
- Pitfall: [Modifying two aggregates in one transaction](/pitfall/modifying-two-aggregates-in-one-transaction.md) — size the boundary first ([Aggregate boundary and size](/decision/aggregate-boundary-size.md))
