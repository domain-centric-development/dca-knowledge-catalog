---
type: Pitfall
title: "Publishing domain events without a transaction"
tags: [pitfall, events, domain-event, application, use-case, spring, modulith]
---

A use case that saves and publishes but carries neither `@Transactional` nor an explicit `TransactionBoundary` block. Nothing fails — that is the problem.

## Why it is wrong

- After-commit listeners (`@TransactionalEventListener`, Spring Modulith's `@ApplicationModuleListener`) are registered on the *current* transaction. Without one they are **silently skipped**: no exception, no log line, the downstream context simply never hears the event.
- The event publication registry (the transactional outbox) has no transaction to join, so it writes its row in its own tiny transaction — the crash window between save and outbox entry is back.
- The save and the publish are no longer atomic; a failure between them leaves a persisted change without its event.

## What forbids it

- [Use cases that publish domain events must have a transaction boundary](/rule/usecase/use-cases-that-publish-domain-events-must-have-a-transaction-boundary.md) — a use case that publishes domain events must have a transaction boundary, declarative or explicit.

## Do instead

Local use cases: class-level `@Transactional`. Use cases that also read from remote-capable ports: the explicit `transactionBoundary.inTransaction(...)` around load–mutate–save–publish, with the remote reads before it. Read-only use cases publish nothing and need no transaction.

- Decision: [Declarative or explicit transaction boundary](/decision/declarative-vs-explicit-transaction-boundary.md)

## Anchors

- Rules: [Use cases that publish domain events must have a transaction boundary](/rule/usecase/use-cases-that-publish-domain-events-must-have-a-transaction-boundary.md) · [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md)
- Markers: [TransactionBoundary](/marker/application/transactionboundary.md) · [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- Guide: [Layer rules](/guide/readme/rules.md) · [Event-driven architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
