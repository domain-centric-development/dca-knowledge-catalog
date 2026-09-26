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
- For new behaviour the red proof catches it — the test must fail before the code exists. For behaviour that already exists there is no red phase, so nothing catches it unless someone looks.
- A backlog that counts such a scenario as covered says the system does something no test holds it to.

## Do instead

- For a test written for existing behaviour: break the behaviour once — a minimal change to the production code on a scratch copy — and require the test to turn red ([Recipe](/recipe/adopt-existing-behaviour.md)).
- For a test that existed before: read it against the scenario. It arranges the `Given`, performs the `When` and asserts every `Then` with the scenario's values, or it is not the scenario's test.

## Anchors

- Guide: [Factory process](/guide/factory.md) · [Test levels](/guide/testing-levels.md)
