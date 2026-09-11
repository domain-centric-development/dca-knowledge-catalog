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

## Related mentions in guides (heuristic)

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [Cross-Bounded Context Communication](/guide/dependency-structure/cross-bounded-context-communication.md)
- [Deployment Pattern Comparison](/guide/deployment-patterns/deployment-pattern-comparison.md)
- [Service Decomposition](/guide/deployment-patterns/service-decomposition.md)
- [A Bounded Context Is a Deep Module](/guide/integration-patterns/a-bounded-context-is-a-deep-module.md)
- [Different Bounded Contexts](/guide/integration-patterns/different-bounded-contexts.md)
- [Same Bounded Context](/guide/integration-patterns/same-bounded-context.md)
- [DOMAIN LAYER RULES](/guide/rules/domain-layer-rules.md)
- [STRATEGIC DESIGN RULES](/guide/rules/strategic-design-rules.md)
