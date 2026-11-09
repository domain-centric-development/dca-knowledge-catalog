---
type: Pitfall
title: "A seeded system is taken as ready before the events the seeding caused are delivered"
tags: [pitfall, events, outbox, bootstrap, testing]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/integration-patterns.md, /marker/application/transactionboundary.md]
---

Sample or reference data is created at start-up through the use cases, as any caller would create it. Part of what belongs to it is made by reactions in other modules: a created item gets its derived records when its event is delivered — after the seeding's transaction, on another thread, at least once.

The start reports ready when the seeding returns, not when those reactions have run.

## Why it is wrong

- **The first request sees half the data.** A page or a test that asks right after the start finds an item without what the reactions provide — and answers "unavailable" or "not found" for something that exists a moment later.
- **It looks like a flaky test or shared state.** It fails rarely, only under load or on a slow machine, and passes alone. The search goes to test isolation, where the cause is not.
- **Two implementations decide it differently.** One waits for its outbox, the other does not; the same scenario holds in one and flickers in the other.

## How to spot it

A failure that names data the seeding creates, right after a start, and goes away on a rerun. Look at what the start waits for: the seeding's own transactions, or also the deliveries they caused.

## Do instead

**The start is ready when its deliveries are.** After seeding, wait until no publication the seeding registered is still pending (delivered or given up), with a timeout that fails the start loudly. Count only this start's publications: a leftover from an earlier process is delivered all the same, but must not block the start.

**Seed an empty store only.** A store that outlives the process already holds the seed; seeding it again creates duplicates or trips the store's own uniqueness.

## Anchors

- Guide: [Integration patterns](/guide/integration-patterns.md)
- Pitfall: [Reaction in the raising transaction](/pitfall/reaction-in-the-raising-transaction.md)
- Recipe: [Isolate the data of integration tests](/recipe/isolate-the-data-of-integration-tests.md)
