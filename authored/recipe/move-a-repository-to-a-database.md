---
type: Recipe
title: Move a repository from memory to a database
tags: [recipe, adapter, persistence, repository]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules.md, /rule/tactical/dca-tac-014.md, /rule/tactical/dca-tac-015.md, /rule/tactical/dca-tac-013.md, /rule/tactical/dca-tac-017.md, /rule/naming/dca-nam-004.md, /rule/hexagonal/dca-hex-005.md, /rule/hexagonal/dca-hex-003.md, /rule/layered/dca-lay-004.md]
---

Put an aggregate into a relational database **without touching the output port or the domain**. The use cases depend on `{Name}Repository`, so replacing what stands behind it is invisible to them. The domain aggregate stays persistence-free; the adapter owns all the mapping. Afterwards the in-memory adapter is a **test fake**, not a second production adapter: one store in production, one fake for the unit tests.

## Steps

1. **Leave the port and the domain alone** — `{Name}Repository` in `application/shared/` and the `{Name}` aggregate do not change. If you find yourself editing either to make the database fit, stop: that leak defeats the point (see [framework-leak-in-domain](/pitfall/framework-leak-in-domain.md)).
2. **Write the schema as a migration** — one versioned script per change (Flyway, Liquibase, EF Core migrations, DbUp — whatever the stack has), applied when the application starts or before it deploys. A schema created by hand or by the ORM at start-up has no history to migrate from later.
3. **State the rules the store holds as constraints** — an identifier that names one thing is a unique column; "at most one *active* one per owner" is a partial unique index. The adapter translates the one violation its port declares into the port's failure and lets every other one travel as what it is ([check-then-save uniqueness](/pitfall/check-then-save-uniqueness.md)).
4. **Write the adapter** — `Jdbc{Name}Repository` ([template](/template/jdbc-repository-adapter.md)), a JPA adapter with its own entity ([template](/template/jpa-repository-adapter.md)), or the stack's equivalent (Dapper, EF Core). Map rows back through `{Name}.reconstitute(...)`, never through `create(...)` ([reconstitution-raises-creation-event](/pitfall/reconstitution-raises-creation-event.md)). Keep the mapping pure — no business logic ([business-logic-in-adapter](/pitfall/business-logic-in-adapter.md)).
5. **Take the row lock where a check precedes a change** — a read that a use case checks and then changes on (a quantity reserved, a state advanced) is read `FOR UPDATE` inside the transaction, so a second caller waits instead of deciding on the same row. An in-process lock serialises one process only.
6. **Make the transaction boundary real** — the boundary opens the database transaction, every repository and store of the use case writes in it, and an outbox that records the use case's events writes in it too ([outbox entry written after commit](/pitfall/outbox-entry-written-after-commit.md)). Only the boundary begins and ends a transaction ([DCA-LAY-004](/rule/layered/dca-lay-004.md)).
7. **Move the in-memory adapter to the test sources** — it becomes the unit tests' fake and stores copies, on write and on read ([an in-memory store hands out live aggregates](/pitfall/an-in-memory-store-hands-out-live-aggregates.md)). No profile switches between the two in production.
8. **Test the adapter against the real database** — an integration test per adapter against the engine production runs, started in a container; the database's own behaviour (constraints, locks, the type mapping) is what the test is for. Then isolate the integration tests' data ([isolate the data of integration tests](/recipe/isolate-the-data-of-integration-tests.md)).
9. **Verify nothing above the port changed** — the existing use-case and domain tests pass untouched; then the project's architecture suite.

## Rules to satisfy (build-time checklist)

- [Repository interfaces must reside in the application output-port package](/rule/tactical/dca-tac-014.md) — the port stays put
- [Repository implementations must reside in the adapter.outgoing package](/rule/tactical/dca-tac-015.md) — the database adapter lives here
- [Repository interfaces should extend the Repository marker](/rule/tactical/dca-tac-013.md)
- [Repository methods must not return non-root Entities](/rule/tactical/dca-tac-017.md) — the adapter maps rows back to the aggregate, never leaks entities
- [Repository interfaces must end with `Repository`](/rule/naming/dca-nam-004.md)
- [Outgoing adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/dca-hex-005.md)
- [Controllers and resources must never access repositories directly](/rule/hexagonal/dca-hex-003.md)
- [Transaction boundaries belong to the application layer](/rule/layered/dca-lay-004.md)

## Anchors

- Templates: [JDBC repository adapter](/template/jdbc-repository-adapter.md) · [JPA repository adapter](/template/jpa-repository-adapter.md) · [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md) · [Aggregate root skeleton](/template/aggregate-root.md) — where `reconstitute` comes from
- Markers: [Repository<T, ID>](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md) · [TransactionBoundary](/marker/application/transactionboundary.md)
- Guide: [Layer rules](/guide/rules.md) ("A repository hands out copies") · [Deviations from the literature](/guide/readme/deviations-from-the-literature.md)
- Pitfalls: [An in-memory store hands out live aggregates](/pitfall/an-in-memory-store-hands-out-live-aggregates.md) · [Check-then-save uniqueness](/pitfall/check-then-save-uniqueness.md) · [Reconstitution raises the creation event](/pitfall/reconstitution-raises-creation-event.md) · [Framework leak in domain](/pitfall/framework-leak-in-domain.md) · [Work started inside a transaction inherits it](/pitfall/work-started-inside-a-transaction-inherits-it.md)
- The base recipe: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md) — where the port and the in-memory adapter come from
- Decision: [Repository vs Store](/decision/repository-vs-store.md)
