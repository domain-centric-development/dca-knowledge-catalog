---
type: Rule
id: DCA-HEX-019
title: Output port implementations must reside in an outgoing adapter package
rule: "An output port is what the application needs from outside; whatever implements it is an outgoing adapter. An implementation in the infrastructure package, the application or the domain is outside the selection of every rule written for outgoing adapters, and infrastructure then holds behaviour instead of wiring alone."
constraint: Output port implementations must reside in an outgoing adapter package.
selects: "Non-interface classes anywhere under scan assignable to the output-port role - repositories, stores, event publishers and every other output port alike, abstract base classes and anonymous classes included. A lambda or a method reference is no class under scan and is not selected. Not selected: a class in an infrastructure package that depends on a type assignable to the input-port role - the bridge that hands an output port a second use case, which is wiring."
checks: "Each resides in <module>.adapter.outgoing.. of some module root. DCA-TAC-015 and DCA-TAC-020 hold repositories and stores the same way in the tactical set."
enforced_by: "HexagonalRules#DCA-HEX-019"
status: enforced
maturity: experimental
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Output port implementations must reside in an outgoing adapter package

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Non-interface classes anywhere under scan assignable to the output-port role - repositories, stores, event publishers and every other output port alike, abstract base classes and anonymous classes included. A lambda or a method reference is no class under scan and is not selected. Not selected: a class in an infrastructure package that depends on a type assignable to the input-port role - the bridge that hands an output port a second use case, which is wiring.

## Check

Each resides in <module>.adapter.outgoing.. of some module root. DCA-TAC-015 and DCA-TAC-020 hold repositories and stores the same way in the tactical set.

## .NET reading

**Selection.** Classes of the scan assignable to IOutputPort - repositories, stores, event publishers and every other output port alike, abstract base classes included; compiler-generated classes are not selected. Not selected: a class in an infrastructure namespace that depends on a type assignable to IInputPort - the bridge that hands an output port a second use case, which is wiring.

**Check.** Each resides in <Module>.Adapter.Outgoing of some module root. DCA-TAC-015 and DCA-TAC-020 hold repositories and stores the same way in the tactical set.

## Implementation

```java
DcaRule.check(
        "DCA-HEX-019",
        "Output port implementations must reside in an outgoing adapter package",
        "An output port is what the application needs from outside; whatever implements it is an"
            + " outgoing adapter. An implementation in the infrastructure package, the application"
            + " or the domain is outside the selection of every rule written for outgoing"
            + " adapters, and infrastructure then holds behaviour instead of wiring alone",
        arch -> {
          CollectedViolations violations =
              CollectedViolations.withHeader(
                  "Output port implementations must reside in an outgoing adapter package\nbecause"
                      + " whatever implements an output port is an outgoing adapter");
          var outgoing =
              com.tngtech.archunit.core.domain.JavaClass.Predicates.resideInAnyPackage(
                  arch.allOutgoingAdapterPatterns());
          var infrastructure =
              com.tngtech.archunit.core.domain.JavaClass.Predicates.resideInAnyPackage(
                  arch.allInfrastructurePatterns());
          String outputPort = arch.layout().markers().outputPort();
          String inputPort = arch.layout().markers().inputPort();
          for (var type : arch.classes()) {
            if (type.isInterface() || !type.isAssignableTo(outputPort) || outgoing.test(type)) {
              continue;
            }
            boolean bridge =
                infrastructure.test(type)
                    && type.getDirectDependenciesFromSelf().stream()
                        .anyMatch(d -> d.getTargetClass().isAssignableTo(inputPort));
            if (!bridge) {
              violations.add(
                  type.getName() + " implements an output port outside the outgoing adapters");
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
        "Each resides in <module>.adapter.outgoing.. of some module root. DCA-TAC-015 and"
            + " DCA-TAC-020 hold repositories and stores the same way in the tactical set.",
        "move the implementation into the outgoing adapter package of its module; the"
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

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allInfrastructurePatterns()`, `allOutgoingAdapterPatterns()`, `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-HEX-019",
        "Output port implementations must reside in an outgoing adapter package",
        "An output port is what the application needs from outside; whatever implements it is an outgoing"
            + " adapter. An implementation in the infrastructure namespace, the application or the domain is"
            + " outside the selection of every rule written for outgoing adapters, and infrastructure then"
            + " holds behaviour instead of wiring alone",
        arch =>
        {
            var outgoing = DcaLayout.AnyOf(arch.AllOutgoingAdapterPatterns());
            var infrastructure = DcaLayout.AnyOf(arch.AllInfrastructurePatterns());
            var violations = new List<string>();
            foreach (var type in arch.Classes.Where(c => !c.IsCompilerGenerated
                && IsAssignableTo(arch, c, arch.Layout.Markers.OutputPort) && !InNamespace(c, outgoing)))
            {
                if (InNamespace(type, infrastructure) && DependsOnAnInputPort(arch, type))
                {
                    continue;
                }

                violations.Add($"{type.FullName} implements an output port outside the outgoing adapters");
            }

            DcaRule.Fail(
                "Output port implementations must reside in an outgoing adapter package",
                violations.OrderBy(v => v, StringComparer.Ordinal).ToList(),
                "move the implementation into the outgoing adapter namespace of its module; the configuration in infrastructure only wires it to its port");
        })
    .Experimental()
    .Selecting(
        "Classes of the scan assignable to IOutputPort - repositories, stores, event publishers and every other"
            + " output port alike, abstract base classes included; compiler-generated classes are not selected."
            + " Not selected: a class in an infrastructure namespace that depends on a type assignable to"
            + " IInputPort - the bridge that hands an output port a second use case, which is wiring.")
    .Checking(
        "Each resides in <Module>.Adapter.Outgoing of some module root. DCA-TAC-015 and DCA-TAC-020 hold"
            + " repositories and stores the same way in the tactical set.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
