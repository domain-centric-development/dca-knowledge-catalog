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

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [Deployment Pattern Comparison](/guide/deployment-patterns/deployment-pattern-comparison.md)
- [Service Decomposition](/guide/deployment-patterns/service-decomposition.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
- [Table of Contents](/guide/readme/table-of-contents.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
