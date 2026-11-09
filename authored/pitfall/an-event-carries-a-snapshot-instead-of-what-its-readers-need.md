---
type: Pitfall
title: "An event carries a snapshot of the aggregate instead of what its readers need"
tags: [pitfall, events, domain-event, integration-event]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domainevent.md, /decision/domain-event-vs-integration-event.md]
---

An event is written by copying the aggregate's fields into it: everything the aggregate knew at that moment, in
case a reader wants it. One writer copies three fields, another five; both are "complete".

## Why it is wrong

- **No reader decides the shape, so every writer does.** Two implementations of the same event differ in fields
  nobody reads — a determinism gap with no test to see it.
- **Every copied field is a contract.** Once published, a field is read by someone or kept forever; removing it
  later is a breaking change, made for data nobody asked for.
- **It leaks the aggregate's shape** into every consumer and ties them to its next change.

## How to spot it

List the event's fields and, for each, the reader that uses it. A field without a reader — in the listeners, the
translators to integration events, the log — is a snapshot field.

## Do instead

**An event carries what happened and what its readers need to react.** Start from the readers: the identity of
what changed, the facts the reaction needs. A new reader that needs more adds the field with its reason; the event
does not grow on speculation.

## Anchors

- Marker: [DomainEvent](/marker/tactical/domainevent.md)
- Decision: [Domain event vs integration event](/decision/domain-event-vs-integration-event.md)
- Pitfall: [An event without a type of its own](/pitfall/an-event-without-a-type-of-its-own.md)
