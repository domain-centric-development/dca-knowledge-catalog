---
type: Section
title: JAVA PACKAGE STRUCTURE
chapter: Domain-Centric Architecture
source: guide
resource: dca-guide/README.md
tags: [guide, section]
---

### Standard Structure (Fully Elaborated)

#### High-Level Structure Overview

```
com.company.project/
│
├── {boundedcontext}/
│   │
│   ├── domain/              [CORE LAYER]
│   │                        Pure business logic with zero dependencies
│   │                        Entities, Value Objects, Aggregates, Domain Services, Domain Events
│   │
│   ├── application/         [USE CASE LAYER]
│   │                        Orchestrates domain objects and defines boundaries
│   │                        Input Ports, Output Ports, Use Cases, Commands, Queries, DTOs
│   │
│   ├── adapter/             [INFRASTRUCTURE INTERFACE LAYER]
│   │                        Connects application to external world
│   │   ├── incoming/        Controllers, Event Consumers, CLI (call Input Ports)
│   │   └── outgoing/        Repository Impl, API Clients, Publishers (implement Output Ports)
│   │
│   └── infrastructure/      [FRAMEWORKS & DRIVERS LAYER]
│                            Framework-specific configuration and cross-cutting concerns
│                            Spring, JPA, Kafka config, Logging, Security
│
├── sharedkernel/            [SHARED ACROSS ALL CONTEXTS - Keep Minimal]
│   ├── marker/              DDD markers (tactical/, strategic/) and port interfaces (port/)
│   ├── domain/model/        Universal value objects (Money, Address, etc.)
│   └── adapter/outgoing/    Shared adapters (e.g., SpringDomainEventPublisher)
│
└── infrastructure/          [GLOBAL INFRASTRUCTURE]
                             Application-wide configuration and setup
```

#### Progressive Complexity Principle

This structure shows **ALL possible subdivisions** for a fully-featured bounded context with significant complexity. However, you should **START SIMPLE** and add structure incrementally:

**🎯 Start Minimal**
- Begin with the 4 core layers (domain, application, adapter, infrastructure) without deep nesting
- Place files directly in layer directories until organization becomes difficult
- A simple bounded context may only need 5-10 files total

**📈 Add When Needed**
- Introduce subdirectories only when you have enough files that organization provides clear benefit
- Typically: >10 files in a directory suggests subdividing
- Let pain points guide structure, not theoretical perfection

**🔄 Refactor Later**
- It's easier to add structure later than to maintain unnecessary complexity early
- Moving files into new subdirectories is a simple refactoring
- IDEs handle this automatically with refactoring tools

**The structure below is a REFERENCE showing all options, not a prescription to use everything from day one.**

#### Grouping use cases into features

DCA has three scales below the system: the **bounded context**, the **layer**, and the **use case**. When the
application layer of one context grows — a dozen use-case packages in one flat list — a fourth, optional scale
fills the gap between layer and use case: the **feature**.

```text
system -> bounded context -> layer -> feature -> use case
```

A *feature* is a domain-named group of related use cases inside one bounded context. It is a navigation and
cohesion boundary and nothing more: not a layer, not a module, not an aggregate owner, not a deployment unit.

The two canonical forms of the application layer — and the only two — are:

```text
application/{usecase}/              # flat: a small context
application/{feature}/{usecase}/    # grouped: cohesive clusters have emerged
```

A context that has grown into features:

```text
checkout/
├── domain/                              # concepts owned by the whole context — never mirrored by feature
│   ├── model/
│   ├── service/
│   ├── event/
│   └── readmodel/
├── application/
│   ├── session/                         # feature
│   │   ├── startcheckout/               # use case — input port, implementation, command/query, result
│   │   ├── getactivecheckoutsession/
│   │   ├── getcheckoutsession/
│   │   └── getconfirmedcheckoutsession/
│   ├── checkoutcompletion/              # feature — a term of the ubiquitous language, not UI jargon
│   │   ├── submitbuyerinfo/
│   │   ├── getshippingoptions/
│   │   ├── submitdelivery/
│   │   ├── getpaymentproviders/
│   │   ├── submitpayment/
│   │   └── confirmcheckout/
│   ├── cartsync/
│   │   └── synccheckoutwithcart/
│   └── shared/                          # context-wide output ports only
├── adapter/
│   ├── incoming/
│   │   ├── web/{session,checkoutcompletion}/   # protocol first, feature below it
│   │   └── event/cartsync/
│   └── outgoing/{persistence,payment,cart,product,event}/   # by technology or partner, as before
├── api/
├── events/
└── infrastructure/
```

**The eight rules of the feature scale:**

1. **Flat first.** A small context keeps `application/{usecase}/`. Add the feature level when cohesive clusters
   have emerged and the flat list has become hard to navigate. The "about ten entries" guidance above is a prompt
   to *evaluate* grouping, not a numeric law.
2. **Feature names come from the ubiquitous language**, lowercase: `cartrecovery`, `checkoutcompletion`,
   `session`. Never technical buckets (`commands`, `queries`, `handlers`, `services`, `utils`) and never delivery
   mechanisms (`web`, `api`).
3. **The use case stays the smallest application unit.** Its input port, implementation, command or query,
   result and any use-case-specific output port stay together in the use-case package.
4. **`application/shared` stays context-wide.** Repository and Store interfaces continue to live there
   (`DCA-TAC-014`, `DCA-TAC-019`); there is no `application/{feature}/shared`. A port used by one use case stays
   with that use case, a port used by several belongs in `application/shared`.
5. **The domain is organised by concept, not mirrored by feature.** Aggregates and value objects belong to the
   bounded context and may serve several features — a feature owns no aggregate.
6. **Incoming adapters may mirror features *below* their protocol:** `adapter/incoming/web/{feature}`,
   `adapter/incoming/event/{feature}`. The protocol segment stays first, so the adapter vocabulary and its rules
   (`DCA-NAM-011`) keep working. Outgoing adapters stay organised by technology or partner.
7. **One form per context.** Within one context, use cases are either all flat or all grouped once a migration is
   complete; a lasting mixture leaves the reader guessing whether a direct child of `application/` is a feature,
   a use case or a leftover. A short-lived mixed state during one refactoring is fine — move one whole context
   atomically. `DCA-USE-014` checks this; `DCA-CYC-005` keeps the feature (or, in a flat context, use-case)
   packages free of cycles — a one-directional dependency between two features is allowed.
8. **A vertical slice is not a feature.** `{context}/{feature}/{domain,application,adapter}` puts a layer segment
   below the feature, so the structural module discovery rightly treats every slice as a module of its own and the
   isolation rules demand communication through `api`/`events`. If that boundary is what you want, model it as a
   module and ask whether it is a separate bounded context. Do not weaken the isolation rules to let a shared
   aggregate span such slices.

A feature relieves *package pressure*. It is not evidence against splitting a context: when language, model or
team ownership have diverged, split the context — grouping use cases does not resolve that.

---

#### Detailed Structure with All Subdivisions

```
com.company.project
│
├── order (bounded context)
│   ├── domain
│   │   ├── model
│   │   │   ├── Order.java (Aggregate Root)
│   │   │   ├── OrderId.java (Value Object)
│   │   │   ├── OrderLine.java (Entity)
│   │   │   └── OrderStatus.java (Value Object/Enum)
│   │   ├── service
│   │   │   └── PricingService.java (Domain Service)
│   │   └── event
│   │       ├── OrderCreated.java (Domain Event)
│   │       └── OrderCancelled.java (Domain Event)
│   │
│   ├── application (use-case focused - each use case self-contained)
│   │   ├── createorder (use case folder - lowercase, contains ALL related files)
│   │   │   ├── CreateOrderInputPort.java
│   │   │   │   interface CreateOrderInputPort extends UseCase<CreateOrderCommand, CreateOrderResult> {}
│   │   │   ├── CreateOrderUseCase.java
│   │   │   │   @Service class CreateOrderUseCase implements CreateOrderInputPort { }
│   │   │   ├── CreateOrderCommand.java
│   │   │   └── CreateOrderResult.java
│   │   │
│   │   ├── findorder (use case folder - lowercase, contains ALL related files)
│   │   │   ├── FindOrderInputPort.java
│   │   │   │   interface FindOrderInputPort extends UseCase<OrderQuery, OrderResult> {}
│   │   │   ├── FindOrderUseCase.java
│   │   │   │   @Service class FindOrderUseCase implements FindOrderInputPort { }
│   │   │   ├── OrderQuery.java
│   │   │   └── OrderResult.java
│   │   │
│   │   ├── cancelorder (use case folder - lowercase, contains ALL related files)
│   │   │   ├── CancelOrderInputPort.java
│   │   │   │   interface CancelOrderInputPort extends UseCase<CancelOrderCommand, CancelOrderResult> {}
│   │   │   ├── CancelOrderUseCase.java
│   │   │   │   @Service class CancelOrderUseCase implements CancelOrderInputPort { }
│   │   │   ├── CancelOrderCommand.java
│   │   │   └── CancelOrderResult.java
│   │   │
│   │   ├── updateorder (use case folder - lowercase, contains ALL related files)
│   │   │   ├── UpdateOrderInputPort.java
│   │   │   │   interface UpdateOrderInputPort extends UseCase<UpdateOrderCommand, UpdateOrderResult> {}
│   │   │   ├── UpdateOrderUseCase.java
│   │   │   │   @Service class UpdateOrderUseCase implements UpdateOrderInputPort { }
│   │   │   ├── UpdateOrderCommand.java
│   │   │   └── UpdateOrderResult.java
│   │   │
│   │   └── shared (SHARED OUTPUT PORTS - infrastructure dependencies)
│   │       ├── OrderRepository.java (Output Port)
│   │       ├── PaymentGateway.java (Output Port)
│   │       ├── InventoryService.java (Output Port)
│   │       └── DomainEventPublisher.java (Output Port)
│   │
│   └── adapter
│       ├── incoming (INCOMING ADAPTERS - call input ports)
│       │   ├── web
│       │   │   ├── OrderPageController.java
│       │   │   ├── dto
│       │   │   │   ├── CreateOrderWebRequest.java
│       │   │   │   └── OrderWebResponse.java
│       │   │   └── mapper
│       │   │       └── OrderWebMapper.java
│       │   ├── api
│       │   │   └── OrderRestController.java
│       │   ├── event
│       │   │   ├── OrderEventConsumer.java
│       │   │   ├── dto
│       │   │   │   └── ExternalOrderEvent.java
│       │   │   └── acl
│       │   │       └── ExternalEventToCommandMapper.java
│       │   └── mcp
│       │       └── OrderMcpToolProvider.java (Model Context Protocol)
│       │
│       └── outgoing (OUTGOING ADAPTERS - implement output ports)
│           ├── persistence
│           │   ├── InMemoryOrderRepository.java (implements OrderRepository)
│           │   └── SampleDataInitializer.java (Optional: for demo data)
│           │   # Note: For production, add JPA/JDBC adapters as needed
│           ├── payment
│           │   ├── PaymentGatewayAdapter.java (implements PaymentGateway)
│           │   └── dto
│           │       └── PaymentRequest.java
│           ├── inventory
│           │   └── InventoryServiceAdapter.java (implements InventoryService)
│           └── messaging
│               ├── DomainEventPublisherAdapter.java (implements DomainEventPublisher)
│               ├── event
│               │   ├── OrderCreatedEvent.java (Integration Event DTO)
│               │   └── OrderCancelledEvent.java (Integration Event DTO)
│               └── mapper
│                   └── OrderEventMapper.java
│
├── customer (bounded context)
│   ├── domain
│   ├── application
│   │   ├── registercustomer
│   │   │   ├── RegisterCustomerInputPort.java
│   │   │   ├── RegisterCustomerUseCase.java
│   │   │   ├── RegisterCustomerCommand.java
│   │   │   └── RegisterCustomerResult.java
│   │   ├── updatecustomer
│   │   │   ├── UpdateCustomerInputPort.java
│   │   │   ├── UpdateCustomerUseCase.java
│   │   │   ├── UpdateCustomerCommand.java
│   │   │   └── UpdateCustomerResult.java
│   │   ├── findcustomer
│   │   │   ├── FindCustomerInputPort.java
│   │   │   ├── FindCustomerUseCase.java
│   │   │   ├── CustomerQuery.java
│   │   │   └── CustomerResult.java
│   │   └── shared
│   │       ├── CustomerRepository.java
│   │       └── EmailService.java
│   └── adapter
│       ├── incoming
│       └── outgoing
│
├── inventory (bounded context)
│   ├── domain
│   ├── application
│   │   ├── reservestock
│   │   │   ├── ReserveStockInputPort.java
│   │   │   ├── ReserveStockUseCase.java
│   │   │   ├── ReserveStockCommand.java
│   │   │   └── ReserveStockResult.java
│   │   ├── releasestock
│   │   │   ├── ReleaseStockInputPort.java
│   │   │   ├── ReleaseStockUseCase.java
│   │   │   ├── ReleaseStockCommand.java
│   │   │   └── ReleaseStockResult.java
│   │   ├── checkavailability
│   │   │   ├── CheckAvailabilityInputPort.java
│   │   │   ├── CheckAvailabilityUseCase.java
│   │   │   ├── AvailabilityQuery.java
│   │   │   └── AvailabilityResult.java
│   │   └── shared
│   │       └── StockRepository.java
│   └── adapter
│       ├── incoming
│       └── outgoing
│
├── sharedkernel (Shared across ALL bounded contexts - keep minimal)
│   ├── marker (All architectural markers consolidated)
│   │   ├── tactical (DDD tactical patterns)
│   │   │   ├── Id.java
│   │   │   │   public interface Id {}  // Base for typed identifiers
│   │   │   ├── Entity.java
│   │   │   │   public interface Entity<T extends Entity<T, ID>, ID extends Id> { ID id(); }
│   │   │   ├── Value.java
│   │   │   │   public interface Value {}  // Marker for value objects
│   │   │   ├── AggregateRoot.java
│   │   │   │   public interface AggregateRoot<T extends AggregateRoot<T, ID>, ID extends Id> extends Entity<T, ID> {}
│   │   │   ├── BaseAggregateRoot.java
│   │   │   │   public abstract class BaseAggregateRoot<T extends AggregateRoot<T, ID>, ID extends Id> implements AggregateRoot<T, ID> {}
│   │   │   ├── DomainEvent.java
│   │   │   │   public interface DomainEvent { UUID eventId(); Instant occurredOn(); }
│   │   │   ├── IntegrationEvent.java
│   │   │   │   public interface IntegrationEvent { UUID eventId(); Instant occurredOn(); }
│   │   │   ├── IntegrationEventType.java
│   │   │   │   @interface IntegrationEventType { String name(); int version() default 1; }  // contract identity as class property
│   │   │   ├── DomainService.java
│   │   │   │   public interface DomainService {}
│   │   │   ├── Factory.java
│   │   │   │   public interface Factory<T> {}
│   │   │   └── Specification.java
│   │   │       public interface Specification<T> { boolean isSatisfiedBy(T t); }
│   │   ├── strategic (DDD strategic patterns)
│   │   │   ├── SharedKernel.java      // Package annotation
│   │   │   ├── BoundedContext.java    // Package annotation
│   │   │   └── OpenHostService.java   // Marker for OHS adapters
│   │   └── port (Hexagonal architecture ports)
│   │       ├── in (Input ports - driving adapters)
│   │       │   ├── InputPort.java     // Marker for all input ports
│   │       │   └── UseCase.java
│   │       │       public interface UseCase<INPUT, OUTPUT> extends InputPort {
│   │       │         OUTPUT execute(INPUT input);
│   │       │       }
│   │       └── out (Output ports - driven adapters)
│   │           ├── OutputPort.java    // Marker for all output ports
│   │           ├── Repository.java
│   │           │   public interface Repository<T extends AggregateRoot<T, ID>, ID extends Id> extends OutputPort {}
│   │           ├── DomainEventPublisher.java
│   │           │   public interface DomainEventPublisher extends OutputPort {
│   │           │     void publish(DomainEvent event);
│   │           │   }
│   │           ├── IntegrationEventPublisher.java
│   │           │   public interface IntegrationEventPublisher extends OutputPort {
│   │           │     void publish(IntegrationEvent event);  // boundary-crossing facts
│   │           │   }
│   ├── application
│   │   └── TransactionBoundary.java   // execution abstraction, NOT a port
│   │       public interface TransactionBoundary {
│   │         <T> T inTransaction(Supplier<T> work);  // explicit transaction boundary
│   │       }
│   └── domain
│       ├── model (Universal value objects)
│       │   ├── Money.java
│       │   ├── Price.java
│       │   ├── ProductId.java  // Shared product identifier
│       │   └── UserId.java     // Shared user identifier
│       └── specification (Specification pattern implementations)
│           ├── CompositeSpecification.java
│           ├── AndSpecification.java
│           ├── OrSpecification.java
│           ├── NotSpecification.java
│           └── SpecificationVisitor.java
│
└── infrastructure (cross-cutting concerns)
    ├── configuration
    │   ├── SpringBootApplication.java
    │   ├── DependencyInjectionConfig.java
    │   ├── WebConfig.java
    │   ├── SecurityConfig.java
    │   └── JpaConfig.java
    ├── persistence
    │   └── DatabaseMigration.java
    ├── messaging
    │   └── KafkaConfig.java
    └── monitoring
        ├── LoggingConfig.java
        └── MetricsConfig.java
```

---

### Structure Evolution Example: From Startup to Maturity

This example shows how a bounded context's structure naturally evolves as complexity grows. For detailed progressive complexity guidelines, see the original structure above.

---

**Use Case Organization - Self-Contained Pattern:**

```
APPLICATION LAYER
├── createorder/                   (USE CASE - All related files together)
│   ├── CreateOrderInputPort.java      ← Input Port Interface
│   │   interface CreateOrderInputPort extends UseCase<CreateOrderCommand, CreateOrderResult>
│   ├── CreateOrderUseCase.java        ← Use Case Implementation
│   │   @Service class CreateOrderUseCase implements CreateOrderInputPort
│   ├── CreateOrderCommand.java        ← Input Model (Command for writes)
│   └── CreateOrderResult.java       ← Output Model
│
├── findorder/                     (USE CASE - All related files together)
│   ├── FindOrderInputPort.java        ← Input Port Interface
│   ├── FindOrderUseCase.java          ← Use Case Implementation
│   ├── OrderQuery.java                ← Input Model (Query for reads)
│   └── OrderResult.java             ← Output Model
│
├── cancelorder/                   (USE CASE - All related files together)
│   ├── CancelOrderInputPort.java      ← Input Port Interface
│   ├── CancelOrderUseCase.java        ← Use Case Implementation
│   ├── CancelOrderCommand.java        ← Input Model
│   └── CancelOrderResult.java       ← Output Model
│
└── shared/                        (SHARED OUTPUT PORTS)
    ├── OrderRepository.java           ← Output Port (used by multiple use cases)
    ├── PaymentGateway.java            ← Output Port
    ├── InventoryService.java          ← Output Port
    └── DomainEventPublisher.java      ← Output Port
```

**Key Principles:**

1. **Each use case is self-contained** in its own folder with ALL related files
2. **InputPort interface** lives WITH the use case, not in a separate port/in/ directory
3. **UseCase implementation** lives WITH the InputPort in the same folder
4. **Command/Query and Result** models live WITH the use case
5. **Output Ports** (repositories, gateways) are shared across use cases in `shared/` directory

**Naming Convention:**
- **Use Case Folders**: lowercase (e.g., `createorder`, `findorder`, `cancelorder`)
- **Input Ports**: `*InputPort extends UseCase<INPUT, OUTPUT>` (e.g., `CreateOrderInputPort extends UseCase<CreateOrderCommand, CreateOrderResult>`)
- **Output Ports**: Domain-specific names (e.g., `OrderRepository`, `PaymentGateway`, `DomainEventPublisher`)
- **Use Case Implementation**: `*UseCase implements *InputPort` (e.g., `CreateOrderUseCase implements CreateOrderInputPort`)
- **Commands**: `*Command` (e.g., `CreateOrderCommand`)
- **Queries**: `*Query` (e.g., `OrderQuery`)
- **Results**: `*Result` (e.g., `CreateOrderResult`)
- **Adapters**: `*Adapter` or specific suffixes (e.g., `InMemoryOrderRepository`, `OrderPageController`, `OrderMcpToolProvider`)

**Benefits:**
- ✅ **High Cohesion** - All files for one use case are together
- ✅ **Single Responsibility** - One folder = one business operation
- ✅ **Easy Navigation** - Find everything related to a use case in one place
- ✅ **Better Scalability** - Structure grows linearly with use cases
- ✅ **Minimal Coupling** - Use cases are independent, share only via output ports
- ✅ **Clear Dependencies** - Use case depends on domain + shared output ports only
- ✅ **Adapters clearly separated** - `adapter/incoming` and `adapter/outgoing`
- ✅ **Self-documenting** - Folder name = business operation name
- ✅ **Team-friendly** - Different developers can work on different use cases independently

**When the flat list outgrows itself — features:**

```
APPLICATION LAYER (grouped form)
├── ordering/                      (FEATURE - a term of the ubiquitous language)
│   ├── createorder/                   ← use case, unchanged inside
│   ├── updateorder/
│   └── cancelorder/
├── fulfilment/                    (FEATURE)
│   ├── shiporder/
│   └── trackshipment/
├── reporting/                     (FEATURE)
│   └── findorder/
└── shared/                        (CONTEXT-WIDE OUTPUT PORTS - not per feature)
    ├── OrderRepository.java
    └── PaymentGateway.java
```

The use-case packages are untouched by the move — only their parent changes. The domain layer is not
mirrored: `Order` serves `ordering`, `fulfilment` and `reporting` alike. See
[Grouping use cases into features](#grouping-use-cases-into-features) for the rules.

## Related markers

- [TransactionBoundary](/marker/application/transactionboundary.md)
- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@OpenHostService](/marker/strategic/openhostservice.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainService](/marker/tactical/domainservice.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Factory](/marker/tactical/factory.md)
- [Id](/marker/tactical/id.md)
- [IntegrationEvent](/marker/tactical/integrationevent.md)
- [@IntegrationEventType](/marker/tactical/integrationeventtype.md)
- [Specification<T>](/marker/tactical/specification.md)
