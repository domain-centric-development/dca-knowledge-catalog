---
type: Pitfall
title: Ordering by timestamp
tags: [pitfall, adapter, persistence, repository, testing]
review: draft
owner: DCA catalog maintainers
evidence: [/template/jdbc-repository-adapter.md, /template/repository-with-in-memory-adapter.md, /recipe/add-a-repository-with-adapter.md, /guide/rules.md]
---

A repository promises "in the order they were added" and the adapter implements it as `ORDER BY created_at, id`. `created_at` is the clock at write time; `id` is a random UUID. Two aggregates saved within one clock tick — a batch, an import, two requests on a fast machine, a test that saves three in a row — carry the same timestamp, and the tie falls to the UUID: a random order, different on every run, and correct often enough that no test shows it.

## Why it is wrong

- A timestamp measures when, not in which order. Its resolution (milliseconds, microseconds, whatever the driver keeps) is a property of the clock, not of the writes; two writes in one tick are equal to it.
- The tie-break hides the defect. `id` makes the sort deterministic for one data set and wrong for the next; a test with three saves passes because the three happened to fall into three ticks.
- The promise sits on the port (`findAll` returns insertion order) and the contract test on the port is what a caller relies on. An adapter that keeps the promise only when the clock cooperates does not implement the port.

## Do instead

Let the database assign the order: a `sequence` column (`GENERATED ALWAYS AS IDENTITY`, `AUTO_INCREMENT`, `AUTOINCREMENT` by dialect) that the insert never names and the update never touches, and `ORDER BY sequence`. Keep `created_at` as what it is — a fact about the row — and never as a sort key for insertion order. In the port contract test, save two aggregates within one instant (a fixed clock, or back to back with no clock in the assertion) and assert their order; the in-memory adapter passes it by keeping a list, the JDBC adapter by the sequence column, and a timestamp order fails it.

- Skeleton with the sequence column: [JDBC repository adapter](/template/jdbc-repository-adapter.md)
- The port and its contract test: [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md)

## Anchors

- Templates: [JDBC repository adapter](/template/jdbc-repository-adapter.md) · [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md)
- Recipe: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
- Guide: [Layer rules](/guide/rules.md) ("A repository hands out copies")
