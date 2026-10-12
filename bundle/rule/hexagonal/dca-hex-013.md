---
type: Rule
id: DCA-HEX-013
title: Outgoing Adapters must not depend on input ports
rule: "An outgoing adapter is driven: the application calls it through an output port. One that calls an input port drives the application instead - it is an incoming adapter filed on the wrong side, and the call it makes runs a second use case from inside the first one's outgoing edge."
constraint: Outgoing Adapters must not depend on input ports.
selects: "Classes in <module>.adapter.outgoing.. of every module root."
checks: "No dependency on a type assignable to InputPort - the input port interfaces and the use case classes implementing them, of any module. Calling another module's published api is not a dependency on an input port, even where that api delegates to one - only direct dependencies are read. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-013"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Outgoing Adapters must not depend on input ports

## Selection

Classes in <module>.adapter.outgoing.. of every module root.

## Check

No dependency on a type assignable to InputPort - the input port interfaces and the use case classes implementing them, of any module. Calling another module's published api is not a dependency on an input port, even where that api delegates to one - only direct dependencies are read. An empty selection passes.

## .NET reading

**Selection.** Classes in <module>.Adapter.Outgoing of every module root.

**Check.** No dependency on a type assignable to IInputPort - the input port interfaces and the use case classes implementing them, of any module. Calling another module's published api is not a dependency on an input port, even where that api delegates to one - only direct dependencies are read; constructor parameters are read from the runtime type as well, so a port injected into an adapter whose members are all async is still found. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-013",
        "Outgoing Adapters must not depend on input ports",
        "An outgoing adapter is driven: the application calls it through an output port. One that"
            + " calls an input port drives the application instead - it is an incoming adapter"
            + " filed on the wrong side, and the call it makes runs a second use case from inside"
            + " the first one's outgoing edge",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allOutgoingAdapterPatterns())
                .should()
                .dependOnClassesThat()
                .areAssignableTo(arch.layout().markers().inputPort())
                .allowEmptyShould(true))
    .selecting("Classes in <module>.adapter.outgoing.. of every module root.")
    .checking(
        "No dependency on a type assignable to InputPort - the input port interfaces and the use"
            + " case classes implementing them, of any module. Calling another module's published"
            + " api is not a dependency on an input port, even where that api delegates to one"
            + " - only direct dependencies are read. An empty selection passes.",
        "move the class to the incoming adapter package, or let the use case reach the"
            + " capability through an output port")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allOutgoingAdapterPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-HEX-013",
        "Outgoing Adapters must not depend on input ports",
        "An outgoing adapter is driven: the application calls it through an output port. One that"
            + " calls an input port drives the application instead - it is an incoming adapter"
            + " filed on the wrong side, and the call it makes runs a second use case from inside"
            + " the first one's outgoing edge",
        arch =>
        {
            var outgoing = DcaLayout.AnyOf(arch.AllOutgoingAdapterPatterns());
            var violations = new List<string>();
            foreach (var adapter in arch.Classes.Where(c => InNamespace(c, outgoing)))
            {
                var ports = adapter.Dependencies
                    .Select(d => d.Target)
                    .Where(t => !t.IsGenericParameter && IsAssignableTo(arch, t, arch.Layout.Markers.InputPort))
                    .Select(t => t.FullName);
                var runtime = arch.RuntimeType(adapter);
                if (runtime is not null)
                {
                    ports = ports.Concat(runtime
                        .GetConstructors(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance)
                        .SelectMany(c => c.GetParameters())
                        .Select(p => p.ParameterType)
                        .Where(t => DcaMarkers.IsAssignableToByName(t, arch.Layout.Markers.InputPort))
                        .Select(t => t.FullName!));
                }

                violations.AddRange(ports.Distinct()
                    .Select(p => $"{adapter.FullName} depends on the input port {p}"));
            }

            DcaRule.Fail(
                "Outgoing Adapters must not depend on input ports",
                violations.Distinct().OrderBy(v => v, StringComparer.Ordinal).ToList(),
                "move the class to the incoming adapter namespace, or let the use case reach the"
                    + " capability through an output port");
        })
    .Selecting("Classes in <module>.Adapter.Outgoing of every module root.")
    .Checking(
        "No dependency on a type assignable to IInputPort - the input port interfaces and the use"
            + " case classes implementing them, of any module. Calling another module's published"
            + " api is not a dependency on an input port, even where that api delegates to one"
            + " - only direct dependencies are read; constructor parameters are read from the"
            + " runtime type as well, so a port injected into an adapter whose members are all"
            + " async is still found. An empty selection passes.")
```

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
