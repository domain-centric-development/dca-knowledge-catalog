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
