---
type: Reference
title: Core Rule Categories — 5. Port and Adapter Rules
tags: [reference]
evidence_for: "/guide/archunit-governance/core-rule-categories.md#5-port-and-adapter-rules"
---

[Full node and context](/guide/archunit-governance/core-rule-categories.md#5-port-and-adapter-rules). This is an evidence excerpt; retain the parent selection and caveats.

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
