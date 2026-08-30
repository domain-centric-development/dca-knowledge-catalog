---
type: Pitfall
title: "Transaction boundary modelled as an output port"
tags: [pitfall, application, hexagonal, port-out, port]
---

Declaring the transaction abstraction as an output port — `interface UnitOfWork extends OutputPort` — and placing its implementation under `adapter/outgoing/`. It looks consistent ("the use case depends on it, adapters implement it"), and that is precisely the mistake: not everything a use case calls is a port.

## Why it is wrong

- An output port describes a capability the application needs from the **outside world**: store an aggregate, look up a price, publish an event. A transaction is no such interaction — it defines the *execution semantics* of several of them. Classifying it as a port blurs what "port" means until every helper qualifies.
- Once it is a port, the architecture rules must special-case it (a "remote-capable port" check has to whitelist it, port-granularity heuristics count it), and reviewers start asking which external system it adapts to. There is none.
- The name `UnitOfWork` carries ORM baggage (change tracking, identity map) that the abstraction does not provide; developers expect the wrong thing.

## What forbids it

- [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md) — its allowed list inside a transaction names the real transactional resources (`Repository`, `Store`, the publishers); the boundary itself is not on it because it is not a port.
- [TransactionBoundary](/marker/application/transactionboundary.md) — the building block documents itself as "an application-layer execution abstraction, deliberately not an output port".

## Do instead

Keep `TransactionBoundary` in the building blocks' `application` namespace (`Application.Transactions` in .NET), not extending `OutputPort`; put the implementation under **infrastructure** (`sharedkernel/infrastructure/transaction`), where the transaction manager is configured — it is framework plumbing, not an adapter to anything. The test for the general case: *does this interface stand for something outside the process?* If not, it is not a port.

- Decision: [Declarative or explicit transaction boundary](/decision/declarative-vs-explicit-transaction-boundary.md)

## Anchors

- Markers: [TransactionBoundary](/marker/application/transactionboundary.md) · [OutputPort](/marker/port-out/outputport.md)
- Rules: [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md)
- Guide: [Layer rules](/guide/readme/rules.md)
