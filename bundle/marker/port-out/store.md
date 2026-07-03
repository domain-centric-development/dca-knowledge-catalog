---
type: Marker
title: Store
category: port-out
kind: interface
signature: public interface Store extends OutputPort
extends: [OutputPort]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/port/out/Store.java
tags: [port-out, marker]
---

Marker interface for Stores — output ports that record or query operational data without an own aggregate lifecycle.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Discussed in

- [Step 5: Adapter Layer - Repository](/book/03-getting-started/step-5-adapter-layer-repository.md)
- [Step 8: Testing](/book/03-getting-started/step-8-testing.md)
- [Stores: persistence for non-aggregate data](/book/06-application-layer/stores-persistence-for-non-aggregate-data.md)
- [Outgoing Adapters](/book/07-adapter-layer/outgoing-adapters.md)
- [Common Patterns](/book/14-events-integration/common-patterns.md)
- [In-Memory Repository](/book/15-persistence-patterns/in-memory-repository.md)
- [Core Concepts](/book/17-event-sourcing/core-concepts.md)
- [Event Store Design](/book/17-event-sourcing/event-store-design.md)
- [Overview](/book/17-event-sourcing/overview.md)
- [ELEMENTS](/guide/readme/elements.md)
