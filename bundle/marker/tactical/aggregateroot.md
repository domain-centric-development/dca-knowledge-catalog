---
type: Marker
title: "AggregateRoot<T, ID>"
category: tactical
kind: interface
signature: "public interface AggregateRoot<T extends AggregateRoot<T, ID>, ID extends Id> extends Entity<T, ID>"
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
extends: [Entity]
methods: ["List<DomainEvent> domainEvents()", "void clearDomainEvents()"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/AggregateRoot.java
tags: [tactical, marker]
---

Marker interface for Aggregate Roots.

## Extends

- [Entity<T, ID>](/marker/tactical/entity.md)

## Governed by

- [Aggregate Roots must implement AggregateRoot<T, ID>](/rule/tactical/aggregate-roots-must-implement-aggregateroot-t-id.md)
- [Aggregate Roots must not have fields with other Aggregate Root types](/rule/tactical/aggregate-roots-must-not-have-fields-with-other-aggregate-root-types.md)
- [Aggregate Roots must not hold references to Repositories or other Output Ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md)
- [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md)
- [Repository methods must not return non-root Entities](/rule/tactical/repository-methods-must-not-return-non-root-entities.md)

## Discussed in

- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
