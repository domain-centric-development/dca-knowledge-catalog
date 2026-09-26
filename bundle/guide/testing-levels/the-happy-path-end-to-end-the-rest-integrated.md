---
type: Section
title: "The happy path end to end, the rest integrated"
chapter: Test Levels in Domain-Centric Architecture
source: guide
resource: dca-guide/topics/testing-levels.md
tags: [guide, section]
---

**Rule: one scenario per story is the happy path. It gets the e2e test; every other scenario is integrated.**

The happy path is the scenario that shows what the story is for, as its author would demonstrate it. It is
marked where the story is written (`#### <key> (happy path)`), not picked later by whoever plans the tests: the
person who knows what the story is for is there when it is written, and two plans cannot pick differently.

One e2e test per story covers the page's wiring once. A browser test per scenario tests the same wiring again,
runs slower and fails for reasons that have nothing to do with the scenario. In a delivery pipeline the cost is
higher still: every mapped test runs several times — red before the build, green after it, once more before
the commit — and a flaky test makes the gate itself non-deterministic.

A scenario whose `Then` only a browser can observe is the exception, and the plan says why
(`browser-only: <why>`). A pipeline gate can check the rule: an end-user test for any other scenario is
refused.

An adapter's translation in all its cases — a refusal from the provider, a timeout, a malformed body — is
reached by the integration tests of the scenarios that name those cases. A case the adapter handles and no
scenario names is not a criterion; it gets an integration test of its own, beside the unit tests for the
invariants.
