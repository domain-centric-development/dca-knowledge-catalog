---
type: Rule
id: DCA-STR-002
title: Shared Kernel must not have dependencies on any bounded context
rule: Shared Kernel must be context-independent — it is shared by all contexts and owned by none.
constraint: Shared Kernel must not have dependencies on any bounded context.
selects: "Classes in the package annotated with @SharedKernel and all its sub-packages. When no shared kernel is declared nothing is selected and the rule passes."
checks: "No selected class depends on a class in a package carrying @BoundedContext or below it, checked once per declared context and reported together. A module that owns layers without declaring @BoundedContext is not a forbidden target here. Dependencies on the base package outside any context, on infrastructure and on third-party code are not checked."
enforced_by: "StrategicPatternRules#DCA-STR-002"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

## Selection

Classes in the package annotated with @SharedKernel and all its sub-packages. When no shared kernel is declared nothing is selected and the rule passes.

## Check

No selected class depends on a class in a package carrying @BoundedContext or below it, checked once per declared context and reported together. A module that owns layers without declaring @BoundedContext is not a forbidden target here. Dependencies on the base package outside any context, on infrastructure and on third-party code are not checked.

## .NET reading

**Selection.** Types in the namespace whose marker class carries [SharedKernel] and all its sub-namespaces. When no shared kernel is declared nothing is selected and the rule passes.

**Check.** No selected type depends on a type in a namespace carrying [BoundedContext] or below it, checked once per declared context and reported together. A module that owns layers without declaring [BoundedContext] is not a forbidden target here. Dependencies on the root namespace outside any context, on infrastructure and on third-party code are not checked.

## Implementation

```java
DcaRule.check(
        "DCA-STR-002",
        "Shared Kernel must not have dependencies on any bounded context",
        "Shared Kernel must be context-independent — it is shared by all contexts and owned by"
            + " none",
        arch -> {
          Optional<String> sharedKernel = arch.sharedKernelPackage();
          if (sharedKernel.isEmpty()) {
            return;
          }
          CollectedViolations violations = CollectedViolations.withoutHeader();
          for (Map.Entry<String, BoundedContext> ctx : arch.boundedContexts().entrySet()) {
            violations.addAll(
                noClasses()
                    .that()
                    .resideInAPackage(sharedKernel.get() + "..")
                    .should()
                    .dependOnClassesThat()
                    .resideInAPackage(ctx.getKey() + "..")
                    .allowEmptyShould(true),
                arch.classes(),
                "Shared Kernel must not depend on bounded context '"
                    + ctx.getValue().name()
                    + "' ("
                    + ctx.getKey()
                    + ") - Shared Kernel must be context-independent");
          }
          violations.throwIfAny();
        })
    .selecting(
        "Classes in the package annotated with @SharedKernel and all its sub-packages. When no"
            + " shared kernel is declared nothing is selected and the rule passes.")
    .checking(
        "No selected class depends on a class in a package carrying @BoundedContext or below"
            + " it, checked once per declared context and reported together. A module that owns"
            + " layers without declaring @BoundedContext is not a forbidden target here."
            + " Dependencies on the base package outside any context, on infrastructure and on"
            + " third-party code are not checked.")
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

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
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

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContexts()`, `classes()`, `sharedKernelPackage()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
