---
type: Reference
title: Event-Driven Architecture in Spring Modulith — Domain Events vs Integration Events
tags: [reference]
evidence_for: "/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#domain-events-vs-integration-events"
---

[Full node and context](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#domain-events-vs-integration-events). This is an evidence excerpt; retain the parent selection and caveats.

### Domain Events vs Integration Events

Spring Modulith supports two types of events that align with [Domain-Driven Design principles](/guide/readme/rules.md):

#### Domain Events (Internal to Module)

**Purpose:** Communication within bounded context (module)

**Location:** `{module}/internal/domain/event/` OR `{module}/events/` if kept internal

**Characteristics:**
- Scope: Same module, can cross aggregates within module
- Marker: Optional `DomainEvent` interface
- Publishing: Via `ApplicationEventPublisher` within use case
- Consumption: Via `@EventListener` within same module
- Persistence: Optional
- Retry: Not automatic
- Transaction: Same transaction as use case

**Example:**
```java
// order/internal/domain/event/OrderCreated.java
public record OrderCreated(
    UUID orderId,
    CustomerId customerId,
    Money totalAmount,
    Instant occurredAt
) implements DomainEvent {
    // Internal domain event - stays within Order module
}
```

#### Integration Events (Cross-Module)

**Purpose:** Communication between modules (bounded contexts)

**Location:** `{module}/events/` (published package)

**Characteristics:**
- **Marker:** `implements Externalized` (Spring Modulith interface) - **KEY DIFFERENCE**
- Scope: Across modules, published to external consumers
- Publishing: Via `ApplicationEventPublisher` + Event Publication Registry
- Consumption: Via `@ApplicationModuleListener` in other modules
- Persistence: Yes (Event Publication Registry ensures delivery)
- Retry: Automatic retry on failure
- Serialization: Must be serializable
- Versioning: Required for cross-module contracts

**Example:**
```java
// order/events/OrderCreatedEvent.java
public record OrderCreatedEvent(
    String eventId,
    String orderId,
    String customerId,
    BigDecimal totalAmount,
    Instant timestamp,
    String version
) implements org.springframework.modulith.events.Externalized {
    // Integration event - crosses module boundaries
    // Implements Externalized = Spring Modulith persists it
}
```
