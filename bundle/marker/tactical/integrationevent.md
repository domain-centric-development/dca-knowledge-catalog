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

## Referenced by ADRs

- [ADR-026: Transactional Outbox for Integration Events](/adr/adr-026-transactional-outbox-integration-events.md)
- [ADR-027: Integration-Event Contract Identity via @IntegrationEventType](/adr/adr-027-integration-event-contract-identity.md)

## Discussed in

- [Outgoing Adapters](/book/07-adapter-layer/outgoing-adapters.md)
- [Common Patterns](/book/14-events-integration/common-patterns.md)
- [Complete Event Flow](/book/14-events-integration/complete-event-flow.md)
- [Domain Events vs Integration Events](/book/14-events-integration/domain-events-vs-integration-events.md)
- [Event Consumption](/book/14-events-integration/event-consumption.md)
- [Integration Events](/book/14-events-integration/integration-events.md)
- [Service Decomposition](/book/deployment-patterns/service-decomposition.md)
- [Event-Driven Architecture in Spring Modulith](/book/spring-modulith/event-driven-architecture-in-spring-modulith.md)
- [RULES](/guide/readme/rules.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
