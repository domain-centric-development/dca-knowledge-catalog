---
type: Rule
id: DCA-TAC-015
title: Repository Implementations must reside in adapter.outgoing package
rule: Repository implementations are outgoing adapters in bounded contexts.
constraint: Repository Implementations must reside in adapter.outgoing package.
selects: "Non-interface classes anywhere under scan assignable to Repository, abstract base classes included."
checks: "The class resides in <module>.adapter.outgoing.. of some module root. An implementation in any other package under scan - a test double, say - is reported; an empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-015"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Non-interface classes anywhere under scan assignable to Repository, abstract base classes included.

## Check

The class resides in <module>.adapter.outgoing.. of some module root. An implementation in any other package under scan - a test double, say - is reported; an empty selection passes.

## .NET reading

**Selection.** Non-interface types below the root namespace assignable to IRepository, abstract base classes included.

**Check.** The type resides in <module>.Adapter.Outgoing of some module root. An implementation anywhere else below the root - a test double, say - is reported; an empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-TAC-015",
        "Repository Implementations must reside in adapter.outgoing package",
        "Repository implementations are outgoing adapters in bounded contexts",
        arch ->
            classes()
                .that()
                .areNotInterfaces()
                .and()
                .areAssignableTo(Repository.class)
                .should()
                .resideInAnyPackage(arch.allOutgoingAdapterPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere under scan assignable to Repository, abstract "
            + "base classes included.")
    .checking(
        "The class resides in <module>.adapter.outgoing.. of some module root. An "
            + "implementation in any other package under scan - a test double, say - is "
            + "reported; an empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allOutgoingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
