---
type: Pitfall
title: "Remote effect before local preconditions: an intent nobody can use"
tags: [pitfall, application, use-case, port-out, events]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/outputport.md, /marker/application/transactionboundary.md]
---

A use case that creates an effect in somebody else's system — a payment intent, a reservation, a shipping label, a provisioning request — and only afterwards loads the aggregate that decides whether the operation is allowed at all. The aggregate then refuses: the state is wrong, a required step is missing, the amount is zero. The use case fails, the transaction rolls back, and the effect stays where it was made.

It is the sibling of [remote call inside a transaction](/pitfall/remote-call-inside-a-transaction.md), and keeping the call out of the transaction is what makes it visible: the remote step now stands on its own, in an order somebody chose.

## Why it is wrong

- **The effect outlives the failure.** A rollback is local. The other system holds a reservation, a hold on funds, a half-created record, and has no idea the caller gave up.
- **Nothing will clean it up.** Whoever wrote the use case saw the refusal as "the user gets an error", not as "we left something behind".
- **The refusal was knowable beforehand.** The preconditions are the aggregate's own; loading it first costs one read, and the read is needed anyway.
- **It gets worse with retries.** A caller who tries again produces a second effect, then a third, each one abandoned in the same way.

## How to spot it

Read the use case in order and mark every line that leaves the process. If the first such line comes before the aggregate has been asked anything, the pitfall is there. A second tell: the aggregate's guard clauses are reachable only *after* the port call, so a test for "state not allowed" passes while the remote call already happened.

## Do instead

**Ask the aggregate first.** Give it a method that asserts the preconditions and changes nothing — `assertReadyFor…()` — holding exactly what the mutating method enforces. The use case loads the aggregate once, asserts, and only then reaches the port.

```java
Order order = orders.findById(id).orElseThrow();
order.assertReadyForDispatch();                 // everything the aggregate can refuse
LabelResult label = carrier.createLabel(order.shipment());   // remote effect
return transactionBoundary.inTransaction(() -> { … });       // short transaction
```

**Close the rest of the window deliberately.** The check cannot be atomic with the write: between them the aggregate can be confirmed, cancelled or expire. Pick one and write it down.

- **Compensate** — on failure, call the port's release operation for the reference just created, and re-throw the original failure. A refused compensation is logged, not raised: the caller needs to know why their request was rejected, not that the clean-up failed too. This uses the port as it already stands, and it usually gives its cancel operation its first caller.
- **Make the effect idempotent** — pass a key derived from the aggregate's identity so a retry reuses the effect instead of creating a second. Better under retries, but it is a change to the port's contract and needs the other system to honour it.

Either way, say in the record what happens when the process dies between the effect and the compensation: that intent is orphaned, and only reconciliation finds it. A sample that pretends otherwise teaches a reader that compensation is a guarantee.

- Related pitfalls: [Remote call inside a transaction](/pitfall/remote-call-inside-a-transaction.md) · [Event listener performs the external effect](/pitfall/event-listener-performs-the-external-effect.md)

## Anchors

- Markers: [OutputPort](/marker/port-out/outputport.md) · [TransactionBoundary](/marker/application/transactionboundary.md)
