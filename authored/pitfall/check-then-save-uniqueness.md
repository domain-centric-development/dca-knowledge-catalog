---
type: Pitfall
title: "Check-then-save uniqueness: a rule that holds until two callers arrive together"
tags: [pitfall, application, use-case, port-out, persistence]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/repository.md, /marker/application/transactionboundary.md]
---

A rule about a *set* of aggregates — at most one open account per customer, one active subscription per tenant, a code or identifier that names exactly one thing — enforced by asking the repository and then writing: `findOpenFor(customer)` and, when nothing comes back, `save(new …)`. Or `existsByCode(code)` and, when it says no, `save(…)`.

Between the question and the write, nothing holds. Two callers ask at the same moment, both hear "nothing there", and both write.

## Why it is wrong

- **No aggregate can hold the rule.** It spans siblings, so the aggregate that is being written cannot see what would make it invalid. Putting the check in the use case does not change that; it only moves the blind spot.
- **A transaction does not close it either** unless the isolation level serialises the read — which it usually does not. The window is small, so it survives every test that runs single-threaded, and appears under load as duplicates nobody can reproduce.
- **The duplicate is the expensive kind.** Two "active" rows where the domain says one, discovered later by whatever reads them with `findFirst` — and which of the two it finds is arbitrary.
- **In-memory adapters hide it best.** A concurrent map overwrites the loser's entry silently, so the store ends up holding a state the domain calls impossible. That is also the adapter a reader copies first when starting a new context.

## How to spot it

Look for a `find…`/`exists…` immediately followed by a `save` of what was not found. Then ask whether the rule could be written as a unique index: if yes, the rule spans aggregates, and the code holds it by looking rather than by claiming.

## Do instead

**Let the store claim the value.** The store is the only place that sees all the siblings, so the rule belongs to it:

- A relational adapter states it as a unique index and lets the constraint speak.
- An in-memory adapter claims the key atomically — a `putIfAbsent`-style index beside the aggregates — and refuses the write when somebody else holds it. Refuse with the same shape a constraint violation has, so callers do not have to know which adapter they are on.

**Let the caller react to the refusal**, rather than trying to avoid it:

```java
try {
  store.save(candidate);
} catch (AlreadyHeld e) {          // what a unique index answers
  return theOneThatWon(store, owner);   // re-read, use it
}
```

Keep the check before the save: it gives the ordinary caller a clear answer without an exception. The claim is what makes the rule true when two callers arrive together.

**Watch what a partial rule costs.** "At most one *active* one" is a conditional uniqueness. Databases express it as a partial or filtered unique index, and not every engine has one; where it is missing, the guard exists in the in-memory adapter and not in the relational one. Say so in the record rather than assuming both adapters are covered.

- Related pitfalls: [Modifying two aggregates in one transaction](/pitfall/modifying-two-aggregates-in-one-transaction.md) · [Remote effect before local preconditions](/pitfall/remote-effect-before-local-preconditions.md)

## Anchors

- Markers: [Repository&lt;T, ID&gt;](/marker/port-out/repository.md) · [TransactionBoundary](/marker/application/transactionboundary.md)
