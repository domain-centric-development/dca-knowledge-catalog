---
type: Rule
id: DCA-LAY-005
title: The shared kernel's output-port markers must all be interfaces
rule: "port.out contains outbound port interfaces (Repository, OutputPort, DomainEventPublisher) shared across all bounded contexts. These must be interfaces to ensure the application layer remains framework-independent and follows the Dependency Inversion Principle. Implementations belong in infrastructure or adapter packages."
constraint: The shared kernel's output-port markers must all be interfaces.
selects: Classes in the building-blocks package hexagonal.port.out.. on the classpath under scan.
checks: "Each is an interface. The project's own output ports in application.shared are not selected; when the building-blocks package is not imported, the rule passes."
enforced_by: "LayeredRules#DCA-LAY-005"
status: enforced
rule_set: layered
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
---

## Selection

Classes in the building-blocks package hexagonal.port.out.. on the classpath under scan.

## Check

Each is an interface. The project's own output ports in application.shared are not selected; when the building-blocks package is not imported, the rule passes.

## .NET reading

**Selection.** Types declared in the building-blocks namespace DomainCentric.BuildingBlocks.Hexagonal.Ports.Out, read by reflection from the building-blocks assembly rather than from the scanned architecture. Compiler-generated types (closures, async state machines of default interface methods) are not selected.

**Check.** Each is an interface. The project's own output ports in Application.Shared are not selected; the rule passes when no non-interface type is found.

## Implementation

```java
DcaRule.of(
        "DCA-LAY-005",
        "The shared kernel's output-port markers must all be interfaces",
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

## Applies to markers

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
