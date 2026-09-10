---
type: Rule
id: DCA-STR-006
title: Outgoing adapters accessing other modules must only use their published api/ and events/ packages
rule: "Cross-module communication goes through the target's published api/ (synchronous) and events/ (asynchronous) packages - DCA's in-process contract convention, package names rather than framework annotations - never through its domain, application, adapter or infrastructure packages. Selects structurally over every module that owns a DCA layer, declared as a bounded context or not."
constraint: Outgoing adapters accessing other modules must only use their published api/ and events/ packages.
selects: "Classes in <module>.adapter.outgoing.. of every isolated module root - every package below the base package that owns a domain, application or adapter package, declared as a bounded context or not, the shared kernel excluded. A module that is the only isolated root has no foreign target and is skipped."
checks: "No selected class depends on a class in another isolated module root (<other>..) unless that class lives in the other module's published packages <other>.api.. or <other>.events.. (segment names from the layout). The other module's domain, application, adapter and infrastructure packages are internal and reported. The allow-list is the package convention alone - no framework annotation is read. Dependencies on the shared kernel and on third-party code are not checked."
enforced_by: "StrategicPatternRules#DCA-STR-006"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/StrategicPatternRules.cs
---

# Outgoing adapters accessing other modules must only use their published api/ and events/ packages

## Selection

Classes in <module>.adapter.outgoing.. of every isolated module root - every package below the base package that owns a domain, application or adapter package, declared as a bounded context or not, the shared kernel excluded. A module that is the only isolated root has no foreign target and is skipped.

## Check

No selected class depends on a class in another isolated module root (<other>..) unless that class lives in the other module's published packages <other>.api.. or <other>.events.. (segment names from the layout). The other module's domain, application, adapter and infrastructure packages are internal and reported. The allow-list is the package convention alone - no framework annotation is read. Dependencies on the shared kernel and on third-party code are not checked.

## .NET reading

**Selection.** Types in <module>.Adapter.Outgoing and below of every isolated module root - every namespace below the root namespace that owns a Domain, Application or Adapter namespace, declared as a bounded context or not, the shared kernel excluded. A module that is the only isolated root has no foreign target and is skipped.

**Check.** No selected type depends on a type in another isolated module root (<other> and below) unless that type lives in the other module's published namespaces <other>.Api or <other>.Events and below (segment names from the layout). The other module's Domain, Application, Adapter and Infrastructure namespaces are internal and reported. The allow-list is the namespace convention alone - no framework attribute is read. Dependencies on the shared kernel and on third-party code are not checked.

## Implementation

```java
DcaRule.check(
        "DCA-STR-006",
        "Outgoing adapters accessing other modules must only use their published api/ and events/"
            + " packages",
        "Cross-module communication goes through the target's published api/ (synchronous) and"
            + " events/ (asynchronous) packages - DCA's in-process contract convention, package"
            + " names rather than framework annotations - never through its domain, application,"
            + " adapter or infrastructure packages. Selects structurally over every module that owns"
            + " a DCA layer, declared as a bounded context or not",
        arch -> {
          List<ArchRule> perModule = new ArrayList<>();
          for (String source : arch.isolatedModuleRoots()) {
            String[] foreign = arch.moduleRootPatternsExcluding(source);
            if (foreign.length == 0) {
              continue;
            }
            String[] published = arch.publishedPackagePatternsExcluding(source);
            perModule.add(
                noClasses()
                    .that()
                    .resideInAPackage(layout.outgoingAdapterPattern(source))
                    .should()
                    .dependOnClassesThat(
                        resideInAnyPackage(foreign).and(not(resideInAnyPackage(published))))
                    .allowEmptyShould(true)
                    .because(
                        "Outgoing adapters in module '"
                            + arch.contextName(source)
                            + "' must not access another module's internals - use its api/ or"
                            + " events/ packages instead"));
          }
          CollectedViolations.check(perModule, arch.classes());
        })
    .selecting(
        "Classes in <module>.adapter.outgoing.. of every isolated module root - every package"
            + " below the base package that owns a domain, application or adapter package,"
            + " declared as a bounded context or not, the shared kernel excluded. A module that"
            + " is the only isolated root has no foreign target and is skipped.")
    .checking(
        "No selected class depends on a class in another isolated module root (<other>..)"
            + " unless that class lives in the other module's published packages <other>.api.."
            + " or <other>.events.. (segment names from the layout). The other module's domain,"
            + " application, adapter and infrastructure packages are internal and reported. The"
            + " allow-list is the package convention alone - no framework annotation is read."
            + " Dependencies on the shared kernel and on third-party code are not checked.")
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `contextName()`, `isolatedModuleRoots()`, `moduleRootPatternsExcluding()`, `publishedPackagePatternsExcluding()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-STR-006",
        title,
        rationale,
        arch =>
        {
            var perModule = new List<IArchRule>();
            foreach (var source in arch.IsolatedModuleRoots())
            {
                var foreign = arch.ModuleRootPatternsExcluding(source);
                if (foreign.Length == 0)
                {
                    continue;
                }

                // Foreign internals = anything in another module except its published Api/Events namespaces.
                var internals = "(?!" + AnyOf(arch.PublishedPatternsExcluding(source)) + ")(?:" + AnyOf(foreign) + ")";
                perModule.Add(
                    Types().That().ResideInNamespaceMatching(Layout.OutgoingAdapterPatternOf(source))
                        .Should().NotDependOnAnyTypesThat().ResideInNamespaceMatching(internals)
                        .Because("Outgoing adapters in module '" + arch.ContextName(source)
                            + "' must not access another module's internals - use its api/ or events/ packages instead"));
            }

            DcaRule.EvaluateAll(perModule, arch, title, rationale);
        })
    .Selecting(
        "Types in <module>.Adapter.Outgoing and below of every isolated module root - every namespace"
            + " below the root namespace that owns a Domain, Application or Adapter namespace,"
            + " declared as a bounded context or not, the shared kernel excluded. A module that"
            + " is the only isolated root has no foreign target and is skipped.")
    .Checking(
        "No selected type depends on a type in another isolated module root (<other> and below)"
            + " unless that type lives in the other module's published namespaces <other>.Api"
            + " or <other>.Events and below (segment names from the layout). The other module's Domain,"
            + " Application, Adapter and Infrastructure namespaces are internal and reported. The"
            + " allow-list is the namespace convention alone - no framework attribute is read."
            + " Dependencies on the shared kernel and on third-party code are not checked.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
