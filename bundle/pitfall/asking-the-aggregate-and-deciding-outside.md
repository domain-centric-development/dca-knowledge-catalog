---
type: Pitfall
title: Asking the aggregate, deciding outside it
tags: [pitfall, aggregate, use-case, domain]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/domain-layer-rules.md, /marker/tactical/aggregateroot.md, /decision/where-does-the-logic-live.md, /pitfall/anemic-domain-model.md]
---

A use case asks the aggregate a row of questions — `isLocked()`, `isConfirmed()`, `isPasswordExpired()` — and builds
the decision from the answers itself: which of them wins, what follows, which failure to raise. Every predicate on its
own is harmless. Together they move the rule out of the aggregate into the use case.

```java
// the rule lives in the use case
if (account.isLocked()) throw new AccountLockedException(account.id());
if (!account.isConfirmed()) throw new AccountNotConfirmedException(account.id());
if (account.isPasswordExpired(clock.now())) throw new PasswordExpiredException(account.id());
account.recordLogin(clock.now());
```

## Why it is wrong

- **The rule has two homes.** The order of the checks and what each one means is business logic. A second use case
  that logs in on another path copies the chain, or forgets one link.
- **The aggregate cannot protect itself.** `recordLogin` runs whatever the caller checked. Called without the chain,
  it records a login the domain would have refused.
- **It reads like a rich model.** The aggregate has behaviour methods, so a review sees no anemic model — yet the
  decision is outside it, as in the anemic case.

## How to spot it

Two or more predicates of one aggregate in one use case, followed by a call on the same aggregate or by a failure the
use case raises itself. The use case's `if` statements name the aggregate's state.

## Do instead

**Tell the aggregate what to do, and let it refuse.** The operation checks its own preconditions and raises the
failure that names the broken rule; the use case calls it and handles the outcome.

```java
account.logIn(clock.now());   // throws AccountLocked, AccountNotConfirmed, PasswordExpired
```

Where the caller needs the reason without the change — to show it, or to choose a path — return a value that carries
it: `LoginPermission permission = account.loginPermission(clock.now())`, granted or refused with a reason. A single
predicate for a display or a filter stays fine; a `boolean` returned is a question, not a rule.

## Anchors

- Guide: [Domain layer rules](/guide/rules/domain-layer-rules.md)
- Decision: [Where does the logic live](/decision/where-does-the-logic-live.md) · [Reading an aggregate: getters that return values](/decision/reading-an-aggregate.md)
- Pitfalls: [Anemic domain model](/pitfall/anemic-domain-model.md) · [A command decided on an earlier read](/pitfall/a-command-decided-on-an-earlier-read.md)
- Marker: [AggregateRoot](/marker/tactical/aggregateroot.md)
