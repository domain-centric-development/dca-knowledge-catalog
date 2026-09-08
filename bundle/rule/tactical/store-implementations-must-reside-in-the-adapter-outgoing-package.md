---
type: Rule
id: DCA-TAC-020
title: Store implementations must reside in the adapter.outgoing package
rule: Store implementations are outgoing adapters in bounded contexts.
constraint: Store implementations must reside in the adapter.outgoing package.
selects: "Non-interface classes anywhere under scan assignable to Store, abstract base classes included."
checks: "The class resides in <module>.adapter.outgoing.. of some module root; an empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-020"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Non-interface classes anywhere under scan assignable to Store, abstract base classes included.

## Check

The class resides in <module>.adapter.outgoing.. of some module root; an empty selection passes.

## .NET reading

**Selection.** Non-interface types below the root namespace assignable to IStore, abstract base classes included.

**Check.** The type resides in <module>.Adapter.Outgoing of some module root; an empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-TAC-020",
        "Store implementations must reside in the adapter.outgoing package",
        "Store implementations are outgoing adapters in bounded contexts",
        arch ->
            classes()
                .that()
                .areNotInterfaces()
                .and()
                .areAssignableTo(Store.class)
                .should()
                .resideInAnyPackage(arch.allOutgoingAdapterPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere under scan assignable to Store, abstract base "
            + "classes included.")
    .checking(
        "The class resides in <module>.adapter.outgoing.. of some module root; an empty "
            + "selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allOutgoingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Store](/marker/port-out/store.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
