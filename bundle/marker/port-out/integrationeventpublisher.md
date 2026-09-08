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

Use cases publish boundary-crossing facts through this port; the implementation (e.g. a
transactional-outbox adapter) decides how the event becomes durable and reaches external
consumers. This keeps the application layer free of delivery concerns.

Distinct from `r`: that port publishes in-context `DomainEvent`s after persistence; this one publishes the versioned, serializable `t` contract to other contexts or systems.

Note the two-level port distinction of the outbox subsystem: this interface is an
**application output port** (used by use cases) and therefore carries the `t`
marker. The outbox *store* behind it is an internal port of the outbox adapter subsystem —
no use case depends on it, so it deliberately carries no marker.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Governed by

- [Output Ports in application.shared must extend OutputPort](/rule/hexagonal/output-ports-in-application-shared-must-extend-outputport.md)
- [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md)
