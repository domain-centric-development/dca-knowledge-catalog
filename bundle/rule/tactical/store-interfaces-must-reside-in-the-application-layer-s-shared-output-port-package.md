---
type: Rule
id: DCA-TAC-019
title: Store interfaces must reside in the application layer's shared output-port package
rule: "Store interfaces are output ports in the application layer (Hexagonal Architecture)."
constraint: Store interfaces must reside in the application layer's shared output-port package.
selects: "Interfaces anywhere under scan assignable to Store, whatever their name, the marker Store itself excluded."
checks: "The interface resides in <module>.application.shared.. of some module root, the shared kernel's included. Implementations are not selected; an empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-019"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Interfaces anywhere under scan assignable to Store, whatever their name, the marker Store itself excluded.

## Check

The interface resides in <module>.application.shared.. of some module root, the shared kernel's included. Implementations are not selected; an empty selection passes.

## .NET reading

**Selection.** Interfaces below the root namespace assignable to IStore, whatever their name; an interface named exactly Store excluded.

**Check.** The interface resides in <module>.Application.Shared of some module root, the shared kernel's included. Implementations are not selected; an empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-TAC-019",
        "Store interfaces must reside in the application layer's shared output-port package",
        "Store interfaces are output ports in the application layer (Hexagonal Architecture)",
        arch ->
            classes()
                .that()
                .areInterfaces()
                .and()
                .areAssignableTo(Store.class)
                .and()
                .doNotHaveSimpleName(STORE_SUFFIX)
                .should()
                .resideInAnyPackage(arch.allSharedOutputPortPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Interfaces anywhere under scan assignable to Store, whatever their name, the "
            + "marker Store itself excluded.")
    .checking(
        "The interface resides in <module>.application.shared.. of some module root, "
            + "the shared kernel's included. Implementations are not selected; an empty "
            + "selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allSharedOutputPortPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Store](/marker/port-out/store.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
