---
type: Section
title: Core Rule Categories
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/archunit-governance.md
tags: [guide, section]
---

### 1. Layer Dependency Rules

Enforce that dependencies only point inward toward the domain.

```java
@ArchTest
static final ArchRule domain_should_not_depend_on_outer_layers =
    noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat()
            .resideInAnyPackage(
                "..application..",
                "..adapter..",
                "..infrastructure.."
            )
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
```

### 2. Framework Independence Rules

Ensure domain and application layers remain framework-agnostic.

```java
@ArchTest
static final ArchRule domain_should_be_framework_agnostic =
    noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat()
            .resideInAnyPackage(
                "org.springframework..",
                "jakarta.persistence..",
                "javax.persistence..",
                "org.hibernate..",
                "jakarta.validation..",
                "javax.validation.."
            )
        .because("Domain must be framework-agnostic");

@ArchTest
static final ArchRule domain_should_not_use_jpa_annotations =
    noFields()
        .that().areDeclaredInClassesThat().resideInAPackage("..domain..")
        .should().beAnnotatedWith("jakarta.persistence.Entity")
        .orShould().beAnnotatedWith("jakarta.persistence.Id")
        .orShould().beAnnotatedWith("jakarta.persistence.Column")
        .orShould().beAnnotatedWith("jakarta.persistence.Table")
        .orShould().beAnnotatedWith("jakarta.persistence.ManyToOne")
        .orShould().beAnnotatedWith("jakarta.persistence.OneToMany")
        .because("Domain should not use JPA annotations - use separate persistence model");

@ArchTest
static final ArchRule application_should_be_framework_agnostic =
    noClasses()
        .that().resideInAPackage("..application..")
        .should().dependOnClassesThat()
            .resideInAnyPackage(
                "org.springframework.web..",
                "jakarta.ws.rs..",
                "org.springframework.data.."
            )
        .because("Application layer should not depend on web or persistence frameworks");

@ArchTest
static final ArchRule application_layer_can_use_minimal_spring =
    classes()
        .that().resideInAPackage("..application..")
        .should().onlyDependOnClassesThat()
            .resideInAnyPackage(
                "..domain..",
                "..application..",
                "..sharedkernel..",
                "java..",
                "org.springframework.stereotype..",  // @Service is acceptable
                "org.springframework.transaction.."   // @Transactional is acceptable (pragmatic)
            )
        .because("Application can use minimal Spring annotations for pragmatism");
```

### 3. DDD Pattern Rules

Validate proper implementation of DDD tactical patterns.

```java
@ArchTest
static final ArchRule aggregates_should_implement_aggregate_root =
    classes()
        .that().haveSimpleNameEndingWith("Aggregate")
        .or().areAnnotatedWith("AggregateRoot")  // If you have custom annotation
        .should().implement(AggregateRoot.class)
        .because("Aggregates must implement AggregateRoot marker interface");

@ArchTest
static final ArchRule value_objects_should_be_immutable =
    classes()
        .that().implement(Value.class)
        .should().haveOnlyFinalFields()
        .andShould().haveOnlyPrivateConstructors()  // Force factory methods
        .because("Value Objects must be immutable");

@ArchTest
static final ArchRule entities_should_have_identity =
    classes()
        .that().implement(Entity.class)
        .should().haveMethod("getId")
        .because("Entities must have identity via getId() method");

@ArchTest
static final ArchRule domain_events_should_be_immutable =
    classes()
        .that().implement(DomainEvent.class)
        .should().haveOnlyFinalFields()
        .because("Domain Events must be immutable (they represent past facts)");

@ArchTest
static final ArchRule domain_services_should_be_stateless =
    classes()
        .that().implement(DomainService.class)
        .should().haveOnlyFinalFields()
        .because("Domain Services should be stateless");

@ArchTest
static final ArchRule aggregates_should_be_in_domain_model =
    classes()
        .that().implement(AggregateRoot.class)
        .should().resideInAPackage("..domain.model..")
        .because("Aggregates belong in domain model package");

@ArchTest
static final ArchRule domain_events_should_be_in_domain_event_package =
    classes()
        .that().implement(DomainEvent.class)
        .should().resideInAPackage("..domain.event..")
        .because("Domain Events belong in domain event package");
```

**Publishing the events is the use case's obligation.** Raising an event and storing the aggregate
are two halves of one operation: an aggregate that is saved while still holding its events loses
them, and — with an identity-mapped or in-memory repository, where the same instance stays around —
they may be published later by an unrelated use case, out of context. Structural rules cannot see
this, but a custom `ArchCondition` can:

```java
ArchCondition<JavaClass> publishAfterSaving =
    new ArchCondition<>("publish the aggregate's domain events after saving it") {
        @Override
        public void check(JavaClass item, ConditionEvents events) {
            boolean saves = item.getMethodCallsFromSelf().stream()
                .anyMatch(call -> call.getTarget().getName().equals("save")
                    && call.getTargetOwner().isAssignableTo(Repository.class));
            if (!saves) {
                return;
            }
            boolean publishes = item.getMethodCallsFromSelf().stream()
                .anyMatch(call -> call.getTarget().getName().equals("publishAndClearEvents")
                    && call.getTargetOwner().isAssignableTo(DomainEventPublisher.class));
            events.add(publishes
                ? SimpleConditionEvent.satisfied(item, item.getSimpleName() + " publishes after saving")
                : SimpleConditionEvent.violated(item,
                    item.getSimpleName() + " saves an aggregate without publishing its domain events"));
        }
    };

@ArchTest
static final ArchRule use_cases_that_save_must_publish =
    classes()
        .that().resideInAPackage("..application..")
        .and().haveSimpleNameEndingWith("UseCase")
        .and().areNotInterfaces()
        .should(publishAfterSaving)
        .because("Unpublished events are lost, and events left on a stored aggregate may surface later out of context");
```

Note the rule demands the call **unconditionally**, not only where an event is expected: whether an
action raised one is the aggregate's business, and a use case that publishes only "when needed"
breaks silently the day an aggregate starts raising an event it did not raise before.

### 4. Naming Convention Rules

Enforce consistent naming across the codebase.

```java
@ArchTest
static final ArchRule input_ports_should_follow_naming =
    classes()
        .that().resideInAPackage("..application..port.in..")
        .or().resideInAPackage("..application..*..") // For use case folder structure
            .and().areInterfaces()
            .and().arePublic()
        .should().haveSimpleNameEndingWith("InputPort")
        .orShould().haveSimpleNameEndingWith("UseCase")
        .orShould().haveSimpleNameEndingWith("Query")
        .because("Input ports should follow naming conventions");

@ArchTest
static final ArchRule use_case_implementations_should_follow_naming =
    classes()
        .that().resideInAPackage("..application..usecase..")
        .or().implement(InputPort.class)
        .and().areNotInterfaces()
        .should().haveSimpleNameEndingWith("UseCase")
        .orShould().haveSimpleNameEndingWith("Service")
        .because("Use case implementations should follow naming conventions");

@ArchTest
static final ArchRule repositories_should_follow_naming =
    classes()
        .that().areAssignableTo(Repository.class)
        .and().areInterfaces()
        .should().haveSimpleNameEndingWith("Repository")
        .because("Repository interfaces should end with 'Repository'");

@ArchTest
static final ArchRule repository_adapters_should_follow_naming =
    classes()
        .that().implement(Repository.class)
        .and().areNotInterfaces()
        .should().haveSimpleNameEndingWith("RepositoryAdapter")
        .orShould().haveSimpleNameEndingWith("RepositoryImpl")
        .because("Repository implementations should follow naming conventions");

@ArchTest
static final ArchRule commands_should_follow_naming =
    classes()
        .that().resideInAPackage("..application..")
        .and().areRecords()
        .should().haveSimpleNameEndingWith("Command")
        .orShould().haveSimpleNameEndingWith("Query")
        .because("Input models should be named Command or Query");

@ArchTest
static final ArchRule results_should_follow_naming =
    classes()
        .that().resideInAPackage("..application..")
        .and().areRecords()
        .and().haveSimpleNameMatching(".*Result.*")
        .should().haveSimpleNameEndingWith("Result")
        .because("Output models should end with 'Result'");
```

### 5. Port and Adapter Rules

Verify proper implementation of hexagonal architecture.

```java
@ArchTest
static final ArchRule input_ports_should_be_interfaces =
    classes()
        .that().resideInAPackage("..application..port.in..")
        .or().haveSimpleNameEndingWith("InputPort")
        .should().beInterfaces()
        .because("Input ports must be interfaces");

@ArchTest
static final ArchRule output_ports_should_be_interfaces =
    classes()
        .that().resideInAPackage("..application..port.out..")
        .or().resideInAPackage("..application..shared..")
        .and().areNotRecords()  // Exclude DTOs
        .should().beInterfaces()
        .because("Output ports must be interfaces");

@ArchTest
static final ArchRule adapters_should_implement_ports =
    classes()
        .that().resideInAPackage("..adapter.outgoing..")
        .and().areNotInterfaces()
        .should().implement(OutputPort.class)  // If you have OutputPort marker
        .orShould().beAnnotatedWith("Component")
        .orShould().beAnnotatedWith("Repository")
        .because("Outbound adapters should implement output ports");

@ArchTest
static final ArchRule input_adapters_should_call_input_ports =
    classes()
        .that().resideInAPackage("..adapter.incoming..")
        .should().dependOnClassesThat()
            .resideInAnyPackage("..application..port.in..", "..application..*InputPort")
        .because("Input adapters should only depend on input ports, not implementations");

@ArchTest
static final ArchRule adapters_should_not_depend_on_each_other =
    noClasses()
        .that().resideInAPackage("..adapter.incoming..")
        .should().dependOnClassesThat()
            .resideInPackage("..adapter.outgoing..")
        .andShould().dependOnClassesThat()
            .resideInPackage("..adapter.incoming..")
        .because("Adapters should not depend on each other directly");
```

### 6. Shared Kernel Rules

Ensure Shared Kernel remains independent and minimal.

```java
@ArchTest
static final ArchRule shared_kernel_should_have_no_dependencies =
    noClasses()
        .that().resideInAPackage("..sharedkernel..")
        .should().dependOnClassesThat()
            .resideInAnyPackage(
                "..domain..",
                "..application..",
                "..adapter..",
                "..infrastructure.."
            )
        .because("Shared Kernel must be independent - no dependencies on bounded contexts");

@ArchTest
static final ArchRule shared_kernel_should_not_use_frameworks =
    noClasses()
        .that().resideInAPackage("..sharedkernel..")
        .should().dependOnClassesThat()
            .resideInAnyPackage(
                "org.springframework..",
                "jakarta..",
                "javax..",
                "org.hibernate.."
            )
        .because("Shared Kernel must be framework-agnostic");

@ArchTest
static final ArchRule bounded_contexts_should_not_depend_on_each_other =
    noClasses()
        .that().resideInAPackage("..order..")
        .should().dependOnClassesThat()
            .resideInAnyPackage(
                "..customer..",
                "..inventory..",
                "..payment.."
            )
        .because("Bounded contexts should not have direct dependencies on each other");
```

### 7. Cyclic Dependency Rules

Detect and prevent circular dependencies.

```java
@ArchTest
static final ArchRule no_cycles_in_packages =
    slices()
        .matching("com.company.project.(*)..")
        .should().beFreeOfCycles()
        .because("Cyclic dependencies make code hard to understand and maintain");

@ArchTest
static final ArchRule no_cycles_between_bounded_contexts =
    slices()
        .matching("com.company.project.(order|customer|inventory|payment).(*)..")
        .should().beFreeOfCycles()
        .because("Bounded contexts should not have cyclic dependencies");
```

---

## Related markers

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainService](/marker/tactical/domainservice.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Value](/marker/tactical/value.md)
