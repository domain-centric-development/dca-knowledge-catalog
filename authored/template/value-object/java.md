---
type: Template
title: "Value object skeleton (Java record implementing Value) — Java"
parent: /template/value-object.md
tags: [template, domain, value-object]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/value.md, /rule/tactical/dca-tac-009.md, /rule/tactical/dca-tac-010.md, /rule/tactical/dca-tac-011.md, /rule/tactical/dca-tac-008.md, /guide/readme/elements.md]
applies_to: [java]
framework: [framework-neutral]
---

The Java code of [Value object skeleton (Java record implementing Value)](/template/value-object.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}.java` — the value object

```java
package {basePackage}.{context}.domain.{name};

import dev.domaincentric.dca.buildingblocks.ddd.tactical.Value;

/** Immutable value object. Equality is by attribute (record), never by identity. */
public record {Name}(String value) implements Value {

    public {Name} {
        // Enforce all invariants here so an instance can never be invalid.
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("{Name} value required");
        }
        // additional format/range checks as the concept demands
    }

    /** Intention-revealing factory (optional but conventional). */
    public static {Name} of(final String value) {
        return new {Name}(value);
    }
}
```

Records give you immutability, `equals`/`hashCode` by attribute, and a canonical
constructor for free. A value object must not reference an entity or aggregate
root, and must not expose setters. If the concept groups several fields, add them
as further record components (each still validated in the compact constructor).

Universal, cross-context value objects live in `sharedkernel/domain/model/`
instead of a bounded context's `domain/` package.
