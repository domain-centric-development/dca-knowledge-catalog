---
type: Rule
id: DCA-USE-006
title: "Types named *Result reside in the application layer"
rule: Use case result models should be in application layer. Domain Value Objects with 'Result' in name are allowed in domain layer.
constraint: "Types named *Result reside in the application layer."
selects: "Classes under the base package whose simple name ends with Result, that do not implement Value and that are not a sealed domain outcome - a sealed type in a domain package, or a case of one."
checks: "Each resides in an application package of some module root (<module>.application..). A domain value object named *Result is exempt because it implements Value, and a sealed outcome type of the domain - a sum type whose cases the domain returns - is exempt because it is part of the model."
enforced_by: "UseCaseRules#DCA-USE-006"
status: enforced
maturity: released
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Types named *Result reside in the application layer

## Selection

Classes under the base package whose simple name ends with Result, that do not implement Value and that are not a sealed domain outcome - a sealed type in a domain package, or a case of one.

## Check

Each resides in an application package of some module root (<module>.application..). A domain value object named *Result is exempt because it implements Value, and a sealed outcome type of the domain - a sum type whose cases the domain returns - is exempt because it is part of the model.

## .NET reading

**Selection.** Types under the root namespace whose name ends with Result, that do not implement IValue and that are not a closed domain outcome - in a domain namespace, an abstract class or record whose constructors are all private or private protected, so that no other assembly can derive from it, or a direct case of one.

**Check.** Each resides in an application namespace of some module root (<module>.Application). A domain value object named *Result is exempt because it implements IValue, and a closed outcome type of the domain - a sum type whose cases the domain returns, the C# reading of a Java sealed type - is exempt because it is part of the model.

## Implementation

```java
DcaRule.of(
        "DCA-USE-006",
        "Types named *Result reside in the application layer",
        "Use case result models should be in application layer. Domain Value Objects with 'Result'"
            + " in name are allowed in domain layer.",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("Result")
                .and()
                .resideInAnyPackage(layout.basePackage() + "..")
                .and(DescribedPredicate.not(arch.layout().markers().is("value")))
                .and(DescribedPredicate.not(sealedDomainOutcome(arch)))
                .should(LayerConditions.be(arch.inApplication()))
                .allowEmptyShould(true))
    .selecting(
        "Classes under the base package whose simple name ends with Result, that do not"
            + " implement Value and that are not a sealed domain outcome - a sealed type in a"
            + " domain package, or a case of one.")
    .checking(
        "Each resides in an application package of some module root (<module>.application..)."
            + " A domain value object named *Result is exempt because it implements Value, and"
            + " a sealed outcome type of the domain - a sum type whose cases the domain"
            + " returns - is exempt because it is part of the model.")
```

## Helpers

### `sealedDomainOutcome`

```java
/**
   * A sealed type in a domain package, or a direct case of one: a sum type the domain returns,
   * whatever it is named.
   */
  private static DescribedPredicate<JavaClass> sealedDomainOutcome(DcaArchitecture arch) {
    DescribedPredicate<JavaClass> inDomain = arch.inDomain();
    return DescribedPredicate.describe(
        "a sealed domain outcome",
        type ->
            inDomain.test(type)
                && (type.isSealed()
                    || type.getRawSuperclass().map(JavaClass::isSealed).orElse(false)
                    || type.getRawInterfaces().stream().anyMatch(JavaClass::isSealed)));
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inApplication()`, `inDomain()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-USE-006",
        "Types named *Result reside in the application layer",
        "Use case result models should be in application layer. Domain Value Objects with 'Result' in name are allowed in domain layer.",
        arch =>
            Types()
                .That()
                .HaveNameEndingWith("Result")
                .And()
                .ResideInNamespaceMatching(DcaLayout.Below(layout.RootNamespace))
                .And()
                .FollowCustomPredicate(t => !arch.Layout.Markers.Is(nameof(DcaMarkers.Value), t), "are not value objects")
                .And()
                .FollowCustomPredicate(t => !IsClosedDomainOutcome(arch, t), "are not a closed domain outcome")
                .Should()
                .FollowCustomCondition(LayerConditions.PlacedIn(arch.InApplication, "the application layer"), "be in the application layer"))
    .Selecting(
        "Types under the root namespace whose name ends with Result, that do not implement IValue and"
            + " that are not a closed domain outcome - in a domain namespace, an abstract class or record"
            + " whose constructors are all private or private protected, so that no other assembly can derive"
            + " from it, or a direct case of one.")
    .Checking(
        "Each resides in an application namespace of some module root"
            + " (<module>.Application). A domain value object named *Result is exempt because it"
            + " implements IValue, and a closed outcome type of the domain - a sum type whose cases the"
            + " domain returns, the C# reading of a Java sealed type - is exempt because it is part of the"
            + " model.")
```

## Related mentions (heuristic)

- [Value](/marker/tactical/value.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
