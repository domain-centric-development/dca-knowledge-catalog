---
type: Rule
id: DCA-HEX-007
title: "Incoming adapters must only access their own bounded context (except event consumers and Open Host Services)"
rule: Incoming adapters must only orchestrate use cases from their own bounded context - use domain events for cross-context integration.
constraint: "Incoming adapters must only access their own bounded context (except event consumers and Open Host Services)."
selects: "Per isolated module root - every module root except the shared kernel, declared a bounded context or not: classes in <module>.adapter.incoming.., excluding those below an adapter.incoming.event package (event consumers). A module that is the only isolated module is skipped."
checks: "No dependency on any class in another isolated module root (<other>..), its published api and events packages included. Dependencies on the shared kernel and on packages outside every module root are not checked. Findings of all modules are collected and reported together; a module without incoming adapters passes."
enforced_by: "HexagonalRules#DCA-HEX-007"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

## Selection

Per isolated module root - every module root except the shared kernel, declared a bounded context or not: classes in <module>.adapter.incoming.., excluding those below an adapter.incoming.event package (event consumers). A module that is the only isolated module is skipped.

## Check

No dependency on any class in another isolated module root (<other>..), its published api and events packages included. Dependencies on the shared kernel and on packages outside every module root are not checked. Findings of all modules are collected and reported together; a module without incoming adapters passes.

## .NET reading

**Selection.** Per isolated module root - every module root except the shared kernel, declared a bounded context or not: types in <module>.Adapter.Incoming, excluding those below an Adapter.Incoming.Event namespace (event consumers). A module that is the only isolated module is skipped.

**Check.** No dependency on any type in another isolated module root (<other> and below), its published Api and Events namespaces included. Dependencies on the shared kernel and on namespaces outside every module root are not checked. Findings of all modules are collected and reported together; a module without incoming adapters passes.

## Implementation

```java
DcaRule.check(
        "DCA-HEX-007",
        "Incoming adapters must only access their own bounded context (except event consumers and"
            + " Open Host Services)",
        "Incoming adapters must only orchestrate use cases from their own bounded context - use"
            + " domain events for cross-context integration",
        arch -> {
          // Structural, over every module that owns a DCA layer - declared as a bounded context
          // or
          // not - so an undeclared module can neither reach out nor be reached into.
          List<ArchRule> perModule = new ArrayList<>();
          for (String module : arch.isolatedModuleRoots()) {
            String[] otherModules = arch.moduleRootPatternsExcluding(module);
            if (otherModules.length == 0) {
              continue;
            }
            perModule.add(
                noClasses()
                    .that()
                    .resideInAPackage(layout.incomingAdapterPattern(module))
                    .and()
                    .resideOutsideOfPackage(eventConsumerPattern())
                    .should()
                    .dependOnClassesThat()
                    .resideInAnyPackage(otherModules)
                    .allowEmptyShould(true)
                    .because(
                        "Incoming adapters in module '"
                            + arch.contextName(module)
                            + "' must only orchestrate use cases from their own module - use"
                            + " domain events for cross-context integration"));
          }
          CollectedViolations.check(perModule, arch.classes());
        })
    .selecting(
        "Per isolated module root - every module root except the shared kernel, declared"
            + " a bounded context or not: classes in <module>.adapter.incoming.., excluding"
            + " those below an adapter.incoming.event package (event consumers). A module that"
            + " is the only isolated module is skipped.")
    .checking(
        "No dependency on any class in another isolated module root (<other>..), its"
            + " published api and events packages included. Dependencies on the shared kernel"
            + " and on packages outside every module root are not checked. Findings of all"
            + " modules are collected and reported together; a module without incoming adapters"
            + " passes.")
```

## Helpers

### `eventConsumerPattern`

```java
/** Pattern of event consumers, which may depend on other contexts' integration events. */
  private String eventConsumerPattern() {
    return ".." + layout.adapterSubpackage() + "." + layout.incomingSubpackage() + ".event..";
  }
```

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

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
