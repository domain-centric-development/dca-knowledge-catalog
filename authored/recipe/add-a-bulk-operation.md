---
type: Recipe
title: Add a bulk operation
tags: [recipe, application, use-case, repository, events]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-009.md, /rule/usecase/dca-use-012.md, /rule/usecase/dca-use-013.md, /rule/tactical/dca-tac-014.md, /rule/usecase/dca-use-002.md, /marker/port-out/repository.md, /marker/port-out/integrationeventpublisher.md, /marker/port-in/usecase.md]
---

Perform one operation over many aggregates at once — delete all, archive everything completed before a date, purge expired sessions. The shape differs from the ordinary writer: no aggregate is loaded, mutated and saved one by one. The repository port does the work in a single call, and the use case owns the unit of work around it.

## Steps

1. **Name it in the ubiquitous language** — `ArchiveCompletedTasks`, `PurgeExpiredSessions`, not `BulkDelete` or `Cleanup`. The use case folder is `application/{usecasename}/` with the usual `{Name}InputPort`, `{Name}UseCase`, `{Name}Command`, `{Name}Result` ([use case skeleton](/template/use-case.md)).
2. **Add the method to the repository port** — `deleteAll()`, `archiveAllBefore(Instant cutoff)`, `deleteExpiredBefore(Instant now)` on `{Name}Repository` in `application/shared/`. The port is freely extensible beyond the inherited `findById`/`save`/`deleteById`; a bulk method is still a question about the collection of one aggregate type. It returns nothing or a count, never a stream of aggregates to mutate.
3. **Write a command use case that calls it** — the use case builds the cutoff from the command, calls the port method once, and returns the count in the `{Name}Result`. No loop of `findById` → mutate → `save`: that turns one statement into N round trips and N transactions' worth of work.
4. **Register no domain event** — nothing was loaded, so no aggregate registered anything, and inventing events per row would fake N facts for one action. If another context must learn about the bulk fact, publish **one** integration event describing it from the use case (`TasksArchivedEvent` with the cutoff and count) through the `IntegrationEventPublisher` ([Domain event or integration event](/decision/domain-event-vs-integration-event.md)); whether an *ordinary* writer should register events nobody consumes yet is a different question — [Register domain events nobody listens to yet?](/decision/domain-events-without-a-consumer.md)).
5. **Draw the boundary declaratively** — class-level `@Transactional` is the right form: the port method is the whole unit of work, and only local ports are called ([Declarative or explicit transaction boundary](/decision/declarative-vs-explicit-transaction-boundary.md)).
6. **Implement the method in every adapter** — the in-memory adapter filters its map, the JDBC adapter runs one `DELETE … WHERE` or `UPDATE … WHERE`, the JPA adapter a bulk query. Add the case to the port's contract test so every implementation agrees on what "before the cutoff" means.
7. **Verify** — `./gradlew test-architecture`.

## Why the two-aggregates pitfall does not apply

[Modifying two aggregates in one transaction](/pitfall/modifying-two-aggregates-in-one-transaction.md) is about a use case that loads two roots, invokes their behaviour and saves both, so that two consistency boundaries commit together. A bulk operation loads and mutates no aggregate at all; it changes storage state of many rows of *one* aggregate type through one port call. There is no invariant spanning the rows that the aggregate boundary would guard — if there were, the operation would have to load each aggregate and let it decide, and this recipe would be the wrong one.

## Rules to satisfy (build-time checklist)

- [Use cases that save an aggregate must publish its domain events](/rule/usecase/dca-use-009.md) — selects the use case but has nothing to check: no `save` is called, so it passes without a `publishAndClearEvents`.
- [Use cases that publish domain events must have a transaction boundary](/rule/usecase/dca-use-012.md) — no domain events are published; the declarative boundary is there for atomicity of the port call, not for the rule.
- [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/dca-use-013.md) — inside `@Transactional` only `Repository`, `Store`, `IntegrationEventPublisher`; a remote-capable port would force the explicit form.
- [Repository interfaces must reside in the application layer's shared output-port package](/rule/tactical/dca-tac-014.md) — the extended port stays in `application/shared/`.
- [Commands must end with `Command` and reside in the application package](/rule/usecase/dca-use-002.md)

## Anchors

- Template: [Use case skeleton](/template/use-case.md)
- Decisions: [Declarative or explicit transaction boundary](/decision/declarative-vs-explicit-transaction-boundary.md) · [Domain event or integration event](/decision/domain-event-vs-integration-event.md)
- Markers: [Repository<T, ID>](/marker/port-out/repository.md) · [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md) · [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- Guide: [Layer rules](/guide/readme/rules.md)
- The ordinary writer this recipe deviates from: [Add a use case](/recipe/add-a-use-case.md) · the port it extends: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
- Pitfall: [Modifying two aggregates in one transaction](/pitfall/modifying-two-aggregates-in-one-transaction.md)
