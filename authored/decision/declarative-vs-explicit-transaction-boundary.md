---
type: Decision
title: Declarative or explicit transaction boundary
tags: [decision, application, use-case, persistence, events]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-012.md, /rule/usecase/dca-use-013.md, /rule/dotnet/dca-net-006.md, /marker/application/transactionboundary.md, /marker/port-out/domaineventpublisher.md, /marker/port-out/integrationeventpublisher.md, /guide/readme/rules.md]
---

Every writing use case runs load → mutate → save → publish inside one short transaction. The question is only **who draws the boundary**: the framework around the whole method, or the use case by hand around part of it.

## Discriminator

Does the use case call an output port that **may leave the process** — another bounded context's API, a payment provider, a mail gateway, a remote catalog? In the monolith these are in-process; the architecture is designed so they can become HTTP without touching the use case, so decide as if they already were.

| Use case | Boundary | Why |
|---|---|---|
| Writes; all ports local (repositories, stores, publishers) | **Declarative** — class-level `@Transactional` (.NET: a decorator/pipeline around `IUseCase`) | Shortest code, whole method atomic, nothing to get wrong |
| Writes; also reads from a remote-capable port | **Explicit** — remote reads first, then `transactionBoundary.inTransaction(() -> { load; mutate; save; publish; })` | The remote round trip must not hold a connection; a rollback could not undo it anyway |
| Writes; needs a remote **effect** (charge, notify) | Explicit boundary for the local part; the effect runs **after commit** as a reaction to an integration event | Retry and idempotency belong to the consumer, not inside the transaction |
| Bulk command without `save` (delete all, archive before date) | **Declarative** `@Transactional`, no publisher | Nothing is loaded or saved per aggregate, so the save-then-publish rule does not apply; the port method is the whole unit of work |
| Read-only | **None** | Nothing to make atomic; remote reads must not be wrapped |

## What the rules enforce

- [Use cases that publish domain events must have a transaction boundary](/rule/usecase/dca-use-012.md) — a publishing use case has a boundary of either kind.
- [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/dca-use-013.md) — a declaratively transactional use case calls no remote-capable port; only `Repository`, `Store`, `DomainEventPublisher`, `IntegrationEventPublisher` inside.
- [Application layer must not use persistence or transaction frameworks](/rule/dotnet/dca-net-006.md) — the application layer never touches the persistence or transaction framework; the only place that knows how a transaction opens is the boundary's infrastructure implementation.

## Contract of the explicit boundary

`TransactionBoundary` is an application-layer execution abstraction, **not an output port** — see [the pitfall](/pitfall/transaction-boundary-modelled-as-an-output-port.md). Nested calls join the outer transaction; an inner failure marks it rollback-only, and the outermost block throws instead of committing — see [swallowed failure in a nested block](/pitfall/swallowed-failure-in-a-nested-transaction.md). Domain events published inside see the same transaction; integration events registered inside become visible to their dispatcher on commit — see [outbox entry written after the commit](/pitfall/outbox-entry-written-after-commit.md).

## Considered and parked

Moving the transactional part into a dedicated handler behind a decorator, so the use case becomes pure orchestration (remote reads → handler → integration event). Stricter, and it removes the lambda from every writer; parked because it hides the boundary from the reader of the use case, and the explicit form keeps both shapes visible side by side.

## Anchors

- Markers: [TransactionBoundary](/marker/application/transactionboundary.md) · [DomainEventPublisher](/marker/port-out/domaineventpublisher.md) · [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md)
- Rules: [Use cases that publish domain events must have a transaction boundary](/rule/usecase/dca-use-012.md) · [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/dca-use-013.md) · [Application layer must not use persistence or transaction frameworks](/rule/dotnet/dca-net-006.md)
- Guide: [Layer rules](/guide/readme/rules.md)
- Recipe: [Add a bulk operation](/recipe/add-a-bulk-operation.md)
- Pitfalls: [Remote call inside a transaction](/pitfall/remote-call-inside-a-transaction.md) · [Publishing domain events without a transaction](/pitfall/publishing-domain-events-without-a-transaction.md)
