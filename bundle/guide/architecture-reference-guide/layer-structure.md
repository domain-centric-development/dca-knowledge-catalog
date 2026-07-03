---
type: Section
title: Layer Structure
chapter: Architecture Reference Guide
source: guide
resource: implementing-domain-centric-architecture/architecture-reference-guide.md
tags: [guide, section]
---

### The Four Layers (Inner to Outer)

```
┌─────────────────────────────────────────┐
│         Infrastructure Layer            │
│  (Framework, Configuration, Main)       │
│  ┌───────────────────────────────────┐  │
│  │       Adapters Layer              │  │
│  │  (In: Web, CLI, Messaging)        │  │
│  │  (Out: Persistence, External)     │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │   Application Layer         │  │  │
│  │  │  (Use Cases, Ports)         │  │  │
│  │  │  ┌───────────────────────┐  │  │  │
│  │  │  │   Domain Layer        │  │  │  │
│  │  │  │  (Business Logic)     │  │  │  │
│  │  │  └───────────────────────┘  │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### 1. Domain Layer
**Purpose**: Pure business logic and rules

**Contains**:
- Entities, Value Objects, Aggregates
- Domain Events (the objects)
- Domain Services
- Domain Exceptions
- Business rules and invariants

**Dependencies**: NONE (maybe Common/Shared module)

**Example Structure**:
```
domain/
├── model/
│   ├── Order.java
│   ├── OrderId.java
│   ├── CustomerId.java
│   └── OrderLine.java
├── events/
│   ├── OrderPlaced.java
│   └── OrderCancelled.java
├── services/
│   └── PricingService.java
└── exceptions/
    └── InvalidOrderException.java
```

### 2. Application Layer
**Purpose**: Use case orchestration and coordination

**Contains**:
- Use case interfaces (inbound ports)
- Use case implementations (application services)
- Outbound port interfaces (SPI)
- Commands, Queries, DTOs
- Application exceptions

**Dependencies**: Domain, Common

**Recommended Structure (Self-Contained Use Case Pattern)**:
```
application/
├── createorder/            # Each use case in own folder - ALL related files together
│   ├── CreateOrderInputPort.java     # Interface: extends UseCase<COMMAND, RESULT>
│   ├── CreateOrderUseCase.java       # Implementation: implements CreateOrderInputPort
│   ├── CreateOrderCommand.java       # Input model (Command for writes)
│   └── CreateOrderResult.java        # Output model
├── findorder/              # Each use case in own folder - ALL related files together
│   ├── FindOrderInputPort.java       # Interface: extends UseCase<QUERY, RESULT>
│   ├── FindOrderUseCase.java         # Implementation: implements FindOrderInputPort
│   ├── OrderQuery.java               # Input model (Query for reads)
│   └── OrderResult.java              # Output model
├── cancelorder/            # Each use case in own folder - ALL related files together
│   ├── CancelOrderInputPort.java
│   ├── CancelOrderUseCase.java
│   ├── CancelOrderCommand.java
│   └── CancelOrderResult.java
└── shared/                 # Shared output ports (used by multiple use cases)
    ├── OrderRepository.java
    ├── DomainEventPublisher.java
    └── PaymentGateway.java
```

**Key Characteristics:**
- ✅ **High Cohesion** - InputPort interface + UseCase implementation + Command + Result all in one folder
- ✅ **Self-Contained** - Everything for one use case is together
- ✅ **Single Responsibility** - One folder = one business operation
- ✅ **Easy Navigation** - Find all related files in one place
- ✅ **Better Scalability** - Structure grows linearly with use cases
- ✅ **Clear Dependencies** - Use case depends only on domain + shared output ports

**Alternative Structure (Classic Port/Service Separation - Legacy Pattern)**:
```
application/
├── port/
│   ├── in/
│   │   ├── CreateOrderInputPort.java    # InputPort interfaces separate from implementations
│   │   └── FindOrderInputPort.java
│   └── out/
│       ├── OrderRepository.java         # Output ports in separate directory
│       └── DomainEventPublisher.java
└── usecase/
    ├── createorder/
    │   ├── CreateOrderUseCase.java      # Implementation separate from interface
    │   ├── CreateOrderCommand.java
    │   └── CreateOrderResult.java
    └── findorder/
        ├── FindOrderUseCase.java
        ├── OrderQuery.java
        └── OrderResult.java
```

**Why Self-Contained Pattern is Preferred:**
- Interface and implementation belong together (same bounded context, same use case)
- Reduces navigation between different directories
- Makes refactoring easier (move one folder = move entire use case)
- Aligns with "package by feature" principle
- Better team collaboration (less merge conflicts)

### 3. Adapters Layer
**Purpose**: Bridge between application and external systems

**Contains**:
- **Inbound Adapters** (Primary/Driving):
  - REST controllers
  - GraphQL resolvers
  - CLI handlers
  - Message queue listeners
  - gRPC services

- **Outbound Adapters** (Secondary/Driven):
  - Database repositories (JPA implementations)
  - Message queue publishers
  - External API clients
  - File system handlers
  - Cache implementations

**Dependencies**: Application, Domain, External Libraries, Common

**Example Structure**:
```
adapters/
├── in/
│   ├── web/
│   │   ├── OrderRestController.java
│   │   └── dto/
│   │       ├── CreateOrderRequest.java
│   │       └── OrderDto.java
│   ├── messaging/
│   │   └── OrderCommandListener.java
│   └── cli/
│       └── OrderCliHandler.java
└── out/
    ├── persistence/
    │   ├── JpaOrderRepository.java
    │   ├── OrderEntity.java
    │   └── SpringDataOrderRepository.java
    ├── messaging/
    │   └── KafkaEventPublisher.java
    └── external/
        └── StripePaymentGateway.java
```

### 4. Infrastructure Layer
**Purpose**: Technical/framework plumbing and wiring

**Contains**:
- Spring/framework configuration
- Dependency injection setup
- Security configuration
- Database configuration
- Logging setup
- Main application class
- Custom framework utilities

**Dependencies**: ALL (wires everything together)

**Example Structure**:
```
infrastructure/
├── configuration/
│   ├── SpringConfig.java
│   ├── SecurityConfig.java
│   ├── DatabaseConfig.java
│   ├── MessagingConfig.java
│   └── BeansConfiguration.java
├── lifecycle/
│   └── AsyncInitializationProcessor.java
└── Application.java  (main entry point)
```

### 5. Shared Kernel (DDD Pattern)
**Purpose**: Code shared across ALL bounded contexts

**Contains**:
- **`sharedkernel.domain`** - Shared domain concepts:
  - **`model/`** - Universal value objects (Money, common IDs, Address)
  - **`specification/`** - Common Specification Pattern classes
- **`sharedkernel.marker`** - Shared port marker interfaces:
  - **`tactical/`** - tactical DDD pattern interfaces (AggregateRoot, Entity, Value, DomainEvent, etc.)
  - **`strategic/`** - strategic DDD pattern interfaces (BoundedContext, SharedKernel, OpenHostService, etc.)
  - **`port.in/`** - Input port interfaces (InputPort, UseCase)
  - **`port.out/`** - Output port interfaces (OutputPort, Repository, DomainEventPublisher, IdentityProvider)

**Dependencies**: NONE (framework-independent)

**Port Interface Hierarchy**:
```
Input Ports (Driving/Primary)        Output Ports (Driven/Secondary)
┌────────────────────────────┐       ┌────────────────────────────┐
│ InputPort (marker)         │       │ OutputPort (marker)        │
│   └── UseCase<INPUT,OUTPUT>│       │   ├── Repository<T, ID>    │
│         └── *InputPort     │       │   ├── DomainEventPublisher │
└────────────────────────────┘       │   └── IdentityProvider     │
                                     └────────────────────────────┘
```

**Example Structure**:
```
sharedkernel/
├── marker/
│   ├── tactical/                ← DDD tactical pattern interfaces
│   │   ├── AggregateRoot.java   # public interface AggregateRoot<ID> extends Entity<ID> {}
│   │   ├── Entity.java          # public interface Entity<ID> { ID getId(); }
│   │   ├── Value.java           # public interface Value {}
│   │   ├── DomainEvent.java     # public interface DomainEvent { Instant occurredOn(); }
│   │   ├── DomainService.java   # Marker interface
│   │   ├── Factory.java         # Marker interface
│   │   └── Specification.java   # public interface Specification<T> { boolean isSatisfiedBy(T t); }
│   ├── strategic/               ← DDD strategic pattern interfaces
│   │   ├── SharedKernel.java
│   │   ├── BoundedContext.java
│   │   └── OpenHostService.java
│   ├── port/
│   │   ├── in/                  ← Input port interfaces
│   │   │   ├── InputPort.java   # public interface InputPort {} (marker)
│   │   │   └── UseCase.java     # public interface UseCase<INPUT, OUTPUT> extends InputPort { OUTPUT execute(INPUT input); }
│   │   └── out/                 ← Output port interfaces
│   │       ├── OutputPort.java  # public interface OutputPort {} (marker)
│   │       ├── Repository.java  # public interface Repository<T, ID> extends OutputPort {}
│   │       ├── DomainEventPublisher.java  # public interface DomainEventPublisher extends OutputPort { void publish(DomainEvent event); }
│   │       └── IdentityProvider.java      # public interface IdentityProvider extends OutputPort {}
│   └── infrastructure/          ← Infrastructure markers
│       └── AsyncInitialize.java # Marker annotation for async initialization
├── domain/
│   ├── model/                   ← Universal value objects
│   │   ├── Money.java
│   │   ├── ProductId.java
│   │   ├── CustomerId.java
│   │   └── Address.java
│   └── exception/               ← Base domain exceptions
│       ├── DomainException.java
│       └── BusinessRuleViolationException.java
└── adapter/
    └── outgoing/                ← Shared adapters
        └── SpringDomainEventPublisher.java
```

**What Belongs in Shared Kernel:**

✅ **Include:**
- **Marker interfaces** that define DDD patterns across all contexts
- **Universal value objects** with identical meaning everywhere (Money, Address)
- **Base port interfaces** that establish application patterns
- **Base exceptions** for common error handling

❌ **Exclude:**
- **Aggregates** - These belong to specific bounded contexts
- **Business logic** - Should live in context-specific domain layers
- **Context-specific value objects** - Only truly universal ones belong here
- **Use case implementations** - Belong to specific contexts
- **Adapters** - Never shared between contexts

**Key Principles**:
- **Keep it minimal** - Changes affect ALL contexts
- Shared Kernel = Code used by 2+ bounded contexts
- Context-specific = Code used by 1 bounded context only
- Only include code with **identical meaning** across all contexts
- When in doubt, **duplicate rather than share**

---

## Related markers

- [@AsyncInitialize](/marker/infrastructure/asyncinitialize.md)
- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [IdentityProvider](/marker/port-out/identityprovider.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@OpenHostService](/marker/strategic/openhostservice.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainService](/marker/tactical/domainservice.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Factory](/marker/tactical/factory.md)
- [Specification<T>](/marker/tactical/specification.md)
