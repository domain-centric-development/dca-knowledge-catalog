---
type: Section
title: ELEMENTS
chapter: Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/README.md
tags: [guide, section]
---

### Domain Layer (Enterprise Business Rules)

#### Tactical Building Blocks
- **Entity** - Object with identity and lifecycle
- **Value Object** - Immutable object without identity
- **Aggregate** - Transactional consistency boundary
- **Aggregate Root** - Entry point entity for aggregate access
- **Domain Service** - Stateless operation on domain objects
- **Domain Event** - Immutable record of domain occurrence (internal to bounded context)
- **Specification** - Encapsulated business rule
- **Factory** - Complex object creation logic

#### Strategic Building Blocks
- **Bounded Context** - Explicit boundary for unified model
- **Ubiquitous Language** - Shared vocabulary in code and conversation
- **Subdomain** - Logical domain partition (Core, Supporting, Generic)

### Application Layer (Use Cases / Application Business Rules)

#### Use Case Pattern with Input Ports

The application layer organizes business operations using a structured **Use Case pattern** where each use case is isolated in its own folder with dedicated Input/Output models:

**Pattern Structure:**
- **Use Case** - Implements business operation (orchestrates domain objects)
- **Input Port** - Interface defining use case contract (`extends UseCase<INPUT, OUTPUT>`)
- **Command/Query** - Input model (Command for writes, Query for reads)
- **Result** - Output model (standardized return type)
- **Output Port** - Interface for infrastructure needs (repositories, gateways, publishers)

**Organization:**
```
application/
├── {usecasename}/          # e.g., createorder, findorder, cancelorder (lowercase)
│   ├── *InputPort.java     # Interface: public interface CreateOrderInputPort extends UseCase<CreateOrderCommand, CreateOrderResult>
│   ├── *UseCase.java       # Implementation: @Service public class CreateOrderUseCase implements CreateOrderInputPort
│   ├── *Command.java       # Input model (for write operations)
│   │   OR *Query.java      # Input model (for read operations)
│   └── *Result.java      # Output model
└── shared/                 # Shared output ports
    └── *Repository.java    # Repository interfaces, DomainEventPublisher, etc.
```

> **Note:** Use case folder names are **lowercase** (e.g., `createorder`, `additemtocart`, `getproductbyid`), while the files inside use **PascalCase** (e.g., `CreateOrderInputPort.java`, `CreateOrderUseCase.java`).

**Benefits:**
- ✅ **Single Responsibility** - One use case class per business operation
- ✅ **Explicit Contracts** - Clear input/output via InputPort interface
- ✅ **Self-Contained** - All related files grouped together
- ✅ **Interface Segregation** - Adapters inject only the specific ports they need
- ✅ **Better Hexagonal Alignment** - Input Ports define the application's external API

**Example:**
```java
// Input Port Interface (defines contract)
public interface CreateOrderInputPort extends UseCase<CreateOrderCommand, CreateOrderResult> {
    CreateOrderResult execute(CreateOrderCommand command);
}

// Use Case Implementation (orchestrates domain)
@Service
public class CreateOrderUseCase implements CreateOrderInputPort {

    private final OrderRepository orderRepository;  // Output Port
    private final DomainEventPublisher eventPublisher;  // Output Port

    @Override
    public CreateOrderResult execute(CreateOrderCommand command) {
        // 1. Convert DTO to domain
        Order order = Order.create(command.customerId(), command.items());

        // 2. Business logic (in domain)
        order.validate();

        // 3. Persist via output port
        orderRepository.save(order);

        // 4. Publish events via output port
        eventPublisher.publish(order.getDomainEvents());

        // 5. Convert domain to DTO
        return CreateOrderResult.from(order);
    }
}

// Input Model (Command)
public record CreateOrderCommand(CustomerId customerId, List<OrderItemDto> items) {}

// Output Model (Result)
public record CreateOrderResult(OrderId orderId, Money total, OrderStatus status) {
    public static CreateOrderResult from(Order order) {
        return new CreateOrderResult(order.getId(), order.getTotal(), order.getStatus());
    }
}
```

#### Application Layer Components

- **Use Case / Application Service** - Orchestrates business operations
- **Input Port** - Interface defining use case entry point
- **Output Port** - Interface for infrastructure needs
- **Command** - Request to change state
- **Query** - Request to retrieve data
- **Input Data / DTO** - Data structure for use case input
- **Output Data / DTO** - Data structure for use case output
- **Repository Interface** - Aggregate persistence abstraction
- **Domain Event Publisher Interface** - Event dispatching abstraction

### Adapter Layer (Interface Adapters)

#### Input Adapters (Driving/Primary)
- **Controller** - Handles HTTP/framework requests
- **Event Consumer** - Handles external events/messages
- **CLI Handler** - Command-line interface
- **GraphQL Resolver** - GraphQL query/mutation handler
- **Scheduled Job** - Time-triggered operations

#### Output Adapters (Driven/Secondary)
- **Repository Adapter** - Persistence implementation
- **Event Publisher Adapter** - Event publishing implementation
- **External API Client** - Third-party service integration
- **Presenter** - Formats use case output for external world
- **Gateway** - Database/external system translation

#### Adapter Components
- **Mapper** - Translation between layers
- **DTO** - Data transfer across boundaries
- **View Model** - Presentation data structure
- **Database Entity** - ORM/persistence model
- **Integration Event** - DTO representing domain event for cross-context communication
- **Event Mapper** - Converts domain events to/from integration events
- **Anti-Corruption Layer (ACL)** - Protects domain from external event formats

### Infrastructure Layer (Frameworks & Drivers)

- **Web Framework** - Spring, Quarkus, etc.
- **Persistence Framework** - JPA, Hibernate, etc.
- **Message Broker** - Kafka, RabbitMQ, etc.
- **Configuration** - Dependency injection, framework setup
- **Cross-Cutting Concerns** - Logging, monitoring, security

### Strategic Architecture

- **Context Map** - Relationships between bounded contexts
- **Anti-Corruption Layer** - Protection from external models
- **Shared Kernel** - Shared code between contexts (see detailed structure below)
- **Open Host Service** - Published integration API
- **Published Language** - Well-documented shared protocol

#### Shared Kernel Pattern (Strategic DDD)

The **Shared Kernel** contains code shared across ALL bounded contexts within your application. It should be kept minimal and requires coordination between teams.

**Structure:**
```
sharedkernel/
├── marker/                        # All architectural markers (consolidated)
│   ├── tactical/                  # DDD Tactical Patterns
│   │   ├── Id.java                # Base interface for identifiers
│   │   ├── Entity.java            # Interface for entities
│   │   ├── Value.java             # Marker for value objects
│   │   ├── AggregateRoot.java     # Interface for aggregate roots
│   │   ├── BaseAggregateRoot.java # Abstract base implementation
│   │   ├── DomainEvent.java       # Interface for domain events
│   │   ├── IntegrationEvent.java  # Interface for integration events
│   │   ├── DomainService.java     # Marker for domain services
│   │   ├── Factory.java           # Marker for factories
│   │   └── Specification.java     # Interface for specifications
│   ├── strategic/                 # DDD Strategic Patterns
│   │   ├── SharedKernel.java      # Annotation for shared kernel packages
│   │   ├── BoundedContext.java    # Annotation for bounded context packages
│   │   └── OpenHostService.java   # Marker for Open Host Service adapters
│   └── port/                      # Hexagonal Architecture Ports
│       ├── in/                    # Input Ports (Driving/Primary)
│       │   ├── InputPort.java     # Marker for all input ports
│       │   └── UseCase.java       # UseCase<INPUT, OUTPUT> extends InputPort
│       └── out/                   # Output Ports (Driven/Secondary)
│           ├── OutputPort.java    # Marker for all output ports
│           ├── Repository.java    # Base repository: extends OutputPort (for Aggregate Roots)
│           ├── Store.java         # Base store: extends OutputPort (for operational data)
│           ├── DomainEventPublisher.java  # Event publishing: extends OutputPort
│           └── IdentityProvider.java      # Identity abstraction with nested interfaces
│
└── domain/
    ├── model/                     # Universal Value Objects
    │   ├── Money.java             # Universal money type
    │   ├── Price.java             # Common price value object
    │   ├── ProductId.java         # Shared product identifier
    │   └── UserId.java            # Shared user identifier
    └── specification/             # Specification Pattern Implementation
        ├── CompositeSpecification.java
        ├── AndSpecification.java
        ├── OrSpecification.java
        ├── NotSpecification.java
        └── SpecificationVisitor.java
```

**Port Interface Hierarchy:**
```
Input Ports (marker/port/in/)        Output Ports (marker/port/out/)
┌────────────────────────────┐       ┌────────────────────────────┐
│ InputPort (marker)         │       │ OutputPort (marker)        │
│   └── UseCase<INPUT,OUTPUT>│       │   ├── Repository<T, ID>    │
│         └── *InputPort     │       │   ├── Store               │
└────────────────────────────┘       │   ├── DomainEventPublisher │
                                     │   └── IdentityProvider     │
                                     └────────────────────────────┘
```

**Identity Pattern (Extensible Design):**
```java
// In sharedkernel/marker/port/out/IdentityProvider.java
public interface IdentityProvider extends OutputPort {
    Identity getCurrentIdentity();

    // Nested interface - contract for identity
    interface Identity {
        UserId userId();
        IdentityType type();
        Optional<String> email();
        Set<String> roles();
        default boolean isAnonymous() { return type().isAnonymous(); }
        default boolean isRegistered() { return type().isRegistered(); }
    }

    // Nested interface - extensible identity type
    interface IdentityType {
        String name();
        boolean isAnonymous();
        boolean isRegistered();
    }
}

// In infrastructure/security/ - PROJECT-SPECIFIC implementations
public enum JwtIdentityType implements IdentityProvider.IdentityType {
    ANONYMOUS, REGISTERED, SERVICE_ACCOUNT;  // Extensible per project
}

public record JwtIdentity(...) implements IdentityProvider.Identity { ... }
```

- **InputPort** - Marker interface for all entry points to the application (called by driving adapters)
- **OutputPort** - Marker interface for all dependencies the application needs (implemented by driven adapters)
- **UseCase<INPUT, OUTPUT>** - Specific input port type with Command/Query → Result pattern
- **Repository<T, ID>** - Collection-like output port for Aggregate Roots (one-per-aggregate)
- **Store** - Output port for operational data without aggregate lifecycle (Value Objects, Events, technical state)

### Repository vs. Store

DCA distinguishes two kinds of persistence-shaped output ports. Both `extend OutputPort`, but their **business semantics differ**:

**Repository** — collection-like interface for Aggregate Roots (Evans, Vernon).

- Exists **only** for Aggregate Roots
- Identity + lifecycle semantics: `findById()`, `save()`, `delete()`
- Extends the `Repository<T, ID>` marker
- One Repository per Aggregate Root

```java
public interface CustomerAccountRepository extends Repository<CustomerAccount, CustomerAccountId> {
    Optional<CustomerAccount> findById(CustomerAccountId id);
    void save(CustomerAccount account);
}
```

**Store** — records or queries operational data without an own aggregate lifecycle.

- Exists for **Value Objects, Events, or technical state** without identity-based access
- Append-/record-style semantics: `record()`, `count()`, `exists()`, `reset()` — no `findById()` / `save()`
- Extends the `Store` marker (`Store extends OutputPort`) — never the `Repository` marker
- Implementation lives in `adapter.outgoing/`

```java
public interface LoginProtectionStore extends Store {
    void record(LoginAttempt attempt);
    int  countRecentFailures(BaseStore baseStore, Email email, Duration window);
    boolean isLoginBlocked(BaseStore baseStore, Email email);
}
```

**Decision matrix:**

| Criterion | Repository | Store |
|---|---|---|
| Stored object | Aggregate Root | Value Object / operational data |
| Identity & lifecycle | yes — `findById`, `save`, `delete` | no — `record`, `count`, `exists` |
| Marker | `extends Repository<T, ID>` | `extends Store` |
| Examples | `CustomerAccountRepository`, `OrderRepository` | `LoginProtectionStore`, `AuditLogStore`, `EventStore` |

**Rules of thumb:**

1. Need `findById()`? → Repository (the object has identity).
2. Need `record()` or `count()`? → Store (the object is recorded, not managed).
3. In doubt: if the stored object is a `Value` or a record, it's almost always a Store.

> **Note on EventStore (Event Sourcing):** The `EventStore` from Event Sourcing is a *specialization* of Store — one specifically for Domain Events that supports aggregate reconstruction. The general `Store` is the broader pattern for any operational data. See `dca-book/17-event-sourcing.md`.

> **Note on cross-cutting `*Response` classes:** Generic Response/error classes (`ErrorResponse`, base `Response`, `SimpleResponse`) belong in the **shared kernel's adapter-incoming package**, not in any individual bounded context. ArchUnit rules that check `*Response` placement must include the shared kernel adapter — discover its package dynamically via `@SharedKernel` rather than hardcoding the name (`shared` / `common` / `core` / `sharedkernel`).

**Why the distinction matters:**
The naming is part of the Ubiquitous Language. A reader should know from the interface name alone whether they're dealing with a managed aggregate (Repository) or recorded data (Store) — without opening the implementation. Both are technically Output Ports in hexagonal architecture, but the business role is fundamentally different.

**What Belongs in Shared Kernel:**

✅ **Include:**
- **Universal value objects** used by multiple contexts (Money, Price, shared IDs)
- **DDD marker interfaces** that define your architectural patterns (Entity, AggregateRoot, Value, etc.)
- **Base port interfaces** (`UseCase<INPUT, OUTPUT>`, `Repository`, `DomainEventPublisher`)
- **Specification pattern implementations** (CompositeSpecification, And/Or/Not specifications)
- **Cross-cutting domain concepts** that have identical meaning everywhere

❌ **Exclude:**
- **Aggregates** - These belong to specific bounded contexts
- **Business logic** - Should live in context-specific domain layers
- **Context-specific value objects** - Only truly universal ones belong here
- **Use case implementations** - Belong to specific contexts
- **Adapters** - Never shared between contexts

**Guidelines:**
- Keep the Shared Kernel **as small as possible**
- Changes to Shared Kernel affect all contexts - coordinate carefully
- Only include code that has **identical meaning** across all contexts
- When in doubt, duplicate rather than share
- Use versioning if Shared Kernel becomes a separate module

**Decision Tree: Should This Go in Shared Kernel?**
```
START: I have code that might be shared
   │
   ├─ Is it used by 2+ bounded contexts?
   │     NO → Keep in single context
   │     YES ↓
   │
   ├─ Does it have IDENTICAL meaning everywhere?
   │     NO → Duplicate instead (different models OK)
   │     YES ↓
   │
   ├─ Is it a marker interface or base type?
   │     YES → Add to sharedkernel/marker/tactical/
   │     NO ↓
   │
   ├─ Is it a universal value object (Money, Address)?
   │     YES → Add to sharedkernel/domain/model/
   │     NO ↓
   │
   └─ Is it a base port interface (UseCase, Repository)?
         YES → Add to sharedkernel/marker/port/
         NO → Probably shouldn't be in Shared Kernel
```

**Example - Marker Interface:**
```java
// sharedkernel/marker/tactical/AggregateRoot.java
public interface AggregateRoot<ID> extends Entity<ID> {
    // Marker interface - identifies aggregate roots for all contexts
}

// sharedkernel/marker/tactical/Entity.java
public interface Entity<ID> {
    ID getId();
    default boolean isSameAs(Entity<ID> other) {
        return this.getId().equals(other.getId());
    }
}
```

**Example - Shared Value Object:**
```java
// sharedkernel/domain/model/Money.java
public record Money(BigDecimal amount, Currency currency) implements Value {

    public Money {
        Objects.requireNonNull(amount);
        Objects.requireNonNull(currency);
        if (amount.scale() > 2) {
            throw new IllegalArgumentException("Money cannot have more than 2 decimal places");
        }
    }

    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Cannot add money with different currencies");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

**Example - Port Interface Hierarchy:**
```java
// sharedkernel/marker/port/in/InputPort.java
public interface InputPort {
    // Marker interface for all input ports (hexagonal architecture concept)
}

// sharedkernel/marker/port/out/OutputPort.java
public interface OutputPort {
    // Marker interface for all output ports (hexagonal architecture concept)
}

// sharedkernel/marker/port/in/UseCase.java
public interface UseCase<INPUT, OUTPUT> extends InputPort {
    OUTPUT execute(INPUT input);
}

// sharedkernel/marker/port/out/Repository.java
public interface Repository<T, ID> extends OutputPort {
    Optional<T> findById(ID id);
    T save(T aggregate);
    void deleteById(ID id);
}

// Usage in a bounded context:
// order/application/createorder/CreateOrderInputPort.java
public interface CreateOrderInputPort extends UseCase<CreateOrderCommand, CreateOrderResult> {
    // Inherits execute() method with specific types
}

// order/application/shared/OrderRepository.java
public interface OrderRepository extends Repository<Order, OrderId> {
    // Inherits base methods, add domain-specific queries
    Optional<Order> findByCustomerId(CustomerId customerId);
}
```

## Related markers

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [IdentityProvider](/marker/port-out/identityprovider.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@OpenHostService](/marker/strategic/openhostservice.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainService](/marker/tactical/domainservice.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Factory](/marker/tactical/factory.md)
- [IntegrationEvent](/marker/tactical/integrationevent.md)
- [Specification<T>](/marker/tactical/specification.md)
