---
type: Rule
id: DCA-NAM-001
title: Application layer InputPort implementations must end with 'UseCase'
rule: "InputPort implementations (use cases) should follow consistent naming conventions (Hexagonal Architecture)."
constraint: Application layer InputPort implementations must end with 'UseCase'.
selects: "Non-interface, non-record classes in <module>.application.. of every module root that are assignable to the configured use-case role - through the interface or an intermediate base class."
checks: The simple name ends with the configured use-case suffix. Interfaces and records are not selected; a class assignable only to the input-port role without the use-case role is not selected either. An empty selection passes.
enforced_by: "NamingRules#DCA-NAM-001"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/NamingRules.cs
---

# Application layer InputPort implementations must end with 'UseCase'

## Selection

Non-interface, non-record classes in <module>.application.. of every module root that are assignable to the configured use-case role - through the interface or an intermediate base class.

## Check

The simple name ends with the configured use-case suffix. Interfaces and records are not selected; a class assignable only to the input-port role without the use-case role is not selected either. An empty selection passes.

## .NET reading

**Selection.** Non-record classes in <module>.Application of every module root that implement IUseCase<TInput, TOutput> - directly or through an I*InputPort interface that extends it.

**Check.** The name ends with the configured use-case suffix. Interfaces and records are not selected; a class implementing only IInputPort without IUseCase is not selected either. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-001",
        "Application layer InputPort implementations must end with '"
            + layout.useCaseSuffix()
            + "'",
        "InputPort implementations (use cases) should follow consistent naming conventions"
            + " (Hexagonal Architecture)",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .areNotInterfaces()
                .and()
                .areNotRecords()
                .and()
                .areAssignableTo(arch.layout().markers().useCase())
                .should()
                .haveSimpleNameEndingWith(layout.useCaseSuffix())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface, non-record classes in <module>.application.. of every module root that"
            + " are assignable to the configured use-case role - through the interface or an"
            + " intermediate base class.")
    .checking(
        "The simple name ends with the configured use-case suffix. Interfaces and records are"
            + " not selected; a class assignable only to the input-port role without the"
            + " use-case role is not selected either. An empty selection passes.",
        "rename the class to *" + layout.useCaseSuffix())
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-NAM-001",
        $"Application layer InputPort implementations must end with '{layout.UseCaseSuffix}'",
        "InputPort implementations (use cases) should follow consistent naming conventions (Hexagonal Architecture)",
        arch =>
        {
            var violations = arch.Classes
                .Where(c => InNamespace(c, DcaLayout.AnyOf(arch.AllApplicationPatterns()))
                    && c.IsRecord != true
                    && ImplementsUseCase(arch, c)
                    && !c.Name.EndsWith(arch.Layout.UseCaseSuffix, StringComparison.Ordinal))
                .Select(c => $"{c.FullName} implements an input port but does not end with '{arch.Layout.UseCaseSuffix}'")
                .ToList();
            DcaRule.Fail(
                $"Application layer InputPort implementations must end with '{arch.Layout.UseCaseSuffix}'",
                violations,
                $"rename the class to *{arch.Layout.UseCaseSuffix}");
        })
    .Selecting(
        "Non-record classes in <module>.Application of every module root that implement"
            + " IUseCase<TInput, TOutput> - directly or through an I*InputPort interface that"
            + " extends it.")
    .Checking(
        "The name ends with the configured use-case suffix. Interfaces and records are"
            + " not selected; a class implementing only IInputPort without IUseCase is not"
            + " selected either. An empty selection passes.")
```

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
