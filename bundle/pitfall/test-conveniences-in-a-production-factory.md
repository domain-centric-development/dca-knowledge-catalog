---
type: Pitfall
title: "Test conveniences in a production factory"
tags: [pitfall, factory, domain, testing]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/factory.md, /marker/tactical/aggregateroot.md]
---

The domain's factory grows methods the application never calls: `createWithId` that skips the creation event, a
`createBasic` with defaults, a method that builds a half-valid instance — each added because a test wanted a
shorter setup.

## Why it is wrong

- **Production code that only tests call** is code the domain does not need, and it ships with every release.
- **It opens a way around the rules.** A method that creates without the creation event, or with an id the caller
  picks, is a back door the next production caller walks through — the event never published, the invariant
  skipped.
- **Two codebases, two factories.** One writer adds the shortcuts, the other keeps one creation path; the same model
  then differs in what it allows.

## How to spot it

For each public factory method, find a caller outside the tests. A method only tests call is a test helper in the
wrong place.

## Do instead

**One creation path in production** — the factory or the aggregate's creating operation, raising its event — and
`reconstitute` for restoring stored state. A test's shortcuts live in the test sources: a builder or a helper that
calls the production path, or `reconstitute` where the test needs a given state.

## Anchors

- Markers: [Factory](/marker/tactical/factory.md) · [AggregateRoot](/marker/tactical/aggregateroot.md)
- Pitfall: [Reconstitution raises the creation event](/pitfall/reconstitution-raises-creation-event.md)
- Pitfall: [An operation nothing calls](/pitfall/an-operation-nothing-calls.md)
