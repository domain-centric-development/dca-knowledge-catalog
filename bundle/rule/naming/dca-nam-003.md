---
type: Rule
id: DCA-NAM-003
title: InputPort interfaces must end with 'InputPort'
rule: "Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)."
constraint: InputPort interfaces must end with 'InputPort'.
selects: "Interfaces in <module>.application.. of every module root that are assignable to InputPort, except the types the inputPort and useCase roles name and those named exactly InputPort or UseCase."
checks: "The simple name ends with the configured input-port suffix (InputPort by default InputPort) - no prefix is required, because Java interfaces carry none; the .NET twin additionally requires the platform's I prefix. Classes and records are not selected, and an interface extending InputPort outside an application package is not checked. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-003"
status: enforced
maturity: released
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/NamingRules.cs
---

# InputPort interfaces must end with 'InputPort'

## Selection

Interfaces in <module>.application.. of every module root that are assignable to InputPort, except the types the inputPort and useCase roles name and those named exactly InputPort or UseCase.

## Check

The simple name ends with the configured input-port suffix (InputPort by default InputPort) - no prefix is required, because Java interfaces carry none; the .NET twin additionally requires the platform's I prefix. Classes and records are not selected, and an interface extending InputPort outside an application package is not checked. An empty selection passes.

## .NET reading

**Selection.** Interfaces in <module>.Application of every module root that are assignable to IInputPort, except the types the InputPort and UseCase roles name and those named exactly InputPort, IInputPort, UseCase or IUseCase.

**Check.** The name starts with I and ends with the configured input-port suffix (InputPort, by default InputPort: IPlaceOrderInputPort). The I prefix is the platform convention and is checked here only: the Java twin requires the suffix and nothing else, because Java interfaces carry no prefix. Classes and records are not selected, and an interface extending IInputPort outside an application namespace is not checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-003",
        "InputPort interfaces must end with '" + suffix + "'",
        "Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)",
        arch ->
            classes()
                .that(arch.inApplication())
                .and()
                .areInterfaces()
                .and(arch.layout().markers().is("inputPort"))
                .and()
                .doNotHaveFullyQualifiedName(arch.layout().markers().inputPort())
                .and()
                .doNotHaveFullyQualifiedName(arch.layout().markers().useCase())
                .and()
                .doNotHaveSimpleName("InputPort")
                .and()
                .doNotHaveSimpleName("UseCase")
                .should()
                .haveSimpleNameEndingWith(suffix)
                .allowEmptyShould(true))
    .selecting(
        "Interfaces in <module>.application.. of every module root that are assignable to"
            + " InputPort, except the types the inputPort and useCase roles name and those named"
            + " exactly InputPort or UseCase.")
    .checking(
        "The simple name ends with the configured input-port suffix ("
            + suffix
            + " by default InputPort) - no prefix is required, because Java interfaces"
            + " carry none; the .NET twin additionally requires the platform's I prefix."
            + " Classes and records are not selected, and an"
            + " interface extending InputPort outside an application package is not checked. An"
            + " empty selection passes.",
        "rename the interface to <UseCaseName>" + suffix)
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inApplication()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-NAM-003",
        $"InputPort interfaces must end with '{layout.InputPortSuffix}'",
        "Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)",
        arch =>
        {
            var suffix = arch.Layout.InputPortSuffix;
            var markers = arch.Layout.Markers;
            var violations = arch.Interfaces
                .Where(i => arch.InApplication(i)
                    && IsRole(arch, i, nameof(DcaMarkers.InputPort))
                    && !IsBaseInputPortName(i.Name)
                    && !IsRoleType(i, markers.InputPort)
                    && !IsRoleType(i, markers.UseCase)
                    && !(i.Name.StartsWith("I", StringComparison.Ordinal) && i.Name.Split('`')[0].EndsWith(suffix, StringComparison.Ordinal)))
                .Select(i => $"{i.FullName} is an input port but is not named I*{suffix}")
                .ToList();
            DcaRule.Fail(
                $"InputPort interfaces must end with '{suffix}'",
                violations,
                $"rename the interface to I<UseCaseName>{suffix}");
        })
    .Selecting(
        "Interfaces in <module>.Application of every module root that are assignable to"
            + " IInputPort, except the types the InputPort and UseCase roles name and those named"
            + " exactly InputPort, IInputPort, UseCase or IUseCase.")
    .Checking(
        "The name starts with I and ends with the configured input-port suffix ("
            + layout.InputPortSuffix
            + ", by default InputPort: IPlaceOrderInputPort). The I prefix is the"
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
