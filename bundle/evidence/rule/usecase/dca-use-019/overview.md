---
type: Reference
title: Query use cases must not write or publish — Overview
tags: [reference]
evidence_for: /rule/usecase/dca-use-019.md
---

[Full node and context](/rule/usecase/dca-use-019.md). This is an evidence excerpt; retain the parent selection and caveats.

# Query use cases must not write or publish

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix, and whose input the configured query role recognises (by default a simple name ending with Query) - a parameter of a public method, or a type argument of the input port they implement.

## Check

No code unit of the class calls a write on the repository or store role - a method whose name is a write verb alone or followed by a capital (save, delete, remove, add, insert, update, upsert, put, store, write, create, append, archive, purge, clear, set, mark) - nor any method of the domain-event or integration-event publisher role. Calls made by another class the use case delegates to are not followed. An empty selection passes.

## .NET reading

**Selection.** Concrete non-nested application operations selected by IInputPort marker or configured use-case suffix, with loadable runtime types, whose input the configured query role recognises (by default a simple name ending with Query): the input type argument of an implemented IUseCase<TInput, TOutput>, or a parameter of a method that implements an IInputPort interface.

**Check.** No method of the class - async state machines and lambdas included - calls a repository write (IRepository.SaveAsync or DeleteByIdAsync, or a method of a repository or store port whose name starts with Save, Delete, Remove, Add, Insert, Update, Upsert, Put, Store, Write, Create, Append, Archive, Purge, Clear, Set or Mark), or any method of the domain-event or integration-event publisher. Only the class's own calls are read: a write reached through a helper class or a second port is not seen, and a store write under another verb passes. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-USE-019",
        "Query use cases must not write or publish",
        "A read never creates. A query has no side effect: it does not create, save or publish,"
            + " and when nothing exists it answers none. Find-or-create is a command, called"
            + " where the caller is about to change state; a page or an answer that only shows"
            + " what exists asks the query",
        arch ->
            classes()
                .that(useCases(arch, layout))
                .and(takingAQuery(layout))
                .should(notWriteOrPublish(layout.markers()))
                .allowEmptyShould(true))
    .experimental()
    .selecting(
        "Non-interface classes in <module>.application.. that implement InputPort or whose"
            + " simple name ends with the configured use-case suffix, and whose input the"
            + " configured query role recognises (by default a simple name ending with Query)"
            + " - a parameter of a public method, or a type argument of the input port they"
            + " implement.")
    .checking(
        "No code unit of the class calls a write on the repository or store role - a method"
            + " whose name is a write verb alone or followed by a capital (save, delete, remove,"
            + " add, insert, update, upsert, put, store, write, create, append, archive, purge,"
            + " clear, set, mark) - nor any method of the domain-event or integration-event"
            + " publisher role. Calls made by another"
            + " class the use case delegates to are not followed. An empty selection passes.",
        "answer none when nothing exists, and move find-or-create into a command the caller"
            + " runs before it changes state")
```

## Helpers
