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

## Referenced by ADRs

- [ADR-002: Framework-Independent Domain Layer](/adr/adr-002-framework-independent-domain.md)
- [ADR-005: Domain Events Publishing Strategy](/adr/adr-005-domain-events-publishing.md)
- [ADR-006: Domain Events as Immutable Records](/adr/adr-006-domain-events-immutable-records.md)
- [ADR-016: Shared Kernel Pattern for Cross-Context Value Objects](/adr/adr-016-shared-kernel-pattern.md)
- [ADR-024: Interface Inversion Pattern for Spring Modulith Event Listeners](/adr/adr-024-interface-inversion-spring-modulith.md)
- [ADR-026: Transactional Outbox for Integration Events](/adr/adr-026-transactional-outbox-integration-events.md)

## Discussed in

- [Tactical Building Blocks](/book/05-domain-layer/tactical-building-blocks.md)
- [Marker Interfaces](/book/11-shared-kernel/marker-interfaces.md)
- [Domain Events vs Integration Events](/book/14-events-integration/domain-events-vs-integration-events.md)
- [Domain Events](/book/14-events-integration/domain-events.md)
- [Event Publishing](/book/14-events-integration/event-publishing.md)
- [Integration Events](/book/14-events-integration/integration-events.md)
- [Event-Driven Architecture in Spring Modulith](/book/spring-modulith/event-driven-architecture-in-spring-modulith.md)
- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [RULES](/guide/readme/rules.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
