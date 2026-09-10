---
type: Rule
id: DCA-USE-006
title: Use Case Result Models must end with 'Result' and reside in application package
rule: Use case result models should be in application layer. Domain Value Objects with 'Result' in name are allowed in domain layer.
constraint: Use Case Result Models must end with 'Result' and reside in application package.
selects: Classes under the base package whose simple name ends with Result and that do not implement Value.
checks: "Each resides in an application package of some module root (<module>.application..). A domain value object named *Result is exempt because it implements Value."
enforced_by: "UseCaseRules#DCA-USE-006"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use Case Result Models must end with 'Result' and reside in application package

## Selection

Classes under the base package whose simple name ends with Result and that do not implement Value.

## Check

Each resides in an application package of some module root (<module>.application..). A domain value object named *Result is exempt because it implements Value.

## .NET reading

**Selection.** Types under the root namespace whose name ends with Result and that do not implement IValue.

**Check.** Each resides in an application namespace of some module root (<module>.Application). A domain value object named *Result is exempt because it implements IValue.

## Implementation

```java
DcaRule.of(
        "DCA-USE-006",
        "Use Case Result Models must end with 'Result' and reside in application package",
        "Use case result models should be in application layer. Domain Value Objects with 'Result'"
            + " in name are allowed in domain layer.",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("Result")
                .and()
                .resideInAnyPackage(layout.basePackage() + "..")
                .and()
                .doNotImplement(Value.class)
                .should()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Classes under the base package whose simple name ends with Result and that do not implement Value.")
    .checking(
        "Each resides in an application package of some module root (<module>.application..). A domain value object named *Result is exempt because it implements Value.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-USE-006",
        "Use Case Result Models must end with 'Result' and reside in application namespace",
        "Use case result models should be in application layer. Domain Value Objects with 'Result' in name are allowed in domain layer.",
        arch =>
            Types()
                .That()
                .HaveNameEndingWith("Result")
                .And()
                .ResideInNamespaceMatching(DcaLayout.Below(layout.RootNamespace))
                .And()
                .DoNotImplementInterface(typeof(IValue))
                .Should()
                .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllApplicationPatterns())))
    .Selecting(
        "Types under the root namespace whose name ends with Result and that do not"
            + " implement IValue.")
    .Checking(
        "Each resides in an application namespace of some module root"
            + " (<module>.Application). A domain value object named *Result is exempt because it"
            + " implements IValue.")
```

## Related mentions (heuristic)

- [Value](/marker/tactical/value.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
