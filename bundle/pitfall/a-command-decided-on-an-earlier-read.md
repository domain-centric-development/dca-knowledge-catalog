---
type: Pitfall
title: "A command decided on an earlier read: the choice holds until the state moves"
tags: [pitfall, application, use-case, aggregate]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/aggregateroot.md, /marker/port-in/usecase.md, /decision/where-authorization-and-validation-live.md]
---

A choice is shown on one request and acted on by the next. A page offers the options that are allowed right now; a form carries the price, the state or the version it was rendered with; a snapshot is taken, the user decides, and the command that follows trusts the snapshot. A remote system answers "accepted", and the step that confirms it takes the answer as still true. The command checks nothing the earlier read decided — the read already did.

Between the read and the command, the state moved: somebody else changed it, a deadline passed, a step was cancelled, a limit was reached. The command carries out a decision that no longer holds.

## Why it is wrong

- **The read is not the rule.** What was allowed when the page was drawn is a hint for the user. The rule is the aggregate's, and only the aggregate, asked at the moment of the change, can say whether it holds now.
- **The caller is not trusted.** A request can carry any value the client chooses — an option that was never offered, a price from yesterday, a state it read an hour ago. A command that takes it on trust lets the client decide what the business decides.
- **Tests do not see it.** A test drives the page and then the command in one breath, with nothing in between; the state cannot move, and the missing check stays green.
- **It looks like validation done once.** The check exists — in the query that built the page — so a review sees the rule and misses that the command never asks it.

## How to spot it

Follow one decision from where it is shown to where it is carried out. If the command receives the decided value (an option, an amount, a target state) and passes it on without loading what the decision rested on and asking the aggregate again, the pitfall is there. Two tells: the guard exists only in the query or the view; the command's parameters include something the server could have read itself.

## Do instead

**Decide again in the command, inside the aggregate.** Load the aggregate the decision is about, and let its own method refuse what no longer holds — the same rule the page used to filter, now enforced at the change. The page may still filter; the aggregate decides.

```java
Subscription subscription = subscriptions.findById(command.subscriptionId()).orElseThrow();
subscription.changePlan(command.planId(), clock.now());   // refuses a plan no longer allowed
```

**Carry identities, not conclusions.** The command names what the user chose — an id — and the server reads everything else (the price, the state, the limit) at the time of the change. A value the client sends that the server can read is a value to read, not to trust.

**Where the change must hold to exactly what the user saw**, say so: carry the version the user saw and let the aggregate refuse a newer one (optimistic concurrency), so the user decides again rather than the command deciding for them.

**A remote answer is an earlier read too.** The step that confirms what another system accepted re-checks the local preconditions before it commits, as it would for any read it did not do itself.

- Related: [Where authorization and validation live](/decision/where-authorization-and-validation-live.md) · [Check-then-save uniqueness](/pitfall/check-then-save-uniqueness.md) · [Remote effect before local preconditions](/pitfall/remote-effect-before-local-preconditions.md)

## Anchors

- Markers: [AggregateRoot](/marker/tactical/aggregateroot.md) · [UseCase](/marker/port-in/usecase.md)
