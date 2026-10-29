---
type: Rule
id: DCA-ERR-003
title: Exceptions declared in the application layer must extend UseCaseException
rule: "A use case that cannot serve a request reports why through its type, so that one incoming adapter can map each outcome onto its protocol and another adapter can map the same outcome onto a different one."
constraint: Exceptions declared in the application layer must extend UseCaseException.
selects: "Classes in <module>.application.. of every module root that are assignable to Throwable and not to DomainException - the exception types the application layer declares itself. The base type UseCaseException lives in the building blocks and is not selected. A subtype of DomainException declared in an application package is not selected either: it is misplaced rather than mis-based, and DCA-ERR-002 owns that case with the remedy that fits it - move the failure to the domain, do not change its base type."
checks: "Each extends UseCaseException, directly or through an intermediate base class. An empty selection passes."
enforced_by: "ErrorHandlingRules#DCA-ERR-003"
status: enforced
maturity: released
rule_set: errors
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Exceptions declared in the application layer must extend UseCaseException

## Selection

Classes in <module>.application.. of every module root that are assignable to Throwable and not to DomainException - the exception types the application layer declares itself. The base type UseCaseException lives in the building blocks and is not selected. A subtype of DomainException declared in an application package is not selected either: it is misplaced rather than mis-based, and DCA-ERR-002 owns that case with the remedy that fits it - move the failure to the domain, do not change its base type.

## Check

Each extends UseCaseException, directly or through an intermediate base class. An empty selection passes.

## .NET reading

**Selection.** Types under <Module>.Application of every module root that are assignable to Exception and not to DomainException - the exception types the application layer declares itself. The base type UseCaseException lives in the building blocks and is not selected. A subtype of DomainException declared in an application namespace is not selected either: it is misplaced rather than mis-based, and DCA-ERR-002 owns that case with the remedy that fits it - move the failure to the domain, do not change its base type.

**Check.** Each derives from UseCaseException, directly or through an intermediate base class. An empty selection passes.

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
                .that(arch.inApplication())
                .and()
                .areAssignableTo(Throwable.class)
                .and(DescribedPredicate.not(arch.layout().markers().is("domainException")))
                .should(LayerConditions.be(arch.layout().markers().is("useCaseException")))
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.application.. of every module root that are assignable to Throwable"
            + " and not to DomainException - the exception types the application layer declares"
            + " itself. The base type UseCaseException lives in the building blocks and is not"
            + " selected. A subtype of DomainException declared in an application package is"
            + " not selected either: it is misplaced rather than mis-based, and DCA-ERR-002"
            + " owns that case with the remedy that fits it - move the failure to the domain,"
            + " do not change its base type.")
    .checking(
        "Each extends UseCaseException, directly or through an intermediate base class. An"
            + " empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inApplication()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
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
        var violations = ProjectExceptions(arch)
            .Where(arch.InApplication)
            // A subtype of DomainException here is misplaced, not mis-based: DCA-ERR-002 owns it
            // and says to move it to the domain. This rule's remedy would turn a broken rule of
            // the model into a use-case failure.
            .Where(t => !arch.Layout.Markers.Is(nameof(DcaMarkers.DomainException), t))
            .Where(t => !arch.Layout.Markers.Is(nameof(DcaMarkers.UseCaseException), t))
            .Select(t => $"{t.FullName} does not extend UseCaseException")
            .ToList();
        DcaRule.Fail("A use-case failure without the application base type", violations);
    })
    .Selecting(
        "Types under <Module>.Application of every module root that are assignable to Exception and "
        + "not to DomainException - the exception types the application layer declares itself. The "
        + "base type UseCaseException lives in the building blocks and is not selected. A subtype of "
        + "DomainException declared in an application namespace is not selected either: it is "
        + "misplaced rather than mis-based, and DCA-ERR-002 owns that case with the remedy that fits "
        + "it - move the failure to the domain, do not change its base type.")
    .Checking(
        "Each derives from UseCaseException, directly or through an intermediate base class. An "
        + "empty selection passes.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
