---
type: Rule
id: DCA-LAY-005
title: No implementation is placed into the building-blocks output-port package
rule: "port.out contains outbound port interfaces (Repository, OutputPort, DomainEventPublisher) shared across all bounded contexts. These must be interfaces to ensure the application layer remains framework-independent and follows the Dependency Inversion Principle. Implementations belong in infrastructure or adapter packages."
constraint: No implementation is placed into the building-blocks output-port package.
selects: Classes in the building-blocks package hexagonal.port.out.. on the classpath under scan.
checks: "Each is an interface. The project's own output ports in application.shared are not selected; when the building-blocks package is not imported, the rule passes."
enforced_by: "LayeredRules#DCA-LAY-005"
status: enforced
rule_set: layered
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/LayeredRules.cs
---

# No implementation is placed into the building-blocks output-port package

## Selection

Classes in the building-blocks package hexagonal.port.out.. on the classpath under scan.

## Check

Each is an interface. The project's own output ports in application.shared are not selected; when the building-blocks package is not imported, the rule passes.

## .NET reading

**Selection.** Types declared in the building-blocks namespace DomainCentric.BuildingBlocks.Hexagonal.Ports.Out, read from types imported in the architecture, including consumer assemblies. Compiler-generated types (closures, async state machines of default interface methods) are not selected.

**Check.** Each is an interface. The project's own output ports in Application.Shared are not selected; the rule passes when no non-interface type is found.

## Implementation

```java
DcaRule.of(
        "DCA-LAY-005",
        "No implementation is placed into the building-blocks output-port package",
        "port.out contains outbound port interfaces (Repository, OutputPort, DomainEventPublisher)"
            + " shared across all bounded contexts. These must be interfaces to ensure the"
            + " application layer remains framework-independent and follows the Dependency"
            + " Inversion Principle. Implementations belong in infrastructure or adapter packages.",
        arch ->
            classes()
                .that()
                .resideInAPackage(DcaLayout.BUILDING_BLOCKS_PORT_OUT_PACKAGE)
                .should()
                .beInterfaces()
                .allowEmptyShould(true))
    .selecting(
        "Classes in the building-blocks package hexagonal.port.out.. on the classpath under"
            + " scan.")
    .checking(
        "Each is an interface. The project's own output ports in application.shared are not"
            + " selected; when the building-blocks package is not imported, the rule passes.")
```
### C# expression

```csharp
DcaRule.Check(
    "DCA-LAY-005",
    title,
    rationale,
    arch =>
    {
        var violations = arch.Architecture.Types.Select(arch.RuntimeType).Where(t => t is not null).Cast<Type>()
            .Where(t => t.Namespace == DcaLayout.BuildingBlocksPortsOutNamespace && !t.IsInterface)
            // closures and async state machines of default interface methods are not port types
            .Where(t => !t.IsDefined(typeof(System.Runtime.CompilerServices.CompilerGeneratedAttribute), false) && !t.Name.Contains('<'))
            .Select(t => $"{t.FullName} is not an interface")
            .ToList();
        DcaRule.Fail($"{title}\nbecause {rationale}", violations);
    })
    .Selecting(
        "Types declared in the building-blocks namespace "
        + "DomainCentric.BuildingBlocks.Hexagonal.Ports.Out, read from types imported in the architecture, including consumer assemblies. Compiler-generated "
        + "types (closures, async state machines of default interface methods) are not selected.")
    .Checking(
        "Each is an interface. The project's own output ports in Application.Shared are not "
        + "selected; the rule passes when no non-interface type is found.")
```

## Related mentions (heuristic)

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
