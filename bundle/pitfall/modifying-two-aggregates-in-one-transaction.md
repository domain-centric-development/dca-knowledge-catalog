---
type: Pitfall
title: "Modifying two aggregates in one transaction"
tags: [pitfall, tactical, aggregate, domain-event, events, application]
---

A single use case that loads two aggregate roots, mutates both, and saves both inside one atomic transaction — `PlaceOrderUseCase` that calls `order.confirm()` **and** `inventory.reserve()` **and** saves each, expecting them to commit or roll back together. The aggregate boundary is also the consistency boundary; spanning two of them in one transaction erases that boundary.

## Why it is wrong

- The aggregate is defined as the transactional consistency boundary — a single unit for data changes. Two aggregates changed atomically means the true consistency unit is now their union, so neither aggregate's boundary is real.
- It creates lock contention and coupling across boundaries: the transaction holds both roots, so unrelated operations on either serialize behind it, and a change to one aggregate's persistence can break the other's.
- It smuggles in a direct object reference between roots (you fetched both to mutate them), which is exactly what reference-by-ID forbids.
- It defeats eventual consistency — the mechanism DCA uses to keep separate aggregates (and contexts) synchronized without a distributed transaction.

## What forbids it

- [Aggregate Roots must not have fields with other Aggregate Root types](/rule/tactical/aggregate-roots-must-not-have-fields-with-other-aggregate-root-types.md) — the no-direct-reference rule; if roots can't hold each other, one operation shouldn't be co-mutating both either.
- [Aggregate Roots must not hold references to repositories or other output ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md) — an aggregate can't reach out to load and change a second root; it changes only its own state.
- [ADR-005: Domain Events Publishing Strategy](/adr/adr-005-domain-events-publishing.md) — aggregates register events during mutation and publish after persistence, so the second aggregate reacts *after* the first commits, not within the same transaction.
- [ADR-003: Aggregate Reference by Identity Only](/adr/adr-003-aggregate-reference-by-id.md) — roots reference each other by ID, reinforcing one root per transaction.

## Do instead

Change one aggregate per transaction. Let it raise a domain event on commit; a handler (in-process listener, or another context's consumer) loads the second aggregate and changes it in its own transaction — eventual consistency. When a genuinely atomic multi-aggregate calculation is unavoidable, isolate it in a rare domain service (see ADR-010), but the default is one write per transaction.

`order.confirm()` → `OrderConfirmed` → handler → `inventory.reserve()` in a separate transaction.

- [Recipe: add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md) · [Recipe: publish a cross-context event](/recipe/publish-a-cross-context-event.md)
- Decisions: [Aggregate boundary size](/decision/aggregate-boundary-size.md) · [Cross-context communication](/decision/cross-context-communication.md)

## Anchors

- Rules: [Aggregate Roots must not have fields with other Aggregate Root types](/rule/tactical/aggregate-roots-must-not-have-fields-with-other-aggregate-root-types.md) · [Aggregate Roots must not hold references to repositories or other output ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md)
- ADRs: [ADR-005 Domain Events Publishing](/adr/adr-005-domain-events-publishing.md) · [ADR-003 Aggregate Reference by Identity](/adr/adr-003-aggregate-reference-by-id.md) · [ADR-010 Domain Services for Multi-Aggregate Operations](/adr/adr-010-domain-services-multi-aggregate.md)
- Markers: [AggregateRoot&lt;T, ID&gt;](/marker/tactical/aggregateroot.md) · [DomainEvent](/marker/tactical/domainevent.md)
- Book: [Tactical Building Blocks](/book/05-domain-layer/tactical-building-blocks.md) · [Domain Events vs Integration Events](/book/14-events-integration/domain-events-vs-integration-events.md)
