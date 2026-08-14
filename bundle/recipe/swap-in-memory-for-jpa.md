---
type: Recipe
title: "Swap the in-memory adapter for JPA"
tags: [recipe, adapter, persistence, repository]
---

Move an aggregate from in-memory storage to a relational database **without touching the output port or the domain**. This is the payoff of the hexagonal boundary: the use cases depend on `{Name}Repository`, so replacing its implementation is invisible to them. The domain aggregate stays persistence-free; a separate JPA entity absorbs all the mapping.

## Steps

1. **Leave the port and the domain alone** — `{Name}Repository` in `application/shared/` and the `{Name}` aggregate do not change. If you find yourself editing either to make JPA fit, stop: that leak defeats the point (see [framework-leak-in-domain](/pitfall/framework-leak-in-domain.md)).
2. **Add a JPA entity** in `adapter/outgoing/persistence/jpa/` — a `@Entity` class distinct from the aggregate. Map aggregate parts as child tables cascaded from the root (`cascade = ALL`, `orphanRemoval = true`); embed value objects (`@Embeddable`) or flatten them to columns. Never cascade across an aggregate boundary.
3. **Add a Spring Data interface** `SpringData{Name}Repository extends JpaRepository<{Name}JpaEntity, ...>` — it speaks entities and primitives, and stays behind the boundary (never injected into a use case).
4. **Write the adapter** `Jpa{Name}RepositoryAdapter implements {Name}Repository`, from the [JPA repository adapter template](/template/jpa-repository-adapter.md). It owns the entity↔aggregate mapping and delegates persistence to the Spring Data interface. Keep the mapper pure — no business logic ([business-logic-in-adapter](/pitfall/business-logic-in-adapter.md)).
5. **Select the adapter by configuration, not by code change** — gate the two adapters on complementary profiles (`@Profile("!inmemory")` and `@Profile("inmemory")`), so exactly one bean exists and the use cases never notice. `@Primary` is the wrong tool here: it selects among *registered* beans, so it silently wins even when the profile says otherwise. Persistence stays explicit-`save()` (persistence-oriented, [Layer rules](/guide/readme/rules.md)), not a live-collection illusion.
6. **Set transaction boundaries** — annotate the adapter (or the use case) `@Transactional`; use `readOnly = true` for finders.
7. **Verify nothing above the port changed** — the existing use-case and domain tests must pass untouched; then `./gradlew test-architecture`.

## Rules to satisfy (build-time checklist)

- [Repository interfaces must reside in the application output-port package](/rule/tactical/repository-interfaces-must-reside-in-application-output-port-package.md) — the port stays put
- [Repository implementations must reside in the adapter.outgoing package](/rule/tactical/repository-implementations-must-reside-in-adapter-outgoing-package.md) — the new JPA adapter lives here
- [Repository interfaces should extend the Repository marker](/rule/tactical/repository-interfaces-should-extend-repository-marker-interface.md)
- [Repository methods must return aggregate roots](/rule/tactical/repository-methods-must-return-aggregate-roots.md) — the adapter maps entities back to the aggregate, never leaks entities
- [Repository interfaces must end with `Repository`](/rule/naming/repository-interfaces-must-end-with-repository.md)
- [Outgoing adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/outgoing-adapters-must-only-use-outbound-ports-not-infrastructure-implementations.md)
- [Controllers and resources must never access repositories directly](/rule/hexagonal/controllers-and-resources-must-never-access-repositories-directly.md)
- [Output ports in application.shared must extend OutputPort](/rule/hexagonal/output-ports-in-application-shared-must-extend-outputport.md)

## Anchors

- Templates: [JPA repository adapter](/template/jpa-repository-adapter.md) · [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md)
- Markers: [Repository<T, ID>](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md)
- Guide: [Layer rules](/guide/readme/rules.md) · [Deviations from the literature](/guide/readme/deviations-from-the-literature.md) · [Context-specific rule sets](/guide/archunit-governance/context-specific-rule-sets.md)
- Pitfalls: [Framework leak in domain](/pitfall/framework-leak-in-domain.md) · [Business logic in adapter](/pitfall/business-logic-in-adapter.md)
- The base recipe: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md) — where the port and in-memory adapter come from
- Decision: [Repository vs Store](/decision/repository-vs-store.md)
