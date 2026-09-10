---
type: Template
title: "Aggregate root skeleton (BaseAggregateRoot + Id + domain event)"
tags: [template, domain, aggregate]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/readme/deviations-from-the-literature.md, /marker/tactical/aggregateroot.md, /marker/tactical/baseaggregateroot.md, /marker/tactical/domainevent.md, /marker/port-out/repository.md, /guide/readme/elements.md, /guide/readme/rules.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for an aggregate root: the consistency boundary that enforces invariants and registers domain events. Replace `{Name}` / `{context}` / `{basePackage}`. The domain layer is framework-free — no Spring/JPA annotations.

## `{Name}Id.java` — typed identity (value object)

```java
package {basePackage}.{context}.domain.{name};

import dev.domaincentric.dca.buildingblocks.ddd.tactical.Id;
import java.util.UUID;

/**
 * Typed identity. Reference other aggregates by their Id, never by object.
 *
 * <p>Implementing {@code Id} is not decoration: {@code AggregateRoot<T, ID extends Id>} and
 * {@code Repository<T, ID extends Id>} bound their ID parameter on it, so a plain record does
 * not satisfy them.
 */
public record {Name}Id(UUID value) implements Id {
    public {Name}Id {
        if (value == null) throw new IllegalArgumentException("id required");
    }
    public static {Name}Id generate() { return new {Name}Id(UUID.randomUUID()); }
}
```

## `{Name}Created.java` — domain event (past tense, immutable)

```java
package {basePackage}.{context}.domain.{name};

import dev.domaincentric.dca.buildingblocks.ddd.tactical.DomainEvent;
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

import dev.domaincentric.dca.buildingblocks.ddd.tactical.BaseAggregateRoot;

/**
 * Two type parameters, not one: {@code BaseAggregateRoot<T extends AggregateRoot<T, ID>, ID extends
 * Id>} is self-referential (F-bounded), which is what lets {@code sameIdentityAs} take the concrete
 * type. The base class holds the events; identity is the aggregate's own field.
 */
public class {Name} extends BaseAggregateRoot<{Name}, {Name}Id> {

    private final {Name}Id id;

    // further invariant-protected state; no setters — mutate through intention-revealing methods

    private {Name}({Name}Id id) {
        this.id = id;
    }

    @Override
    public {Name}Id id() {
        return id;
    }

    /** Factory enforces creation invariants and registers the creation event. */
    public static {Name} create({Name}Id id /*, args */) {
        var aggregate = new {Name}(id);
        // enforce invariants here
        aggregate.registerEvent({Name}Created.of(id));
        return aggregate;
    }

    /**
     * Rebuilds a stored aggregate from persisted state. Registers no event: a stored aggregate is
     * a fact, and re-reading it must not replay what the writer already published. Only outgoing
     * adapters (in-memory, JDBC, JPA) call this.
     */
    public static {Name} reconstitute({Name}Id id /*, persisted state */) {
        var aggregate = new {Name}(id);
        // assign the persisted state as-is; invariants were enforced when it was written
        return aggregate;
    }

    // behavior methods enforce invariants, then registerEvent(...)
}
```

Two factories, two moments in the aggregate's life: `create` is the birth of a new business fact and registers `{Name}Created`; `reconstitute` is a repository handing back what it stored and registers nothing — an adapter that rebuilds through `create` publishes a phantom creation event on the next save ([Reconstitution raises the creation event](/pitfall/reconstitution-raises-creation-event.md)).

The use case persists the aggregate, then publishes and clears its domain events. Repository for this aggregate: see the use-case template's output ports and [Deviations from the literature](/guide/readme/deviations-from-the-literature.md).

## Realizes / governed by

- Markers: [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md) · [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md) · [DomainEvent](/marker/tactical/domainevent.md) · [Repository<T, ID>](/marker/port-out/repository.md)
- Guide: [Layer elements](/guide/readme/elements.md) · [Layer rules](/guide/readme/rules.md)
- Recipe: [Add an aggregate](/recipe/add-an-aggregate.md)
- Pitfall: [Reconstitution raises the creation event](/pitfall/reconstitution-raises-creation-event.md)
