---
type: Rule
id: DCA-USE-012
title: Use cases that publish domain events must run inside a transaction boundary
rule: "Integration events are relayed after commit (@TransactionalEventListener, @ApplicationModuleListener) and their publication is registered in the publishing transaction. Without an active transaction the after-commit listeners are skipped silently and nothing is registered: the use case succeeds, the other contexts never hear of it. The use case that publishes owns the boundary - @Transactional on the class or the executing method, or an explicit UnitOfWork.run(...) around save and publish."
constraint: Use cases that publish domain events must run inside a transaction boundary.
enforced_by: "UseCaseRules#DCA-USE-012"
status: enforced
rule_set: usecase
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
not_applicable_dotnet: "Guards Spring's after-commit relay (@TransactionalEventListener / @ApplicationModuleListener), which is skipped silently without an active transaction. .NET has no ambient transaction attribute on use cases; after-save delivery is the job of the integration-event outbox adapter, not of the use case"
---

```java
DcaRule.of(
    "DCA-USE-012",
    "Use cases that publish domain events must run inside a transaction boundary",
    "Integration events are relayed after commit (@TransactionalEventListener,"
        + " @ApplicationModuleListener) and their publication is registered in the publishing"
        + " transaction. Without an active transaction the after-commit listeners are skipped"
        + " silently and nothing is registered: the use case succeeds, the other contexts never"
        + " hear of it. The use case that publishes owns the boundary - @Transactional on the"
        + " class or the executing method, or an explicit UnitOfWork.run(...) around save and"
        + " publish",
    arch ->
        classes()
            .that()
            .resideInAPackage(layout.applicationPattern())
            .and()
            .haveSimpleNameEndingWith(layout.useCaseSuffix())
            .and()
            .areNotInterfaces()
            .should(
                beTransactionalWhenPublishing(layout.frameworkAnnotations().transactional()))
            .allowEmptyShould(true))
```

## Applies to markers

- [UnitOfWork](/marker/port-out/unitofwork.md)
