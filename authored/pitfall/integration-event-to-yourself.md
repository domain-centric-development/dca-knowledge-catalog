---
type: Pitfall
title: An integration event to yourself
tags: [pitfall, events, integration-event, outbox]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/integration-patterns/reacting-to-an-event.md, /marker/tactical/domainevent.md, /marker/tactical/integrationevent.md, /marker/tactical/integrationeventtype.md]
---

A context needs a durable reaction to a fact of its own. The only durable delivery the application has is the outbox
for integration events, so the fact is translated into an integration event, published, and consumed again by a
listener in the same context. No other context reads the contract.

## Why it is wrong

- It buys a published contract — a name, a version, compatibility rules, a place in the context's public surface —
  for a reader that ships with the writer and changes with it.
- The context map shows a contract nobody outside consumes, and reviewers treat it as a promise to strangers.
- It is the symptom, not the cause: the application has no durable delivery for domain events, and the outbox for
  integration events was bent to fill the gap.

## Do instead

That is what domain events are for. Capture the domain event in the outbox and subscribe with a transactional
listener: delivered after the commit, in its own transaction. Publish an integration event only when another context
consumes it.

## Anchors

- Decision: [Reacting to an event: one path, two listener kinds](/decision/reacting-to-an-event.md) · [Domain event vs. integration event](/decision/domain-event-vs-integration-event.md)
- Guide: [Reacting to an event](/guide/integration-patterns/reacting-to-an-event.md)
- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [IntegrationEvent](/marker/tactical/integrationevent.md) · [IntegrationEventType](/marker/tactical/integrationeventtype.md)
