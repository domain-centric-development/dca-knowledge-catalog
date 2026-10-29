---
type: Decision
title: "Reading an aggregate: getters that return values, not a mediator"
tags: [decision, aggregate, value-object, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/domain-layer-rules.md, /decision/result-shape-and-assembly.md, /marker/tactical/aggregateroot.md, /marker/tactical/value.md]
---

A use case that shows an aggregate needs its state: a name, an amount, a status. Two ways to get it out.

**A mediator ("interest").** Vaughn Vernon describes it in *Implementing Domain-Driven Design* (ch. 14, "Use a
Mediator to Publish Aggregate Internal State"): the caller passes an interface, and the aggregate calls
`informName(...)`, `informAmount(...)` on it, so it needs no getters and reveals no structure. The cost: one
`inform…` method per attribute, an implementation per caller that collects the calls into an object again, and — in
his own example — the values handed over as bare strings and ids.

**Getters that return values.** The aggregate offers read methods that return its value objects and ids:
`name()` returns a `ProductName`, `price()` a `Money`. The use case assembles the `*Result` from them.

**DCA reads through getters that return values.** The value objects carry the meaning and the rules across the
boundary, so nothing is revealed that a type does not already promise; the mapping happens once, in the result
assembly. What stays forbidden is the other half of the "no getters" advice: a setter, and a use case that reads the
state to decide what the aggregate should do — that decision is the aggregate's
([Asking the aggregate, deciding outside it](/pitfall/asking-the-aggregate-and-deciding-outside.md)).

A getter returns a value object or an id, never a bare primitive (`DCA-TAC-025`, experimental); a `boolean`
predicate is the one bare return that passes.

## Anchors

- Guide: [Domain layer rules](/guide/rules/domain-layer-rules.md)
- Decision: [Result shape and assembly](/decision/result-shape-and-assembly.md)
- Markers: [AggregateRoot](/marker/tactical/aggregateroot.md) · [Value](/marker/tactical/value.md)
