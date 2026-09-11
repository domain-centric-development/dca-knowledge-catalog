---
type: Template
title: "Value object skeleton (Java record implementing Value)"
tags: [template, domain, value-object]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/value.md, /rule/tactical/dca-tac-009.md, /rule/tactical/dca-tac-010.md, /rule/tactical/dca-tac-011.md, /rule/tactical/dca-tac-008.md, /guide/elements.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for a value object: an immutable, attribute-equal concept with no identity. Model it as a Java `record` implementing the `Value` marker, with validation in the compact constructor. Replace `{Name}` (PascalCase), `{context}`, `{name}` (lowercase), `{basePackage}`. The domain layer is framework-free — no Spring/JPA annotations.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`value-object/java.md`](/template/value-object/java.md)

## Realizes / governed by

- Marker: [Value](/marker/tactical/value.md)
- Rules: [Value Object classes should be final (immutability)](/rule/tactical/dca-tac-009.md) · [Value Object fields must be final (deep immutability)](/rule/tactical/dca-tac-010.md) · [Value Objects must not have setter methods](/rule/tactical/dca-tac-011.md) · [Value Objects must not contain Aggregate Roots or Entities](/rule/tactical/dca-tac-008.md)
- Guide: [Layer elements](/guide/elements.md)
- Decision: [Entity vs. Value Object](/decision/entity-vs-value-object.md)
- Recipe: [Add a value object](/recipe/add-a-value-object.md)
