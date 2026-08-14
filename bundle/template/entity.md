---
type: Template
title: "Entity skeleton (implements Entity<T, ID>, identity-based)"
tags: [template, domain, entity]
---

Domain-free skeleton for an entity: a domain object with a distinct identity that lives *inside* an aggregate. An entity is not an aggregate root — it cannot exist on its own and is created and mutated only through its aggregate root, which is why its constructor and mutators are package-private. Replace `{Name}` / `{context}` / `{name}` / `{basePackage}`. The domain layer is framework-free.

## `{Name}Id.java` — the entity's identity (value object)

```java
package {basePackage}.{context}.domain.{name};

import {basePackage}.sharedkernel.marker.tactical.Id;
import java.util.UUID;

/** Local identity of the entity within its aggregate. */
public record {Name}Id(UUID value) implements Id {
    public {Name}Id {
        if (value == null) throw new IllegalArgumentException("id required");
    }
    public static {Name}Id generate() { return new {Name}Id(UUID.randomUUID()); }
}
```

## `{Name}.java` — the entity

```java
package {basePackage}.{context}.domain.{name};

import {basePackage}.sharedkernel.marker.tactical.Entity;

/** Entity within the {aggregate} aggregate. Created and modified only via the aggregate root. */
public final class {Name} implements Entity<{Name}, {Name}Id> {

    private final {Name}Id id;
    // additional invariant-protected state; mutable fields have no public setters

    /** Package-private — instances are created only by the aggregate root, never from outside. */
    {Name}(final {Name}Id id /*, args */) {
        this.id = id;
    }

    @Override
    public {Name}Id id() {
        return id;
    }

    /** Package-private mutator — only the aggregate root may change entity state. */
    void change(/* args */) {
        // enforce invariants, then mutate
    }
}
```

Identity comes from `id()`; the marker's default `sameIdentityAs` compares by it,
so two entities are equal when their ids match, regardless of attributes. Keep the
constructor and mutators package-private so the enclosing aggregate root stays the
only way to create or change the entity — this is what the "not instantiated
directly from outside the aggregate" rule enforces. An entity must not hold a
field of an aggregate-root type; reference other aggregates by their Id.

## Realizes / governed by

- Marker: [Entity<T, ID>](/marker/tactical/entity.md) · [Id](/marker/tactical/id.md)
- Rules: [Entities must have an ID field](/rule/tactical/entities-must-have-an-id-field.md) · [Entities must not be instantiated directly from outside the aggregate](/rule/tactical/entities-must-not-be-instantiated-directly-from-outside-the-aggregate.md) · [Entities must not have fields with Aggregate Root types](/rule/tactical/entities-must-not-have-fields-with-aggregate-root-types.md) · [Domain model classes must not have public setter methods](/rule/tactical/domain-model-classes-must-not-have-public-setter-methods.md)
- Guide: [Layer elements](/guide/readme/elements.md)
- Decision: [Entity vs. Value Object](/decision/entity-vs-value-object.md)
- Recipe: [Add an aggregate](/recipe/add-an-aggregate.md)
