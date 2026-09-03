---
type: Marker
title: "@BoundedContext"
category: strategic
kind: annotation
signature: "public @interface BoundedContext"
package: dev.domaincentric.dca.buildingblocks.ddd.strategic
methods: ["String name()", "String description()"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/strategic/BoundedContext.java
tags: [strategic, marker]
---

Marks a package as a Bounded Context in Domain-Driven Design.

## Governed by

- [Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages](/rule/contextmap/upstream-externalupstream-and-partnership-may-only-be-declared-on-bounded-context-packages.md)
- [Diagnostic: Display discovered bounded contexts](/rule/strategic/diagnostic-display-discovered-bounded-contexts.md)
- [Shared Kernel must not have dependencies on any bounded context](/rule/strategic/shared-kernel-must-not-have-dependencies-on-any-bounded-context.md)

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
