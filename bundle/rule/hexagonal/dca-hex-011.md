---
type: Rule
id: DCA-HEX-011
title: "Incoming Adapters must depend on input port interfaces, not on use case classes"
rule: "A driving adapter drives the application through its port. Injecting the concrete implementation instead couples the adapter to one realisation of the use case, defeats the Dependency Inversion Principle the port exists for, and makes the adapter untestable without the real use case and everything it depends on."
constraint: "Incoming Adapters must depend on input port interfaces, not on use case classes."
selects: "Classes in <module>.adapter.incoming.. of every module root, event consumers included."
checks: "No dependency on a use case implementation: a non-interface class assignable to InputPort, directly or through a *InputPort interface - abstract base classes included. Depending on the input port interfaces themselves is what the rule expects. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-011"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Incoming Adapters must depend on input port interfaces, not on use case classes

## Selection

Classes in <module>.adapter.incoming.. of every module root, event consumers included.

## Check

No dependency on a use case implementation: a non-interface class assignable to InputPort, directly or through a *InputPort interface - abstract base classes included. Depending on the input port interfaces themselves is what the rule expects. An empty selection passes.

## .NET reading

**Selection.** Classes in <module>.Adapter.Incoming of every module root, event consumers included.

**Check.** No dependency on a use case implementation: a class assignable to IInputPort, directly or through an I*InputPort interface - abstract base classes included. Depending on the input port interfaces themselves is what the rule expects. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-011",
        "Incoming Adapters must depend on input port interfaces, not on use case classes",
        "A driving adapter drives the application through its port. Injecting the concrete"
            + " implementation instead couples the adapter to one realisation of the use case,"
            + " defeats the Dependency Inversion Principle the port exists for, and makes the"
            + " adapter untestable without the real use case and everything it depends on",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .should()
                .dependOnClassesThat(useCaseImplementations(arch.layout().markers()))
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.adapter.incoming.. of every module root, event consumers"
            + " included.")
    .checking(
        "No dependency on a use case implementation: a non-interface class assignable to"
            + " InputPort, directly or through a *InputPort interface - abstract base classes"
            + " included. Depending on the input port interfaces themselves is what the rule"
            + " expects. An empty selection passes.")
```

## Helpers

### `useCaseImplementations`

```java
/** A use case implementation: a class (never an interface) behind an {@link InputPort}. */
  private static DescribedPredicate<JavaClass> useCaseImplementations(DcaMarkers markers) {
    return new DescribedPredicate<>("are use case implementations rather than input ports") {
      @Override
      public boolean test(JavaClass javaClass) {
        return !javaClass.isInterface() && javaClass.isAssignableTo(markers.inputPort());
      }
    };
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-HEX-011",
        "Incoming Adapters must depend on input port interfaces, not on use case classes",
        "A driving adapter drives the application through its port. Injecting the concrete"
            + " implementation instead couples the adapter to one realisation of the use case,"
            + " defeats the Dependency Inversion Principle the port exists for, and makes the"
            + " adapter untestable without the real use case and everything it depends on",
        arch =>
        {
            var violations = arch.Classes
                .Where(c => InNamespace(c, DcaLayout.AnyOf(arch.AllIncomingAdapterPatterns())))
                .SelectMany(c => c.Dependencies
                    .Select(d => d.Target)
                    .Where(t => IsUseCaseImplementation(arch, t))
                    .Select(t => $"{c.FullName} depends on the use case class {t.FullName}"))
                .Distinct()
                .OrderBy(v => v, StringComparer.Ordinal)
                .ToList();
            DcaRule.Fail(
                "Incoming Adapters must depend on input port interfaces, not on use case classes",
                violations,
                "inject the I<UseCaseName>InputPort interface instead of the <UseCaseName> class");
        })
    .Selecting(
        "Classes in <module>.Adapter.Incoming of every module root, event consumers"
            + " included.")
    .Checking(
        "No dependency on a use case implementation: a class assignable to"
            + " IInputPort, directly or through an I*InputPort interface - abstract base classes"
            + " included. Depending on the input port interfaces themselves is what the rule"
            + " expects. An empty selection passes.")
```

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
