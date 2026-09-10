---
type: Template
title: "Specification skeleton (business rule as a first-class object) — Java"
parent: /template/specification.md
tags: [template, domain, specification]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/specification.md, /rule/advanced/dca-adv-017.md, /rule/advanced/dca-adv-018.md, /guide/readme/elements.md, /guide/architecture-reference-guide/framework-annotations-rules.md, /guide/spring-modulith/shared-kernel-in-spring-modulith.md]
applies_to: [java]
framework: [framework-neutral]
---

The Java code of [Specification skeleton (business rule as a first-class object)](/template/specification.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

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
