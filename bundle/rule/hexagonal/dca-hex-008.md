---
type: Rule
id: DCA-HEX-008
title: "Classes named *Repository must reside in the outgoing adapter package (name-based discovery of unmarked repositories)"
rule: "Repository implementations are secondary adapters (outgoing ports)."
constraint: "Classes named *Repository must reside in the outgoing adapter package (name-based discovery of unmarked repositories)."
selects: Non-interface classes anywhere on the classpath under scan whose simple name ends with Repository - implementations and abstract base classes alike. The Repository port interfaces themselves are not selected.
checks: "Each resides in <module>.adapter.outgoing.. of some module root. Whether the class implements a Repository port is not checked - only the name is. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-008"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Classes named *Repository must reside in the outgoing adapter package (name-based discovery of unmarked repositories)

## Selection

Non-interface classes anywhere on the classpath under scan whose simple name ends with Repository - implementations and abstract base classes alike. The Repository port interfaces themselves are not selected.

## Check

Each resides in <module>.adapter.outgoing.. of some module root. Whether the class implements a Repository port is not checked - only the name is. An empty selection passes.

## .NET reading

**Selection.** Classes anywhere in the loaded assemblies whose name ends with Repository - implementations and abstract base classes alike. The IRepository port interfaces themselves are not selected.

**Check.** Each resides in <module>.Adapter.Outgoing of some module root. Whether the class implements an IRepository port is not checked - only the name is. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-008",
        "Classes named *Repository must reside in the outgoing adapter package (name-based discovery of unmarked repositories)",
        "Repository implementations are secondary adapters (outgoing ports)",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("Repository")
                .and()
                .areNotInterfaces()
                .should()
                .resideInAnyPackage(arch.allOutgoingAdapterPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan whose simple name"
            + " ends with Repository - implementations and abstract base classes alike. The"
            + " Repository port interfaces themselves are not selected.")
    .checking(
        "Each resides in <module>.adapter.outgoing.. of some module root. Whether the"
            + " class implements a Repository port is not checked - only the name is. An empty"
            + " selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allOutgoingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-HEX-008",
        "Classes named *Repository must reside in the outgoing adapter namespace (name-based discovery of unmarked repositories)",
        "Repository implementations are secondary adapters (outgoing ports)",
        arch => Classes().That().HaveNameEndingWith("Repository")
            .Should().ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllOutgoingAdapterPatterns())))
    .Selecting(
        "Classes anywhere in the loaded assemblies whose name ends with Repository -"
            + " implementations and abstract base classes alike. The IRepository port interfaces"
            + " themselves are not selected.")
    .Checking(
        "Each resides in <module>.Adapter.Outgoing of some module root. Whether the"
            + " class implements an IRepository port is not checked - only the name is. An empty"
            + " selection passes.")
```

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
