---
type: Section
title: Framework Annotations Rules
chapter: Architecture Reference Guide
source: guide
resource: implementing-domain-centric-architecture/architecture-reference-guide.md
tags: [guide, section]
---

### By Layer

#### ❌ Domain Layer - NEVER

**Domain must be pure - NO framework annotations**

```java
// ✅ CORRECT - Pure domain
public class Order {
    private OrderId id;
    private CustomerId customerId;

    public static Order create(CustomerId customerId) {
        // Business logic
    }
}

// ❌ WRONG - Framework pollution
@Entity  // ❌ NO JPA!
public class Order {
    @Id  // ❌ NO!
    private Long id;

    @Autowired  // ❌ NO Spring!
    private OrderValidator validator;
}
```

**Why**: Domain is the heart of your application. It must be:
- Framework-agnostic
- Portable
- Testable without any infrastructure
- Long-lived (frameworks change, business rules don't)

#### ⚠️ Application Layer - Minimally (Pragmatic) or Never (Purist)

**Purist Approach** (Recommended for strict Clean Architecture):
```java
// ✅ Pure - No annotations
public class CreateOrderService implements CreateOrderUseCase {
    private final OrderRepository repository;

    // Plain constructor - no @Autowired
    public CreateOrderService(OrderRepository repository) {
        this.repository = repository;
    }
}
```

**Pragmatic Approach** (Common in real projects):
```java
// ⚠️ Acceptable - Minimal Spring coupling
@Service  // Just marks it as a bean
public class CreateOrderService implements CreateOrderUseCase {
    private final OrderRepository repository;

    // Constructor injection works without @Autowired in modern Spring
    public CreateOrderService(OrderRepository repository) {
        this.repository = repository;
    }
}
```

**Decision factors**:
- Strict portability → Purist (no annotations)
- Pragmatic/fast development → Minimal annotations OK
- Team preference and project goals

#### ✅ Adapters Layer - YES

**Adapters are the integration point - framework annotations are expected**

```java
// ✅ CORRECT - REST adapter
@RestController
@RequestMapping("/api/orders")
public class OrderRestController {
    private final CreateOrderUseCase createOrder;

    @Autowired
    public OrderRestController(CreateOrderUseCase createOrder) {
        this.createOrder = createOrder;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public OrderDto create(@RequestBody @Valid CreateOrderRequest req) {
        OrderId id = createOrder.execute(toCommand(req));
        return toDto(id);
    }
}

// ✅ CORRECT - JPA adapter (separate from domain!)
@Entity
@Table(name = "orders")
public class OrderEntity {  // NOT the domain Order!
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "customer_id")
    private String customerId;

    // Mapping to/from domain
    public Order toDomain() {
        return new Order(
            new OrderId(id),
            new CustomerId(customerId)
        );
    }

    public static OrderEntity fromDomain(Order order) {
        OrderEntity entity = new OrderEntity();
        entity.id = order.getId().getValue();
        entity.customerId = order.getCustomerId().getValue();
        return entity;
    }
}

// ✅ CORRECT - Repository adapter
@Repository
public class JpaOrderRepository implements OrderRepository {
    private final SpringDataOrderRepository jpaRepo;

    @Override
    public void save(Order order) {
        OrderEntity entity = OrderEntity.fromDomain(order);
        jpaRepo.save(entity);
    }

    @Override
    public Optional<Order> findById(OrderId id) {
        return jpaRepo.findById(id.getValue())
            .map(OrderEntity::toDomain);
    }
}
```

#### ✅ Infrastructure Layer - YES

**Infrastructure is all about framework configuration**

```java
// ✅ CORRECT
@Configuration
@EnableKafka
public class MessagingConfig {

    @Bean
    public DomainEventPublisher eventPublisher(KafkaTemplate<String, String> kafka) {
        return new KafkaEventPublisher(kafka);
    }
}

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### The JPA/Persistence Pattern

**Problem**: Domain needs to be persisted, but JPA requires annotations

**❌ WRONG Solution**: Put JPA on domain
```java
// domain/Order.java
@Entity  // ❌ Pollutes domain with JPA
public class Order {
    @Id
    private Long id;
}
```

**✅ CORRECT Solution**: Separate persistence model
```java
// domain/Order.java
public class Order {  // Pure domain - no JPA
    private OrderId id;
    private CustomerId customerId;
    private List<OrderLine> lines;

    // Business methods
}

// adapters/out/persistence/OrderEntity.java
@Entity
@Table(name = "orders")
public class OrderEntity {  // JPA model - separate!
    @Id
    @GeneratedValue
    private Long id;

    private String customerId;

    @OneToMany(cascade = CascadeType.ALL)
    private List<OrderLineEntity> lines;

    // Bidirectional mapping
    public Order toDomain() {
        return new Order(
            new OrderId(id),
            new CustomerId(customerId),
            lines.stream()
                .map(OrderLineEntity::toDomain)
                .collect(toList())
        );
    }

    public static OrderEntity fromDomain(Order order) {
        OrderEntity entity = new OrderEntity();
        entity.id = order.getId().getValue();
        entity.customerId = order.getCustomerId().getValue();
        entity.lines = order.getLines().stream()
            .map(OrderLineEntity::fromDomain)
            .collect(toList());
        return entity;
    }
}

// adapters/out/persistence/JpaOrderRepository.java
@Repository
public class JpaOrderRepository implements OrderRepository {
    private final SpringDataOrderRepository jpaRepo;

    @Override
    public void save(Order order) {
        OrderEntity entity = OrderEntity.fromDomain(order);
        jpaRepo.save(entity);
    }

    @Override
    public Optional<Order> findById(OrderId id) {
        return jpaRepo.findById(id.getValue())
            .map(OrderEntity::toDomain);
    }
}
```

**Yes, this means two separate classes** - but:
- Domain stays pure
- Persistence can change independently
- Different persistence strategies possible
- Domain focused on business, not persistence

### Summary Table

| Layer | Framework Annotations | Examples | Reason |
|-------|----------------------|----------|---------|
| **Domain** | ❌ NEVER | Pure Java/Kotlin only | Must be portable, framework-agnostic |
| **Application** | ⚠️ Minimal (or never) | Maybe `@Service` | Prefer pure, but pragmatic minimal OK |
| **Adapters** | ✅ YES | `@RestController`, `@Entity`, `@Repository` | Integration point with frameworks |
| **Infrastructure** | ✅ YES | `@Configuration`, `@Bean`, `@EnableXxx` | All about framework setup |
| **Common** | ⚠️ Neutral only | `@NotNull`, `@Nullable`, custom annotations | Shared across all layers |

---

## Related markers

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
