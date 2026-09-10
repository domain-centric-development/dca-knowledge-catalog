---
type: Marker
title: "@SharedKernel"
category: strategic
kind: annotation
signature: "public @interface SharedKernel"
package: dev.domaincentric.dca.buildingblocks.ddd.strategic.relationships
methods: ["String description() default \"\""]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/strategic/relationships/SharedKernel.java
tags: [strategic, marker]
---

Marks a package as the Shared Kernel in Domain-Driven Design.

A Shared Kernel is a small, carefully curated subset of the domain model that is shared
between bounded contexts. Changes to the Shared Kernel require coordination between all teams
that use it.

**Usage:** Place this annotation on a `package-info.java` file at the root of the
shared kernel package.

```java
@SharedKernel(description = "Common value objects and DDD markers")
package com.acme.shop.sharedkernel;

import dev.domaincentric.dca.buildingblocks.ddd.strategic.relationships.SharedKernel;
```

**What belongs in the Shared Kernel:**

- Universal value objects (Money, Currency)
- Cross-context identifiers (ProductId, UserId)
- DDD marker interfaces (Entity, AggregateRoot, Value)
- Common domain primitives

**What does NOT belong in the Shared Kernel:**

- Aggregates (each belongs to one context)
- Context-specific business logic
- Infrastructure concerns

## Related mentions in guides (heuristic)

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Complete Test Suites](/guide/archunit-governance/complete-test-suites.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Approach 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md)
- [Approach 2: Strategy/Callback Pattern](/guide/domain-services-with-data-dependencies/approach-2-strategy-callback-pattern.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
- [Shared Kernel in Spring Modulith](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)
