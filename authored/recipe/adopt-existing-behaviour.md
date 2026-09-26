---
type: Recipe
title: Adopt existing behaviour into the backlog
tags: [recipe, testing, migration]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/factory.md, /guide/testing-levels.md]
---

Describe what the system already does as a story, and let it count as delivered only with evidence. The story is never built; it is adopted: every scenario mapped to a test that exists and is green, a test the adoption writes itself shown to work by one break, and a fresh review confirming that each test asserts its scenario.

## Steps

1. **Write the story as for new behaviour** — keyed scenarios under business rules, the project's own words — and mark it adopted (`status: adopted`). Describe what the system does today, not what an old ticket asked for ([Adopt or migrate](/decision/adopt-or-migrate-existing-behaviour.md)).
2. **Plan: find the behaviour and its test.** For each scenario, name where the behaviour lives and which existing test covers it — or that none does. A scenario the code does not show at all is not adoptable: the story describes behaviour the system does not have.
3. **Map every scenario to a test.** The existing test where there is one. Where there is none, write a **characterization test**: green on today's code, asserting the scenario's outcome with its values.
4. **Break every test you wrote, once.** A minimal change to the production code that turns exactly this test red, kept as a patch beside the story and applied to a scratch copy — never to the working tree. A test that stays green under its break proves nothing.
5. **Review the claim.** A fresh reviewer reads every mapped test against its scenario: does it arrange the `Given`, perform the `When`, assert every `Then`? A test that passes without asserting the outcome is a defect ([pitfall](/pitfall/a-green-test-that-asserts-nothing.md)).
6. **Deliver as adopted.** Every test green, every break red, the review passed: the story counts as delivered, a new story may depend on it, and its tests are guarded like any delivered story's.

## Checklist

- No production code and no existing test changed by the adoption.
- A story is adopted whole or not at all: missing tests are written, not listed as open.
- Adopt the part the next new story touches, not the whole system in one go.

## Anchors

- Guide: [Factory process](/guide/factory.md) · [Test levels](/guide/testing-levels.md)
- Decision: [Adopt or migrate existing behaviour](/decision/adopt-or-migrate-existing-behaviour.md)
