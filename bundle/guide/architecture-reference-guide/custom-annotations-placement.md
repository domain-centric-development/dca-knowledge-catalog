---
type: Section
title: Custom Annotations Placement
chapter: Architecture Reference Guide
source: guide
resource: implementing-domain-centric-architecture/architecture-reference-guide.md
tags: [guide, section]
---

Example: `@AsyncInitialize` annotation (similar to `@PostConstruct`)

### Understanding Shared Kernel Common Layer

Before discussing placement options, it's important to understand the **Shared Kernel** pattern from Domain-Driven Design:

**Shared Kernel** = Code shared across ALL bounded contexts in your application

Within the Shared Kernel, we distinguish between:

1. **`sharedkernel.domain`** - Domain concepts shared across contexts
   - Example: `Money`, `ProductId`, `CustomerId`
   - Represents business concepts needed by multiple contexts

2. **`sharedkernel.common`** - Technical utilities shared across contexts
   - Example: `@AsyncInitialize`, `Clock`, utility interfaces
   - NOT business logic, but cross-cutting technical concerns
   - Framework-agnostic (no Spring, no JPA, pure Java)

3. **`[context].common`** - Context-specific utilities (alternative)
   - Example: `product.common.annotation.ProductLifecycle`
   - Only needed within one bounded context
   - Use when the concern is specific to that context

**Key Difference from "Infrastructure"**:
- `sharedkernel.common` = Accessible by ALL layers, ALL contexts, framework-agnostic
- `infrastructure` = Framework wiring, configuration, Spring beans, NOT accessible by domain/application

**Why this matters for `@AsyncInitialize`**:
- It's NOT a framework annotation (not from Spring/Jakarta)
- It's NOT infrastructure code (no Spring dependencies)
- It IS technical metadata (like `@Nullable`, `@NonNull`)
- It SHOULD be accessible across all contexts and layers
- Therefore → belongs in `sharedkernel.common.annotation`

### Option 1: Infrastructure Only (If only adapters/infrastructure need it)

```
infrastructure/
├── annotations/
│   └── AsyncInitialize.java              ← Annotation definition
└── lifecycle/
    └── AsyncInitializationProcessor.java  ← Processor implementation
```

**Use case**: Only adapters and infrastructure components need async initialization

**Limitation**: Application layer cannot use it (would violate dependency rules)

### Option 2: Shared Kernel (Recommended - DDD Pattern)

**For cross-context concerns** (used by multiple bounded contexts):

```
sharedkernel/
└── common/
    └── annotation/
        └── AsyncInitialize.java              ← Annotation definition

infrastructure/
└── config/
    └── AsyncInitializationProcessor.java     ← Processor implementation
```

**For context-specific concerns** (used by single bounded context only):

```
product/                                       ← One bounded context
└── common/
    └── annotation/
        └── ProductLifecycle.java              ← Context-specific annotation

infrastructure/
└── config/
    └── ProductLifecycleProcessor.java         ← Processor implementation
```

**Dependency flow**:
```
Domain (no deps)
  ↑
Application (depends on sharedkernel)
  ↑
Adapters (depends on sharedkernel)
  ↑
Infrastructure (depends on sharedkernel, processes annotation)
```

**Benefits**:
- Application layer can use it (accessible from any layer)
- Still framework-agnostic (pure Java metadata, no framework dependencies)
- Infrastructure provides the processing logic (follows DIP)
- Portable across frameworks (annotation definition is framework-independent)
- Follows DDD Shared Kernel pattern (shared across bounded contexts)
- Clear distinction between shared vs context-specific concerns

### Implementation Example

**The Annotation** (in shared kernel):
```java
// sharedkernel/common/annotation/AsyncInitialize.java
package de.yourapp.sharedkernel.common.annotation;

import java.lang.annotation.*;

/**
 * Marks a method to be called asynchronously after bean initialization.
 *
 * <p>This is a <b>custom, framework-agnostic</b> annotation (NOT from Spring/Jakarta).
 * It belongs in the Shared Kernel because it's a technical concern used across
 * multiple bounded contexts (Product, Cart, Order, etc.).
 *
 * <p>Similar to @PostConstruct but executes in a separate thread pool.
 * The annotation itself has NO framework dependencies - it's pure Java metadata.
 * The processing logic resides in Infrastructure layer using Spring's BeanPostProcessor.
 *
 * <p><b>Why Shared Kernel?</b>
 * <ul>
 *   <li>Framework-agnostic (no Spring, no Jakarta, pure Java)</li>
 *   <li>Accessible by all layers (domain, application, adapters)</li>
 *   <li>Shared across all bounded contexts</li>
 *   <li>Technical concern, not business logic</li>
 * </ul>
 *
 * @see de.yourapp.infrastructure.config.AsyncInitializationProcessor
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface AsyncInitialize {

    /**
     * Order of execution (lower values first).
     * Useful when multiple async initializations have dependencies.
     */
    int order() default 0;

    /**
     * Timeout in milliseconds for the initialization task.
     */
    long timeout() default 30000;
}
```

**The Processor** (in infrastructure):
```java
// infrastructure/config/AsyncInitializationProcessor.java
package de.yourapp.infrastructure.config;

import de.yourapp.sharedkernel.common.annotation.AsyncInitialize;  // ← From shared kernel!
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.core.task.TaskExecutor;
import org.springframework.stereotype.Component;

import java.lang.reflect.Method;
import java.util.concurrent.CompletableFuture;

/**
 * Infrastructure processor that IMPLEMENTS the behavior for @AsyncInitialize.
 *
 * <p>This is where the framework-specific code lives (Spring BeanPostProcessor).
 * The annotation itself (in sharedkernel) is framework-agnostic.
 *
 * <p><b>Separation of Concerns:</b>
 * <ul>
 *   <li>Annotation definition: sharedkernel.common.annotation (pure Java)</li>
 *   <li>Annotation processing: infrastructure.config (Spring-specific)</li>
 * </ul>
 */
@Component
public class AsyncInitializationProcessor implements BeanPostProcessor {

    private final TaskExecutor taskExecutor;

    public AsyncInitializationProcessor(TaskExecutor taskExecutor) {
        this.taskExecutor = taskExecutor;
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName)
            throws BeansException {

        Class<?> clazz = bean.getClass();
        for (Method method : clazz.getDeclaredMethods()) {
            if (method.isAnnotationPresent(AsyncInitialize.class)) {
                AsyncInitialize annotation = method.getAnnotation(AsyncInitialize.class);

                CompletableFuture.runAsync(() -> {
                    try {
                        method.setAccessible(true);
                        method.invoke(bean);
                    } catch (Exception e) {
                        throw new RuntimeException(
                            "Failed to execute @AsyncInitialize on " + beanName, e);
                    }
                }, taskExecutor);
            }
        }
        return bean;
    }
}
```

**Configuration** (in infrastructure):
```java
// infrastructure/configuration/AsyncConfig.java
@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean
    public TaskExecutor asyncInitializationExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(5);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-init-");
        executor.initialize();
        return executor;
    }
}
```

**Usage Examples**:

**Example 1: Shared Kernel Annotation (Cross-Context)**

When an annotation is needed by MULTIPLE bounded contexts, place it in `sharedkernel.common.annotation`:

```java
// ============ PRODUCT CONTEXT ============

// product/application/service/ProductQueryService.java
package de.yourapp.product.application.service;

import de.yourapp.sharedkernel.common.annotation.AsyncInitialize;  // ← Shared!
import org.springframework.stereotype.Service;

@Service
public class ProductQueryService {
    private ProductCache productCache;

    @AsyncInitialize(order = 1)  // ✅ OK - from sharedkernel
    public void warmupProductCache() {
        this.productCache = preloadPopularProducts();
    }
}

// ============ CART CONTEXT ============

// cart/application/service/CartService.java
package de.yourapp.cart.application.service;

import de.yourapp.sharedkernel.common.annotation.AsyncInitialize;  // ← Same annotation!
import org.springframework.stereotype.Service;

@Service
public class CartService {
    private PricingRules pricingRules;

    @AsyncInitialize(order = 2)  // ✅ OK - from sharedkernel
    public void preloadPricingRules() {
        this.pricingRules = loadComplexPricingRules();
    }
}

// ============ ORDER CONTEXT ============

// order/adapter/outgoing/persistence/OrderRepository.java
package de.yourapp.order.adapter.outgoing.persistence;

import de.yourapp.sharedkernel.common.annotation.AsyncInitialize;  // ← All contexts use it!
import org.springframework.stereotype.Repository;

@Repository
public class JpaOrderRepository implements OrderRepository {
    private Cache<OrderId, Order> cache;

    @AsyncInitialize(order = 3)  // ✅ OK - from sharedkernel
    public void warmupOrderCache() {
        this.cache = preloadRecentOrders();
    }
}
```

**Example 2: Context-Specific Annotation (Single Context)**

When an annotation is ONLY needed by ONE bounded context, place it in that context's `common` package:

```java
// product/common/annotation/ProductLifecycle.java
package de.yourapp.product.common.annotation;

import java.lang.annotation.*;

/**
 * Product-specific lifecycle annotation.
 * Only used within the Product bounded context.
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface ProductLifecycle {
    String phase();
}

// product/application/service/ProductService.java
package de.yourapp.product.application.service;

import de.yourapp.product.common.annotation.ProductLifecycle;  // ← Context-specific!
import org.springframework.stereotype.Service;

@Service
public class ProductService {

    @ProductLifecycle(phase = "catalog-refresh")  // ✅ Only used in Product context
    public void refreshProductCatalog() {
        // Product-specific initialization
    }
}
```

**Key Differences:**

| Aspect | Shared Kernel | Context-Specific |
|--------|---------------|------------------|
| **Location** | `sharedkernel.common.annotation` | `[context].common.annotation` |
| **Usage** | Multiple bounded contexts | Single bounded context |
| **Example** | `@AsyncInitialize`, `@Nullable` | `@ProductLifecycle`, `@CartRule` |
| **Accessibility** | All contexts, all layers | Only that context |
| **When to use** | Cross-cutting technical concern | Context-specific technical concern |
```

### Decision Matrix

| Factor | Infrastructure Only | Shared Kernel | Context-Specific |
|--------|-------------------|---------------|------------------|
| **Application needs it?** | ❌ No | ✅ Yes | ✅ Yes (within context) |
| **Multiple contexts need it?** | N/A | ✅ Yes | ❌ No |
| **Dependency complexity** | ✅ Simpler | ⚠️ Adds sharedkernel | ⚠️ Adds context.common |
| **Framework independence** | ⚠️ Less portable | ✅ Fully portable | ✅ Portable within context |
| **DDD compliance** | ⚠️ Not DDD pattern | ✅ Shared Kernel pattern | ✅ Context boundary |
| **Clean Architecture compliance** | Only if unused in app | ✅ Full compliance | ✅ Full compliance |
| **Recommended for** | Infra/adapter-only | Cross-context concerns | Single-context concerns |
| **Examples** | `@Internal` | `@AsyncInitialize`, `@Nullable` | `@ProductLifecycle` |

### Recommendation

**Use Shared Kernel approach** for annotations like `@AsyncInitialize` when:
1. ✅ Needed by multiple bounded contexts (Product, Cart, Order)
2. ✅ Used across multiple layers (application, adapters, infrastructure)
3. ✅ Framework-agnostic (pure Java metadata, no Spring/Jakarta)
4. ✅ Technical concern, not business logic
5. ✅ Follows DDD Shared Kernel pattern

**Use Context-Specific approach** when:
1. ✅ Only ONE bounded context needs it
2. ✅ Business rules specific to that context
3. ✅ Not shared across contexts

**Avoid Infrastructure approach** for application-layer concerns because:
1. ❌ Violates dependency rules (application can't depend on infrastructure)
2. ❌ Limits flexibility (only adapters can use it)
3. ❌ Doesn't follow Clean Architecture principles

---

## Common Patterns

### Pattern 1: Domain Event Publishing

**Domain events flow**:

```java
// 1. Domain - The event (data)
// domain/events/OrderPlaced.java
public class OrderPlaced implements DomainEvent {
    private final OrderId orderId;
    private final CustomerId customerId;
    private final Instant occurredAt;

    // Constructor, getters
}

// 2. Domain - Aggregate collects events
// domain/model/Order.java
public class Order {
    private List<DomainEvent> uncommittedEvents = new ArrayList<>();

    public static Order create(CustomerId customerId, List<OrderLine> lines) {
        Order order = new Order(/* ... */);
        order.uncommittedEvents.add(new OrderPlaced(order.getId(), customerId));
        return order;
    }

    public List<DomainEvent> getUncommittedEvents() {
        return List.copyOf(uncommittedEvents);
    }

    public void clearEvents() {
        uncommittedEvents.clear();
    }
}

// 3. Application - Port for publishing
// application/ports/out/DomainEventPublisher.java
public interface DomainEventPublisher {
    void publish(DomainEvent event);
    void publishAll(List<DomainEvent> events);
}

// 4. Application - Service uses publisher
// application/services/CreateOrderService.java
public class CreateOrderService implements CreateOrderUseCase {
    private final OrderRepository repository;
    private final DomainEventPublisher eventPublisher;

    @Override
    public OrderId execute(CreateOrderCommand command) {
        Order order = Order.create(command.customerId(), command.lines());
        repository.save(order);

        // Publish collected events
        eventPublisher.publishAll(order.getUncommittedEvents());
        order.clearEvents();

        return order.getId();
    }
}

// 5. Adapter - Implementation
// adapters/out/messaging/KafkaEventPublisher.java
@Component
public class KafkaEventPublisher implements DomainEventPublisher {
    private final KafkaTemplate<String, String> kafka;

    @Override
    public void publish(DomainEvent event) {
        kafka.send("domain-events", serialize(event));
    }

    @Override
    public void publishAll(List<DomainEvent> events) {
        events.forEach(this::publish);
    }
}
```

### Pattern 2: Query Separation (CQRS Light)

```java
// Separate read and write models

// application/ports/in/commands/
public interface CreateOrderUseCase {
    OrderId execute(CreateOrderCommand command);
}

// application/ports/in/queries/
public interface GetOrderQuery {
    OrderDto execute(OrderId orderId);
}

// application/services/
public class OrderCommandService implements CreateOrderUseCase {
    // Write operations
}

public class OrderQueryService implements GetOrderQuery {
    // Read operations - can use different repositories
}
```

### Pattern 3: Repository with Separate Persistence Model

```java
// Domain model
// domain/model/Order.java
public class Order {
    private OrderId id;
    private CustomerId customerId;
    private Money totalAmount;

    // Rich domain behavior
    public void addLine(OrderLine line) { }
    public void cancel() { }
}

// Persistence model
// adapters/out/persistence/OrderEntity.java
@Entity
@Table(name = "orders")
public class OrderEntity {
    @Id
    private Long id;
    private String customerId;
    private BigDecimal totalAmount;
    private String currency;

    // Mapping logic
    public Order toDomain() {
        return new Order(
            new OrderId(id),
            new CustomerId(customerId),
            new Money(totalAmount, Currency.getInstance(currency))
        );
    }

    public static OrderEntity fromDomain(Order order) {
        OrderEntity entity = new OrderEntity();
        entity.id = order.getId().getValue();
        entity.customerId = order.getCustomerId().getValue();
        entity.totalAmount = order.getTotalAmount().getAmount();
        entity.currency = order.getTotalAmount().getCurrency().getCurrencyCode();
        return entity;
    }
}

// Repository adapter
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

### Pattern 4: Exception Handling Across Layers

```java
// Domain exceptions
// domain/exceptions/InvalidOrderException.java
public class InvalidOrderException extends RuntimeException {
    public InvalidOrderException(String message) {
        super(message);
    }
}

// Application exceptions
// application/exceptions/OrderNotFoundException.java
public class OrderNotFoundException extends RuntimeException {
    public OrderNotFoundException(OrderId id) {
        super("Order not found: " + id);
    }
}

// Adapter exception handling
// adapters/in/web/GlobalExceptionHandler.java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(OrderNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handle(OrderNotFoundException ex) {
        return new ErrorResponse(ex.getMessage());
    }

    @ExceptionHandler(InvalidOrderException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handle(InvalidOrderException ex) {
        return new ErrorResponse(ex.getMessage());
    }
}
```

---

## ArchUnit Governance

### Automated Architecture Testing

**ArchUnit** is a Java library that allows you to enforce architectural rules through automated tests. It helps prevent architectural violations and ensures consistency as your codebase evolves.

**Key Benefits:**
- ✅ **Continuous Validation** - Architecture rules verified on every build
- ✅ **Early Detection** - Catch violations before code review
- ✅ **Living Documentation** - Architecture rules as executable tests
- ✅ **Team Alignment** - Explicit, enforceable architectural guidelines

### Essential ArchUnit Rules for Domain-Centric Architecture

#### 1. Layer Dependency Rules

```java
@ArchTest
static final ArchRule domain_should_not_depend_on_any_layer =
    noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat()
            .resideInAnyPackage("..application..", "..adapter..", "..infrastructure..")
        .because("Domain must be independent of outer layers");

@ArchTest
static final ArchRule application_should_not_depend_on_adapters =
    noClasses()
        .that().resideInAPackage("..application..")
        .should().dependOnClassesThat()
            .resideInAnyPackage("..adapter..", "..infrastructure..")
        .because("Application should only depend on domain");

@ArchTest
static final ArchRule adapters_should_not_depend_on_infrastructure =
    noClasses()
        .that().resideInAPackage("..adapter..")
        .should().dependOnClassesThat()
            .resideInPackage("..infrastructure..")
        .because("Adapters should not depend on infrastructure layer");
```

#### 2. Framework Independence Rules

```java
@ArchTest
static final ArchRule domain_should_be_framework_agnostic =
    noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat()
            .resideInAnyPackage("org.springframework..", "jakarta.persistence..", "javax.persistence..")
        .because("Domain must be framework-agnostic");

@ArchTest
static final ArchRule domain_should_not_use_jpa_annotations =
    noFields()
        .that().areDeclaredInClassesThat().resideInAPackage("..domain..")
        .should().beAnnotatedWith("jakarta.persistence.Entity")
        .orShould().beAnnotatedWith("jakarta.persistence.Id")
        .orShould().beAnnotatedWith("jakarta.persistence.Column")
        .because("Domain should not use JPA annotations - use separate persistence model");

@ArchTest
static final ArchRule application_should_be_framework_agnostic =
    noClasses()
        .that().resideInAPackage("..application..")
        .should().dependOnClassesThat()
            .resideInAnyPackage("org.springframework.web..", "jakarta.ws.rs..")
        .because("Application layer should not depend on web frameworks");
```

#### 3. DDD Pattern Rules

```java
@ArchTest
static final ArchRule aggregates_should_implement_aggregate_root =
    classes()
        .that().haveSimpleNameEndingWith("Aggregate")
        .or().areAnnotatedWith(Aggregate.class)
        .should().implement(AggregateRoot.class)
        .because("Aggregates must implement AggregateRoot marker interface");

@ArchTest
static final ArchRule value_objects_should_be_immutable =
    classes()
        .that().implement(Value.class)
        .should().haveOnlyFinalFields()
        .because("Value Objects must be immutable");

@ArchTest
static final ArchRule entities_should_have_identity =
    classes()
        .that().implement(Entity.class)
        .should().haveMethod("getId")
        .because("Entities must have identity");

@ArchTest
static final ArchRule domain_events_should_be_immutable =
    classes()
        .that().implement(DomainEvent.class)
        .should().haveOnlyFinalFields()
        .because("Domain Events must be immutable");
```

#### 4. Naming Convention Rules

```java
@ArchTest
static final ArchRule input_ports_should_have_correct_suffix =
    classes()
        .that().resideInAPackage("..application..port.in..")
        .or().resideInAPackage("..application..*..")
            .and().areInterfaces()
            .and().arePublic()
        .should().haveSimpleNameEndingWith("InputPort")
        .orShould().haveSimpleNameEndingWith("UseCase")
        .orShould().haveSimpleNameEndingWith("Query")
        .because("Input ports should follow naming conventions");

@ArchTest
static final ArchRule use_case_implementations_should_have_suffix =
    classes()
        .that().resideInAPackage("..application..usecase..")
        .or().implement(InputPort.class)
        .should().haveSimpleNameEndingWith("UseCase")
        .orShould().haveSimpleNameEndingWith("Service")
        .because("Use case implementations should follow naming conventions");

@ArchTest
static final ArchRule repositories_should_have_correct_suffix =
    classes()
        .that().areAssignableTo(Repository.class)
        .should().haveSimpleNameEndingWith("Repository")
        .because("Repositories should end with 'Repository'");
```

#### 5. Port and Adapter Rules

```java
@ArchTest
static final ArchRule input_ports_should_be_interfaces =
    classes()
        .that().resideInAPackage("..application..port.in..")
        .should().beInterfaces()
        .because("Input ports must be interfaces");

@ArchTest
static final ArchRule output_ports_should_be_interfaces =
    classes()
        .that().resideInAPackage("..application..port.out..")
        .or().resideInAPackage("..application..shared..")
        .should().beInterfaces()
        .because("Output ports must be interfaces");

@ArchTest
static final ArchRule input_adapters_should_not_be_accessed_by_output_adapters =
    noClasses()
        .that().resideInAPackage("..adapter.outgoing..")
        .should().dependOnClassesThat()
            .resideInPackage("..adapter.incoming..")
        .because("Adapters should not depend on each other");
```

#### 6. Shared Kernel Rules

```java
@ArchTest
static final ArchRule shared_kernel_should_have_no_dependencies =
    noClasses()
        .that().resideInAPackage("..sharedkernel..")
        .should().dependOnClassesThat()
            .resideInAnyPackage("..domain..", "..application..", "..adapter..", "..infrastructure..")
        .because("Shared Kernel must be independent - no dependencies on contexts");

@ArchTest
static final ArchRule shared_kernel_should_not_use_frameworks =
    noClasses()
        .that().resideInAPackage("..sharedkernel..")
        .should().dependOnClassesThat()
            .resideInAnyPackage("org.springframework..", "jakarta..", "javax..")
        .because("Shared Kernel must be framework-agnostic");
```

### Complete Test Suite Example

```java
package com.company.project.architecture;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;
import static com.tngtech.archunit.library.Architectures.layeredArchitecture;

/**
 * Architecture tests enforcing Domain-Centric Architecture rules.
 *
 * These tests verify:
 * - Layer dependencies (inward only)
 * - Framework independence (domain/application)
 * - DDD patterns (aggregates, value objects, events)
 * - Naming conventions
 * - Port/Adapter patterns
 */
@AnalyzeClasses(packages = "com.company.project", importOptions = ImportOption.DoNotIncludeTests.class)
public class DomainCentricArchitectureTest {

    // Layer Dependency Tests
    @ArchTest
    static final ArchRule layered_architecture_is_respected =
        layeredArchitecture()
            .consideringAllDependencies()
            .layer("Domain").definedBy("..domain..")
            .layer("Application").definedBy("..application..")
            .layer("Adapter").definedBy("..adapter..")
            .layer("Infrastructure").definedBy("..infrastructure..")

            .whereLayer("Domain").mayNotAccessAnyLayer()
            .whereLayer("Application").mayOnlyAccessLayers("Domain")
            .whereLayer("Adapter").mayOnlyAccessLayers("Application", "Domain")
            .whereLayer("Infrastructure").mayAccessAnyLayer()

            .because("Dependencies must point inward toward domain");

    // Framework Independence Tests
    @ArchTest
    static final ArchRule domain_is_framework_independent =
        noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
                .resideInAnyPackage(
                    "org.springframework..",
                    "jakarta.persistence..",
                    "javax.persistence..",
                    "org.hibernate.."
                )
            .because("Domain must be framework-agnostic");

    // DDD Pattern Tests
    @ArchTest
    static final ArchRule value_objects_are_immutable =
        classes()
            .that().implement(Value.class)
            .should().haveOnlyFinalFields()
            .because("Value Objects must be immutable");

    @ArchTest
    static final ArchRule domain_events_are_immutable =
        classes()
            .that().implement(DomainEvent.class)
            .should().haveOnlyFinalFields()
            .because("Domain Events must be immutable");

    // Port/Adapter Tests
    @ArchTest
    static final ArchRule input_ports_are_interfaces =
        classes()
            .that().resideInAPackage("..application..port.in..")
            .or().haveSimpleNameEndingWith("InputPort")
            .should().beInterfaces()
            .because("Input ports must be interfaces");

    @ArchTest
    static final ArchRule output_ports_are_interfaces =
        classes()
            .that().resideInAPackage("..application..port.out..")
            .or().resideInAPackage("..application..shared..")
            .and().areNotRecords()
            .should().beInterfaces()
            .because("Output ports must be interfaces");
}
```

### Running ArchUnit Tests

**Maven Configuration:**
```xml
<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit-junit5</artifactId>
    <version>1.2.1</version>
    <scope>test</scope>
</dependency>
```

**Gradle Configuration:**
```gradle
testImplementation 'com.tngtech.archunit:archunit-junit5:1.2.1'
```

**Execution:**
- Tests run automatically with your regular test suite
- Failures indicate architectural violations
- Can be integrated into CI/CD pipeline
- Acts as architectural guardrails

### Benefits in Practice

1. **Prevents Drift** - Architecture stays aligned with principles over time
2. **Onboarding** - New developers learn rules through failing tests
3. **Refactoring Safety** - Catch accidental violations during restructuring
4. **Documentation** - Rules are executable and always up-to-date
5. **Code Review** - Automated checks reduce manual review burden

---

## Quick Reference Tables

### Where Things Live

| Component | Layer | Example |
|-----------|-------|---------|
| Entities, Value Objects | Domain | `Order`, `OrderId`, `Money` |
| Domain Events (objects) | Domain | `OrderPlaced`, `OrderCancelled` |
| Domain Services | Domain | `PricingService` |
| Use Case Interfaces | Application | `CreateOrderUseCase` |
| Use Case Implementations | Application | `CreateOrderService` |
| Outbound Port Interfaces | Application | `OrderRepository`, `DomainEventPublisher` |
| Commands, Queries | Application | `CreateOrderCommand`, `OrderQuery` |
| REST Controllers | Adapters (in) | `OrderRestController` |
| CLI Handlers | Adapters (in) | `OrderCliHandler` |
| Message Listeners | Adapters (in) | `OrderCommandListener` |
| JPA Repositories | Adapters (out) | `JpaOrderRepository` |
| JPA Entities | Adapters (out) | `OrderEntity` |
| Message Publishers | Adapters (out) | `KafkaEventPublisher` |
| External API Clients | Adapters (out) | `PaymentGatewayClient` |
| Spring Configuration | Infrastructure | `BeansConfiguration` |
| Framework Processors | Infrastructure | `AsyncInitializationProcessor` |
| Custom Annotations | Shared Kernel | `@AsyncInitialize` (in sharedkernel.common.annotation) |

### Dependency Matrix Quick Reference

```
Layer          | Depends On
---------------+--------------------------------------------
Domain         | (Nothing or Shared Kernel domain concepts)
Application    | Domain, Shared Kernel
Adapters       | Application, Domain, External libs, Shared Kernel
Infrastructure | ALL
Shared Kernel  | (Nothing - framework-independent)
```

### Port Implementation Quick Reference

```
Port Type  | Interface Location | Implementation Location | Used By
-----------+--------------------+------------------------+------------------
Inbound    | application/       | application/           | adapters/in/
Outbound   | application/       | adapters/out/          | application/
```

### Framework Annotations Quick Reference

```
Layer          | Framework Annotations | Example
---------------+----------------------+-------------------------------------------
Domain         | ❌ NEVER             | Pure Java only
Application    | ⚠️ Minimal or Never  | Maybe @Service
Adapters       | ✅ YES               | @RestController, @Entity
Infrastructure | ✅ YES               | @Configuration, @Bean
Shared Kernel  | ⚠️ Neutral only      | Custom annotations (@AsyncInitialize)
```

---

## Final Checklist

When adding new code, ask yourself:

- [ ] Does this belong in domain (business logic) or elsewhere (technical)?
- [ ] If it's an interface, is it inbound (used by app) or outbound (app uses it)?
- [ ] Are my dependencies pointing inward?
- [ ] Am I putting framework annotations in the right layer?
- [ ] Do I have separate domain and persistence models?
- [ ] Is my domain free of infrastructure concerns?
- [ ] Are adapters using (not implementing) inbound ports?
- [ ] Are adapters implementing (not using) outbound ports?
- [ ] Is infrastructure only doing wiring and configuration?
- [ ] Can I test my domain/application without any framework?

---

**Remember**: These are guidelines, not laws. Real projects may require pragmatic compromises, but understanding these principles helps you make informed architectural decisions.

## Related markers

- [@AsyncInitialize](/marker/infrastructure/asyncinitialize.md)
- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Value](/marker/tactical/value.md)
