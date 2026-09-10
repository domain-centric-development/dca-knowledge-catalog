---
type: Rule
id: DCA-STR-003
title: Modules must not access each other in the application layer
rule: "An application layer talks to other modules through its own output ports, implemented by adapters - never directly. Selects structurally over every module that owns a DCA layer, declared as a bounded context or not: an undeclared module must not be able to escape isolation by staying off the context map."
constraint: Modules must not access each other in the application layer.
selects: "Classes in <module>.application.. of every isolated module root - every package below the base package that owns a domain, application or adapter package, declared as a bounded context or not, the shared kernel excluded. A module that is the only isolated root has no foreign target and is skipped."
checks: "No selected class depends on any class in another isolated module root or below it (<other>..), the other module's api and events packages included. A dependency is any reference - field, parameter, return type, record component, type argument or call - not only a method call. Dependencies on the shared kernel, on infrastructure and on third-party code are not checked. Violations are collected per module and reported together."
enforced_by: "StrategicPatternRules#DCA-STR-003"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/StrategicPatternRules.cs
---

# Modules must not access each other in the application layer

## Selection

Classes in <module>.application.. of every isolated module root - every package below the base package that owns a domain, application or adapter package, declared as a bounded context or not, the shared kernel excluded. A module that is the only isolated root has no foreign target and is skipped.

## Check

No selected class depends on any class in another isolated module root or below it (<other>..), the other module's api and events packages included. A dependency is any reference - field, parameter, return type, record component, type argument or call - not only a method call. Dependencies on the shared kernel, on infrastructure and on third-party code are not checked. Violations are collected per module and reported together.

## .NET reading

**Selection.** Types in <module>.Application and below of every isolated module root - every namespace below the root namespace that owns a Domain, Application or Adapter namespace, declared as a bounded context or not, the shared kernel excluded. A module that is the only isolated root has no foreign target and is skipped.

**Check.** No selected type depends on any type in another isolated module root or below it (<other> and below), the other module's Api and Events namespaces included. A dependency is any reference - field, parameter, return type, record component, type argument or call - not only a method call. Dependencies on the shared kernel, on infrastructure and on third-party code are not checked. Violations are collected per module and reported together.

## Implementation

```java
DcaRule.check(
        "DCA-STR-003",
        "Modules must not access each other in the application layer",
        "An application layer talks to other modules through its own output ports, implemented by"
            + " adapters - never directly. Selects structurally over every module that owns a DCA"
            + " layer, declared as a bounded context or not: an undeclared module must not be able"
            + " to escape isolation by staying off the context map",
        arch -> {
          List<ArchRule> perModule = new ArrayList<>();
          for (String source : arch.isolatedModuleRoots()) {
            String[] forbidden = arch.moduleRootPatternsExcluding(source);
            if (forbidden.length == 0) {
              continue;
            }
            // dependOnClassesThat, not accessClassesThat: "access" is a method call or field
            // access, so a field, parameter or record component of a foreign type slips past
            // it.
            perModule.add(
                noClasses()
                    .that()
                    .resideInAPackage(layout.applicationPattern(source))
                    .should()
                    .dependOnClassesThat()
                    .resideInAnyPackage(forbidden)
                    .allowEmptyShould(true)
                    .because(
                        "The application layer of module '"
                            + arch.contextName(source)
                            + "' must not access other modules directly - define output ports and"
                            + " use adapters instead"));
          }
          CollectedViolations.check(perModule, arch.classes());
        })
    .selecting(
        "Classes in <module>.application.. of every isolated module root - every package below"
            + " the base package that owns a domain, application or adapter package, declared"
            + " as a bounded context or not, the shared kernel excluded. A module that is the only"
            + " isolated root has no foreign target and is skipped.")
    .checking(
        "No selected class depends on any class in another isolated module root or below it"
            + " (<other>..), the other module's api and events packages included. A dependency"
            + " is any reference - field, parameter, return type, record component, type"
            + " argument or call - not only a method call. Dependencies on the shared kernel,"
            + " on infrastructure and on third-party code are not checked. Violations are"
            + " collected per module and reported together.")
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

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
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

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `contextName()`, `isolatedModuleRoots()`, `moduleRootPatternsExcluding()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-STR-003",
        title,
        rationale,
        arch =>
        {
            var perModule = new List<IArchRule>();
            foreach (var source in arch.IsolatedModuleRoots())
            {
                var forbidden = arch.ModuleRootPatternsExcluding(source);
                if (forbidden.Length == 0)
                {
                    continue;
                }

                // Dependencies, not accesses: a field, parameter or record component of a foreign
                // type is a dependency even without a method call.
                perModule.Add(
                    Types().That().ResideInNamespaceMatching(Layout.ApplicationPatternOf(source))
                        .Should().NotDependOnAnyTypesThat().ResideInNamespaceMatching(AnyOf(forbidden))
                        .Because("The application layer of module '" + arch.ContextName(source)
                            + "' must not access other modules directly - define output ports and use adapters instead"));
            }

            DcaRule.EvaluateAll(perModule, arch, title, rationale);
        })
    .Selecting(
        "Types in <module>.Application and below of every isolated module root - every namespace"
            + " below the root namespace that owns a Domain, Application or Adapter namespace, declared"
            + " as a bounded context or not, the shared kernel excluded. A module that is the only"
            + " isolated root has no foreign target and is skipped.")
    .Checking(
        "No selected type depends on any type in another isolated module root or below it"
            + " (<other> and below), the other module's Api and Events namespaces included. A dependency"
            + " is any reference - field, parameter, return type, record component, type"
            + " argument or call - not only a method call. Dependencies on the shared kernel,"
            + " on infrastructure and on third-party code are not checked. Violations are"
            + " collected per module and reported together.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
