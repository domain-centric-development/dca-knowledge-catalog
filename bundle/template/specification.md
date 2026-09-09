---
type: Template
title: "Specification skeleton (business rule as a first-class object)"
tags: [template, domain, specification]
---

Domain-free skeleton for the **Specification pattern**: a business rule expressed as a first-class, immutable domain object that answers a single yes/no question via `isSatisfiedBy(candidate)`. Use it to make a named business rule reusable across validation, selection, and construction, and combinable (`and`/`or`/`not`) into richer rules. It implements the generic `Specification<T>` marker (which declares `boolean isSatisfiedBy(T candidate)`), lives in the domain layer, carries **no** Spring annotation, and its type name ends with `Specification`. Replace `{Name}` / `{T}` (the candidate type) / `{context}` / `{basePackage}`.

## `{Name}Specification.java` — specification (domain layer)

```java
package {basePackage}.{context}.domain.{concept};

import dev.domaincentric.dca.buildingblocks.ddd.tactical.Specification;

/**
 * {Business rule phrased in the ubiquitous language}, e.g. "an order is eligible
 * for express shipping". Immutable and framework-free.
 */
public final class {Name}Specification implements Specification<{T}> {

    private final {Criterion} criterion;

    public {Name}Specification(final {Criterion} criterion) {
        this.criterion = criterion;
    }

    @Override
    public boolean isSatisfiedBy(final {T} candidate) {
        // express the business rule against the candidate's domain state
        return /* rule */;
    }
}
```

The class is `final`, immutable (only `final` fields set in the constructor), and
holds no framework dependency. It phrases the rule in domain terms — a reader
knows *what* it checks from the name alone.

## Combining specifications

Composite specifications let callers build complex rules from simple ones without
touching the leaf classes:

```java
public final class AndSpecification<{T}> implements Specification<{T}> {

    private final Specification<{T}> left;
    private final Specification<{T}> right;

    public AndSpecification(final Specification<{T}> left, final Specification<{T}> right) {
        this.left = left;
        this.right = right;
    }

    @Override
    public boolean isSatisfiedBy(final {T} candidate) {
        return left.isSatisfiedBy(candidate) && right.isSatisfiedBy(candidate);
    }
}
```

Provide `and` / `or` / `not` combinators (as default methods on a shared base or
as explicit composites) so rules compose in the ubiquitous language. A
specification tests an in-memory candidate; when the question is really "which
stored objects match", that is a repository query, not a specification — see the
decision link.

## Realizes / governed by

- Marker: [Specification<T>](/marker/tactical/specification.md)
- Rules: [Specifications must end with 'Specification'](/rule/advanced/specifications-must-end-with-specification.md) · [Specifications must not have Spring annotations](/rule/advanced/specifications-must-not-carry-container-annotations.md)
- Guide: [Layer elements](/guide/readme/elements.md) · [Framework annotation rules](/guide/architecture-reference-guide/framework-annotations-rules.md) · [Shared kernel](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)
- Decisions: [Specification or query method](/decision/specification-vs-query-method.md)
