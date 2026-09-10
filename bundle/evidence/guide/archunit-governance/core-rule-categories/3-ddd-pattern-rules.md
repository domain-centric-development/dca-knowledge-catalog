---
type: Reference
title: Core Rule Categories — 3. DDD Pattern Rules
tags: [reference]
evidence_for: "/guide/archunit-governance/core-rule-categories.md#3-ddd-pattern-rules"
---

[Full node and context](/guide/archunit-governance/core-rule-categories.md#3-ddd-pattern-rules). This is an evidence excerpt; retain the parent selection and caveats.

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
