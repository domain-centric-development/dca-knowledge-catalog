---
type: Section
title: Ports and Adapters
chapter: Architecture Reference Guide
source: guide
resource: implementing-domain-centric-architecture/architecture-reference-guide.md
tags: [guide, section]
---

### Port Types

#### Inbound Ports (Primary/Driving)
- **What**: Interfaces that define what the application can do
- **Location**: `application/ports/in/` or `application/usecases/`
- **Implemented by**: Application services (in application layer)
- **Used by**: Inbound adapters (REST controllers, CLI, etc.)
- **Also called**: Use cases, Input ports, Driving ports

**Example**:
```java
// application/ports/in/CreateOrderUseCase.java
public interface CreateOrderUseCase {
    OrderId execute(CreateOrderCommand command);
}

// application/services/CreateOrderService.java
public class CreateOrderService implements CreateOrderUseCase {
    @Override
    public OrderId execute(CreateOrderCommand command) {
        // Implementation
    }
}

// adapters/in/web/OrderRestController.java
@RestController
public class OrderRestController {
    private final CreateOrderUseCase createOrder;  // USES the port

    @PostMapping("/orders")
    public ResponseEntity<?> create(@RequestBody CreateOrderRequest req) {
        OrderId id = createOrder.execute(toCommand(req));  // CALLS
        return ResponseEntity.ok(id);
    }
}
```

#### Outbound Ports (Secondary/Driven)
- **What**: Interfaces that define what the application needs
- **Location**: `application/ports/out/` or `application/spi/`
- **Implemented by**: Outbound adapters (in adapters layer)
- **Used by**: Application services
- **Also called**: SPI (Service Provider Interface), Output ports, Driven ports

**Example**:
```java
// application/ports/out/OrderRepository.java
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(OrderId id);
}

// application/ports/out/DomainEventPublisher.java
public interface DomainEventPublisher {
    void publish(DomainEvent event);
}

// application/services/CreateOrderService.java
public class CreateOrderService implements CreateOrderUseCase {
    private final OrderRepository repository;  // USES the port
    private final DomainEventPublisher publisher;  // USES the port

    @Override
    public OrderId execute(CreateOrderCommand command) {
        Order order = Order.create(command);
        repository.save(order);  // CALLS
        publisher.publish(new OrderCreated(order));  // CALLS
        return order.getId();
    }
}

// adapters/out/persistence/JpaOrderRepository.java
public class JpaOrderRepository implements OrderRepository {  // IMPLEMENTS
    @Override
    public void save(Order order) {
        // Implementation
    }
}

// adapters/out/messaging/KafkaEventPublisher.java
public class KafkaEventPublisher implements DomainEventPublisher {  // IMPLEMENTS
    @Override
    public void publish(DomainEvent event) {
        // Implementation
    }
}
```

### Key Differences

| Aspect | Inbound Ports | Outbound Ports |
|--------|---------------|----------------|
| **Direction** | Into the application | Out of the application |
| **Defined by** | Application layer | Application layer |
| **Implemented by** | Application layer | Adapters layer (out) |
| **Used by** | Adapters layer (in) | Application layer |
| **Example** | `CreateOrderUseCase` | `OrderRepository` |

---

## Related markers

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [DomainEvent](/marker/tactical/domainevent.md)
