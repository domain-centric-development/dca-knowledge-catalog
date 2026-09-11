---
type: Template
title: "Specification skeleton (business rule as a first-class object)"
tags: [template, domain, specification]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/specification.md, /rule/advanced/dca-adv-017.md, /rule/advanced/dca-adv-018.md, /guide/elements.md, /guide/quick-reference/framework-annotations.md, /guide/spring-modulith/shared-kernel-in-spring-modulith.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for the **Specification pattern**: a business rule expressed as a first-class, immutable domain object that answers a single yes/no question via `isSatisfiedBy(candidate)`. Use it to make a named business rule reusable across validation, selection, and construction, and combinable (`and`/`or`/`not`) into richer rules. It implements the generic `Specification<T>` marker (which declares `boolean isSatisfiedBy(T candidate)`), lives in the domain layer, carries **no** Spring annotation, and its type name ends with `Specification`. Replace `{Name}` / `{T}` (the candidate type) / `{context}` / `{basePackage}`.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`specification/java.md`](/template/specification/java.md)

## Realizes / governed by

- Marker: [Specification<T>](/marker/tactical/specification.md)
- Rules: [Specifications must end with 'Specification'](/rule/advanced/dca-adv-017.md) · [Specifications must not have Spring annotations](/rule/advanced/dca-adv-018.md)
- Guide: [Layer elements](/guide/elements.md) · [Framework annotation rules](/guide/quick-reference/framework-annotations.md) · [Shared kernel](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)
- Decisions: [Specification or query method](/decision/specification-vs-query-method.md)
