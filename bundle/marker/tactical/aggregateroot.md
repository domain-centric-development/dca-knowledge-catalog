---
type: Marker
title: "AggregateRoot<T, ID>"
category: tactical
kind: interface
signature: "public interface AggregateRoot<T extends AggregateRoot<T, ID>, ID extends Id> extends Entity<T, ID>"
extends: [Entity]
methods: ["List<DomainEvent> domainEvents()", "void clearDomainEvents()"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/tactical/AggregateRoot.java
tags: [tactical, marker]
---

Marker interface for Aggregate Roots.

## Extends

- [Entity<T, ID>](/marker/tactical/entity.md)

## Governed by

- [Aggregate Roots must implement AggregateRoot<T, ID>](/rule/tactical/aggregate-roots-must-implement-aggregateroot-t-id.md)
- [Aggregate Roots must not have fields with other Aggregate Root types](/rule/tactical/aggregate-roots-must-not-have-fields-with-other-aggregate-root-types.md)
- [Aggregate Roots must not hold references to Repositories or other Output Ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md)
- [Entities must not be instantiated directly from outside the aggregate](/rule/tactical/entities-must-not-be-instantiated-directly-from-outside-the-aggregate.md)
- [Entities must not have fields with Aggregate Root types](/rule/tactical/entities-must-not-have-fields-with-aggregate-root-types.md)
- [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md)
- [Repository methods must return Aggregate Roots](/rule/tactical/repository-methods-must-return-aggregate-roots.md)
- [Value Objects must not contain Aggregate Roots or Entities](/rule/tactical/value-objects-must-not-contain-aggregate-roots-or-entities.md)

## Referenced by ADRs

- [ADR-002: Framework-Independent Domain Layer](/adr/adr-002-framework-independent-domain.md)
- [ADR-004: Persistence-Oriented Repository Pattern](/adr/adr-004-persistence-oriented-repository.md)
- [ADR-005: Domain Events Publishing Strategy](/adr/adr-005-domain-events-publishing.md)
- [ADR-008: Repository Interfaces as Output Ports in Application Layer](/adr/adr-008-repository-interfaces-as-output-ports.md)
- [ADR-011: Bounded Context Isolation via Package Structure](/adr/adr-011-bounded-context-isolation.md)
- [ADR-016: Shared Kernel Pattern for Cross-Context Value Objects](/adr/adr-016-shared-kernel-pattern.md)

## Discussed in

- [Tactical Building Blocks](/book/05-domain-layer/tactical-building-blocks.md)
- [Complete Examples](/book/11-shared-kernel/complete-examples.md)
- [Marker Interfaces](/book/11-shared-kernel/marker-interfaces.md)
- [Key Differences](/book/clean-architecture-comparison/key-differences.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
