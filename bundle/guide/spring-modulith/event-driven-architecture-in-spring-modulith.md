---
type: Section
title: Event-Driven Architecture in Spring Modulith
chapter: Spring Modulith Implementation
source: guide
resource: implementing-domain-centric-architecture/spring-modulith.md
tags: [guide, section]
---

### Domain Events vs Integration Events

Spring Modulith supports two types of events that align with [Domain-Driven Design principles](./README.md#domain-event-rules-internal-to-bounded-context):

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

### Event Architecture Comparison

| Aspect | Domain Event | Integration Event |
|--------|--------------|-------------------|
| **Scope** | Within module | Across modules |
| **Package** | `internal/domain/event/` | `events/` (published) |
| **Marker** | Optional `DomainEvent` | `implements Externalized` ⭐ |
| **Serialization** | Not required | Required |
| **Versioning** | Not required | Required |
| **Delivery** | Sync (in-tx) *or* async (registry-backed) | Async, externalized via registry |
| **Persistence** | Only when delivered async (registry) | Yes (Event Publication Registry) |
| **Retry** | Only when delivered async (registry) | Yes (automatic) |
| **Visibility** | Private to module | Public to all modules |

> **Delivery mode is orthogonal to event type.** Persistence and retry come from
> **asynchronous, registry-backed delivery** — not from an event being "integration".
> A domain event handled by a synchronous listener runs in the publishing transaction and
> needs neither. A domain event handled by an **async** `@ApplicationModuleListener` is
> persisted in the registry and redelivered at-least-once — the same durable, in-process
> transactional-outbox guarantee, still **without leaving the module**. The integration
> event differs only in that its async delivery is *externalized* to a broker.

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

### Event Publishing Pattern

**Publishing Domain Event (internal):**
```java
@Service
@RequiredArgsConstructor
public class CreateOrderUseCase {
    private final ApplicationEventPublisher events;
    private final OrderRepository orders;

    @Transactional
    public OrderId execute(CreateOrderCommand command) {
        // 1. Create aggregate
        Order order = Order.create(command);

        // 2. Save aggregate
        orders.save(order);

        // 3. Publish domain event (same transaction)
        events.publishEvent(new OrderCreated(
            order.getId(),
            order.getCustomerId(),
            order.getTotalAmount(),
            Instant.now()
        ));

        return order.getId();
    }
}
```

**Converting to Integration Event (cross-module):**
```java
// Listening to domain event and publishing integration event
@Component
@RequiredArgsConstructor
class OrderEventPublisher {
    private final ApplicationEventPublisher events;

    @EventListener
    void on(OrderCreated event) {
        // Map domain event → integration event
        events.publishEvent(new OrderCreatedEvent(
            UUID.randomUUID().toString(),
            event.orderId().toString(),
            event.customerId().toString(),
            event.totalAmount().getAmount(),
            event.occurredAt(),
            "v1"  // Version for compatibility
        ));
        // Integration event persisted by Event Publication Registry
    }
}
```

### Event Consumption Pattern

**Consuming Integration Event (from another module):**
```java
@Component
@RequiredArgsConstructor
class InventoryEventListener {
    private final ReserveStockUseCase reserveStock;

    @ApplicationModuleListener  // Spring Modulith async listener
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    void on(OrderCreatedEvent event) {
        // Anti-Corruption Layer: Convert integration event → command
        var command = new ReserveStockCommand(
            OrderId.of(event.orderId()),
            // Map to Inventory's domain language
        );

        // Execute use case in Inventory's bounded context
        reserveStock.execute(command);

        // Event marked complete in Event Publication Registry
    }
}
```

**Key Points:**
- `@ApplicationModuleListener` enables async processing in new transaction
- `Propagation.REQUIRES_NEW` ensures independent transaction
- Failures trigger automatic retry (configured via Spring Modulith)
- Anti-Corruption Layer protects consuming module's domain

### Idempotent Consumers

At-least-once delivery means every listener must expect duplicates and out-of-order arrival:

```java
@ApplicationModuleListener
void on(OrderCreatedEvent event) {
    if (processedEvents.contains(event.eventId())) {
        return; // Duplicate delivery — already handled
    }
    reserveStock.execute(toCommand(event));
    processedEvents.markProcessed(event.eventId());
}
```

**Rules:**
- **Deduplicate** — track processed event IDs in the consumer's own store, or make the operation naturally idempotent (e.g., `reserveStock(orderId)` upserts the reservation instead of inserting a new one)
- **Tolerate out-of-order arrival** — never assume the previous event was already seen
- **Never drop silently** — permanently failing events go to a dead-letter mechanism (e.g., alert plus manual resubmission of incomplete publications after retries are exhausted)

### Anti-Corruption Layer (ACL) Pattern

When consuming integration events from other modules, use an **Anti-Corruption Layer** to protect your domain model from external event formats. The ACL translates external events into your module's domain language.

**Purpose:**
- **Isolation** - Protect domain from changes in other modules
- **Translation** - Convert external language to internal language
- **Validation** - Ensure external data meets internal invariants
- **Decoupling** - Module's domain remains independent

**Pattern Structure:**
```
Consuming Module (Inventory):
│
├── events/ (listening to external events)
│   └── OrderEventConsumer.java        ← Event listener (adapter)
│
├── acl/ (anti-corruption layer)
│   └── OrderEventToInventoryMapper.java  ← ACL Translator
│
└── application/
    └── reservestock/
        ├── ReserveStockInputPort.java
        ├── ReserveStockUseCase.java
        └── ReserveStockCommand.java     ← Internal command (domain language)
```

**Complete ACL Example:**

```java
// ========== PRODUCING MODULE (Order) ==========

// Order module publishes integration event
package com.company.ecommerce.order.events;

public record OrderCreatedEvent(
    String eventId,
    String orderId,
    String customerId,
    List<OrderItemDto> items,  // External DTO format
    BigDecimal totalAmount,
    String currency,
    Instant timestamp,
    String version
) implements org.springframework.modulith.events.Externalized {
    // Integration event - Order's language
}

public record OrderItemDto(
    String productId,
    int quantity,
    BigDecimal price
) {}

// ========== CONSUMING MODULE (Inventory) ==========

// 1. EVENT LISTENER (Adapter) - Receives external event
package com.company.ecommerce.inventory.adapter.incoming.event;

@Component
@RequiredArgsConstructor
public class OrderEventConsumer {

    private final OrderEventToInventoryMapper acl;  // ACL translator
    private final ReserveStockInputPort reserveStock;  // Use case

    @ApplicationModuleListener
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void on(OrderCreatedEvent event) {  // External event (Order's language)

        // Use ACL to translate external event → internal command
        ReserveStockCommand command = acl.toReserveStockCommand(event);

        // Execute use case with internal command (Inventory's language)
        reserveStock.execute(command);

        // Event marked complete in Event Publication Registry
    }
}

// 2. ANTI-CORRUPTION LAYER (ACL) - Translator
package com.company.ecommerce.inventory.acl;

@Component
public class OrderEventToInventoryMapper {

    /**
     * Translates OrderCreatedEvent (Order's language)
     * → ReserveStockCommand (Inventory's language)
     *
     * This is the Anti-Corruption Layer - it protects Inventory's domain
     * from Order's event structure and terminology.
     */
    public ReserveStockCommand toReserveStockCommand(OrderCreatedEvent event) {

        // Validation - protect domain invariants
        if (event.items() == null || event.items().isEmpty()) {
            throw new IllegalArgumentException("Order must have items");
        }

        // Translation - Order's OrderItemDto → Inventory's StockReservationItem
        List<StockReservationItem> reservationItems = event.items().stream()
            .map(this::toStockReservationItem)
            .toList();

        // Create command in Inventory's language
        return new ReserveStockCommand(
            OrderReference.of(event.orderId()),  // Inventory's value object
            reservationItems,                     // Inventory's domain objects
            ReservationReason.ORDER_PLACEMENT    // Inventory's enum
        );
    }

    private StockReservationItem toStockReservationItem(OrderItemDto orderItem) {
        return new StockReservationItem(
            ProductSku.of(orderItem.productId()),  // Inventory's SKU value object
            Quantity.of(orderItem.quantity())      // Inventory's Quantity value object
        );
        // Note: Inventory doesn't care about price - that's Order's concern
    }
}

// 3. INTERNAL COMMAND (Application Layer) - Inventory's language
package com.company.ecommerce.inventory.application.reservestock;

public record ReserveStockCommand(
    OrderReference orderReference,      // Inventory's value object
    List<StockReservationItem> items,   // Inventory's domain concept
    ReservationReason reason             // Inventory's enum
) {}

// Inventory's value objects - its own domain language
public record OrderReference(String value) {
    public static OrderReference of(String value) {
        return new OrderReference(value);
    }
}

public record ProductSku(String value) {
    public static ProductSku of(String value) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("SKU cannot be empty");
        }
        return new ProductSku(value);
    }
}

public record Quantity(int value) {
    public static Quantity of(int value) {
        if (value <= 0) {
            throw new IllegalArgumentException("Quantity must be positive");
        }
        return new Quantity(value);
    }
}

public enum ReservationReason {
    ORDER_PLACEMENT,
    MANUAL_RESERVATION,
    RESTOCK_RETURN
}

// 4. USE CASE (Application Layer) - Uses Inventory's domain
package com.company.ecommerce.inventory.application.reservestock;

@Service
@RequiredArgsConstructor
public class ReserveStockUseCase implements ReserveStockInputPort {

    private final StockRepository stockRepository;  // Inventory's repository

    @Override
    public ReserveStockResult execute(ReserveStockCommand command) {
        // Work with Inventory's domain language and rules
        // No knowledge of Order module's structure

        for (StockReservationItem item : command.items()) {
            Stock stock = stockRepository.findBySku(item.sku())
                .orElseThrow(() -> new StockNotFoundException(item.sku()));

            stock.reserve(item.quantity(), command.orderReference());

            stockRepository.save(stock);
        }

        return new ReserveStockResult(true);
    }
}
```

**Key Benefits of ACL:**

1. **Language Independence**
   - Order uses `OrderItemDto` with `productId`
   - Inventory uses `StockReservationItem` with `ProductSku`
   - ACL translates between the two

2. **Structural Independence**
   - Order's event structure can change
   - ACL absorbs the change
   - Inventory's domain remains stable

3. **Validation at Boundary**
   - ACL validates external data before it enters domain
   - Protects domain invariants
   - Fails fast on invalid external data

4. **Decoupled Evolution**
   - Order and Inventory teams work independently
   - Each module uses its own ubiquitous language
   - No shared domain objects across contexts

**ACL Placement Rules:**

✅ **Correct:**
- ACL in consuming module: `inventory/acl/OrderEventToInventoryMapper.java`
- Translates external event → internal command
- Located in adapter layer or dedicated `acl/` package

❌ **Incorrect:**
- No ACL - Use case directly consumes external event
- Shared domain objects between modules
- External event structure leaking into domain

### Event Mapper Pattern (Domain Event → Integration Event)

The **Event Mapper** is the outbound equivalent of ACL - it translates internal domain events into external integration events.

**Structure:**
```
Producing Module (Order):
│
├── domain/event/
│   └── OrderCreated.java             ← Internal domain event
│
├── adapter/outgoing/messaging/
│   └── OrderEventMapper.java         ← Event Mapper
│
└── events/ (published)
    └── OrderCreatedEvent.java        ← External integration event
```

**Example:**

```java
// Internal Domain Event (Order's domain language)
package com.company.ecommerce.order.domain.event;

public record OrderCreated(
    OrderId orderId,                   // Domain value object
    CustomerId customerId,             // Domain value object
    List<OrderLine> orderLines,        // Domain entities
    Money totalAmount,                 // Domain value object
    Instant occurredAt
) implements DomainEvent {}

// Event Mapper (Adapter)
package com.company.ecommerce.order.adapter.outgoing.messaging;

@Component
@RequiredArgsConstructor
public class OrderEventMapper {

    private final ApplicationEventPublisher events;

    @EventListener  // Listen to internal domain event
    public void on(OrderCreated domainEvent) {

        // Map domain event → integration event (DTO)
        OrderCreatedEvent integrationEvent = toIntegrationEvent(domainEvent);

        // Publish integration event (persisted by Event Publication Registry)
        events.publishEvent(integrationEvent);
    }

    private OrderCreatedEvent toIntegrationEvent(OrderCreated domainEvent) {
        return new OrderCreatedEvent(
            UUID.randomUUID().toString(),         // Event ID for idempotency
            domainEvent.orderId().getValue(),     // Extract primitive from value object
            domainEvent.customerId().getValue(),  // Extract primitive from value object
            toOrderItemDtos(domainEvent.orderLines()),  // Map to DTOs
            domainEvent.totalAmount().getAmount(),
            domainEvent.totalAmount().getCurrency().getCurrencyCode(),
            domainEvent.occurredAt(),
            "v1"  // Version for compatibility
        );
    }

    private List<OrderItemDto> toOrderItemDtos(List<OrderLine> orderLines) {
        return orderLines.stream()
            .map(line -> new OrderItemDto(
                line.getProductId().getValue(),
                line.getQuantity(),
                line.getPrice().getAmount()
            ))
            .toList();
    }
}

// External Integration Event (Published DTO)
package com.company.ecommerce.order.events;

public record OrderCreatedEvent(
    String eventId,
    String orderId,
    String customerId,
    List<OrderItemDto> items,
    BigDecimal totalAmount,
    String currency,
    Instant timestamp,
    String version
) implements org.springframework.modulith.events.Externalized {}
```

**Key Principles:**

1. **Domain events stay internal** - Never cross module boundaries
2. **Integration events are DTOs** - Serializable, versioned, primitive types
3. **Event Mapper translates** - Domain language → External DTO
4. **Two-step publishing** - Domain event → Event Mapper → Integration event

### Best Practices

**When to Use Domain Events:**
- Communication within the same module
- Eventual consistency between aggregates in same bounded context
- Triggering side effects in same transaction

**When to Use Integration Events:**
- Communication between different modules (bounded contexts)
- Cross-team integration points
- Events that may be externalized to message broker later
- When guaranteed delivery and retry are needed

**Naming Conventions:**
- Domain Events: Past tense, no suffix (e.g., `OrderCreated`, `PaymentProcessed`)
- Integration Events: Past tense + "Event" suffix (e.g., `OrderCreatedEvent`, `PaymentProcessedEvent`)

## Related markers

- [DomainEvent](/marker/tactical/domainevent.md)
