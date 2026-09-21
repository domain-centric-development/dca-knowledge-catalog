---
type: Rule
id: DCA-TAC-014
title: "Repository interfaces must reside in the application layer (local to a use case or shared)"
rule: "Repository interfaces are output ports in the application layer (Hexagonal Architecture)."
constraint: "Repository interfaces must reside in the application layer (local to a use case or shared)."
selects: "Interfaces anywhere under scan assignable to Repository, whatever their name, the marker Repository itself excluded."
checks: "The interface resides in <module>.application.. of some module root, the shared kernel's included. Implementations are not selected; an empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-014"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Repository interfaces must reside in the application layer (local to a use case or shared)

## Selection

Interfaces anywhere under scan assignable to Repository, whatever their name, the marker Repository itself excluded.

## Check

The interface resides in <module>.application.. of some module root, the shared kernel's included. Implementations are not selected; an empty selection passes.

## .NET reading

**Selection.** Interfaces below the root namespace assignable to IRepository, whatever their name; an interface named exactly Repository excluded.

**Check.** The interface resides in <module>.Application of some module root, the shared kernel's included. Implementations are not selected; an empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-TAC-014",
        "Repository interfaces must reside in the application layer (local to a use case or shared)",
        "Repository interfaces are output ports in the application layer (Hexagonal Architecture)",
        arch ->
            // areAssignableTo, not implement: ArchUnit's implement() matches non-interfaces
            // only.
            classes()
                .that()
                .areInterfaces()
                .and()
                .areAssignableTo(arch.layout().markers().repository())
                .and()
                .doNotHaveSimpleName(arch.layout().repositorySuffix())
                .should()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Interfaces anywhere under scan assignable to Repository, whatever their name, "
            + "the marker Repository itself excluded.")
    .checking(
        "The interface resides in <module>.application.. of some module root, "
            + "the shared kernel's included. Implementations are not selected; an empty "
            + "selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-014",
    "Repository interfaces must reside in the application layer (local to a use case or shared)",
    "Repository interfaces are output ports in the application layer (Hexagonal Architecture)",
    arch => RequireNamespace(RepositoryInterfaces(arch), DcaLayout.AnyOf(arch.AllApplicationPatterns()), "Repository interfaces", "an application namespace of its module (use-case-local or Shared)"))
    .Selecting(
        "Interfaces below the root namespace assignable to IRepository, whatever "
        + "their name; an interface named exactly Repository excluded.")
    .Checking(
        "The interface resides in <module>.Application of some module root, the "
        + "shared kernel's included. Implementations are not selected; an empty "
        + "selection passes.")
```

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
