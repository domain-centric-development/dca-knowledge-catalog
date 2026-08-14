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

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Interface vs Implementation Placement](/guide/architecture-reference-guide/interface-vs-implementation-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Ports and Adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
