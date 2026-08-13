---
type: Marker
title: DomainEventPublisher
category: port-out
kind: interface
signature: public interface DomainEventPublisher extends OutputPort
extends: [OutputPort]
methods: ["void publish(DomainEvent event)", "void publishAndClearEvents(AggregateRoot<?, ?> aggregate)"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/port/out/DomainEventPublisher.java
tags: [port-out, marker]
---

Outbound port for publishing domain events.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Governed by

- [sharedkernel.application.port should only contain interfaces (Outbound Ports)](/rule/layered/sharedkernel-application-port-should-only-contain-interfaces-outbound-ports.md)
- [Use cases that save an aggregate must publish its domain events](/rule/usecase/use-cases-that-save-an-aggregate-must-publish-its-domain-events.md)

## Referenced by ADRs

- [ADR-004: Persistence-Oriented Repository Pattern](/adr/adr-004-persistence-oriented-repository.md)
- [ADR-005: Domain Events Publishing Strategy](/adr/adr-005-domain-events-publishing.md)
- [ADR-007: Hexagonal Architecture with Explicit Port/Adapter Separation](/adr/adr-007-hexagonal-architecture.md)
- [ADR-008: Repository Interfaces as Output Ports in Application Layer](/adr/adr-008-repository-interfaces-as-output-ports.md)
- [ADR-012: Use Case Input/Output Models (Command/Query Pattern)](/adr/adr-012-use-case-input-output-models.md)

## Discussed in

- [Configuration Classes](/book/08-infrastructure-layer/configuration-classes.md)
- [Domain Events](/book/14-events-integration/domain-events.md)
- [Event Publishing](/book/14-events-integration/event-publishing.md)
- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Interface vs Implementation Placement](/guide/architecture-reference-guide/interface-vs-implementation-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Ports and Adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
