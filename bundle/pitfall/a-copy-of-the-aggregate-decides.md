---
type: Pitfall
title: A copy of the aggregate decides
tags: [pitfall, aggregate, adapter, use-case, domain]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/domain-layer-rules.md, /marker/tactical/aggregateroot.md, /decision/read-model-vs-domain-query.md, /decision/who-uses-a-domain-service.md, /pitfall/asking-the-aggregate-and-deciding-outside.md]
---

The aggregate decides whether an order can still be changed. Beside it, a list of the words that mean "closed" (`CLOSED_STATES = {"shipped", "delivered", "cancelled"}`) filters the orders a page offers for editing; a read model answers `canEdit` from its own copy of the status; an adapter checks `status.startsWith("cancel")` before it hands an order on. Each copy decides what the aggregate already decides.

```java
// the second home of the rule
static final Set<String> CLOSED = Set.of("shipped", "delivered", "cancelled");
boolean editable = !CLOSED.contains(row.status());
```

## Why it is wrong

- **The rule is written twice.** The day a new state is added — `returned` — the aggregate refuses the change and the copy still offers it, or the other way round.
- **The copy decides on stale words.** It knows how the state is spelled in storage, not what it means. A rename in the model is a behaviour change in every copy.
- **Nothing ties them together.** A test of the aggregate passes; the copy has no test of its own, because nobody sees it as a rule.

## How to spot it

- A set, a list or an enum outside the domain that names states of an aggregate.
- A string comparison on a stored state field: `equals("…")`, `startsWith(…)`, `in (…)`.
- A read model or result field with a verdict (`canEdit`, `isDone`, `allowed`) computed from fields rather than taken from the aggregate.

## What catches it

No rule sees it — a list of words is an ordinary constant. It is a review question: where does this verdict come from?

## Do instead

A decision asks the aggregate: load it (or restore it from what was read) and call its query method — `order.isEditable()`. A copy the use case returns is a read model; it carries the verdict the aggregate gave when the read model was built, as a value, and never computes it again from its own fields ([Who uses a domain service — and where a read model computes](/decision/who-uses-a-domain-service.md)). Where the list exists to filter many rows cheaply, the query that filters is a method of the repository the aggregate's rule names — one place, next to the rule — not a second spelling in the adapter.

## Anchors

- Guide: [Domain layer rules](/guide/rules/domain-layer-rules.md)
- Marker: [AggregateRoot](/marker/tactical/aggregateroot.md)
- Decisions: [Read model vs. domain query](/decision/read-model-vs-domain-query.md) · [Who uses a domain service — and where a read model computes](/decision/who-uses-a-domain-service.md)
- Related pitfalls: [Asking the aggregate, deciding outside it](/pitfall/asking-the-aggregate-and-deciding-outside.md) · [A state changed past the aggregate](/pitfall/a-state-changed-past-the-aggregate.md)
