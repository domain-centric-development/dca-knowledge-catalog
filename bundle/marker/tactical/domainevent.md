---
type: Marker
title: DomainEvent
category: tactical
kind: interface
signature: public interface DomainEvent
methods: ["UUID eventId()", "Instant occurredOn()"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/tactical/DomainEvent.java
tags: [tactical, marker]
---

Interface for Domain Events.

## Governed by

- [Domain Events must have a timestamp field](/rule/advanced/domain-events-must-have-a-timestamp-field.md)
- [Domain Events must implement DomainEvent Marker Interface and be records](/rule/advanced/domain-events-must-implement-domainevent-marker-interface-and-be-records.md)
- [Domain Events must not have Spring annotations](/rule/advanced/domain-events-must-not-have-spring-annotations.md)
- [Domain Events must reside in domain package](/rule/advanced/domain-events-must-reside-in-domain-package.md)
- [Domain Events should be immutable (final or records)](/rule/advanced/domain-events-should-be-immutable-final-or-records.md)
- [Domain Events that are not Integration Events must not have a version field](/rule/advanced/domain-events-that-are-not-integration-events-must-not-have-a-version-field.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
