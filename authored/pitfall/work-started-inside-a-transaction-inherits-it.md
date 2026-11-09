---
type: Pitfall
title: "Work started inside a transaction inherits it"
tags: [pitfall, infrastructure, persistence, application]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/application/transactionboundary.md, /rule/layered/dca-lay-004.md]
---

The transaction boundary keeps the open transaction where the code below it finds it without being handed it: a thread-bound resource, an async-local value, an ambient transaction scope. Repositories, stores and the outbox write in it because they ask "is there a current transaction?".

Anything started from inside the transaction and left running — a background task, a timer, a fire-and-forget call, a hosted service started in that flow — carries the same context along.

## Why it is wrong

- **It writes on a connection it does not own.** The background work runs its statements on the transaction's connection, concurrently with the use case, or after the transaction ended on a connection already returned.
- **Its writes commit or roll back with work it has nothing to do with** — or fail with "the transaction has completed".
- **It passes every test that does not start work in the background**, and appears as a sporadic connection error in production.

Where a resource is bound to the thread, a new thread does not inherit it and the same code fails differently: the work runs without any transaction. Either way the work does not run where the author thought.

## How to spot it

Search the code that runs inside the boundary for anything that outlives the call: a started task that is not awaited, a timer, a scheduled job, a hook that starts work. Check whether the boundary runs its after-commit hooks while the transaction is still current.

## Do instead

**Start such work after the commit, outside the transaction.** The boundary runs its after-commit and after-rollback hooks once the transaction is no longer current; work that has to follow a use case is started from there, or handed to an outbox and run by its dispatcher.

## Anchors

- Marker: [TransactionBoundary](/marker/application/transactionboundary.md)
- Rule: [Transaction boundaries belong to the application layer](/rule/layered/dca-lay-004.md)
- Pitfalls: [Outbox entry written after commit](/pitfall/outbox-entry-written-after-commit.md) · [Swallowed failure in a nested transaction](/pitfall/swallowed-failure-in-a-nested-transaction.md)
