---
type: Pitfall
title: "An operation nothing calls"
tags: [pitfall, aggregate, domain, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/aggregateroot.md, /guide/rules.md]
---

The aggregate carries operations the model "obviously" needs — `suspend`, `close`, `abandon`, `expire`, a
quantity change — and no use case calls them. They were written with the aggregate, ahead of the behaviour that
would use them.

## Why it is wrong

- **Unproven code.** No scenario holds it, no use case reaches it; its rules are guesses, and its tests prove the
  guesses.
- **It looks like supported behaviour.** The next writer reuses the operation and inherits rules nobody decided, or
  writes a second one beside it because the first does not quite fit.
- **Two codebases diverge silently.** One writer adds the speculative operations, the other does not; nothing that
  runs notices.

## How to spot it

For each public operation of an aggregate, find a caller in the application layer. One that only the aggregate's own
tests call is speculative. Where the project keeps a glossary with operations, compare: an operation in the code that
no use case triggers, or one in the glossary that no code has.

## Do instead

**An operation arrives with the use case that calls it** and the scenario that holds it. Remove the ones nothing
calls; a state that only stored data can carry (a status set by a process the application does not own yet) stays
readable through `reconstitute`, and its tests build it that way.

## Anchors

- Marker: [AggregateRoot](/marker/tactical/aggregateroot.md)
- Guide: [Layer rules](/guide/rules.md)
- Pitfall: [Test conveniences in a production factory](/pitfall/test-conveniences-in-a-production-factory.md)
