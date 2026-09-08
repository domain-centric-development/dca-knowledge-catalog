---
type: Rule
id: DCA-TAC-018
title: "Store interfaces must extend the Store marker, not Repository"
rule: Stores extend the Store marker; Repository is reserved for Aggregate Roots.
constraint: "Store interfaces must extend the Store marker, not Repository."
selects: "Interfaces anywhere under scan whose simple name ends with Store, the marker Store itself excluded."
checks: "The interface is assignable to the Store marker and not assignable to Repository; both must hold. An interface not named *Store is never reported; an empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-018"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Interfaces anywhere under scan whose simple name ends with Store, the marker Store itself excluded.

## Check

The interface is assignable to the Store marker and not assignable to Repository; both must hold. An interface not named *Store is never reported; an empty selection passes.

## .NET reading

**Selection.** Interfaces below the root namespace whose name ends with Store; interfaces named exactly Store or IStore excluded.

**Check.** The interface is assignable to the IStore marker and not assignable to IRepository; both must hold, and each failing alone is reported. An interface not named *Store is never reported; an empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-TAC-018",
        "Store interfaces must extend the Store marker, not Repository",
        "Stores extend the Store marker; Repository is reserved for Aggregate Roots",
        arch ->
            classes()
                .that()
                .areInterfaces()
                .and()
                .haveSimpleNameEndingWith(STORE_SUFFIX)
                .and()
                .doNotHaveSimpleName(STORE_SUFFIX)
                .should()
                .beAssignableTo(Store.class)
                .andShould()
                .notBeAssignableTo(Repository.class)
                .allowEmptyShould(true))
    .selecting(
        "Interfaces anywhere under scan whose simple name ends with Store, the marker "
            + "Store itself excluded.")
    .checking(
        "The interface is assignable to the Store marker and not assignable to "
            + "Repository; both must hold. An interface not named *Store is never reported; "
            + "an empty selection passes.")
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
