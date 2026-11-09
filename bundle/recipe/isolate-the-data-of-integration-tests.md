---
type: Recipe
title: Isolate the data of integration tests
tags: [recipe, testing, persistence]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/testing-levels.md]
---

Integration tests run the application against a real database. Each test must see the data it set up and nothing another test left — without paying for a fresh application per test. There are two shapes; pick by what the test framework caches and how it runs tests in parallel.

## The two shapes

| | One application, reset between tests | One database per application instance |
|---|---|---|
| Fits | a framework that caches the application context across test classes and runs them one after another (a shared context is the fast path) | a framework that runs test classes in parallel, each with an application of its own |
| Isolation | before each test, the database goes back to a known state: every table emptied and the seed run again, or a snapshot of the seeded state restored | every application a test starts gets its own database, copied from a template migrated once (`CREATE DATABASE … TEMPLATE …`) |
| Costs | a reset per test (milliseconds for a snapshot restore), and nothing a test sets up survives into the next | a database copy per application, and the application starts per class |
| Breaks when | a test changes configuration and so forces a context of its own; a scheduled job in the shared context acts on what other tests left | two tests of one class rely on each other's data |

The expensive third shape — a fresh application per test class *only* to get fresh data — is what both replace: in a framework that caches contexts, each class with a database of its own is a cache miss and an application start.

## Steps

1. **One database server per test run**, started in a container with the engine production runs. Raise its connection limit and keep each application's pool small; many applications share it.
2. **Migrate once.** The template (or the shared database) is migrated by the same migrations production runs.
3. **Choose the shape** from the table, and put it in one place: a test listener or extension for the reset, a factory for the per-instance database. No test class sets its own database.
4. **Seed as production starts:** the same seeder, which fills an empty store only, and a start that is ready when the seeding's events are delivered ([a seeded system is taken as ready before its events are delivered](/pitfall/a-seeded-system-is-ready-before-its-events-are-delivered.md)).
5. **Remove once-per-class setup** (a static "already done" flag, a set-up that runs before all tests): with a reset per test, data set up once is gone for the second test. Set up per test.
6. **Switch off background jobs that act on stored state** (scheduled redelivery, clean-ups) in the shared application; the tests about them switch them on in an application of their own.
7. **Measure the suite before and after** — application starts and wall time.

## Anchors

- Guide: [Testing levels](/guide/testing-levels.md)
- Recipe: [Move a repository from memory to a database](/recipe/move-a-repository-to-a-database.md) · [Test a scenario integrated](/recipe/test-a-scenario-integrated.md)
- Pitfall: [A seeded system is taken as ready before its events are delivered](/pitfall/a-seeded-system-is-ready-before-its-events-are-delivered.md)
