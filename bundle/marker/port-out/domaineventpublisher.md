---
type: Marker
title: DomainEventPublisher
category: port-out
kind: interface
signature: public interface DomainEventPublisher extends OutputPort
package: dev.domaincentric.dca.buildingblocks.hexagonal.port.out
extends: [OutputPort]
methods: ["void publish(DomainEvent event)", "void publishAndClearEvents(AggregateRoot<?, ?> aggregate)"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/hexagonal/port/out/DomainEventPublisher.java
tags: [port-out, marker]
---

Outbound port for publishing domain events.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Governed by

- [The shared kernel's output-port markers must all be interfaces](/rule/layered/the-shared-kernel-s-output-port-markers-must-all-be-interfaces.md)
- [Transactional use cases must not call remote-capable output ports](/rule/usecase/transactional-use-cases-must-not-call-remote-capable-output-ports.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Interface vs Implementation Placement](/guide/architecture-reference-guide/interface-vs-implementation-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Ports and Adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
