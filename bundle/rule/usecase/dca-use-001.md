---
type: Rule
id: DCA-USE-001
title: The base InputPort contract is not redeclared in the project
rule: "Base InputPort interface defines the generic contract for all use cases (Hexagonal Architecture)."
constraint: The base InputPort contract is not redeclared in the project.
selects: Interfaces named InputPort anywhere on the classpath under scan.
checks: The interface resides in the building-blocks package hexagonal.port.in - the generic contract is not redeclared in the project.
enforced_by: "UseCaseRules#DCA-USE-001"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# The base InputPort contract is not redeclared in the project

## Selection

Interfaces named InputPort anywhere on the classpath under scan.

## Check

The interface resides in the building-blocks package hexagonal.port.in - the generic contract is not redeclared in the project.

## .NET reading

**Selection.** Interfaces named InputPort or IInputPort anywhere in the loaded assemblies.

**Check.** The interface resides in the building-blocks namespace Hexagonal.Ports.In - the generic contract is not redeclared in the project.

## Implementation

```java
DcaRule.of(
        "DCA-USE-001",
        "The base InputPort contract is not redeclared in the project",
        "Base InputPort interface defines the generic contract for all use cases (Hexagonal"
            + " Architecture)",
        arch ->
            classes()
                .that()
                .areInterfaces()
                .and()
                .haveSimpleName("InputPort")
                .should()
                .resideInAPackage(DcaLayout.BUILDING_BLOCKS_PORT_IN_PACKAGE)
                .allowEmptyShould(true))
    .selecting("Interfaces named InputPort anywhere on the classpath under scan.")
    .checking(
        "The interface resides in the building-blocks package hexagonal.port.in - the generic contract is not redeclared in the project.")
```
### C# expression

```csharp
DcaRule.Of(
        "DCA-USE-001",
        "The base InputPort contract is not redeclared in the project",
        "Base IInputPort interface defines the generic contract for all use cases (Hexagonal Architecture)",
        arch =>
            Interfaces()
                .That()
                .HaveNameMatching("^I?InputPort$")
                .Should()
                .ResideInNamespaceMatching(DcaLayout.Exactly(DcaLayout.BuildingBlocksPortsInNamespace)))
    .Selecting(
        "Interfaces named InputPort or IInputPort anywhere in the loaded assemblies.")
    .Checking(
        "The interface resides in the building-blocks namespace Hexagonal.Ports.In - the"
            + " generic contract is not redeclared in the project.")
```

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
