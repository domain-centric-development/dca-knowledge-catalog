---
type: Marker
title: "@BoundedContext"
category: strategic
kind: annotation
signature: "public @interface BoundedContext"
package: dev.domaincentric.dca.buildingblocks.ddd.strategic
methods: ["String name()", "String description() default \"\""]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/strategic/BoundedContext.java
tags: [strategic, marker]
---

Marks a package as a Bounded Context in Domain-Driven Design.

A Bounded Context is an explicit boundary within which a domain model exists. Each Bounded
Context has its own Ubiquitous Language and should be isolated from other contexts.

**Usage:** Place this annotation on a `package-info.java` file at the root of a
bounded context package.

```java
@BoundedContext(name = "Product Catalog", description = "Product management and catalog")
package com.acme.shop.product;

import dev.domaincentric.dca.buildingblocks.ddd.strategic.BoundedContext;
```

**Architectural Rules:**

- Bounded contexts must not directly depend on each other (except via Shared Kernel or
events)
- Each bounded context has its own domain, application, and adapter layers
- Cross-context communication should use domain events or Anti-Corruption Layers

## Governed by

- [Anti-Corruption Layer: upstream contract types must stay inside the matching adapter](/rule/contextmap/anti-corruption-layer-upstream-contract-types-must-stay-inside-the-matching-adapter.md)
- [Conformist: upstream contract types must never reach the domain layer](/rule/contextmap/conformist-upstream-contract-types-must-never-reach-the-domain-layer.md)
- [Cross-context dependencies on published interfaces require an Upstream declaration](/rule/contextmap/cross-context-dependencies-on-published-interfaces-require-an-upstream-declaration.md)
- [Diagnostic: Display declared context map](/rule/contextmap/diagnostic-display-declared-context-map.md)
- [Distinct external system names must not collide after mermaid id normalization](/rule/contextmap/distinct-external-system-names-must-not-collide-after-mermaid-id-normalization.md)
- [External system contract types must respect the declared translation and interaction](/rule/contextmap/external-system-contract-types-must-respect-the-declared-translation-and-interaction.md)
- [ExternalUpstream declarations must be well-formed and unique per name and interaction](/rule/contextmap/externalupstream-declarations-must-be-well-formed-and-unique-per-name-and-interaction.md)
- [Implemented Upstream declarations must be backed by an actual code dependency](/rule/contextmap/implemented-upstream-declarations-must-be-backed-by-an-actual-code-dependency.md)
- [Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric](/rule/contextmap/partnership-declarations-must-reference-an-existing-bounded-context-never-themselves-and-must-be-symmetric.md)
- [Upstream declarations and Spring Modulith allowedDependencies must agree](/rule/contextmap/upstream-declarations-and-spring-modulith-alloweddependencies-must-agree.md)
- [Upstream declarations must be unique per context and channel, and via must not be empty](/rule/contextmap/upstream-declarations-must-be-unique-per-context-and-channel-and-via-must-not-be-empty.md)
- [Upstream declarations must reference an existing bounded context and never the declaring context itself](/rule/contextmap/upstream-declarations-must-reference-an-existing-bounded-context-and-never-the-declaring-context-itself.md)
- [Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages](/rule/contextmap/upstream-externalupstream-and-partnership-may-only-be-declared-on-bounded-context-packages.md)
- [Diagnostic: Display discovered bounded contexts](/rule/strategic/diagnostic-display-discovered-bounded-contexts.md)
- [Shared Kernel must not have dependencies on any bounded context](/rule/strategic/shared-kernel-must-not-have-dependencies-on-any-bounded-context.md)
- [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Deployment Pattern Comparison](/guide/deployment-patterns/deployment-pattern-comparison.md)
- [Service Decomposition](/guide/deployment-patterns/service-decomposition.md)
- [ELEMENTS](/guide/readme/elements.md)
- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
- [Table of Contents](/guide/readme/table-of-contents.md)
