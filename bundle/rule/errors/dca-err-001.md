---
type: Rule
id: DCA-ERR-001
title: Exceptions declared in the domain layer must extend DomainException
rule: A failure the model raises is a broken business rule and says so through its type; a caller that cannot tell one from the platform's own failures cannot answer either of them properly.
constraint: Exceptions declared in the domain layer must extend DomainException.
selects: "Classes in <module>.domain.. of every module root that are assignable to Throwable - the exception types the domain layer declares itself. The base type DomainException lives in the building blocks and is not selected."
checks: "Each extends DomainException, directly or through an intermediate base class. Where the exception is thrown is not checked - a throw site is not part of the import model - so a guard that raises the platform's argument exception is outside this rule. An empty selection passes."
enforced_by: "ErrorHandlingRules#DCA-ERR-001"
status: enforced
rule_set: errors
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Exceptions declared in the domain layer must extend DomainException

## Selection

Classes in <module>.domain.. of every module root that are assignable to Throwable - the exception types the domain layer declares itself. The base type DomainException lives in the building blocks and is not selected.

## Check

Each extends DomainException, directly or through an intermediate base class. Where the exception is thrown is not checked - a throw site is not part of the import model - so a guard that raises the platform's argument exception is outside this rule. An empty selection passes.

## .NET reading

**Selection.** Types under <Module>.Domain of every module root that are assignable to Exception - the exception types the domain layer declares itself. The base type DomainException lives in the building blocks and is not selected.

**Check.** Each derives from DomainException, directly or through an intermediate base class. Where the exception is thrown is not checked - a throw site is not part of the type model - so a guard that raises the platform's argument exception is outside this rule. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ERR-001",
        "Exceptions declared in the domain layer must extend DomainException",
        "A failure the model raises is a broken business rule and says so through its type; a"
            + " caller that cannot tell one from the platform's own failures cannot answer"
            + " either of them properly",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allDomainPatterns())
                .and()
                .areAssignableTo(Throwable.class)
                .should()
                .beAssignableTo(DomainException.class)
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.domain.. of every module root that are assignable to Throwable -"
            + " the exception types the domain layer declares itself. The base type"
            + " DomainException lives in the building blocks and is not selected.")
    .checking(
        "Each extends DomainException, directly or through an intermediate base class. Where"
            + " the exception is thrown is not checked - a throw site is not part of the import"
            + " model - so a guard that raises the platform's argument exception is outside"
            + " this rule. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ERR-001",
    "Exceptions declared in the domain layer must extend DomainException",
    "A failure the model raises is a broken business rule and says so through its type; a caller"
        + " that cannot tell one from the platform's own failures cannot answer either of them"
        + " properly",
    arch =>
    {
        var domain = new Regex(DcaLayout.AnyOf(arch.AllDomainPatterns()));
        var violations = ProjectExceptions(arch)
            .Where(t => domain.IsMatch(t.Namespace?.FullName ?? ""))
            .Where(t => !IsAssignableTo(t, typeof(DomainException)))
            .Select(t => $"{t.FullName} does not extend DomainException")
            .ToList();
        DcaRule.Fail("DCA-ERR-001: a domain failure without the domain base type", violations);
    })
    .Selecting(
        "Types under <Module>.Domain of every module root that are assignable to Exception - the "
        + "exception types the domain layer declares itself. The base type DomainException lives in "
        + "the building blocks and is not selected.")
    .Checking(
        "Each derives from DomainException, directly or through an intermediate base class. Where "
        + "the exception is thrown is not checked - a throw site is not part of the type model - so "
        + "a guard that raises the platform's argument exception is outside this rule. An empty "
        + "selection passes.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
