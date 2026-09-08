---
type: Rule
id: DCA-MAP-004
title: Upstream declarations must reference an existing bounded context and never the declaring context itself
rule: A dangling or self-referencing upstream edge describes a relationship that cannot exist.
constraint: Upstream declarations must reference an existing bounded context and never the declaring context itself.
selects: "Every @Upstream declaration on the package-info of every package carrying @BoundedContext, reading context(). PLANNED declarations are included."
checks: "context() names an existing bounded context - a package carrying @BoundedContext, identified by its name relative to the base package - and is not the declaring context itself. Whether any code depends on the target is not established here."
enforced_by: "ContextMapRules#DCA-MAP-004"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

## Selection

Every @Upstream declaration on the package-info of every package carrying @BoundedContext, reading context(). PLANNED declarations are included.

## Check

context() names an existing bounded context - a package carrying @BoundedContext, identified by its name relative to the base package - and is not the declaring context itself. Whether any code depends on the target is not established here.

## .NET reading

**Selection.** Every [Upstream] declaration on the marker class of every namespace carrying [BoundedContext], reading Context. Planned declarations are included.

**Check.** Context names an existing bounded context - a namespace whose marker class carries [BoundedContext], identified by its name relative to the root namespace - and is not the declaring context itself. Whether any code depends on the target is not established here.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-004",
        "Upstream declarations must reference an existing bounded context and never the declaring"
            + " context itself",
        "A dangling or self-referencing upstream edge describes a relationship that cannot exist",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          Set<String> moduleNames = moduleNames(arch);
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
              violations.require(
                  moduleNames.contains(u.context()),
                  "Context '"
                      + source
                      + "' declares @Upstream(context = \""
                      + u.context()
                      + "\") but no bounded context module with that name exists (known: "
                      + moduleNames
                      + ")");
              violations.require(
                  !u.context().equals(source),
                  "Context '" + source + "' declares itself as its own upstream");
            }
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every @Upstream declaration on the package-info of every package carrying"
            + " @BoundedContext, reading context(). PLANNED declarations are included.")
    .checking(
        "context() names an existing bounded context - a package carrying"
            + " @BoundedContext, identified by its name relative to the base package - and"
            + " is not the declaring context itself. Whether any code depends on the target"
            + " is not established here.")
```

## Helpers

### `moduleNames`

```java
private static Set<String> moduleNames(DcaArchitecture arch) {
  Set<String> names = new LinkedHashSet<>();
  arch.boundedContextPackages().forEach(p -> names.add(arch.contextName(p)));
  return names;
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

### `CollectedViolations.withoutHeader`

```java
/** A collector whose report is the bare list of violations. */
  static CollectedViolations withoutHeader() {
    return new CollectedViolations("");
  }
```

### `CollectedViolations.require`

```java
/** Records the violation unless the condition holds. */
  void require(boolean condition, String violation) {
    if (!condition) {
      add(violation);
    }
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

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
  }
```

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `contextName()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
