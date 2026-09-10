---
type: Section
title: ELEMENTS
chapter: Domain-Centric Architecture
source: guide
resource: dca-guide/README.md
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

#### Shaping the Result

The rules above fix the *edges* of a result: its name and place (`*Result`, in the use-case package), its
immutability, and that response DTOs and view models belong to the adapter. The *middle* — what a result may
carry, who assembles it and how big it should be — follows seven sentences.

1. **A result carries values, never identities.** Allowed: primitives, nested records, value objects
   (shared kernel included — `Money`, `ProductId`), enriched domain models and read models (`Value` records
   from `domain/model` and `domain/readmodel`). Forbidden: anything assignable to `AggregateRoot` or `Entity`.
   Identity and behaviour stay behind the port; the adapter gets an answer, not a handle on the model.
   Enforced transitively — through nested records, part records and generic arguments (`List<T>`,
   `Optional<T>`, `Map<K,V>`) — by `DCA-USE-015`.
2. **Command results are small.** A command returns ids, status or outcome, and what the caller needs for its
   next step — not the view. The view comes from a query use case or a read model. Returning a whole read model
   from a command is the documented exception (it saves a remote caller a round trip), and then it returns the
   read-model `Value`, never a parade of primitives.
3. **Part records are named by content; `*Result` is the top level only.** `CartItemSummary`, `LineItemData`,
   `ProfileView` — nested in the result they belong to. A part shared by several use cases moves to
   `application/shared`; there is no feature-level `shared`.
4. **The application layer assembles the result — in order of effort.** (a) A static factory `from(...)` on the
   result, parts as records with their own `from`. (b) A projection that needs several ports is orchestration
   and lives in the use-case body. (c) When it grows or several use cases need it, a dedicated **`*Assembler`**
   in the use-case folder or `application/shared`. Never `*Mapper`, `*Converter` (`DCA-NAM-008`), never
   `Helper`.
5. **Large aggregates hand out a snapshot, not a getter parade.** A `Value` record in `domain/readmodel`, built
   by `Snapshot.from(aggregate)` — a value like any other (`DCA-TAC-008`…`DCA-TAC-012`). The snapshot *is* the result field; the use case does not
   flatten it a second time.
6. **The active-domain restriction is asymmetric.** An incoming adapter may read the domain values and read
   models a `Result` delivers and format them for HTTP, HTML, MCP or another transport. It must not inject or
   invoke a domain service (`DCA-HEX-012`), construct aggregates, entities or domain values, or execute domain
   behaviour: it translates external input into a `Command`/`Query` and calls an input port. Outgoing adapters
   are different: a repository or persistence adapter necessarily maps, constructs and reconstitutes domain
   objects while implementing an output port. That mapping may restore state; it must not make new business
   decisions.
7. **One model for every adapter.** Vernon's Domain Payload Object (handing whole aggregates to the UI) and the
   Mediator/double-dispatch rendering are not taken, also for in-process UIs — see
   [Deviations from the literature](#deviations-from-the-literature).

**Snapshot as the result field:**
```java
// domain/readmodel — a Value built from the aggregate, no identity of its own
public record CheckoutCartSnapshot(
        CheckoutSessionId sessionId, CheckoutStep step, CheckoutSessionStatus status,
        List<LineItemSnapshot> lineItems, Money subtotal, @Nullable CheckoutTotals totals,
        @Nullable BuyerInfo buyerInfo, @Nullable DeliveryAddress deliveryAddress)
        implements Value {
    public static CheckoutCartSnapshot from(CheckoutSession session) { /* copies state, no behaviour */ }
}

// application — the query result wraps the snapshot; nothing is flattened again
public record GetCheckoutSessionResult(boolean found, @Nullable CheckoutCartSnapshot session) {
    public static GetCheckoutSessionResult found(CheckoutCartSnapshot session) {
        return new GetCheckoutSessionResult(true, session);
    }
}
```

**Command vs. query sizing:**
```java
// Command: what the caller needs next — the next page asks the query
public record SubmitDeliveryResult(String sessionId, String currentStep, String status) {
    public static SubmitDeliveryResult from(CheckoutSession session) {
        return new SubmitDeliveryResult(
                session.id().value().toString(), session.currentStep().name(), session.status().name());
    }
}

// Query: the read model the page renders
public record GetCheckoutSessionResult(boolean found, @Nullable CheckoutCartSnapshot session) { ... }
```

What an incoming adapter may do with a delivered value or read model: call its **own, parameterless queries**
— `lineTotal()`, `priceDifference()`, `isValidForCheckout()` on an enriched cart are derivations of the
value's own state, and a read model that could not answer them would be no read model. What it must not do:
obtain or invoke a domain service, construct aggregates, entities or domain values, combine values from
several sources into a new business fact, or trigger behaviour with side effects. When a page needs a fact the
read model does not know — the tax contained in a subtotal, whether a checkout step may be opened — that fact
is computed in the use case and delivered in the result. The result is too poor when an adapter has to import
a domain service to render: a page controller that has to decide whether a checkout step may be opened asks
the query for that decision (the use case invokes the domain service and delivers a `StepAccess` value) and
maps the answer to a route.

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

**The building blocks are a dependency, not shared-kernel code.** The architectural markers — tactical
DDD interfaces, strategic annotations and the port hierarchy — are generic: they assign a role and carry
no business method. They ship as a published library, and the shared kernel of an application holds only
what is specific to *that* application:

```kotlin
// build.gradle.kts
dependencies {
    implementation("dev.domaincentric:dca-building-blocks:0.1.2")     // markers, ports, TransactionBoundary
    testImplementation("dev.domaincentric:dca-archunit:0.3.0")        // the rules that select on them
}
```

```xml
<!-- pom.xml -->
<dependency>
  <groupId>dev.domaincentric</groupId>
  <artifactId>dca-building-blocks</artifactId>
  <version>0.1.2</version>
</dependency>
```

```
dotnet add package DomainCentric.BuildingBlocks            # .NET twin: I-prefixed interfaces, attributes, async ports
dotnet add package DomainCentric.ArchRules.Xunit           # same rule ids, xUnit base class
```

What the library defines, by package (Java) and namespace (.NET):

```
dev.domaincentric.dca.buildingblocks            DomainCentric.BuildingBlocks
├── ddd.tactical                                ├── Ddd.Tactical
│   Id, Entity, Value, AggregateRoot,           │   IId, IEntity, IValue, IAggregateRoot,
│   BaseAggregateRoot, DomainEvent,             │   AggregateRootBase, IDomainEvent,
│   IntegrationEvent, @IntegrationEventType,    │   IIntegrationEvent, [IntegrationEventType],
│   DomainService, DomainGateway, Factory,      │   IDomainService, IDomainGateway, IFactory,
│   Specification                               │   ISpecification<T>
├── ddd.strategic                               ├── Ddd.Strategic
│   @BoundedContext (on package-info)           │   [BoundedContext] (on a context marker class)
├── ddd.strategic.relationships                 ├── Ddd.Strategic.Relationships
│   @SharedKernel, @OpenHostService, @Upstream, │   [SharedKernel], [OpenHostService], [Upstream],
│   @ExternalUpstream, @Partnership             │   [ExternalUpstream], [Partnership]
├── hexagonal.port.in                           ├── Hexagonal.Ports.In
│   InputPort, UseCase<INPUT, OUTPUT>           │   IInputPort, IUseCase<TInput, TOutput>
├── hexagonal.port.out                          ├── Hexagonal.Ports.Out
│   OutputPort, Repository<T, ID>, Store,       │   IOutputPort, IRepository<T, TId>, IStore,
│   DomainEventPublisher,                       │   IDomainEventPublisher,
│   IntegrationEventPublisher                   │   IIntegrationEventPublisher
└── application                                 └── Application.Transactions
    TransactionBoundary (execution abstraction,     ITransactionBoundary
    not a port)
```

The rest of this guide names the Java types; the .NET names follow the host language's convention
(`I` prefix, attributes, `Async` suffix) — see [Language Mappings](/guide/language-mappings.md).

**Structure of the application's shared kernel:**
```
sharedkernel/                      # @SharedKernel on package-info.java
├── application/
│   └── shared/                    # Application-specific ports shared by several contexts
│       └── IdentityProvider.java  # e.g. current caller's identity — NOT a generic marker
│
├── domain/
│   ├── model/                     # Universal Value Objects
│   │   ├── Money.java             # Universal money type
│   │   ├── Price.java             # Common price value object
│   │   ├── ProductId.java         # Shared product identifier
│   │   └── UserId.java            # Shared user identifier
│   └── specification/             # Specification Pattern Implementation
│       ├── CompositeSpecification.java
│       ├── AndSpecification.java
│       ├── OrSpecification.java
│       ├── NotSpecification.java
│       └── SpecificationVisitor.java
│
└── (no adapters: the DomainEventPublisher and TransactionBoundary implementations
     come from the dca-spring dependency — see below)
```

**The runtime adapters are a dependency too.** The two ports that every use case needs at runtime —
`DomainEventPublisher` and `TransactionBoundary` — have Spring implementations in
`dev.domaincentric:dca-spring`: `SpringDomainEventPublisher` (over `ApplicationEventPublisher`, dispatch
first, clear afterwards) and `SpringTransactionBoundary` (over `TransactionTemplate`, `REQUIRED`
propagation, nested failures mark the transaction rollback-only), plus an `InMemoryTransactionBoundary`
for tests. A Spring Boot application needs nothing but the dependency: the auto-configuration registers
both beans, the boundary once a `PlatformTransactionManager` exists, and backs off where the application
defines a port itself. An application on another framework writes the two classes in its shared kernel
(`sharedkernel/adapter/outgoing/event/`, `sharedkernel/infrastructure/transaction/`).

```kotlin
implementation("dev.domaincentric:dca-spring:0.1.0")
```

> **The silent failure this guards.** `spring-boot-starter` and `spring-modulith-starter-core` bring no
> transaction manager and not even Boot's `TransactionAutoConfiguration` (it lives in
> `spring-boot-transaction`). In that in-memory starting configuration `@Transactional` compiles and does
> nothing: no proxy, no transaction, and every `@TransactionalEventListener` / `@ApplicationModuleListener`
> is skipped without a log line — while the rules stay green. Until a database arrives, add
> `spring-boot-transaction`, a small `PlatformTransactionManager` bean of your own (deliberately visible
> code, not a library class) and `spring-modulith-events-api` for the listener annotation itself.

**Port Interface Hierarchy** (defined by the library):
```
Input Ports (hexagonal.port.in)      Output Ports (hexagonal.port.out)
┌────────────────────────────┐       ┌─────────────────────────────────┐
│ InputPort (marker)         │       │ OutputPort (marker)             │
│   └── UseCase<INPUT,OUTPUT>│       │   ├── Repository<T, ID>         │
│         └── *InputPort     │       │   ├── Store                     │
└────────────────────────────┘       │   ├── DomainEventPublisher      │
                                     │   └── IntegrationEventPublisher │
                                     └─────────────────────────────────┘
```

Only *generic* contracts are building blocks: interfaces that assign an architectural role and
carry no business methods. A port with domain-specific methods — even one that several bounded
contexts share — is an **application-specific shared port** and belongs in
`sharedkernel/application/shared/`, mirroring the `application/shared/` convention each bounded
context uses for its own ports. The rules and the tooling select on the library's types, so this
separation keeps project concepts out of the reusable building-block set — and a new generic marker
is a contribution to the library, not a file in your shared kernel.

**Example — an application-specific shared port (Identity):**
```java
// In sharedkernel/application/shared/IdentityProvider.java — project-specific, not a marker
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

// In the owning context's adapter/outgoing/security/ - PROJECT-SPECIFIC implementations
public enum JwtIdentityType implements IdentityProvider.IdentityType {
    ANONYMOUS, REGISTERED, SERVICE_ACCOUNT;  // Extensible per project
}

public record JwtIdentity(...) implements IdentityProvider.Identity { ... }
```

**Why the identity port is not a building block.** Its contract returns `UserId` — a value object of
*this* project's shared kernel — and its `IdentityType` encodes *this* shop's two-cookie design (anonymous
visitor vs. registered customer). A reusable marker must carry neither, and a marker only earns its place
once a rule selects on it; every rule about identity that exists today ("the domain never reads the
caller") works over the layer packages alone. So the port is written per project, following the cut below.

**How to cut the identity port:**

1. **One output port, in the shared kernel's `application/shared/`** (or in a single context's
   `application/shared/` if only that context needs it). It extends `OutputPort`, returns an `Identity`
   made of the project's own types, and knows nothing about tokens, cookies or headers.
2. **The implementation is an outgoing adapter of the context that owns authentication** — it reads the
   security context the framework populated (`adapter/outgoing/security/`). Incoming adapters and use cases
   see only the port.
3. **The authentication filter enriches, it never gates.** It attaches an identity or nothing and lets the
   request proceed; every request has an identity (an anonymous visitor is one). Blanket
   "must be authenticated" rules at the token boundary are not where authorization lives.
4. **Ownership goes into the command.** A use case that acts on somebody's resource takes the caller as a
   field — `GetCartByIdQuery(cartId, customerId)`, `StartCheckoutCommand(cartId, customerId)` — and asks the
   repository a *scoped* question (`findByIdForCustomer(cartId, customerId)`) instead of loading by id and
   comparing afterwards. The incoming adapter resolves the caller through the port and fills the field; the
   use case never calls the identity port to find out on whose behalf it runs.
5. **A claims-only gate may stay in the adapter.** "Does this token carry the staff role?" reads nothing but
   the caller's claims and is a property of the *exposure*, so the REST resource or page controller may
   check it and refuse. Anything that needs the resource — is this cart theirs — is a property of the
   *operation* and belongs to the use case, through the command field of step 4.
6. **The domain never sees the caller.** No `User` parameter on an aggregate method, no role check in a
   value object; `cart.checkout()` protects *its* invariants (not empty, not already completed), the use
   case has already answered *who may*.
7. **A use case without a caller says so.** An event consumer completing a cart after a confirmed checkout
   acts on nobody's behalf; leave its command unscoped and document why, or the next reader "fixes" it.

Refusals are decided in the use case and *rendered* in the adapter: whether a stranger's cart answers
`403` or `404` is a protocol choice (a `403` confirms the id exists), and the REST resource makes it.

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

- Exists for **Value Objects, Events, or technical state** without an aggregate lifecycle
- Append-/record-style semantics: `record()`, `count()`, `exists()`, `reset()` — lookup by key is allowed; no aggregate `save()` / `delete()` semantics
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
| Aggregate lifecycle | yes — `save`, `delete` | no — `record`, `count`, `exists`; lookup by key allowed |
| Marker | `extends Repository<T, ID>` | `extends Store` |
| Examples | `CustomerAccountRepository`, `OrderRepository` | `LoginProtectionStore`, `AuditLogStore`, `EventStore` |

**Rules of thumb:**

1. Lookup by key (`findById`) is allowed on a Store too; aggregate lifecycle determines Repository semantics.
2. Need `record()` or `count()`? → Store (the object is recorded, not managed).
3. In doubt: if the stored object is a `Value` or a record, it's almost always a Store.

> **Note on EventStore (Event Sourcing):** The `EventStore` from Event Sourcing is a *specialization* of Store — one specifically for Domain Events that supports aggregate reconstruction. The general `Store` is the broader pattern for any operational data.

> **Note on cross-cutting `*Response` classes:** Generic Response/error classes (`ErrorResponse`, base `Response`, `SimpleResponse`) belong in the **shared kernel's adapter-incoming package**, not in any individual bounded context. ArchUnit rules that check `*Response` placement must include the shared kernel adapter — discover its package dynamically via `@SharedKernel` rather than hardcoding the name (`shared` / `common` / `core` / `sharedkernel`).

**Why the distinction matters:**
The naming is part of the Ubiquitous Language. A reader should know from the interface name alone whether they're dealing with a managed aggregate (Repository) or recorded data (Store) — without opening the implementation. Both are technically Output Ports in hexagonal architecture, but the business role is fundamentally different.

**What Belongs in Shared Kernel:**

✅ **Include:**
- **Universal value objects** used by multiple contexts (Money, Price, shared IDs)
- **Application-specific shared ports** with identical meaning in every context (an `IdentityProvider`)
- **Shared adapters** that implement a library port once for the whole application — on Spring these come from `dca-spring` (`SpringDomainEventPublisher`, `SpringTransactionBoundary`); other frameworks write them here
- **Specification pattern implementations** (CompositeSpecification, And/Or/Not specifications)
- **Cross-cutting domain concepts** that have identical meaning everywhere

📦 **Comes from the dependency, not written here:**
- **DDD marker interfaces** (Entity, AggregateRoot, Value, DomainEvent, …) and **strategic annotations**
- **Base port interfaces** (`UseCase<INPUT, OUTPUT>`, `Repository`, `Store`, `DomainEventPublisher`) and `TransactionBoundary`

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
   ├─ Is it a generic marker or base port (a role, no business method)?
   │     YES → It is a building block: use the library's type, or propose it there
   │     NO ↓
   │
   ├─ Is it a universal value object (Money, Address)?
   │     YES → Add to sharedkernel/domain/model/
   │     NO ↓
   │
   └─ Is it a port with business methods that every context reads the same way?
         YES → Add to sharedkernel/application/shared/
         NO → Probably shouldn't be in Shared Kernel
```

**The tactical markers, as the library defines them:**
```java
// dev.domaincentric.dca.buildingblocks.ddd.tactical — from dca-building-blocks, not written per project
public interface Id {
    // Marker interface - typed identifiers, no type parameter of their own
}

public interface Entity<T extends Entity<T, ID>, ID extends Id> {
    ID id();
    default boolean sameIdentityAs(T other) {
        return other != null && id().equals(other.id());
    }
}

public interface AggregateRoot<T extends AggregateRoot<T, ID>, ID extends Id>
        extends Entity<T, ID> {
    // Marker interface - identifies aggregate roots for all contexts
}
```

```csharp
// DomainCentric.BuildingBlocks.Ddd.Tactical — the same contracts in C#
public interface IId { }
public interface IEntity<TSelf, TId> : IEntity where TSelf : IEntity<TSelf, TId> where TId : IId { TId Id { get; } }
public interface IAggregateRoot<TSelf, TId> : IEntity<TSelf, TId>, IAggregateRoot
    where TSelf : IAggregateRoot<TSelf, TId> where TId : IId { }
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

**The port hierarchy, as the library defines it — and how a context uses it:**
```java
// dev.domaincentric.dca.buildingblocks.hexagonal.port.in
public interface InputPort {
    // Marker interface for all input ports (hexagonal architecture concept)
}

public interface UseCase<INPUT, OUTPUT> extends InputPort {
    OUTPUT execute(INPUT input);
}

// dev.domaincentric.dca.buildingblocks.hexagonal.port.out
public interface OutputPort {
    // Marker interface for all output ports (hexagonal architecture concept)
}

public interface Repository<T extends AggregateRoot<T, ID>, ID extends Id> extends OutputPort {
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

## Related mentions (heuristic)

- [TransactionBoundary](/marker/application/transactionboundary.md)
- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@OpenHostService](/marker/strategic/openhostservice.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
- [@Upstream](/marker/strategic/upstream.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainGateway](/marker/tactical/domaingateway.md)
- [DomainService](/marker/tactical/domainservice.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Factory](/marker/tactical/factory.md)
- [Id](/marker/tactical/id.md)
- [IntegrationEvent](/marker/tactical/integrationevent.md)
- [@IntegrationEventType](/marker/tactical/integrationeventtype.md)
- [Specification<T>](/marker/tactical/specification.md)

## Evidence slices

- [Domain Layer (Enterprise Business Rules)](/evidence/guide/readme/elements/domain-layer-enterprise-business-rules.md)
- [Application Layer (Use Cases / Application Business Rules)](/evidence/guide/readme/elements/application-layer-use-cases-application-business-rules.md)
- [Adapter Layer (Interface Adapters)](/evidence/guide/readme/elements/adapter-layer-interface-adapters.md)
- [Infrastructure Layer (Frameworks & Drivers)](/evidence/guide/readme/elements/infrastructure-layer-frameworks-drivers.md)
- [Strategic Architecture](/evidence/guide/readme/elements/strategic-architecture.md)
- [Repository vs. Store](/evidence/guide/readme/elements/repository-vs-store.md)
