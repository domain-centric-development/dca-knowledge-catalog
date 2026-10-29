---
type: Rule
id: DCA-USE-001
title: The base InputPort contract is not redeclared in the project
rule: "Base InputPort interface defines the generic contract for all use cases (Hexagonal Architecture)."
constraint: The base InputPort contract is not redeclared in the project.
selects: "Interfaces named InputPort or IInputPort anywhere on the classpath under scan - both spellings, so the rule means the same in both languages - except the type the inputPort role names."
checks: "The interface resides in the building-blocks package hexagonal.port.in or in the package of the configured inputPort role - the generic contract is declared once, by the vocabulary in use, and not redeclared elsewhere in the project."
enforced_by: "UseCaseRules#DCA-USE-001"
status: enforced
maturity: released
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# The base InputPort contract is not redeclared in the project

## Selection

Interfaces named InputPort or IInputPort anywhere on the classpath under scan - both spellings, so the rule means the same in both languages - except the type the inputPort role names.

## Check

The interface resides in the building-blocks package hexagonal.port.in or in the package of the configured inputPort role - the generic contract is declared once, by the vocabulary in use, and not redeclared elsewhere in the project.

## .NET reading

**Selection.** Interfaces named InputPort or IInputPort anywhere in the loaded assemblies - except the type the InputPort role names.

**Check.** The interface resides in the building-blocks namespace Hexagonal.Ports.In or in the namespace of the configured InputPort role - the generic contract is declared once, by the vocabulary in use, and not redeclared elsewhere in the project.

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
                .and(
                    JavaClass.Predicates.simpleName("InputPort")
                        .or(JavaClass.Predicates.simpleName("IInputPort")))
                .and()
                .doNotHaveFullyQualifiedName(arch.layout().markers().inputPort())
                .should()
                .resideInAnyPackage(
                    Stream.concat(
                            Stream.of(DcaLayout.BUILDING_BLOCKS_PORT_IN_PACKAGE),
                            arch
                                .layout()
                                .markers()
                                .declaringPackagePatternsOf(List.of("inputPort"))
                                .stream())
                        .distinct()
                        .toArray(String[]::new))
                .allowEmptyShould(true))
    .selecting(
        "Interfaces named InputPort or IInputPort anywhere on the classpath under scan - both"
            + " spellings, so the rule means the same in both languages - except the type the"
            + " inputPort role names.")
    .checking(
        "The interface resides in the building-blocks package hexagonal.port.in or in the"
            + " package of the configured inputPort role - the generic contract is declared"
            + " once, by the vocabulary in use, and not redeclared elsewhere in the project.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
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
                .And()
                .FollowCustomPredicate(t => t.FullName != arch.Layout.Markers.InputPort, "are not the type the InputPort role names")
                .Should()
                .ResideInNamespaceMatching(DcaLayout.AnyOf(
                    new[] { DcaLayout.BuildingBlocksPortsInNamespace }
                        .Concat(arch.Layout.Markers.DeclaringNamespacesOf(new[] { nameof(DcaMarkers.InputPort) }))
                        .Distinct(StringComparer.Ordinal)
                        .Select(DcaLayout.Exactly))))
    .Selecting(
        "Interfaces named InputPort or IInputPort anywhere in the loaded assemblies - except the type the"
            + " InputPort role names.")
    .Checking(
        "The interface resides in the building-blocks namespace Hexagonal.Ports.In or in the namespace of"
            + " the configured InputPort role - the generic contract is declared once, by the vocabulary in"
            + " use, and not redeclared elsewhere in the project.")
```

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
