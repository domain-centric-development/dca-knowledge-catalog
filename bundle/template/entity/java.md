---
type: Template
title: "Entity skeleton (implements Entity<T, ID>, identity-based) — Java"
parent: /template/entity.md
tags: [template, domain, entity]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/entity.md, /marker/tactical/id.md, /rule/tactical/dca-tac-004.md, /rule/tactical/dca-tac-005.md, /rule/tactical/dca-tac-007.md, /rule/tactical/dca-tac-006.md, /guide/readme/elements.md]
applies_to: [java]
framework: [framework-neutral]
---

The Java code of [Entity skeleton (implements Entity<T, ID>, identity-based)](/template/entity.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}Id.java` — the entity's identity (value object)

```java
package {basePackage}.{context}.domain.{name};

import dev.domaincentric.dca.buildingblocks.ddd.tactical.Id;
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

import dev.domaincentric.dca.buildingblocks.ddd.tactical.Entity;

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
