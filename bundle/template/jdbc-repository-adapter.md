---
type: Template
title: "JDBC repository adapter skeleton (JdbcClient)"
tags: [template, adapter, persistence, repository, spring]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/repository.md, /marker/port-out/outputport.md, /rule/tactical/dca-tac-015.md, /rule/hexagonal/dca-hex-008.md, /rule/usecase/dca-use-009.md, /rule/tactical/dca-tac-013.md, /guide/readme/rules.md, /guide/readme/deviations-from-the-literature.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for a **JDBC outgoing adapter** that implements the *same* `{Name}Repository` output port as the [in-memory adapter](/template/repository-with-in-memory-adapter.md) and the [JPA adapter](/template/jpa-repository-adapter.md). The port and the aggregate do not change; only the class behind the boundary does. It lives in `adapter/outgoing/persistence/`, is named `Jdbc{Name}Repository`, and speaks SQL through Spring's `JdbcClient`: `save` is an upsert, a `RowMapper` rebuilds the aggregate through its `reconstitute(...)` factory, and `findAll` orders by an explicit column. Replace `{Name}` (aggregate) / `{name}` / `{context}` / `{basePackage}`.

**When to pick JDBC over JPA.** Choose it when you want the SQL to be visible and the mapping to be yours: no ORM identity map, no lazy loading, no dirty checking behind the aggregate's back. It fits aggregates that are stored as one row or one document (a JSON column for the parts) and read whole, which is how a repository hands out aggregates anyway. Prefer JPA when the schema is wide, relational and shared with other tooling, or when the team already carries the ORM. Either way the domain stays persistence-free; the difference is entirely inside this package.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`jdbc-repository-adapter/java.md`](/template/jdbc-repository-adapter/java.md)

## Realizes / governed by

- Marker: [Repository<T, ID>](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md)
- Rules: [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/dca-tac-015.md) · [Classes named *Repository must reside in the outgoing adapter package](/rule/hexagonal/dca-hex-008.md) · [Use cases that save an aggregate must publish its domain events](/rule/usecase/dca-use-009.md) · [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/dca-tac-013.md)
- Guide: [Layer rules](/guide/readme/rules.md) (repository interface rules — "A repository hands out copies") · [Deviations from the literature](/guide/readme/deviations-from-the-literature.md)
- Pitfalls: [Reconstitution raises creation event](/pitfall/reconstitution-raises-creation-event.md) · [Business logic in adapter](/pitfall/business-logic-in-adapter.md) · [Framework leak in domain](/pitfall/framework-leak-in-domain.md)
- Sibling templates: [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md) · [JPA repository adapter](/template/jpa-repository-adapter.md) · [Aggregate root](/template/aggregate-root.md)
- Recipe: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
