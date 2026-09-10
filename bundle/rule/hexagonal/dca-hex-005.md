---
type: Rule
id: DCA-HEX-005
title: Outgoing adapters must not use another module's infrastructure
rule: Technical infrastructure reuse preserves module isolation.
constraint: Outgoing adapters must not use another module's infrastructure.
selects: Classes in every module's outgoing adapter package.
checks: Dependencies on global infrastructure and the adapter's own module infrastructure pass; infrastructure of another module fails. Module boundaries use exact package segments.
enforced_by: "HexagonalRules#DCA-HEX-005"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Outgoing adapters must not use another module's infrastructure

## Selection

Classes in every module's outgoing adapter package.

## Check

Dependencies on global infrastructure and the adapter's own module infrastructure pass; infrastructure of another module fails. Module boundaries use exact package segments.

## .NET reading

**Selection.** Types in every module's outgoing adapter namespace.

**Check.** Global and own-module infrastructure dependencies pass; another module's infrastructure fails. Boundaries use exact namespace segments.

## Implementation

```java
DcaRule.check(
        "DCA-HEX-005",
        "Outgoing adapters must not use another module's infrastructure",
        "Technical infrastructure reuse preserves module isolation",
        arch -> {
          CollectedViolations violations =
              CollectedViolations.withHeader(
                  "Outgoing adapters must not use another module's infrastructure\nbecause"
                      + " technical infrastructure reuse preserves module isolation");
          for (var adapter : arch.classes()) {
            if (!com.tngtech.archunit.core.domain.JavaClass.Predicates.resideInAnyPackage(
                    arch.allOutgoingAdapterPatterns())
                .test(adapter)) continue;
            String owner = arch.moduleRootOf(adapter.getPackageName());
            for (var dependency : adapter.getDirectDependenciesFromSelf()) {
              var target = dependency.getTargetClass();
              String targetOwner =
                  arch.isolatedModuleRoots().stream()
                      .filter(
                          root ->
                              target.getPackageName().equals(layout.infrastructurePackage(root))
                                  || target
                                      .getPackageName()
                                      .startsWith(layout.infrastructurePackage(root) + "."))
                      .findFirst()
                      .orElse(layout.basePackage());
              if (arch.infrastructureImplementation().test(target)
                  && !java.util.Objects.equals(owner, targetOwner)
                  && !layout.basePackage().equals(targetOwner))
                violations.add(dependency.getDescription());
            }
          }
          violations.throwIfAny();
        })
    .selecting("Classes in every module's outgoing adapter package.")
    .checking(
        "Dependencies on global infrastructure and the adapter's own module infrastructure pass; infrastructure of another module fails. Module boundaries use exact package segments.")
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allOutgoingAdapterPatterns()`, `classes()`, `infrastructureImplementation()`, `isolatedModuleRoots()`, `moduleRootOf()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check("DCA-HEX-005", "Outgoing adapters must not use another module's infrastructure",
        "Technical infrastructure reuse preserves module isolation",
        arch => DcaRule.Fail("Another module's infrastructure is forbidden",
            arch.Types.Where(t => Regex.IsMatch(t.Namespace?.FullName ?? "", DcaLayout.AnyOf(arch.AllOutgoingAdapterPatterns())))
                .SelectMany(adapter => adapter.Dependencies.Select(d => d.Target)
                    .Where(target => arch.IsInfrastructureImplementation(target)
                        && arch.IsolatedModuleRoots().Any(root => root != arch.ModuleRootOf(adapter.Namespace?.FullName ?? "")
                            && DcaLayout.IsBelow(target.Namespace?.FullName ?? "", root + "." + Layout.InfrastructureSegment)))
                    .Select(target => $"{adapter.FullName} depends on {target.FullName}")).ToList()))
    .Selecting("Types in every module's outgoing adapter namespace.")
    .Checking("Global and own-module infrastructure dependencies pass; another module's infrastructure fails. Boundaries use exact namespace segments.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
