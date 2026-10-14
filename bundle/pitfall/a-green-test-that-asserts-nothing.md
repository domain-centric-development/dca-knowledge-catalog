---
type: Pitfall
title: A green test that asserts nothing
tags: [pitfall, testing]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/factory.md, /guide/testing-levels.md]
---

A test is mapped to a scenario and it is green — but it does not assert the scenario's outcome. It loads the page and checks the title, it calls the use case and checks that no exception was thrown, or it asserts a value the arrangement put there itself. It stays green whatever the code does.

## Why it is wrong

- Green alone is no evidence: a test that asserts nothing passes, and a runner that matched no test passes too.
- For new behaviour the red proof catches it only for the first assertion that fails — the test must fail before the code exists, and it stops there. An assertion after it, on another clause of the scenario, is never seen red. For behaviour that already exists there is no red phase at all, so nothing catches it unless someone looks.
- A backlog that counts such a scenario as covered says the system does something no test holds it to.

## Do instead

- For every clause of the scenario — its `Then` and each `And` — a break probe: the smallest change to the production code that violates that clause and leaves the others standing must turn that clause's assertion red. For new behaviour this is the red phase taken clause by clause, not test by test. Two shapes fail every probe: an assertion inside a condition that nothing meets, and an absence checked right after the action, before the page or the system has reacted.
- For a test written for existing behaviour: break the behaviour once — a minimal change to the production code on a scratch copy — and require the test to turn red ([Recipe](/recipe/adopt-existing-behaviour.md)).
- For a test that existed before: read it against the scenario. It arranges the `Given`, performs the `When` and asserts every `Then` with the scenario's values, or it is not the scenario's test.

## Anchors

- Guide: [Factory process](/guide/factory.md) · [Test levels](/guide/testing-levels.md)
