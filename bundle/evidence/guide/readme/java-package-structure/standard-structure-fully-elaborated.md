---
type: Reference
title: "JAVA PACKAGE STRUCTURE — Standard Structure (Fully Elaborated)"
tags: [reference]
evidence_for: "/guide/readme/java-package-structure.md#standard-structure-fully-elaborated"
---

[Full node and context](/guide/readme/java-package-structure.md#standard-structure-fully-elaborated). This is an evidence excerpt; retain the parent selection and caveats.

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
│   ├── application/shared/  Application-specific ports shared by several contexts (IdentityProvider)
│   ├── domain/model/        Universal value objects (Money, Address, etc.)
│   └── adapter/outgoing/    Shared adapters only where no library ships them (Spring: dca-spring does)
│
└── infrastructure/          [GLOBAL INFRASTRUCTURE]
                             Application-wide configuration and setup

Architectural markers (AggregateRoot, UseCase, Repository, @BoundedContext, …) are not part of
the application: they come from the dca-building-blocks dependency (see Shared Kernel Pattern).
```

#### .NET Solution Structure

The same shape in C#: **one project per bounded context**, folders for the layers, PascalCase
segments. A context is declared by a marker class in its root namespace (C# has no `package-info`).

```
src/
├── Company.Project.{Context}/        one assembly per bounded context (namespace Company.Project.{Context})
│   ├── {Context}Context.cs           [BoundedContext], [Upstream], [Partnership] — the context declaration
│   ├── Domain/                       Model/, Event/, Service/, Specification/
│   ├── Application/                  {UseCase}/ or {Feature}/{UseCase}/ — I*InputPort, *UseCase, *Command, *Result
│   │   └── Shared/                   output ports, context-wide
│   ├── Adapter/
│   │   ├── Incoming/                 Web/, Api/, Event/ (call input ports)
│   │   └── Outgoing/                 Persistence/, Event/, … (implement output ports)
│   └── Infrastructure/               DI registration: Add{Context}Context()
├── Company.Project.SharedKernel/     [SharedKernel] marker class; Domain/Model, Application/Shared, shared adapters
├── Company.Project.Infrastructure/   composition root, cross-cutting concerns
└── Company.Project.Web/              the host (ASP.NET Core); controllers live in the contexts
tests/
└── Company.Project.ArchitectureTests/   DcaArchitectureTest subclass (Debug build), all context assemblies
```

Building blocks come from `DomainCentric.BuildingBlocks`, the rules from `DomainCentric.ArchRules.Xunit`
— the same rule ids as the Java library. Every rule speaks of namespaces where the Java text says
packages; a project boundary per context is the .NET way of making the module boundary physical.

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

`withOperationContainers("usecases")` (C#: `WithOperationContainers("UseCases")`)
can declare an organisational segment such as `application/usecases/<usecase>`.
Configured segments do not contribute to flat/grouped depth; the operation class's
marker or suffix determines the root. Supporting subfolders are allowed. A context
mixing flat and feature-grouped operations remains invalid after normalization.

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
│   │   // Markers, port interfaces and TransactionBoundary are NOT here — they come from the
│   │   // dca-building-blocks dependency (dev.domaincentric.dca.buildingblocks.ddd.tactical,
│   │   // .ddd.strategic, .hexagonal.port.in/.out, .application). Only application-specific code:
│   ├── application
│   │   └── shared
│   │       └── IdentityProvider.java   // project-specific shared port: extends OutputPort
│   │   // DomainEventPublisher / TransactionBoundary implementations: dca-spring (auto-configured);
│   │   // a non-Spring application writes them under adapter/outgoing/event and infrastructure/transaction
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
