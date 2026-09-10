---
type: Template
title: "Factory skeleton (complex aggregate creation in the domain)"
tags: [template, domain, factory]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/factory.md, /rule/advanced/dca-adv-013.md, /rule/advanced/dca-adv-014.md, /rule/advanced/dca-adv-015.md, /rule/advanced/dca-adv-016.md, /guide/readme/elements.md, /guide/architecture-reference-guide/framework-annotations-rules.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for a **Factory**: a domain-layer object that encapsulates complex creation of an aggregate so that every returned instance is fully formed and satisfies its invariants from the first moment. Use it when construction is multi-step, requires knowledge the aggregate doesn't own, or would otherwise force a constructor to break the aggregate's invariants. It implements the `Factory` marker, is stateless (or minimal `final` state), carries **no** Spring annotation, and lives beside the aggregate in the domain layer. For simple cases prefer a static factory method on the aggregate itself (`{Name}.of(...)`) over a separate class — see the decision link. Replace `{Name}` (aggregate) / `{name}` / `{context}` / `{basePackage}`.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`factory/java.md`](/template/factory/java.md)

## Realizes / governed by

- Marker: [Factory](/marker/tactical/factory.md)
- Rules: [Factories should implement Factory Marker Interface](/rule/advanced/dca-adv-013.md) · [Factories must reside in domain package](/rule/advanced/dca-adv-014.md) · [Factories must not have Spring annotations](/rule/advanced/dca-adv-015.md) · [Factories should be stateless (only final fields for dependencies)](/rule/advanced/dca-adv-016.md)
- Guide: [Layer elements](/guide/readme/elements.md) · [Framework annotation rules](/guide/architecture-reference-guide/framework-annotations-rules.md)
- Decisions: [Factory or constructor](/decision/factory-vs-constructor.md)
- Related template: [Aggregate root](/template/aggregate-root.md)
