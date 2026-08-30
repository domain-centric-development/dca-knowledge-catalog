---
type: Pitfall
title: "Swallowed failure in a nested transaction block"
tags: [pitfall, application, use-case, infrastructure, persistence]
---

An outer `inTransaction` block that calls another use case (or helper) which opens its own `inTransaction`, catches the inner exception, and carries on to commit:

```java
transactionBoundary.inTransaction(() -> {
  try {
    reserveStockUseCase.execute(cmd);   // joins the outer transaction, throws
  } catch (RuntimeException e) {
    log.warn("stock reservation failed, continuing");
  }
  orders.save(order);                   // commits — with half of the inner work
  return result;
});
```

## Why it is wrong

- A nested block *joins* the outer transaction; there is one commit. The inner code may already have written rows before it threw. Catching the exception does not un-write them — committing now persists a partial inner result next to the outer one.
- Spring's `REQUIRED` propagation marks the shared transaction rollback-only in that case and the outermost commit fails with `UnexpectedRollbackException`. An in-memory or hand-rolled boundary that does not emulate this lets the commit through silently, so the bug only appears when the real transaction manager arrives.
- It hides a design smell: the outer block wanted the inner work to be optional, which means it belonged in its own transaction (or after the commit, as a reaction to an event).

## What forbids it

- [TransactionBoundary](/marker/application/transactionboundary.md) — the building block's contract: a failure in an inner block marks the shared transaction rollback-only; the outermost block rolls back and throws instead of committing half of the work.

## Do instead

If the inner work is optional, run it **after** the outer commit as a listener on the integration event (retry, idempotent), or in a separate transaction started outside the outer block. Inside one transaction, let failures propagate. Implementations of the boundary keep a rollback-only flag so the outermost block cannot commit a poisoned transaction.

- Decision: [Declarative or explicit transaction boundary](/decision/declarative-vs-explicit-transaction-boundary.md)

## Anchors

- Markers: [TransactionBoundary](/marker/application/transactionboundary.md)
- Guide: [Layer rules](/guide/readme/rules.md)
