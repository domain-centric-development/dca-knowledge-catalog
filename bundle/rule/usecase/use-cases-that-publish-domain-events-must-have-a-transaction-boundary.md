---
type: Rule
id: DCA-USE-012
title: Use cases that publish domain events must have a transaction boundary
rule: "Integration events are relayed after commit (@TransactionalEventListener, @ApplicationModuleListener) and their publication is registered in the publishing transaction. Without an active transaction the after-commit listeners are skipped silently and nothing is registered: the use case succeeds, the other contexts never hear of it. The use case that publishes owns the boundary - either declarative transaction metadata (@Transactional on the class or the executing method) or an explicit TransactionBoundary.inTransaction(...) around save and publish. Checked per entry path, following calls within the class: from every entry point - a method callable from outside the class, or one nothing in the class calls - no route down to the publishing method may be free of an annotation or a boundary; a covered caller does not cover another route to the same helper, and a boundary on one route does not cover a second route. Whether the publication sits inside the block handed to inTransaction(...) is not visible in ArchUnit's call model, which folds a lambda's body into the enclosing method; that placement stays a review check."
constraint: Use cases that publish domain events must have a transaction boundary.
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
    "Use cases that publish domain events must have a transaction boundary",
    "Integration events are relayed after commit (@TransactionalEventListener,"
        + " @ApplicationModuleListener) and their publication is registered in the publishing"
        + " transaction. Without an active transaction the after-commit listeners are skipped"
        + " silently and nothing is registered: the use case succeeds, the other contexts never"
        + " hear of it. The use case that publishes owns the boundary - either declarative"
        + " transaction metadata (@Transactional on the class or the executing method) or an"
        + " explicit TransactionBoundary.inTransaction(...) around save and publish. Checked"
        + " per entry path, following calls within the class: from every entry point - a"
        + " method callable from outside the class, or one nothing in the class calls - no route"
        + " down to the publishing method may be free of an annotation or a boundary; a covered"
        + " caller does not cover another route to the same helper, and a boundary on one route"
        + " does not cover a second route. Whether the publication sits inside the block"
        + " handed to inTransaction(...) is not visible in ArchUnit's call model, which folds a"
        + " lambda's body into the enclosing method; that placement stays a review check",
    arch ->
        classes()
            .that()
            .resideInAnyPackage(arch.allApplicationPatterns())
            .and()
            .haveSimpleNameEndingWith(layout.useCaseSuffix())
            .and()
            .areNotInterfaces()
            .should(
                beTransactionalWhenPublishing(layout.frameworkAnnotations().transactional()))
            .allowEmptyShould(true))
```

## Applies to markers

- [TransactionBoundary](/marker/application/transactionboundary.md)
