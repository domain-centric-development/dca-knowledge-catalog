---
type: Marker
title: IntegrationEventPublisher
category: port-out
kind: interface
signature: public interface IntegrationEventPublisher extends OutputPort
package: dev.domaincentric.dca.buildingblocks.hexagonal.port.out
extends: [OutputPort]
methods: ["void publish(IntegrationEvent event)"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/hexagonal/port/out/IntegrationEventPublisher.java
tags: [port-out, marker]
---

Outbound port for publishing integration events across bounded-context boundaries.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Governed by

- [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md)
