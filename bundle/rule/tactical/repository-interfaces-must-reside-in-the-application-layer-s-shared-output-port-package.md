---
type: Rule
id: DCA-TAC-014
title: Repository interfaces must reside in the application layer's shared output-port package
rule: "Repository interfaces are output ports in the application layer (Hexagonal Architecture)."
constraint: Repository interfaces must reside in the application layer's shared output-port package.
selects: "Interfaces anywhere under scan assignable to Repository, whatever their name, the marker Repository itself excluded."
checks: "The interface resides in <module>.application.shared.. of some module root, the shared kernel's included. Implementations are not selected; an empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-014"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Interfaces anywhere under scan assignable to Repository, whatever their name, the marker Repository itself excluded.

## Check

The interface resides in <module>.application.shared.. of some module root, the shared kernel's included. Implementations are not selected; an empty selection passes.

## .NET reading

**Selection.** Interfaces below the root namespace assignable to IRepository, whatever their name; an interface named exactly Repository excluded.

**Check.** The interface resides in <module>.Application.Shared of some module root, the shared kernel's included. Implementations are not selected; an empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-TAC-014",
        "Repository interfaces must reside in the application layer's shared output-port package",
        "Repository interfaces are output ports in the application layer (Hexagonal Architecture)",
        arch ->
            // areAssignableTo, not implement: ArchUnit's implement() matches non-interfaces
            // only.
            classes()
                .that()
                .areInterfaces()
                .and()
                .areAssignableTo(Repository.class)
                .and()
                .doNotHaveSimpleName(REPOSITORY_SUFFIX)
                .should()
                .resideInAnyPackage(arch.allSharedOutputPortPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Interfaces anywhere under scan assignable to Repository, whatever their name, "
            + "the marker Repository itself excluded.")
    .checking(
        "The interface resides in <module>.application.shared.. of some module root, "
            + "the shared kernel's included. Implementations are not selected; an empty "
            + "selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allSharedOutputPortPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
