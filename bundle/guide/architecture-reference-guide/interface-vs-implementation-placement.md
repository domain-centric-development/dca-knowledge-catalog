---
type: Section
title: Interface vs Implementation Placement
chapter: Architecture Reference Guide
source: guide
resource: implementing-domain-centric-architecture/architecture-reference-guide.md
tags: [guide, section]
---

### The Asymmetry Rule

**Inbound Ports**: Interface AND Implementation in Application layer
```
application/
├── ports/in/
│   └── CreateOrderUseCase.java        ← Interface
└── services/
    └── CreateOrderService.java         ← Implementation (implements CreateOrderUseCase)
```

**Outbound Ports**: Interface in Application, Implementation in Adapters
```
application/
└── ports/out/
    └── OrderRepository.java            ← Interface only

adapters/
└── out/persistence/
    └── JpaOrderRepository.java         ← Implementation (implements OrderRepository)
```

### Why This Asymmetry?

- **Application services ARE the business logic** - they belong in the application layer
- **Infrastructure implementations are technical details** - they belong in adapters
- This maintains the Dependency Inversion Principle (DIP)

### Complete Flow Example

```java
// ============ APPLICATION LAYER ============

// Inbound Port (Interface)
public interface CreateOrderUseCase {
    OrderId execute(CreateOrderCommand command);
}

// Outbound Ports (Interfaces)
public interface OrderRepository {
    void save(Order order);
}

public interface DomainEventPublisher {
    void publish(DomainEvent event);
}

// Application Service (Implements inbound, uses outbound)
public class CreateOrderService implements CreateOrderUseCase {
    private final OrderRepository repository;
    private final DomainEventPublisher publisher;

    public CreateOrderService(OrderRepository repository,
                             DomainEventPublisher publisher) {
        this.repository = repository;
        this.publisher = publisher;
    }

    @Override
    public OrderId execute(CreateOrderCommand command) {
        Order order = Order.create(command);
        repository.save(order);
        publisher.publish(new OrderCreated(order));
        return order.getId();
    }
}

// ============ ADAPTERS LAYER ============

// Inbound Adapter (USES inbound port)
@RestController
public class OrderRestController {
    private final CreateOrderUseCase createOrder;

    @PostMapping("/orders")
    public ResponseEntity<?> create(@RequestBody CreateOrderRequest req) {
        OrderId id = createOrder.execute(toCommand(req));
        return ResponseEntity.ok(id);
    }
}

// Outbound Adapters (IMPLEMENT outbound ports)
@Repository
public class JpaOrderRepository implements OrderRepository {
    private final SpringDataOrderRepository jpaRepo;

    @Override
    public void save(Order order) {
        OrderEntity entity = OrderEntity.fromDomain(order);
        jpaRepo.save(entity);
    }
}

@Component
public class KafkaEventPublisher implements DomainEventPublisher {
    private final KafkaTemplate<String, String> kafka;

    @Override
    public void publish(DomainEvent event) {
        kafka.send("events", serialize(event));
    }
}

// ============ INFRASTRUCTURE LAYER ============

// Wiring Everything Together
@Configuration
public class BeansConfiguration {

    @Bean
    public CreateOrderUseCase createOrderUseCase(
            OrderRepository repository,
            DomainEventPublisher publisher) {
        return new CreateOrderService(repository, publisher);
    }

    @Bean
    public OrderRepository orderRepository() {
        return new JpaOrderRepository(...);
    }

    @Bean
    public DomainEventPublisher eventPublisher() {
        return new KafkaEventPublisher(...);
    }
}
```

---

## Related markers

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [DomainEvent](/marker/tactical/domainevent.md)
