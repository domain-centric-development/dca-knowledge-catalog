---
type: Rule
id: DCA-HEX-009
title: Output Ports in application.shared must extend OutputPort
rule: "Top-level interfaces in application.shared are output ports and must extend OutputPort to be part of the port hierarchy. Nested interfaces (e.g. IdentityProvider.Identity) are part of their enclosing port's contract, not ports themselves."
constraint: Output Ports in application.shared must extend OutputPort.
selects: "Top-level interfaces in <module>.application.<shared>.. of every module root, excluding package-info. Nested interfaces are not selected - they belong to their enclosing port's contract."
checks: "The interface is assignable to OutputPort, directly or through Repository, Store, DomainEventPublisher, IntegrationEventPublisher or another OutputPort sub-interface. Classes, records and enums in application.shared are not checked. An empty selection passes. The rule presumes the vocabulary has a common port root: withOutputPort must be set whenever any port role is, because every port of the project is measured against it. A vocabulary that has no such root has nothing this rule can assert - switch the id off rather than pointing the role at an unrelated type."
enforced_by: "HexagonalRules#DCA-HEX-009"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Output Ports in application.shared must extend OutputPort

## Selection

Top-level interfaces in <module>.application.<shared>.. of every module root, excluding package-info. Nested interfaces are not selected - they belong to their enclosing port's contract.

## Check

The interface is assignable to OutputPort, directly or through Repository, Store, DomainEventPublisher, IntegrationEventPublisher or another OutputPort sub-interface. Classes, records and enums in application.shared are not checked. An empty selection passes. The rule presumes the vocabulary has a common port root: withOutputPort must be set whenever any port role is, because every port of the project is measured against it. A vocabulary that has no such root has nothing this rule can assert - switch the id off rather than pointing the role at an unrelated type.

## .NET reading

**Selection.** Top-level interfaces in <module>.Application.Shared of every module root. Nested interfaces are not selected - they belong to their enclosing port's contract.

**Check.** The interface is assignable to IOutputPort, directly or through IRepository, IStore, IDomainEventPublisher, IIntegrationEventPublisher or another IOutputPort sub-interface. Classes, records and enums in Application.Shared are not checked. An empty selection passes. The rule presumes the vocabulary has a common port root: OutputPort must be set whenever any port role is, because every port of the project is measured against it. A vocabulary that has no such root has nothing this rule can assert - switch the id off rather than pointing the role at an unrelated type.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-009",
        "Output Ports in application.shared must extend OutputPort",
        "Top-level interfaces in application.shared are output ports and must extend OutputPort to"
            + " be part of the port hierarchy. Nested interfaces (e.g. IdentityProvider.Identity)"
            + " are part of their enclosing port's contract, not ports themselves",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allSharedOutputPortPatterns())
                .and()
                .areInterfaces()
                .and()
                .areTopLevelClasses()
                .and()
                .haveSimpleNameNotEndingWith("package-info")
                .should()
                .beAssignableTo(arch.layout().markers().outputPort())
                .allowEmptyShould(true))
    .selecting(
        "Top-level interfaces in <module>.application.<shared>.. of every module root,"
            + " excluding package-info. Nested interfaces are not selected - they belong to"
            + " their enclosing port's contract.")
    .checking(
        "The interface is assignable to OutputPort, directly or through Repository,"
            + " Store, DomainEventPublisher, IntegrationEventPublisher or another OutputPort"
            + " sub-interface. Classes, records and enums in application.shared are not checked."
            + " An empty selection passes. The rule presumes the vocabulary has a common port"
            + " root: withOutputPort must be set whenever any port role is, because every port"
            + " of the project is measured against it. A vocabulary that has no such root has"
            + " nothing this rule can assert - switch the id off rather than pointing the role"
            + " at an unrelated type.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allSharedOutputPortPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-HEX-009",
        "Output Ports in Application.Shared must extend IOutputPort",
        "Top-level interfaces in Application.Shared are output ports and must extend IOutputPort to"
            + " be part of the port hierarchy. Nested interfaces (e.g. IIdentityProvider.Identity)"
            + " are part of their enclosing port's contract, not ports themselves",
        arch => Interfaces().That().ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllSharedOutputPortPatterns()))
            .And().FollowCustomPredicate(i => !i.IsNested, "are top-level interfaces")
            .Should().FollowCustomCondition(
                i => new ConditionResult(i, i.IsAssignableTo(arch.Layout.Markers.OutputPort), $"{i.FullName} is not assignable to {arch.Layout.Markers.OutputPort}"),
                "be assignable to the configured output-port marker"))
    .Selecting(
        "Top-level interfaces in <module>.Application.Shared of every module root."
            + " Nested interfaces are not selected - they belong to their enclosing port's"
            + " contract.")
    .Checking(
        "The interface is assignable to IOutputPort, directly or through IRepository,"
            + " IStore, IDomainEventPublisher, IIntegrationEventPublisher or another IOutputPort"
            + " sub-interface. Classes, records and enums in Application.Shared are not checked."
            + " An empty selection passes. The rule presumes the vocabulary has a common port"
            + " root: OutputPort must be set whenever any port role is, because every port of"
            + " the project is measured against it. A vocabulary that has no such root has"
            + " nothing this rule can assert - switch the id off rather than pointing the role"
            + " at an unrelated type.")
```

## Related mentions (heuristic)

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
