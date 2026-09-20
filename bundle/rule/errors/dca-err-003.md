---
type: Rule
id: DCA-ERR-003
title: Exceptions declared in the application layer must extend UseCaseException
rule: "A use case that cannot serve a request reports why through its type, so that one incoming adapter can map each outcome onto its protocol and another adapter can map the same outcome onto a different one."
constraint: Exceptions declared in the application layer must extend UseCaseException.
selects: "Classes in <module>.application.. of every module root that are assignable to Throwable - the exception types the application layer declares itself. The base type UseCaseException lives in the building blocks and is not selected."
checks: "Each extends UseCaseException, directly or through an intermediate base class. A subtype of DomainException declared in an application package is reported here as well: a failure of the model belongs to the model. An empty selection passes."
enforced_by: "ErrorHandlingRules#DCA-ERR-003"
status: enforced
rule_set: errors
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Exceptions declared in the application layer must extend UseCaseException

## Selection

Classes in <module>.application.. of every module root that are assignable to Throwable - the exception types the application layer declares itself. The base type UseCaseException lives in the building blocks and is not selected.

## Check

Each extends UseCaseException, directly or through an intermediate base class. A subtype of DomainException declared in an application package is reported here as well: a failure of the model belongs to the model. An empty selection passes.

## .NET reading

**Selection.** Types under <Module>.Application of every module root that are assignable to Exception - the exception types the application layer declares itself. The base type UseCaseException lives in the building blocks and is not selected.

**Check.** Each derives from UseCaseException, directly or through an intermediate base class. A subtype of DomainException declared in an application namespace is reported here as well: a failure of the model belongs to the model. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ERR-003",
        "Exceptions declared in the application layer must extend UseCaseException",
        "A use case that cannot serve a request reports why through its type, so that one"
            + " incoming adapter can map each outcome onto its protocol and another adapter can"
            + " map the same outcome onto a different one",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .areAssignableTo(Throwable.class)
                .should()
                .beAssignableTo(UseCaseException.class)
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.application.. of every module root that are assignable to Throwable"
            + " - the exception types the application layer declares itself. The base type"
            + " UseCaseException lives in the building blocks and is not selected.")
    .checking(
        "Each extends UseCaseException, directly or through an intermediate base class. A"
            + " subtype of DomainException declared in an application package is reported here"
            + " as well: a failure of the model belongs to the model. An empty selection"
            + " passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ERR-003",
    "Exceptions declared in the application layer must extend UseCaseException",
    "A use case that cannot serve a request reports why through its type, so that one incoming"
        + " adapter can map each outcome onto its protocol and another adapter can map the same"
        + " outcome onto a different one",
    arch =>
    {
        var application = new Regex(DcaLayout.AnyOf(arch.AllApplicationPatterns()));
        var violations = ProjectExceptions(arch)
            .Where(t => application.IsMatch(t.Namespace?.FullName ?? ""))
            .Where(t => !IsAssignableTo(t, typeof(UseCaseException)))
            .Select(t => $"{t.FullName} does not extend UseCaseException")
            .ToList();
        DcaRule.Fail("DCA-ERR-003: a use-case failure without the application base type", violations);
    })
    .Selecting(
        "Types under <Module>.Application of every module root that are assignable to Exception - "
        + "the exception types the application layer declares itself. The base type UseCaseException "
        + "lives in the building blocks and is not selected.")
    .Checking(
        "Each derives from UseCaseException, directly or through an intermediate base class. A "
        + "subtype of DomainException declared in an application namespace is reported here as "
        + "well: a failure of the model belongs to the model. An empty selection passes.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
