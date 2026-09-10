---
type: Section
title: Core Rule Categories
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: dca-guide/archunit-governance.md
tags: [guide, section]
---

Each category below corresponds to one or more rule sets of the library (`layered`/`onion`, `hexagonal`,
`tactical`, `strategic`, `naming`, `cycles`, `contextmap`, …). The code is what the library runs,
written out in plain ArchUnit so you can read what a rule checks — and copy its shape for a rule of
your own.

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

Use cases may be registered by configuration or carry an injectable stereotype. A
static reference does not prove registration, and runtime scanning need not leave one;
`DCA-NAM-002` therefore only lists unannotated Java operations as an informational
diagnostic. It never fails. .NET registration is code and has no stereotype counterpart.
Outgoing adapters may reuse global and own-module infrastructure; another module's
infrastructure remains private (`DCA-HEX-005`).

Domain metadata is classified by configured roles, including members and composed
metadata. Types prohibit injectable/container, persistence-entity and transactional
roles; fields (and .NET properties) prohibit injection-site and persistence-mapping
roles; methods prohibit transaction and event-listener roles, plus setter injection
except on events; constructors prohibit injection-site metadata. Java detects direct
and meta-annotations. .NET checks an attribute's namespace and every base attribute
type against persistence, injection, transaction and container namespace lists; no
event-listener attribute role is configured by default. Unclassified metadata is
allowed by this check, without claiming it harmless. Events, services, factories and
specifications have exclusive `ADV-004/011/015/018` ownership; `ONI-003` owns the
remaining domain-model types, so one type is never reported twice for metadata.

The following examples illustrate individual checks; the published rules apply the complete role policy above.

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
        .should().beAnnotatedWith("jakarta.persistence.Id")
        .orShould().beAnnotatedWith("jakarta.persistence.Column")
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

The immutability rules check **shallow instance state**, including inherited fields and
setter methods, on ordinary classes and records alike. Java classes must be final (or
records) with final fields; C# classes must be sealed or records with readonly fields
and get-only or init-only properties. Structs are inspected too. Referenced objects and
collection contents are not recursively checked. Record syntax alone is not proof of
immutability. `DCA-NET-004` requires struct values to be readonly; immutable classes
with equality remain valid. `DCA-TAC-012` checks equality for hand-written structs.
`DCA-USE-015` checks both class and struct results for exposed identities.

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

This condition looks at the class as a whole, which is enough to teach the idea. Two things it does
not see: a publication in one method covers a save in an *unrelated* method, and a helper shared by
two entry methods appears to connect them. A production version — the published `DCA-USE-009` rule
does this — follows the calls within the class and judges every *entry path*: each entry point that
reaches a `save` — a method callable from outside the class, or one nothing in the class calls — must
also reach a `publishAndClearEvents`; a public method stays an entry point when a wrapper calls it. Even
then, bytecode does not say in which order the two calls run or that they concern the same aggregate,
and ArchUnit attributes a lambda's body to the enclosing method; those remain review checks.

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

**What a result may carry (`DCA-USE-015`).** A result is the use case's answer, not a handle on the model:
values, enriched models and read models may cross the boundary, aggregate roots and entities may not. The
check walks the record's components transitively — nested records, part records anywhere in the application
layer (`application/shared` included), and the type arguments of `List<T>`, `Optional<T>` and `Map<K,V>` — because part records are named
by content (`CartItemSummary`), not `*Result`, and would otherwise slip past a name-based selection:

```java
@ArchTest
static void results_should_not_expose_aggregate_roots_or_entities(JavaClasses classes) {
    var violations = classes.stream()
        .filter(c -> c.getSimpleName().endsWith("Result")
                  && c.getPackageName().contains(".application."))
        .flatMap(result -> identityBearingComponents(result).stream()
            .map(path -> result.getSimpleName() + " exposes " + path))
        .toList();

    assertThat(violations)
        .as("A result carries values, never aggregate roots or entities")
        .isEmpty();
}

// walks fields, record components and generic type arguments; recurses into records of the
// same package; reports the path to the first type assignable to AggregateRoot or Entity
private static List<String> identityBearingComponents(JavaClass result) { /* ... */ }
```

### 5. Port and Adapter Rules

Ordinary use cases do not invoke other use cases, whether directly, through an
input port, or through an application helper. Shared collaborators that do not call
operations remain valid. `DCA-USE-016` follows dependencies within the module's
application layer and reports `Caller -> Target [via Helper]`. Explicit coordination
uses a caller-side exception, for example
`dca.rule.DCA-USE-016.ignore=^com\.example\.module\.application\.coordinate\.CoordinatorUseCase -> `.
This permits the coordinator to invoke operations; it does not permit an operation
to invoke the coordinator, and `DCA-CYC-005` still detects coordination cycles,
including two operations inside the same feature. No coordinator marker is implied.
When a reliable exception cannot be expressed, use WARN with a recorded reason and
review the coordinator's transaction boundaries and partial-failure semantics manually.
Reflection, container lookups and calls through interfaces outside the InputPort
hierarchy also require manual review.

The input port describes the complete effective public instance surface (`DCA-USE-017`).
Declared and inherited business methods, unrelated-interface methods and public
properties/getters/setters must be in the input-port contract. Constructors, Object
members and compiler-generated members are exempt; a property accessor is not exempt
merely because it has a special runtime name. Ordinary, inherited and explicit
input-port implementations are valid. In .NET, `DCA-NET-003` separately validates
`IUseCase<TIn,TOut>.ExecuteAsync(input, CancellationToken)` returning `Task<T>` through
the interface map; it does not count declared public methods.

For every declared ACL interaction, the matching adapter must contain a class that
uses that upstream's channel contract and the declaring context's own domain or
application model (`DCA-MAP-008`). Two translators for different upstreams may share
an adapter package. Evidence for one upstream does not satisfy another interaction.
This identifies a structural translation site, without proving translation quality.


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
        .because("Output ports live in application packages and must be interfaces");

@ArchTest
static final ArchRule adapters_should_implement_ports =
    classes()
        .that().resideInAPackage("..adapter.outgoing..")
        .and().areNotInterfaces()
        .should().implement(OutputPort.class)  // If you have OutputPort marker
        .orShould().beAnnotatedWith("Component")
        .orShould().beAnnotatedWith("Repository")
        .because("Outbound adapters should implement output ports");

// A driving adapter drives the application *through its port*. Depending on the
// application package is not enough to express that: the use case class lives there
// too, so the rule below has to name the implementation and forbid it.
@ArchTest
static final ArchRule input_adapters_should_depend_on_input_ports_not_use_case_classes =
    noClasses()
        .that().resideInAPackage("..adapter.incoming..")
        .should().dependOnClassesThat(
            describe(
                "are use case implementations rather than input ports",
                javaClass -> !javaClass.isInterface() && javaClass.isAssignableTo(InputPort.class)))
        .because("Injecting the concrete use case couples the adapter to one realisation, "
            + "defeats the Dependency Inversion Principle the port exists for, and makes the "
            + "adapter untestable without the real use case and everything it depends on");

// An incoming adapter translates external input, calls an input port and formats its
// result. A domain service in its constructor means it derives business facts itself —
// the use case owns that collaboration and puts the outcome into the result. Outgoing
// adapters are deliberately not selected: repositories construct and reconstitute
// domain objects while implementing output ports.
@ArchTest
static final ArchRule incoming_adapters_should_not_depend_on_domain_services =
    noClasses()
        .that().resideInAPackage("..adapter.incoming..")
        .should().dependOnClassesThat().areAssignableTo(DomainService.class)
        .because("Injecting or invoking a domain service bypasses the application boundary; "
            + "the use case owns that collaboration and puts its outcome into the result");

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
manages an Aggregate Root's lifecycle (`save`, `delete`, invariants), a `Store` records or queries
operational data that has no aggregate lifecycle (`record`, `count`, `exists`) — it may look an
operational record up by key (`findById`); the difference is lifecycle, not lookup. Without rules the
distinction is doctrine only — a `*Store` can quietly grow a `save` and nothing fails.

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
        .filter(m -> Set.of("save", "deleteById", "delete").contains(m.getName()))
        .map(m -> m.getFullName() + " — Repository semantics on a Store")
        .toList();

    assertThat(violations)
        .as("Stores use record/count/exists/lookup semantics, not save/delete")
        .isEmpty();
}
```

If a Store legitimately needs `save` or `delete`, the stored object has a lifecycle with invariants —
rename the port to `*Repository` and model the object as an Aggregate Root.

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

**Three traps worth naming, because each produces a rule that can never fail.**

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

*Selecting by declaration.* If the isolation rule iterates over the *declared* contexts — the
packages that carry the marker — a module that owns `domain/`, `application/` and `adapter/` but
declares nothing is outside the rule twice over: its imports are never checked, and nobody is
forbidden to import its internals. It passes the whole suite for lack of a subject. Select
**structurally** instead: every package that owns a layer is a module, declared or not, and is both
a source and a forbidden target. What the marker decides is membership of the context map, not
whether the module is isolated. The allow-list is a package convention too — a module's `api/`
(synchronous, in-process) and `events/` (asynchronous) packages are the only part of it a neighbour's
adapter may depend on. Package names, not framework annotations, so the rule holds without any
module system on the class path, and a module that deliberately is *not* a bounded context (one that
borrows a foreign system's language, say) needs no declaration to be governed.

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

// Inside one context: the packages directly below application/ — the features in a grouped layout
// (application/{feature}/{usecase}), the use cases in a flat one — must not depend on each other in
// a circle. application/shared is the context-wide port package and is not a slice. Catalog: DCA-CYC-005.
@ArchTest
static final ArchRule no_cycles_between_features =
    slices()
        .matching("com.company.project.order.application.(*)..")
        .ignoreDependency(alwaysTrue(), resideInAPackage("..application.shared.."))
        .should().beFreeOfCycles()
        .because("A cycle between two features means the grouping does not carry its weight");
```

A second structural rule keeps the feature level legible: within one module the use-case packages use *one*
depth — all `application.<usecase>` or all `application.<feature>.<usecase>` — never a mixture, and never a
use case directly in `application` or nested deeper than a feature (`DCA-USE-014`). Both rules check package
shape only; they infer nothing about bounded contexts or aggregate ownership.


### 8. Context Map Rules

Context relationships are declared on each context's `package-info.java` (`@Upstream`,
`@ExternalUpstream`, `@Partnership`). Because the declarations are plain annotations, ArchUnit can
check them against the real dependency graph — the context map becomes *executable*.

```java
@Test
void implemented_upstreams_are_backed_by_code() {
    for (var context : boundedContextPackages()) {
        for (Upstream upstream : packageAnnotations(context, Upstream.class)) {
            if (upstream.status() != Upstream.Status.IMPLEMENTED) continue;   // PLANNED is exempt
            String target = contextPackage(upstream.context());
            classes().that().resideInAPackage(context + "..")
                .should().dependOnClassesThat().resideInAPackage(target + "..")
                .because("Context '" + context + "' declares @Upstream(" + upstream.context()
                    + ") as IMPLEMENTED — a declaration without a dependency is stale; mark it PLANNED or remove it")
                .check(classes);
        }
    }
}

@Test
void cross_context_dependencies_require_a_declaration() {
    for (var context : boundedContextPackages()) {
        Set<String> declared = declaredUpstreamsAndPartners(context);
        for (var other : boundedContextPackages()) {
            if (other.equals(context) || declared.contains(other)) continue;
            noClasses().that().resideInAPackage(context + "..")
                .should().dependOnClassesThat().resideInAPackage(other + "..")
                .because("Context '" + context + "' depends on '" + other
                    + "' without declaring it — add @Upstream(context = ..., translation = ..., via = ...)")
                .check(classes);
        }
    }
}

@Test
void conformist_contract_types_never_reach_the_domain() {
    for (var context : boundedContextPackages()) {
        for (Upstream upstream : packageAnnotations(context, Upstream.class)) {
            if (upstream.translation() != Upstream.Translation.CONFORMIST) continue;
            noClasses().that().resideInAPackage(context + ".domain..")
                .should().dependOnClassesThat().resideInAPackage(contextPackage(upstream.context()) + "..")
                .because("Conformism does not suspend domain purity — the domain layer stays free of upstream types")
                .check(classes);
        }
    }
}
```

The full set (13 rules) also verifies that declarations are well-formed (target exists, never self,
unique per channel), that `@Partnership` is symmetric, that Anti-Corruption-Layer contract types stay
inside the translating adapter, and — when Spring Modulith is used — that `@Upstream` declarations and
`allowedDependencies` agree. A companion test renders `docs/context-map.md` (table + Mermaid) from the
same annotations, so the diagram can never contradict the code.

`packageAnnotations()` reads repeatable annotations from the `package-info` class:

```java
static <T extends Annotation> List<T> packageAnnotations(String packageName, Class<T> type) {
    try {
        return List.of(Class.forName(packageName + ".package-info").getAnnotationsByType(type));
    } catch (ClassNotFoundException e) {
        return List.of();
    }
}
```

---

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@Upstream](/marker/strategic/upstream.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainService](/marker/tactical/domainservice.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Id](/marker/tactical/id.md)
- [Value](/marker/tactical/value.md)

## Evidence slices

- [Overview](/evidence/guide/archunit-governance/core-rule-categories/overview.md)
- [1. Layer Dependency Rules](/evidence/guide/archunit-governance/core-rule-categories/1-layer-dependency-rules.md)
- [2. Framework Independence Rules](/evidence/guide/archunit-governance/core-rule-categories/2-framework-independence-rules.md)
- [3. DDD Pattern Rules](/evidence/guide/archunit-governance/core-rule-categories/3-ddd-pattern-rules.md)
- [4. Naming Convention Rules](/evidence/guide/archunit-governance/core-rule-categories/4-naming-convention-rules.md)
- [5. Port and Adapter Rules](/evidence/guide/archunit-governance/core-rule-categories/5-port-and-adapter-rules.md)
- [6. Shared Kernel Rules](/evidence/guide/archunit-governance/core-rule-categories/6-shared-kernel-rules.md)
- [7. Cyclic Dependency Rules](/evidence/guide/archunit-governance/core-rule-categories/7-cyclic-dependency-rules.md)
- [8. Context Map Rules](/evidence/guide/archunit-governance/core-rule-categories/8-context-map-rules.md)
