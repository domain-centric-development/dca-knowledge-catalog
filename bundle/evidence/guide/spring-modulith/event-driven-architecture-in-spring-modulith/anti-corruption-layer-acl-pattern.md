---
type: Reference
title: "Event-Driven Architecture in Spring Modulith — Anti-Corruption Layer (ACL) Pattern"
tags: [reference]
evidence_for: "/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#anti-corruption-layer-acl-pattern"
---

[Full node and context](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#anti-corruption-layer-acl-pattern). This is an evidence excerpt; retain the parent selection and caveats.

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
