---
type: Marker
title: "BaseAggregateRoot<T, ID>"
category: tactical
kind: class
signature: "public abstract class BaseAggregateRoot<T extends AggregateRoot<T, ID>, ID extends Id> implements AggregateRoot<T, ID>"
extends: [AggregateRoot]
methods: ["throw new IllegalArgumentException(\"Domain event cannot be null\")"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/tactical/BaseAggregateRoot.java
tags: [tactical, marker]
---

Abstract base class for Aggregate Roots providing domain event collection.

## Extends

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)

## Referenced by ADRs

- [ADR-002: Framework-Independent Domain Layer](/adr/adr-002-framework-independent-domain.md)
- [ADR-003: Aggregate Reference by Identity Only](/adr/adr-003-aggregate-reference-by-id.md)
- [ADR-005: Domain Events Publishing Strategy](/adr/adr-005-domain-events-publishing.md)
- [ADR-007: Hexagonal Architecture with Explicit Port/Adapter Separation](/adr/adr-007-hexagonal-architecture.md)

## Discussed in

- [Marker Interfaces](/book/11-shared-kernel/marker-interfaces.md)
- [Domain Events](/book/14-events-integration/domain-events.md)
