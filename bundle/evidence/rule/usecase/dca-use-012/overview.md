---
type: Reference
title: Use cases that publish domain events must have a transaction boundary — Overview
tags: [reference]
evidence_for: /rule/usecase/dca-use-012.md
---

[Full node and context](/rule/usecase/dca-use-012.md). This is an evidence excerpt; retain the parent selection and caveats.

# Use cases that publish domain events must have a transaction boundary

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.

## Check

For every method that calls a DomainEventPublisher, every route from each entry point down to it is covered: the class carries one of the configured transactional annotations, or every uncovered unit on the route is either annotated or calls TransactionBoundary.inTransaction. A covered caller does not cover a second route to the same helper. With an empty transactional role only the explicit boundary counts. Whether the publish call sits inside the inTransaction block is not checked - ArchUnit folds a lambda into its enclosing method.

## .NET reading

**Selection.** Concrete application operations selected by IInputPort marker or suffix with loadable runtime types, including closure and async units.

**Check.** Every entry path to an IDomainEventPublisher call crosses a unit calling ITransactionBoundary.InTransactionAsync (including its extension overloads) or carrying the configured TransactionalAttribute; a type-level attribute covers all paths. Static limit: a boundary call in the same unit passes even when publication follows an empty boundary block. Runtime rollback containment must be tested separately.

## Implementation

```java
DcaRule.of(
        "DCA-USE-012",
        "Use cases that publish domain events must have a transaction boundary",
        "Integration events are relayed after commit by the framework's after-commit listeners,"
            + " and their publication is registered in the publishing transaction. Without an"
            + " active transaction the after-commit listeners are skipped silently and nothing is"
            + " registered: the use case succeeds, the other contexts never hear of it. The use"
            + " case that publishes owns the boundary - either declarative transaction metadata"
            + " (the configured transactional annotation on the class or the executing method) or"
            + " an explicit TransactionBoundary.inTransaction(...) around save and publish. Checked"
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
                .or()
                .areAssignableTo(InputPort.class)
                .and()
                .areNotInterfaces()
                .should(
                    beTransactionalWhenPublishing(
                        layout.frameworkAnnotations().transactional()))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.")
    .checking(
        "For every method that calls a DomainEventPublisher, every route from each entry point"
            + " down to it is covered: the class carries one of the configured transactional"
            + " annotations, or every uncovered unit on the route is either annotated or calls"
            + " TransactionBoundary.inTransaction. A covered caller does not cover a second route"
            + " to the same helper. With an empty transactional role only the explicit boundary"
            + " counts. Whether the publish call sits inside the inTransaction block is not"
            + " checked - ArchUnit folds a lambda into its enclosing method.")
```

## Helpers
