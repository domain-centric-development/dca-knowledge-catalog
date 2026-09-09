---
type: Reference
title: Core Rule Categories — 4. Naming Convention Rules
tags: [reference]
evidence_for: "/guide/archunit-governance/core-rule-categories.md#4-naming-convention-rules"
---

[Full node and context](/guide/archunit-governance/core-rule-categories.md#4-naming-convention-rules). This is an evidence excerpt; retain the parent selection and caveats.

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
