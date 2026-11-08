---
type: Decision
title: A yes/no fact or a state — a boolean field, an enum, or separate fields
tags: [decision, tactical, aggregate, value-object, ubiquitous-language]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/domain-layer-rules.md, /rule/tactical/dca-tac-025.md, /decision/name-an-operation-in-the-glossary.md, /pitfall/asking-the-aggregate-and-deciding-outside.md, /marker/tactical/aggregateroot.md, /marker/tactical/value.md]
---

An aggregate often holds something that is true or not: an order is paid, an account is locked, an entry is completed. Two implementations of the same story model it differently — one as a `boolean` field with a predicate, one as a value `EntryState` with two constants — and both are defensible. Where the method decides, they agree.

## The discriminator

Ask, for each fact the aggregate holds:

1. **Does it have exactly two values, and is the change between them a single operation?** Then it is a yes/no fact. *Completed* or not, reached by `complete()`.
2. **Does it have three or more values, or do its transitions carry rules?** *Draft → submitted → approved → rejected*, where only a submitted order may be approved: that is a state. It is an enum, or a value when the transitions are the value's own rules.
3. **Can two such facts be true at the same time?** *Completed* and *archived*, *archived* and *deleted* hold independently. Each is a fact of its own — two fields, never one status whose values multiply the combinations.
4. **Does the glossary already decide it?** If the people who own the domain name a status with its values, the glossary wins, even for two values.

## Options

### A single yes/no fact: a `boolean` field (do this)

The aggregate keeps the fact to itself, is told to change it and answers when asked:

```java
private boolean completed;

public void complete() {
    if (completed) throw new EntryAlreadyCompleted(id);
    this.completed = true;
}

public boolean isCompleted() { return completed; }
```

The field stays internal: no setter, and no domain method takes a `boolean`. `setCompleted(true)` — a flag argument — would let the caller set the state instead of triggering the behaviour, and the rule the aggregate guards in `complete()` would be bypassed. A reverse operation, where the domain has one, is an operation of its own with its own name: `reopen()`, not `setCompleted(false)`.

A persisted aggregate keeps the same shape. The factory that rebuilds it from storage hands the stored fact back as the `boolean` it was — that is no flag argument, because nothing is triggered and no caller decides the state:

```java
static Entry reconstitute(EntryId id, Title title, boolean completed) {
    Entry entry = new Entry(id, title);
    entry.completed = completed;
    return entry;
}
```

Only that factory may take the `boolean`; every operation still names what happens.

### Three or more states, or transitions with rules: an enum or a value

```java
private OrderStatus status;   // DRAFT, SUBMITTED, APPROVED, REJECTED

public void approve() {
    if (status != OrderStatus.SUBMITTED) throw new OrderNotSubmitted(id);
    this.status = OrderStatus.APPROVED;
}
```

The operations stay named after what happens; the status is never set from outside. When the allowed transitions are many, they move into the enum or the value (`status.approve()` returns the next status or refuses).

### Several independent facts: one field each

`completed`, `archived`, `deleted` as three `boolean` fields — each with its own operation and predicate. Folded into one status, the combinations become values of their own (`COMPLETED_AND_ARCHIVED`), and every new fact doubles them.

## Consequences

- The rule `DCA-TAC-025` (experimental) holds the shape: a `boolean` field and a `boolean` returned pass; a `boolean` parameter of a domain method, and a `boolean` the caller can set from outside, are reported as flag arguments. The factory that rebuilds a stored aggregate is the exception, recognised by its name — `reconstitute` or `restore` by default, configurable where a project names it otherwise; its other parameters are checked as usual.
- Whether a fact has two values or more is a question about the domain, not about the code. A rule cannot answer it; the glossary can.
- A two-valued fact that later gains a third value becomes an enum then — the operations keep their names, only the field changes.

## Anchors

- Guide: [Domain layer rules](/guide/rules/domain-layer-rules.md) — a single yes/no fact is a `boolean` field
- Rule: [Domain types must not hold bare primitives, strings or time types; a boolean only as a field or a predicate](/rule/tactical/dca-tac-025.md)
- Markers: [AggregateRoot&lt;T, ID&gt;](/marker/tactical/aggregateroot.md) · [Value](/marker/tactical/value.md)
- Related decisions: [Name an operation in the glossary](/decision/name-an-operation-in-the-glossary.md) · [Reading an aggregate](/decision/reading-an-aggregate.md)
- Related pitfall: [Asking the aggregate, deciding outside it](/pitfall/asking-the-aggregate-and-deciding-outside.md)
