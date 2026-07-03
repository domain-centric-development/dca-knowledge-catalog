---
type: Template
title: "Aggregate root skeleton (BaseAggregateRoot + Id + domain event)"
tags: [template, domain, aggregate]
---

Domain-free skeleton for an aggregate root: the consistency boundary that enforces invariants and registers domain events. Replace `{Name}` / `{context}` / `{basePackage}`. The domain layer is framework-free — no Spring/JPA annotations.

## `{Name}Id.java` — typed identity (value object)

```java
package {basePackage}.{context}.domain.{name};

import java.util.UUID;

/** Typed identity. Reference other aggregates by their Id, never by object (ADR-003). */
public record {Name}Id(UUID value) {
    public {Name}Id {
        if (value == null) throw new IllegalArgumentException("id required");
    }
    public static {Name}Id generate() { return new {Name}Id(UUID.randomUUID()); }
}
```

## `{Name}Created.java` — domain event (past tense, immutable)

```java
package {basePackage}.{context}.domain.{name};

import {basePackage}.sharedkernel.marker.tactical.DomainEvent;
import java.time.Instant;
import java.util.UUID;

/** Internal fact. Stays in this context; never serialized across a boundary (no version field). */
public record {Name}Created(UUID eventId, Instant occurredOn, {Name}Id {name}Id)
        implements DomainEvent {
    public static {Name}Created of({Name}Id id) {
        return new {Name}Created(UUID.randomUUID(), Instant.now(), id);
    }
}
```

## `{Name}.java` — the aggregate root

```java
package {basePackage}.{context}.domain.{name};

import {basePackage}.sharedkernel.marker.tactical.BaseAggregateRoot;

public class {Name} extends BaseAggregateRoot<{Name}Id> {

    // invariant-protected state; no setters — mutate through intention-revealing methods

    private {Name}({Name}Id id) {
        super(id);
    }

    /** Factory enforces creation invariants and registers the creation event. */
    public static {Name} create({Name}Id id /*, args */) {
        var aggregate = new {Name}(id);
        // enforce invariants here
        aggregate.registerDomainEvent({Name}Created.of(id));
        return aggregate;
    }

    // behavior methods enforce invariants, then registerDomainEvent(...)
}
```

The use case persists the aggregate, then publishes and clears its domain events (ADR-005). Repository for this aggregate: see the use-case template's output ports and [ADR-008](/adr/adr-008-repository-interfaces-as-output-ports.md).

## Realizes / governed by

- Markers: [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md) · [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md) · [DomainEvent](/marker/tactical/domainevent.md) · [Repository<T, ID>](/marker/port-out/repository.md)
- ADRs: [ADR-003 Reference by Id](/adr/adr-003-aggregate-reference-by-id.md) · [ADR-006 Domain Events as Records](/adr/adr-006-domain-events-immutable-records.md) · [ADR-005 Domain Events Publishing](/adr/adr-005-domain-events-publishing.md)
- Recipe: [Add an aggregate](/recipe/add-an-aggregate.md)
