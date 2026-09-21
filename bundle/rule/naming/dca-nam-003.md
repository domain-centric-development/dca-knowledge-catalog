---
type: Rule
id: DCA-NAM-003
title: InputPort interfaces must end with 'InputPort'
rule: "Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)."
constraint: InputPort interfaces must end with 'InputPort'.
selects: "Interfaces in <module>.application.. of every module root that are assignable to InputPort, except those named exactly InputPort or UseCase."
checks: "The simple name ends with InputPort - no prefix is required, because Java interfaces carry none; the .NET twin additionally requires the platform's I prefix. Classes and records are not selected, and an interface extending InputPort outside an application package is not checked. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-003"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/NamingRules.cs
---

# InputPort interfaces must end with 'InputPort'

## Selection

Interfaces in <module>.application.. of every module root that are assignable to InputPort, except those named exactly InputPort or UseCase.

## Check

The simple name ends with InputPort - no prefix is required, because Java interfaces carry none; the .NET twin additionally requires the platform's I prefix. Classes and records are not selected, and an interface extending InputPort outside an application package is not checked. An empty selection passes.

## .NET reading

**Selection.** Interfaces in <module>.Application of every module root that are assignable to IInputPort, except those named exactly InputPort, IInputPort, UseCase or IUseCase.

**Check.** The name starts with I and ends with InputPort (IPlaceOrderInputPort). The I prefix is the platform convention and is checked here only: the Java twin requires the suffix and nothing else, because Java interfaces carry no prefix. Classes and records are not selected, and an interface extending IInputPort outside an application namespace is not checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-003",
        "InputPort interfaces must end with 'InputPort'",
        "Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .areInterfaces()
                .and()
                .areAssignableTo(arch.layout().markers().inputPort())
                .and()
                .doNotHaveSimpleName("InputPort")
                .and()
                .doNotHaveSimpleName("UseCase")
                .should()
                .haveSimpleNameEndingWith("InputPort")
                .allowEmptyShould(true))
    .selecting(
        "Interfaces in <module>.application.. of every module root that are assignable to"
            + " InputPort, except those named exactly InputPort or UseCase.")
    .checking(
        "The simple name ends with InputPort - no prefix is required, because Java interfaces"
            + " carry none; the .NET twin additionally requires the platform's I prefix."
            + " Classes and records are not selected, and an"
            + " interface extending InputPort outside an application package is not checked. An"
            + " empty selection passes.",
        "rename the interface to <UseCaseName>InputPort")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-NAM-003",
        "InputPort interfaces must end with 'InputPort'",
        "Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)",
        arch =>
        {
            var violations = arch.Interfaces
                .Where(i => InNamespace(i, DcaLayout.AnyOf(arch.AllApplicationPatterns()))
                    && IsAssignableTo(arch, i, arch.Layout.Markers.InputPort)
                    && !IsBaseInputPortName(i.Name)
                    && !(i.Name.StartsWith("I", StringComparison.Ordinal) && i.Name.EndsWith("InputPort", StringComparison.Ordinal)))
                .Select(i => $"{i.FullName} is an input port but is not named I*InputPort")
                .ToList();
            DcaRule.Fail(
                "InputPort interfaces must end with 'InputPort'",
                violations,
                "rename the interface to I<UseCaseName>InputPort");
        })
    .Selecting(
        "Interfaces in <module>.Application of every module root that are assignable to"
            + " IInputPort, except those named exactly InputPort, IInputPort, UseCase or IUseCase.")
    .Checking(
        "The name starts with I and ends with InputPort (IPlaceOrderInputPort). The I prefix is the"
            + " platform convention and is checked here only: the Java twin requires the suffix and"
            + " nothing else, because Java interfaces carry no prefix. Classes and records are not"
            + " selected, and an interface extending IInputPort outside an application namespace is"
            + " not checked. An empty selection passes.")
```

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
