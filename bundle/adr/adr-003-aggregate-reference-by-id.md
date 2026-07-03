---
type: ADR
title: "ADR-003: Aggregate Reference by Identity Only"
adr: 3
status: accepted
pattern: "Aggregate Roots MUST reference other Aggregate Roots by ID only, NEVER by direct object reference."
resource: ai-architecture-sample/docs/architecture/adr/adr-003-aggregate-reference-by-id.md
tags: [adr, aggregate]
---

Aggregate Roots MUST reference other Aggregate Roots by ID only, NEVER by direct object reference.

**Consequences:** Clear Boundaries · Performance · Scalability · Flexibility · Simple Transactions · Easy Testing · Eventual Consistency · None identified

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md)

## Enforced by

- [Aggregate Roots must not have fields with other Aggregate Root types](/rule/tactical/aggregate-roots-must-not-have-fields-with-other-aggregate-root-types.md)
- [Entities must not have fields with Aggregate Root types](/rule/tactical/entities-must-not-have-fields-with-aggregate-root-types.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
