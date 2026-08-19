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

// The Entity marker already declares id(), so requiring the method checks what the
// compiler enforces. What is worth checking is that the identity is a value object:
// a field whose *type* implements the Id marker. Matching on a field *name* ending in
// "id" accepts valid, paid and uuid, and passes an entity that has no identity at all.
@ArchTest
static void entities_should_have_an_identity_field(JavaClasses classes) {
    var violations = classes.stream()
        .filter(c -> c.isAssignableTo(Entity.class) && !c.isInterface() && !c.getModifiers().contains(ABSTRACT))
        .filter(c -> c.getAllFields().stream().noneMatch(f -> f.getRawType().isAssignableTo(Id.class)))
        .map(JavaClass::getName)
        .toList();

    assertThat(violations)
        .as("Entities must hold their identity as a field typed as an Id value object")
        .isEmpty();
}

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
        .that().resideInAPackage("..application..")
        .and().areInterfaces()
        .and().areAssignableTo(InputPort.class)
        .and().doNotHaveSimpleName("InputPort")
        .and().doNotHaveSimpleName("UseCase")
        .should().haveSimpleNameEndingWith("InputPort")
        .because("Input ports are matched by marker, not by package: DCA places each input port "
               + "in its own use-case folder, so there is no ..application.port.in.. to point at");

@ArchTest
static final ArchRule use_case_implementations_should_follow_naming =
    classes()
        .that().implement(InputPort.class)
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
        .that().haveSimpleNameEndingWith("InputPort")
        .should().beInterfaces()
        .because("Input ports must be interfaces");

@ArchTest
static final ArchRule output_ports_should_be_interfaces =
    classes()
        .that().resideInAPackage("..application.shared..")
        .and().areNotRecords()  // Exclude nested result records
        .should().beInterfaces()
        .because("Output ports live in application.shared and must be interfaces");

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
            .resideInAnyPackage("..application..")
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

**What a repository may hand back.** The often-quoted form of this rule is "repository methods
return Aggregate Roots". As a positive requirement it is wrong: a repository legitimately returns a
`boolean` from an `existsBy...`, a count, a page wrapper, or a Value Object composed for one use case
— Vernon's *use-case optimal query*. The invariant worth enforcing is the prohibition. A repository
must not hand out an Entity that is **not** an Aggregate Root, because a caller holding one can
mutate part of an aggregate without passing its root, and the root's invariants never run.

```java
@ArchTest
static void repositories_should_not_expose_non_root_entities(JavaClasses classes) {
    var violations = classes.stream()
        .filter(c -> c.isInterface() && c.isAssignableTo(Repository.class))
        .flatMap(repo -> repo.getMethods().stream())
        .flatMap(m -> typesInvolvedIn(m.getReturnType()).stream()
            .filter(t -> t.isAssignableTo(Entity.class) && !t.isAssignableTo(AggregateRoot.class))
            .map(t -> m.getFullName() + " exposes " + t.getName()))
        .toList();

    assertThat(violations).isEmpty();
}

// Recursive, because the forbidden type is almost never the raw return type.
private static List<JavaClass> typesInvolvedIn(JavaType type) {
    var involved = new ArrayList<JavaClass>();
    var erasure = type.toErasure();
    involved.add(erasure);
    erasure.tryGetComponentType().ifPresent(involved::add);
    if (type instanceof JavaParameterizedType p) {
        p.getActualTypeArguments().forEach(arg -> involved.addAll(typesInvolvedIn(arg)));
    } else if (type instanceof JavaWildcardType w) {
        w.getUpperBounds().forEach(bound -> involved.addAll(typesInvolvedIn(bound)));
    }
    return involved;
}
```

The traversal is the whole rule. A tempting shortcut — enumerate `List`, `Set` and `Collection` by
name and call `tryGetComponentType()` on the raw type — inspects nothing at all: that method resolves
**array** component types, so it returns empty for every collection. Add `Optional` to the name list
and `Map<K, List<X>>` still walks through. Walk the type arguments instead and there is no list to
keep current.

Note the type-parameter side needs no rule. `Repository<T extends AggregateRoot<T, ID>, ID extends Id>`
already makes a repository for a non-root entity a compile error.

**Repository vs. Store.** Both are output ports, but they promise different things: a `Repository`
manages an Aggregate Root by identity (`findById`, `save`, `delete`), a `Store` records or queries
operational data that has no aggregate lifecycle (`record`, `count`, `exists`). Without rules the
distinction is doctrine only — a `*Store` can quietly grow a `findById` and nothing fails.

```java
@ArchTest
static final ArchRule stores_should_extend_the_store_marker =
    classes()
        .that().areInterfaces()
        .and().haveSimpleNameEndingWith("Store")
        .and().doNotHaveSimpleName("Store")
        .should().beAssignableTo(Store.class)
        .andShould().notBeAssignableTo(Repository.class)
        .because("Repository is reserved for Aggregate Roots");

@ArchTest
static final ArchRule store_interfaces_should_be_shared_output_ports =
    classes()
        .that().areInterfaces()
        .and().areAssignableTo(Store.class)
        .and().doNotHaveSimpleName("Store")
        .should().resideInAPackage("..application.shared..")
        .because("A Store is an output port — the contract belongs to the application layer");

@ArchTest
static final ArchRule store_implementations_should_be_outgoing_adapters =
    classes()
        .that().areNotInterfaces()
        .and().areAssignableTo(Store.class)
        .should().resideInAPackage("..adapter.outgoing..")
        .because("Store implementations are outgoing adapters");
```

The fourth rule cannot be written as a fluent `ArchRule` — it inspects method names on the matched
interfaces, so it is expressed as a plain assertion:

```java
@ArchTest
static void stores_should_not_have_repository_methods(JavaClasses classes) {
    var violations = classes.stream()
        .filter(c -> c.isInterface()
                  && c.isAssignableTo(Store.class)
                  && !c.getSimpleName().equals("Store"))
        .flatMap(store -> store.getMethods().stream())
        .filter(m -> Set.of("findById", "save", "deleteById", "delete").contains(m.getName()))
        .map(m -> m.getFullName() + " — Repository semantics on a Store")
        .toList();

    assertThat(violations)
        .as("Stores use record/count/exists semantics, not findById/save")
        .isEmpty();
}
```

If a Store legitimately needs `findById`, the stored object has identity — rename the port to
`*Repository` and model the object as an Aggregate Root.

### 6. Shared Kernel Rules

Ensure Shared Kernel remains independent and minimal.

```java
// Contexts are discovered, not enumerated. Discovery needs the imported classes, so the
// rule is a method-style test — a static-field rule is built before any classes exist.
@ArchTest
static void shared_kernel_should_not_depend_on_any_context(JavaClasses classes) {
    noClasses()
        .that().resideInAPackage("..sharedkernel..")
        .should().dependOnClassesThat(
            resideInAnyPackage(boundedContextPatterns(classes))
                .and(not(resideInAPackage("..sharedkernel.."))))
        .because("Shared Kernel must be independent - no dependencies on bounded contexts")
        .check(classes);
}

// Every bounded context marks its root package once:
//
//   @BoundedContext
//   package com.company.project.order;
//
// The helper turns those markers into ArchUnit package patterns. A context added
// tomorrow is discovered on the next run — nothing to register.
private static String[] boundedContextPatterns(JavaClasses classes) {
    return StreamSupport.stream(classes.spliterator(), false)
        .filter(c -> c.getSimpleName().equals("package-info"))
        .filter(c -> c.isAnnotatedWith(BoundedContext.class))
        .map(c -> c.getPackageName() + "..")
        .distinct()
        .sorted()
        .toArray(String[]::new);
}

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

// Discovered, not enumerated: one rule per context, forbidding every other context.
// A context added tomorrow is covered without being registered here.
@ArchTest
static void bounded_contexts_should_not_depend_on_each_other(JavaClasses classes) {
    var contexts = List.of(boundedContextPatterns(classes));   // the helper defined above
    for (String source : contexts) {
        String[] others = contexts.stream().filter(c -> !c.equals(source)).toArray(String[]::new);
        if (others.length == 0) continue;
        noClasses()
            .that().resideInAPackage(source)
            .should().dependOnClassesThat().resideInAnyPackage(others)
            .allowEmptyShould(true)
            .because("Bounded contexts must not have direct dependencies on each other")
            .check(classes);
    }
}
```

**Two traps worth naming, because both produce a rule that can never fail.**

*Enumerating contexts.* `resideInAPackage("..order..")` versus a hand-written list of the other
three works until somebody adds a fifth context — which is then unguarded, silently. Discover the
contexts instead (a marker annotation on `package-info.java` is enough) and generate one rule per
context. The rule set then grows with the codebase.

*Excluding the shared kernel by pattern.* A shared kernel has its own `domain/` package, so
forbidding `..sharedkernel..` from depending on `..domain..` forbids it from using **its own**
`Money` and `ProductId`. The same cuts the other way: every context's domain must be able to reach
`sharedkernel.domain..`, so a per-context isolation rule must not treat the shared kernel as a
foreign context. Discovery solves this for free — the shared kernel carries a different marker than
a bounded context, so it never lands among the forbidden targets and needs no allow-list.

*And use `dependOnClassesThat`, never `accessClassesThat`.* ArchUnit counts an access as a method
call or field access. A field, parameter or record component of a forbidden type is a dependency,
not an access, so an isolation rule written with `accessClassesThat` stays green while a class holds
the forbidden type outright.

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
        .matching("com.company.project.(*).(*)..")   // every context, not a fixed list
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
- [Store](/marker/port-out/store.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainService](/marker/tactical/domainservice.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Id](/marker/tactical/id.md)
- [Value](/marker/tactical/value.md)
