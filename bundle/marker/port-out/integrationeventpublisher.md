---
type: Marker
title: IntegrationEventPublisher
category: port-out
kind: interface
signature: public interface IntegrationEventPublisher extends OutputPort
extends: [OutputPort]
methods: ["void publish(IntegrationEvent event)"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/port/out/IntegrationEventPublisher.java
tags: [port-out, marker]
---

Outbound port for publishing integration events across bounded-context boundaries.

## Extends

- [OutputPort](/marker/port-out/outputport.md)
