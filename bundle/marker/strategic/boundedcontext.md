---
type: Marker
title: "@BoundedContext"
category: strategic
kind: annotation
signature: "public @interface BoundedContext"
methods: ["String name()", "String description()"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/strategic/BoundedContext.java
tags: [strategic, marker]
---

Marks a package as a Bounded Context in Domain-Driven Design.

## Governed by

- [Incoming adapters must only access their own bounded context (except event consumers and Open Host Services)](/rule/hexagonal/incoming-adapters-must-only-access-their-own-bounded-context-except-event-consumers-and-open-host-services.md)
- [Outgoing adapters may access Open Host Services from other contexts](/rule/hexagonal/outgoing-adapters-may-access-open-host-services-from-other-contexts.md)
- [Bounded contexts must not directly access each other in application layer (except allowed dependencies)](/rule/strategic/bounded-contexts-must-not-directly-access-each-other-in-application-layer-except-allowed-dependencies.md)
- [Diagnostic: Display discovered bounded contexts](/rule/strategic/diagnostic-display-discovered-bounded-contexts.md)
- [Outgoing adapters accessing other contexts must only use OpenHostService classes (except allowed ACL patterns)](/rule/strategic/outgoing-adapters-accessing-other-contexts-must-only-use-openhostservice-classes-except-allowed-acl-patterns.md)
- [Shared Kernel must not have dependencies on any bounded context](/rule/strategic/shared-kernel-must-not-have-dependencies-on-any-bounded-context.md)
- [HTTP Response Models must end with 'Response' and reside in adapter incoming package](/rule/usecase/http-response-models-must-end-with-response-and-reside-in-adapter-incoming-package.md)

## Referenced by ADRs

- [ADR-016: Shared Kernel Pattern for Cross-Context Value Objects](/adr/adr-016-shared-kernel-pattern.md)

## Discussed in

- [Principle 4: Bounded Contexts](/book/02-core-principles/principle-4-bounded-contexts.md)
- [Bounded Context Structure](/book/09-package-structure/bounded-context-structure.md)
- [Why Bounded Contexts Matter](/book/10-bounded-contexts/why-bounded-contexts-matter.md)
- [Strategic DDD Patterns](/book/appendix-a-glossary/strategic-ddd-patterns.md)
- [Service Decomposition](/book/deployment-patterns/service-decomposition.md)
- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Service Decomposition](/guide/deployment-patterns/service-decomposition.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
