---
type: Template
title: "Aggregate root skeleton (BaseAggregateRoot + Id + domain event)"
tags: [template, domain, aggregate]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/readme/deviations-from-the-literature.md, /marker/tactical/aggregateroot.md, /marker/tactical/baseaggregateroot.md, /marker/tactical/domainevent.md, /marker/port-out/repository.md, /guide/elements.md, /guide/rules.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for an aggregate root: the consistency boundary that enforces invariants and registers domain events. Replace `{Name}` / `{context}` / `{basePackage}`. The domain layer is framework-free — no Spring/JPA annotations.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`aggregate-root/java.md`](/template/aggregate-root/java.md)

## Realizes / governed by

- Markers: [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md) · [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md) · [DomainEvent](/marker/tactical/domainevent.md) · [Repository<T, ID>](/marker/port-out/repository.md)
- Guide: [Layer elements](/guide/elements.md) · [Layer rules](/guide/rules.md)
- Recipe: [Add an aggregate](/recipe/add-an-aggregate.md)
- Pitfall: [Reconstitution raises the creation event](/pitfall/reconstitution-raises-creation-event.md)
