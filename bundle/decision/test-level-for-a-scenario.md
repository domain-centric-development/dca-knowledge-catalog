---
type: Decision
title: "Which test level for a scenario: unit, integration or end to end"
tags: [decision, testing, use-case, adapter]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/testing-levels.md, /guide/e2e-testing.md, /guide/factory.md]
---

Every scenario of a story gets exactly one test that proves it, and the level decides what the suite costs to run and how reliably it fails. The rule: **the lowest level that observes the scenario's `Then` from outside.**

## The discriminator

Ask, in order:

1. **Is it the story's happy path** — the one scenario marked `(happy path)`, the one that shows what the story is for? → **end to end**, through the page. One per story covers the page's wiring.
2. **Can only a browser observe the `Then`** — a countdown, a script's reaction to a click, a notification, anything after the page has loaded? → **end to end**, and the plan says why (`browser-only`).
3. **Otherwise** → **integration**: the use case through the wired application, real adapters, an external system stubbed at the protocol ([Recipe](/recipe/test-a-scenario-integrated.md)).

An invariant of an aggregate or value object is not a scenario; it gets a **unit** test beside them.

## Options

| | Unit | Integration | End to end |
|---|---|---|---|
| Runs | one domain type, no framework | the use case through the wired application | the running application through its page |
| Proves | an invariant | the scenario's `Then` and the adapters it passes | the page's wiring, and what only a browser sees |
| External system | not reached | stubbed at the protocol | stubbed at the protocol |
| Speed and reliability | fastest, deterministic | fast, deterministic | slowest, most exposed to timing |
| Per story | as many as the invariants | every scenario but the happy path | the happy path |

## Not a scenario: the journey

A flow across an epic's stories that must never break is a **journey**, tested end to end to the epic's outcome event once its stories are delivered. It is a regression guard, green when written, and never a story's criterion ([Test levels](/guide/testing-levels.md)).

## Anchors

- Guide: [Test levels](/guide/testing-levels.md) · [E2E testing](/guide/e2e-testing.md) · [Factory process](/guide/factory.md)
- Pitfall: [Mocking the port whose adapter the change is about](/pitfall/mocking-the-port-of-the-changed-adapter.md)
