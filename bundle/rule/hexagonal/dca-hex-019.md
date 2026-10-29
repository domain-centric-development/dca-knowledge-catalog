---
type: Rule
id: DCA-HEX-019
title: Output port implementations are placed in the outgoing adapters
rule: "An output port is what the application needs from outside; whatever implements it is an outgoing adapter - the implemented port says so. An implementation placed in the infrastructure package, the application, the domain or in no layer at all is outside the selection of every rule written for outgoing adapters, and infrastructure then holds behaviour instead of wiring alone."
constraint: Output port implementations are placed in the outgoing adapters.
selects: "Non-interface classes anywhere under scan assignable to the output-port role - repositories, stores, event publishers and every other output port alike, abstract base classes and anonymous classes included. A lambda or a method reference is no class under scan and is not selected. Not selected: a class in an infrastructure package that depends on a type assignable to the input-port role - the bridge that hands an output port a second use case, which is wiring."
checks: "Each is placed in the outgoing adapter layer - by default <module>.adapter.outgoing.., or wherever the layout's outgoing-adapter marker places it; a class the layout places in no layer is reported as well. DCA-TAC-015 and DCA-TAC-020 hold repositories and stores the same way in the tactical set."
enforced_by: "HexagonalRules#DCA-HEX-019"
status: enforced
maturity: experimental
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Output port implementations are placed in the outgoing adapters

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Non-interface classes anywhere under scan assignable to the output-port role - repositories, stores, event publishers and every other output port alike, abstract base classes and anonymous classes included. A lambda or a method reference is no class under scan and is not selected. Not selected: a class in an infrastructure package that depends on a type assignable to the input-port role - the bridge that hands an output port a second use case, which is wiring.

## Check

Each is placed in the outgoing adapter layer - by default <module>.adapter.outgoing.., or wherever the layout's outgoing-adapter marker places it; a class the layout places in no layer is reported as well. DCA-TAC-015 and DCA-TAC-020 hold repositories and stores the same way in the tactical set.

## .NET reading

**Selection.** Classes of the scan assignable to IOutputPort - repositories, stores, event publishers and every other output port alike, abstract base classes included; compiler-generated classes are not selected. Not selected: a class in an infrastructure namespace that depends on a type assignable to IInputPort - the bridge that hands an output port a second use case, which is wiring.

**Check.** Each is placed in the outgoing adapter layer - by default <Module>.Adapter.Outgoing, or wherever the layout's outgoing-adapter marker places it - by a layer attribute on the class, on its namespace or its assembly, or by the namespace path; a class the layout places in no layer is reported as well. DCA-TAC-015 and DCA-TAC-020 hold repositories and stores the same way in the tactical set.

## Implementation

```java
DcaRule.check(
        "DCA-HEX-019",
        "Output port implementations are placed in the outgoing adapters",
        "An output port is what the application needs from outside; whatever implements it is an"
            + " outgoing adapter - the implemented port says so. An implementation placed in the"
            + " infrastructure package, the application, the domain or in no layer at all is"
            + " outside the selection of every rule written for outgoing adapters, and"
            + " infrastructure then holds behaviour instead of wiring alone",
        arch -> {
          CollectedViolations violations =
              CollectedViolations.withHeader(
                  "Output port implementations are placed in the outgoing adapters\nbecause"
                      + " whatever implements an output port is an outgoing adapter");
          var outputPort = arch.layout().markers().is("outputPort");
          var inputPort = arch.layout().markers().is("inputPort");
          for (var type : arch.classes()) {
            if (type.isInterface() || !outputPort.test(type)) {
              continue;
            }
            var placement = arch.placement(type);
            if (placement.isEmpty()) {
              violations.add(
                  type.getName()
                      + " implements an output port but sits in no layer - declare the layer"
                      + " of its package (DCA-LAY-007 lists such classes), or switch the"
                      + " hexagonal set off while the project has no layers");
              continue;
            }
            if (placement.get().layer() == DcaLayout.Layer.OUTGOING_ADAPTER) {
              continue;
            }
            boolean bridge =
                placement.get().layer() == DcaLayout.Layer.INFRASTRUCTURE
                    && type.getDirectDependenciesFromSelf().stream()
                        .anyMatch(d -> inputPort.test(d.getTargetClass()));
            if (!bridge) {
              violations.add(
                  type.getName()
                      + " implements an output port but is placed in the "
                      + placement.get().layer().role()
                      + " layer ("
                      + placement.get().source().name().toLowerCase(java.util.Locale.ROOT)
                      + " "
                      + placement.get().layerPackage()
                      + ")");
            }
          }
          violations.throwIfAny();
        })
    .experimental()
    .selecting(
        "Non-interface classes anywhere under scan assignable to the output-port role -"
            + " repositories, stores, event publishers and every other output port alike,"
            + " abstract base classes and anonymous classes included. A lambda or a method"
            + " reference is no class under scan and is not selected. Not selected: a class in"
            + " an infrastructure package that depends on a type assignable to the input-port"
            + " role - the bridge that hands an output port a second use case, which is wiring.")
    .checking(
        "Each is placed in the outgoing adapter layer - by default <module>.adapter.outgoing..,"
            + " or wherever the layout's outgoing-adapter marker places it; a class the layout"
            + " places in no layer is reported as well. DCA-TAC-015 and"
            + " DCA-TAC-020 hold repositories and stores the same way in the tactical set.",
        "move the implementation into the outgoing adapter layer of its module; the"
            + " configuration in infrastructure only wires it to its port")
```

## Helpers

### `CollectedViolations.check`

```java
/** Evaluates every rule, then throws all their violations at once. */
  static void check(List<ArchRule> rules, JavaClasses classes) {
    CollectedViolations collected = withoutHeader();
    rules.forEach(rule -> collected.addAll(rule, classes));
    collected.throwIfAny();
  }
```

### `CollectedViolations.withHeader`

```java
/** A collector whose report starts with the given statement of what the rule demands. */
  static CollectedViolations withHeader(String header) {
    return new CollectedViolations(header);
  }
```

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
}
```

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
  }
```

### `CollectedViolations.throwIfAny`

```java
/**
   * Throws the collected violations as one {@link DcaRuleViolation}; nothing when there are none.
   */
  void throwIfAny() {
    if (!violations.isEmpty()) {
      throw new DcaRuleViolation(header, violations);
    }
  }
```

### `CollectedViolations.withoutHeader`

```java
/** A collector whose report is the bare list of violations. */
  static CollectedViolations withoutHeader() {
    return new CollectedViolations("");
  }
```

### `CollectedViolations.addAll`

```java
/**
   * Evaluates one ArchUnit rule and records each of its violation details, suffixed with the
   * explanation of what the rule was checking — the detail alone ({@code Class A depends on B})
   * does not say why that dependency is wrong.
   */
  void addAll(ArchRule rule, JavaClasses classes, String explanation) {
    for (String detail : rule.evaluate(classes).getFailureReport().getDetails()) {
      add(explanation.isEmpty() ? detail : detail + " - " + explanation);
    }
  }

/** Evaluates one ArchUnit rule and records its violation details as they are. */
  void addAll(ArchRule rule, JavaClasses classes) {
    addAll(rule, classes, "");
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()`, `placement()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-HEX-019",
        "Output port implementations are placed in the outgoing adapters",
        "An output port is what the application needs from outside; whatever implements it is an outgoing"
            + " adapter - the implemented port says so. An implementation placed in the infrastructure namespace,"
            + " the application, the domain or in no layer at all is outside the selection of every rule written"
            + " for outgoing adapters, and infrastructure then holds behaviour instead of wiring alone",
        arch =>
        {
            var violations = new List<string>();
            foreach (var type in arch.Classes.Where(c => !c.IsCompilerGenerated && IsRole(arch, c, nameof(DcaMarkers.OutputPort))))
            {
                var placement = arch.PlacementOf(type);
                if (placement is null)
                {
                    violations.Add($"{type.FullName} implements an output port but sits in no layer - declare the layer"
                        + " of its namespace (DCA-LAY-007 lists such types), or switch the hexagonal set off while the"
                        + " project has no layers");
                    continue;
                }

                if (placement.Layer == DcaLayout.Layer.OutgoingAdapter)
                {
                    continue;
                }

                if (placement.Layer == DcaLayout.Layer.Infrastructure && DependsOnAnInputPort(arch, type))
                {
                    continue;
                }

                violations.Add($"{type.FullName} implements an output port but is placed in the {DcaLayout.RoleOf(placement.Layer)}"
                    + $" layer ({placement.Source.ToString().ToLowerInvariant()} {placement.LayerNamespace})");
            }

            DcaRule.Fail(
                "Output port implementations are placed in the outgoing adapters",
                violations.OrderBy(v => v, StringComparer.Ordinal).ToList(),
                "move the implementation into the outgoing adapter layer of its module; the configuration in infrastructure only wires it to its port");
        })
    .Experimental()
    .Selecting(
        "Classes of the scan assignable to IOutputPort - repositories, stores, event publishers and every other"
            + " output port alike, abstract base classes included; compiler-generated classes are not selected."
            + " Not selected: a class in"
            + " an infrastructure namespace that depends on a type assignable to IInputPort - the bridge that"
            + " hands an output port a second use case, which is wiring.")
    .Checking(
        "Each is placed in the outgoing adapter layer - by default <Module>.Adapter.Outgoing, or wherever the"
            + " layout's outgoing-adapter marker places it - by a layer attribute on the class, on its namespace or"
            + " its assembly, or by the namespace path; a class the layout places in no layer is reported as well."
            + " DCA-TAC-015 and DCA-TAC-020 hold repositories and"
            + " stores the same way in the tactical set.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
