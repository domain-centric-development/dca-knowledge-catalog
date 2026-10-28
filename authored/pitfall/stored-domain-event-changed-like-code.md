---
type: Pitfall
title: A stored domain event changed like code
tags: [pitfall, events, outbox]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/integration-patterns/reacting-to-an-event.md, /marker/tactical/domainevent.md, /marker/tactical/integrationeventtype.md]
---

A domain event is renamed, a field removed, the record moved to another package — a refactoring the compiler and
every test accept. The application is deployed. Publications that were still due in the outbox, written
by the previous deployment, can no longer be read: deserialisation fails, or the stored type name points at a class
that no longer exists. The reactions they should have triggered never run.

## Why it is wrong

- "Domain events need no versioning" holds only for in-process delivery that completes inside the transaction. Once a
  transactional listener exists, the event is persisted data, and the next deployment reads what the previous one
  wrote.
- Many outboxes record the event's fully qualified class name and the listener's identity (bean and method). A package
  move or a renamed listener method breaks every pending publication without changing a line of behaviour.
- The failure appears in production only, after a deployment, for publications that happened to be in flight.

## Do instead

Treat a domain event in the outbox like a database row — no version number, but what a migration needs:

- **Tolerant reading.** Ignore unknown fields, default missing ones. Adding a field is always safe.
- **Two steps** for a rename or removal: add the new field and keep reading the old one; drop the old one a
  deployment later.
- **Or deploy on an empty outbox:** drain it first and check for failed publications.
- **A logical type name** where the outbox lets you record one, as integration events do with their type metadata.
- **Carry little.** Ids practically never change; every extra field is one more thing that can.

## Anchors

- Guide: [Reacting to an event](/guide/integration-patterns/reacting-to-an-event.md)
- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [IntegrationEventType](/marker/tactical/integrationeventtype.md)
- Decision: [Reacting to an event: one path, two listener kinds](/decision/reacting-to-an-event.md)
