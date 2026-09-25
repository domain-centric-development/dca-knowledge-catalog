---
type: Decision
title: "Existing behaviour into the backlog: adopt, or migrate the old tickets"
tags: [decision, migration, testing]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/factory.md]
---

A project that enters a story-driven delivery process with code of its own has behaviour no story describes. A new story cannot depend on it, and the process cannot tell what it already has. There are two ways to bring it in, and only one of them holds.

## Options

| | Migrate old tickets | Adopt existing behaviour |
|---|---|---|
| Source | the tracker's history: what was once asked for | the system as it is today: its pages, APIs and tests |
| Intent, goal, outcome | invented where the ticket did not state them | stated for what the system does now, by someone who knows |
| Evidence | none — the ticket says "done" | every scenario on a green test; a written test broken once; a review of each test |
| Result | a backlog that claims things nobody checked | a backlog a new story can depend on |

## The discriminator

Ask: **does the story describe what the system does today, and can a test show it?** Then adopt it. If the only source is an old ticket, the story would invent its intent — leave it out; the behaviour it asked for is adopted when a new story touches it.

## Limits

- Green is weaker than red-then-green: every mapped test is read against its scenario, and a written one needs its break.
- Adoption is incremental: the part the next new story touches, not the whole system in one run.

## Anchors

- Guide: [Factory process](/guide/factory.md)
- Recipe: [Adopt existing behaviour into the backlog](/recipe/adopt-existing-behaviour.md) · Pitfall: [A green test that asserts nothing](/pitfall/a-green-test-that-asserts-nothing.md)
