---
type: Section
title: Key Differences
chapter: Domain-Centric Architecture vs Clean Architecture
source: guide
resource: implementing-domain-centric-architecture/clean-architecture-comparison.md
tags: [guide, section]
---

### 1. Domain Modeling (Biggest Difference)

| Aspect | Clean Architecture | Domain-Centric Architecture |
|--------|-------------------|----------------------------|
| **Entities** | Simple objects with business rules | Rich domain model (DDD) |
| **Patterns** | Entities only | Entities, Value Objects, Aggregates, Domain Services |
| **Complexity** | Simpler, procedural possible | More sophisticated domain modeling |
| **Focus** | Use Cases are central | Domain Model is central |

**Clean Architecture:**
```java
// Entity: Simple object with business rules
public class Order {
    private String id;
    private List<OrderLine> lines;

    // Simple business rules
    public boolean isValid() {
        return lines != null && !lines.isEmpty();
    }
}
```

**Domain-Centric Architecture:**
```java
// Aggregate Root: Rich domain model
public class Order implements AggregateRoot<OrderId> {
    private final OrderId id;
    private final CustomerId customerId;
    private final List<OrderLine> lines;
    private OrderStatus status;

    // Rich domain logic
    public void addOrderLine(Product product, Quantity quantity) {
        validateCanAddLine();
        OrderLine line = OrderLine.create(product, quantity);
        lines.add(line);
        registerDomainEvent(new OrderLineAdded(id, line.getId()));
    }

    public void cancel() {
        if (!status.canTransitionTo(OrderStatus.CANCELLED)) {
            throw new InvalidOrderStateException();
        }
        this.status = OrderStatus.CANCELLED;
        registerDomainEvent(new OrderCancelled(id, Instant.now()));
    }

    // Aggregate invariants
    private void validateCanAddLine() {
        if (status != OrderStatus.DRAFT) {
            throw new OrderNotModifiableException();
        }
    }
}
```

> **See:** [Domain-Centric Architecture - Domain Layer Rules](./README.md#domain-layer-rules) for full DDD patterns

### 2. Strategic Design

| Aspect | Clean Architecture | Domain-Centric Architecture |
|--------|-------------------|----------------------------|
| **Bounded Contexts** | Not explicitly addressed | Central concept |
| **Ubiquitous Language** | Not emphasized | Required |
| **Context Mapping** | Not included | Explicit relationships |
| **Subdomains** | Not addressed | Core, Supporting, Generic |

**Clean Architecture:**
- Focuses on **tactical** architecture (layers, dependencies)
- Doesn't provide guidance on **strategic** boundaries

**Domain-Centric Architecture:**
- Includes both **tactical** (layers) and **strategic** (bounded contexts) design
- Explicit guidance on how to partition large systems

> **See:** [Domain-Centric Architecture - Strategic Design Rules](./README.md#strategic-design-rules)

### 3. Domain Events

| Aspect | Clean Architecture | Domain-Centric Architecture |
|--------|-------------------|----------------------------|
| **Domain Events** | Not part of core pattern | Fundamental building block |
| **Event Types** | Not distinguished | Domain Events vs Integration Events |
| **Event-Driven** | Not emphasized | Central integration pattern |

**Clean Architecture:**
- Events not explicitly part of the pattern
- Can be added, but not core

**Domain-Centric Architecture:**
- Domain Events are first-class citizens
- Clear distinction: Domain Events (internal) vs Integration Events (external)
- Event-driven architecture built-in

**Example:**
```java
// Domain-Centric: Events as core pattern
public class CreateOrderUseCase {
    @Transactional
    public OrderId execute(CreateOrderCommand command) {
        Order order = Order.create(command);
        orders.save(order);

        // Domain event publishing
        events.publish(new OrderCreated(
            order.getId(),
            order.getCustomerId(),
            Instant.now()
        ));

        return order.getId();
    }
}
```

> **See:** [Domain-Centric Architecture - Domain Event Rules](./README.md#domain-event-rules-internal-to-bounded-context)

### 4. Terminology

| Clean Architecture | Domain-Centric Architecture | Notes |
|-------------------|----------------------------|-------|
| **Entities** | **Domain Model** (Entities, VOs, Aggregates) | DCA is more specific |
| **Use Cases** | **Use Cases / Application Services** | Same concept |
| **Input Port** | **Input Port** | Same |
| **Output Port** | **Output Port** | Same |
| **Controllers** | **Input Adapters** | Same concept, different name |
| **Gateways** | **Output Adapters** | Same concept, different name |
| **Presenters** | **Presenters** (optional in DCA) | DCA uses DTOs more |

### 5. Package Structure

**Clean Architecture (typical):**
```
com.company.project
├── entities/
│   ├── Order.java
│   └── Customer.java
├── usecases/
│   ├── CreateOrder.java
│   └── FindOrder.java
├── controllers/
│   └── OrderController.java
├── gateways/
│   └── OrderGateway.java
└── presenters/
    └── OrderPresenter.java
```

**Domain-Centric Architecture:**
```
com.company.project
├── order/ (bounded context)
│   ├── domain/
│   │   ├── model/ (Entities, VOs, Aggregates)
│   │   ├── service/ (Domain Services)
│   │   └── event/ (Domain Events)
│   ├── application/
│   │   ├── port/
│   │   │   ├── in/ (Input Ports)
│   │   │   └── out/ (Output Ports)
│   │   └── usecase/ (Use Cases)
│   ├── adapter/
│   │   ├── in/ (Input Adapters)
│   │   └── out/ (Output Adapters)
│   └── infrastructure/
└── customer/ (bounded context)
```

**Key Difference:** Domain-Centric Architecture organizes by **bounded context first**, then by layer.

> **See:** [Domain-Centric Architecture - Package Structure](./README.md#java-package-structure)

### 6. Presenter Pattern

**Clean Architecture:**
- **Presenters** are a core pattern
- Use Case calls Presenter to format output
- Presenter creates View Model

```java
// Clean Architecture: Presenter pattern
public class CreateOrderUseCase {
    private final CreateOrderPresenter presenter;

    public void execute(CreateOrderRequest request) {
        Order order = ...;
        presenter.present(order); // Presenter formats output
    }
}
```

**Domain-Centric Architecture:**
- **DTOs** are preferred over Presenters
- Use Case returns DTO directly
- Presenter is optional, used only for complex formatting

```java
// Domain-Centric: DTO pattern
public class CreateOrderUseCase {
    public CreateOrderResponse execute(CreateOrderCommand command) {
        Order order = ...;
        return new CreateOrderResponse(
            order.getId(),
            order.getTotalAmount()
        ); // Returns DTO directly
    }
}
```

### 7. Aggregate Pattern

**Clean Architecture:**
- No explicit Aggregate pattern
- Entities are independent
- Transactions not explicitly addressed

**Domain-Centric Architecture:**
- **Aggregates** are fundamental
- Aggregate Root controls access
- One transaction per Aggregate
- Eventual consistency between Aggregates

**Example:**
```java
// Domain-Centric: Aggregate pattern
public class Order implements AggregateRoot<OrderId> {
    private final OrderId id;
    private final List<OrderLine> lines; // Internal entities

    // Access to OrderLine only through Order (Aggregate Root)
    public void addLine(Product product, Quantity quantity) {
        OrderLine line = OrderLine.create(product, quantity);
        lines.add(line);
    }

    // No direct access to OrderLine from outside
}

// Repository only for Aggregate Root
public interface OrderRepository {
    void save(Order order); // Saves entire aggregate
    Optional<Order> findById(OrderId id);
}
```

**Repository interface placement:** Classic DDD literature (Evans, Vernon, Millett/Tune) places repository interfaces in the domain layer. DCA deliberately places them in the application layer as output ports — consistent with Hexagonal and Clean Architecture, where the use case owns the contracts it depends on. See [ADR-008: Repository Interfaces as Output Ports](../ai-architecture-sample/docs/architecture/adr/adr-008-repository-interfaces-as-output-ports.md) for the full rationale.

> **See:** [Domain-Centric Architecture - Aggregate Rules](./README.md#aggregate-rules)

### 8. Cross-Context Integration

**Clean Architecture:**
- Not explicitly addressed
- Assumes single application context

**Domain-Centric Architecture:**
- Explicit patterns for cross-context integration
- Anti-Corruption Layer
- Integration Events vs Domain Events
- Context Map

> **See:** [Domain-Centric Architecture - Integration Patterns](./README.md#integration-patterns)

## Related markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)

## Related ADRs

- [ADR-008: Repository Interfaces as Output Ports in Application Layer](/adr/adr-008-repository-interfaces-as-output-ports.md)
