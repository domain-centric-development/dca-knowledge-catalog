---
type: Reference
title: Event-Driven Architecture in Spring Modulith — Spring Modulith Event Publication Registry
tags: [reference]
evidence_for: "/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#spring-modulith-event-publication-registry"
---

[Full node and context](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#spring-modulith-event-publication-registry). This is an evidence excerpt; retain the parent selection and caveats.

### Spring Modulith Event Publication Registry

Spring Modulith provides an **Event Publication Registry** that ensures reliable event delivery:

**Features:**
- **Persistent Events**: Events marked with `@Externalized` are persisted to database
- **Guaranteed Delivery**: Events are marked complete only after successful processing
- **Automatic Retry**: Failed event handlers are retried automatically
- **Idempotency Support**: Handlers can be idempotent via event IDs
- **Observability**: Track event processing status and failures

**Configuration:**
```java
@Configuration
@EnableApplicationModuleListener  // Enables async event processing
public class EventConfiguration {
    // Spring Modulith auto-configures Event Publication Registry
    // when spring-modulith-events-jdbc or spring-modulith-events-jpa is on classpath
}
```

**Built-in Transactional Outbox:** The registry is Spring Modulith's equivalent of the Transactional Outbox pattern. The event publication is persisted in the same transaction as the aggregate state change, so neither can exist without the other. Completion is tracked after the listener executes successfully, and incomplete publications can be resubmitted — giving at-least-once delivery. Externalized events (Kafka, RabbitMQ, etc.) get the same guarantee; a dedicated outbox table plus relay process is only needed outside Spring Modulith.
