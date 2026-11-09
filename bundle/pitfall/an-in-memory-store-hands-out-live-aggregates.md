---
type: Pitfall
title: "An in-memory store hands out live aggregates — and hides a missing save and a missing rollback"
tags: [pitfall, adapter, persistence, repository, testing]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules.md, /marker/port-out/repository.md, /marker/application/transactionboundary.md]
---

A map-backed repository that returns the instance it holds — `store.get(id)` — and stores the instance it is given. Every caller works on the same object as the store.

## Why it is wrong

- **A missing `save()` goes unseen.** The caller changed the stored object already; the test that should catch the forgotten write passes. Against a database the change is gone, because loading a row builds a new object.
- **A rollback undoes nothing.** A use case that changes an aggregate, then fails or refuses, has already changed the store. A database would have rolled the change back; the test that passes in memory asserts a state production never has — or the other way round, a test cannot see that its rollback is missing.
- **Two requests share one aggregate.** One request's half-made change is visible to another before anything committed.
- **It is the adapter a reader copies first**, and the one the unit tests keep after the database arrives — so the gap travels with the fake.

## How to spot it

Look at the repository's `find…` methods: do they return the stored value itself? Look at `save`: does it put the argument into the map? Then mutate a loaded aggregate in a test without saving and load it again — if the change is there, the store hands out live objects.

## Do instead

**Store copies, on write and on read.** Map through the aggregate's `reconstitute` both ways, as a database adapter must ([Layer rules](/guide/rules.md), "A repository hands out copies"). Registered domain events are not carried over.

**Run the transaction rules against the real store.** A fake that copies still keeps a change that was saved and then rolled back; only the database undoes it. The boundary's rollback, the outbox written in the same transaction and the row locks are tested against the engine production runs.

## Anchors

- Markers: [Repository&lt;T, ID&gt;](/marker/port-out/repository.md) · [TransactionBoundary](/marker/application/transactionboundary.md)
- Recipe: [Move a repository from memory to a database](/recipe/move-a-repository-to-a-database.md)
- Template: [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md)
