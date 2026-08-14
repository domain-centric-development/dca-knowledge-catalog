---
type: Marker
title: IntegrationEvent
category: tactical
kind: interface
signature: public interface IntegrationEvent
methods: ["UUID eventId()", "Instant occurredOn()"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/tactical/IntegrationEvent.java
tags: [tactical, marker]
---

Marker interface for Integration Events — adapter-layer DTOs published across bounded contexts.

## Governed by

- [Domain Events that are not Integration Events must not have a version field](/rule/advanced/domain-events-that-are-not-integration-events-must-not-have-a-version-field.md)
- [Integration Events must be annotated with IntegrationEventType](/rule/advanced/integration-events-must-be-annotated-with-integrationeventtype.md)
- [Integration Events must not have a version field](/rule/advanced/integration-events-must-not-have-a-version-field.md)
- [Integration Events must be in events or adapter outgoing event packages](/rule/strategic/integration-events-must-be-in-events-or-adapter-outgoing-event-packages.md)
- [Integration Events should be immutable records](/rule/strategic/integration-events-should-be-immutable-records.md)

## Discussed in

- [Service Decomposition](/guide/deployment-patterns/service-decomposition.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
