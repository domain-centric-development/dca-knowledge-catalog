---
type: Marker
title: "Entity<T, ID>"
category: tactical
kind: interface
signature: "public interface Entity<T extends Entity<T, ID>, ID extends Id>"
methods: ["ID id()"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/tactical/Entity.java
tags: [tactical, marker]
---

Marker for Entity.

## Governed by

- [Domain model classes must not have public setter methods](/rule/tactical/domain-model-classes-must-not-have-public-setter-methods.md)
- [Entities must have an ID field](/rule/tactical/entities-must-have-an-id-field.md)
- [Entities must not be instantiated directly from outside the aggregate](/rule/tactical/entities-must-not-be-instantiated-directly-from-outside-the-aggregate.md)
- [Entities must not have fields with Aggregate Root types](/rule/tactical/entities-must-not-have-fields-with-aggregate-root-types.md)
- [Repository methods must return Aggregate Roots](/rule/tactical/repository-methods-must-return-aggregate-roots.md)
- [Value Objects must not contain Aggregate Roots or Entities](/rule/tactical/value-objects-must-not-contain-aggregate-roots-or-entities.md)

## Referenced by ADRs

- [ADR-005: Domain Events Publishing Strategy](/adr/adr-005-domain-events-publishing.md)

## Discussed in

- [Step 3: Domain Layer - Entity & Aggregate](/book/03-getting-started/step-3-domain-layer-entity-aggregate.md)
- [Tactical Building Blocks](/book/05-domain-layer/tactical-building-blocks.md)
- [Outgoing Adapters](/book/07-adapter-layer/outgoing-adapters.md)
- [JPA Repository Implementation](/book/15-persistence-patterns/jpa-repository-implementation.md)
- [Event Store Design](/book/17-event-sourcing/event-store-design.md)
- [Naming Conventions](/book/appendix-d-cheat-sheet/naming-conventions.md)
- [Key Differences](/book/clean-architecture-comparison/key-differences.md)
- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Framework Annotations Rules](/guide/architecture-reference-guide/framework-annotations-rules.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
