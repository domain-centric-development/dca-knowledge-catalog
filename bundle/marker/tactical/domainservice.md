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
- Named after activities or actions (e.g., PricingService, CartTotalCalculator)
- Express domain concepts in the Ubiquitous Language
- Should NOT have Spring annotations (@Service, @Component)
- Instantiated by Application Services

**Examples:**

- Calculating cart totals with complex tax rules (involves multiple items)
- Applying pricing rules and discounts (domain logic not belonging to a single entity)
- Validating business constraints that span multiple aggregates

**Reference:** Eric Evans' Domain-Driven Design (2003), Chapter 5: "A Model Expressed in
Software"

## Governed by

- [Domain Services must implement DomainService Marker Interface and reside in domain.service](/rule/advanced/domain-services-must-implement-domainservice-marker-interface-and-reside-in-domain-service.md)
- [Domain Services must not have Spring annotations](/rule/advanced/domain-services-must-not-have-spring-annotations.md)
- [Domain Services must reside in domain package](/rule/advanced/domain-services-must-reside-in-domain-package.md)
- [Domain Services should be stateless (only final fields for dependencies)](/rule/advanced/domain-services-should-be-stateless-only-final-fields-for-dependencies.md)
- [Incoming Adapters must not depend on domain services](/rule/hexagonal/incoming-adapters-must-not-depend-on-domain-services.md)

## Discussed in

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Approach 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md)
- [Approach 2: Strategy/Callback Pattern](/guide/domain-services-with-data-dependencies/approach-2-strategy-callback-pattern.md)
- [Comparison: When to Use Which Approach](/guide/domain-services-with-data-dependencies/comparison-when-to-use-which-approach.md)
- [Default Rule: Pure Domain Services (90% of Cases)](/guide/domain-services-with-data-dependencies/default-rule-pure-domain-services-90-of-cases.md)
- [Problem Statement](/guide/domain-services-with-data-dependencies/problem-statement.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
