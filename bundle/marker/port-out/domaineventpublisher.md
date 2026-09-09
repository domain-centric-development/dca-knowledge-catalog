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

This interface defines the contract for publishing domain events from the application layer to
the infrastructure layer, enabling loose coupling between aggregates and event handlers.

This is an outbound port (secondary/driven port in Hexagonal Architecture) used across all
bounded contexts, making it part of the Shared Kernel. The application layer depends on this
interface, while concrete implementations reside in the infrastructure layer, following the
Dependency Inversion Principle.

**Usage Pattern:**

```java
// In Application Service after saving aggregate:
Product product = productRepository.save(product);
domainEventPublisher.publishAndClearEvents(product);
```

**Benefits:**

- Application layer remains framework-independent
- Events are published only after successful persistence
- Enables asynchronous event handling
- Supports eventual consistency across aggregates
- Easy to swap implementations or mock for testing

**Sequence of operations — save, dispatch, then clear.** The use case calls `publishAndClearEvents` after `save`, inside the same transaction, so an event is never
dispatched for state that was not persisted. The implementation dispatches the collected events
first and clears the aggregate *afterwards*: clearing is the acknowledgement that every
listener has seen the event. A listener that throws therefore fails the use case and leaves the
events on the aggregate — nothing is silently lost. Clearing before dispatch would drop events on
the first failing listener.

Integration events derived from these domain events (by an outgoing event adapter listening
in-process) are recorded in a transactional outbox inside the same transaction and delivered
after commit, at least once; their consumers are idempotent.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Governed by

- [Output Ports in application.shared must extend OutputPort](/rule/hexagonal/output-ports-in-application-shared-must-extend-outputport.md)
- [The shared kernel's output-port markers must all be interfaces](/rule/layered/the-shared-kernel-s-output-port-markers-must-all-be-interfaces.md)
- [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md)
- [Use cases that publish domain events must have a transaction boundary](/rule/usecase/use-cases-that-publish-domain-events-must-have-a-transaction-boundary.md)
- [Use cases that save an aggregate must publish its domain events](/rule/usecase/use-cases-that-save-an-aggregate-must-publish-its-domain-events.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Interface vs Implementation Placement](/guide/architecture-reference-guide/interface-vs-implementation-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Ports and Adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
