---
type: Template
title: "Entity skeleton (implements Entity<T, ID>, identity-based)"
tags: [template, domain, entity]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/entity.md, /marker/tactical/id.md, /rule/tactical/dca-tac-004.md, /rule/tactical/dca-tac-005.md, /rule/tactical/dca-tac-007.md, /rule/tactical/dca-tac-006.md, /guide/elements.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for an entity: a domain object with a distinct identity that lives *inside* an aggregate. An entity is not an aggregate root — it cannot exist on its own and is created and mutated only through its aggregate root, which is why its constructor and mutators are package-private. Replace `{Name}` / `{context}` / `{name}` / `{basePackage}`. The domain layer is framework-free.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`entity/java.md`](/template/entity/java.md)

## Realizes / governed by

- Marker: [Entity<T, ID>](/marker/tactical/entity.md) · [Id](/marker/tactical/id.md)
- Rules: [Entities must have an ID field](/rule/tactical/dca-tac-004.md) · [Entities must not be instantiated directly from outside the aggregate](/rule/tactical/dca-tac-005.md) · [Entities must not have fields with Aggregate Root types](/rule/tactical/dca-tac-007.md) · [Domain model classes must not have public setter methods](/rule/tactical/dca-tac-006.md)
- Guide: [Layer elements](/guide/elements.md)
- Decision: [Entity vs. Value Object](/decision/entity-vs-value-object.md)
- Recipe: [Add an aggregate](/recipe/add-an-aggregate.md)
