---
type: Marker
title: DomainService
category: tactical
kind: interface
signature: public interface DomainService
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/DomainService.java
tags: [tactical, marker]
---

Marker interface for Domain Services.

Domain Services are stateless operations that don't naturally belong to an Entity or Value
Object. They encapsulate domain logic that involves multiple domain objects or doesn't fit within
a single Aggregate.

**Characteristics:**

- Stateless (only final fields for dependencies)
- Named after activities or actions (e.g., TariffCalculator, RouteOptimizer)
- Express domain concepts in the Ubiquitous Language
- Carries no container stereotype - the domain does not know the container
- Instantiated by Application Services

**Examples:**

- Calculating a total across several items under complex tax rules
- Applying tariff and discount rules (domain logic not belonging to a single entity)
- Validating business constraints that span multiple aggregates

**Reference:** Eric Evans' Domain-Driven Design (2003), Chapter 5: "A Model Expressed in
Software"

## Governed by

- [Marked domain services reside in a module domain](/rule/advanced/dca-adv-010.md)

## Related mentions in guides (heuristic)

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Approach 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md)
- [Approach 2: Strategy/Callback Pattern](/guide/domain-services-with-data-dependencies/approach-2-strategy-callback-pattern.md)
- [Comparison: When to Use Which Approach](/guide/domain-services-with-data-dependencies/comparison-when-to-use-which-approach.md)
- [Default Rule: Pure Domain Services (90% of Cases)](/guide/domain-services-with-data-dependencies/default-rule-pure-domain-services-90-of-cases.md)
- [Problem Statement](/guide/domain-services-with-data-dependencies/problem-statement.md)
- [Application Layer (Use Cases / Application Business Rules)](/guide/elements/application-layer-use-cases-application-business-rules.md)
- [Domain services over supplied facts](/guide/integration-patterns/domain-services-over-supplied-facts.md)
- [DOMAIN LAYER RULES](/guide/rules/domain-layer-rules.md)
