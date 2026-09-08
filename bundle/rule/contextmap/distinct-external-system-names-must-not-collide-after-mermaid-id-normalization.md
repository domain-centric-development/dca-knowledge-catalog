---
type: Rule
id: DCA-MAP-003
title: Distinct external system names must not collide after mermaid id normalization
rule: The generated context map renders one node per normalized external system name — two spellings of the same system would silently merge into one node.
constraint: Distinct external system names must not collide after mermaid id normalization.
selects: "Every @ExternalUpstream declaration on the package-info of every package carrying @BoundedContext, across all contexts, reading name(). PLANNED declarations are included."
checks: "Two declarations whose name() differs but normalizes to the same node id of the generated context map (the renderer's own normalization) are reported as a collision. Repeating one spelling of a name is not a collision."
enforced_by: "ContextMapRules#DCA-MAP-003"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

## Selection

Every @ExternalUpstream declaration on the package-info of every package carrying @BoundedContext, across all contexts, reading name(). PLANNED declarations are included.

## Check

Two declarations whose name() differs but normalizes to the same node id of the generated context map (the renderer's own normalization) are reported as a collision. Repeating one spelling of a name is not a collision.

## .NET reading

**Selection.** Every [ExternalUpstream] declaration on the marker class of every namespace carrying [BoundedContext], across all contexts, reading Name. Planned declarations are included.

**Check.** Two declarations whose Name differs but normalizes to the same node id of the generated context map (the renderer's own normalization) are reported as a collision. Repeating one spelling of a name is not a collision.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-003",
        "Distinct external system names must not collide after mermaid id normalization",
        "The generated context map renders one node per normalized external system name — two"
            + " spellings of the same system would silently merge into one node",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          Map<String, String> idToName = new LinkedHashMap<>();
          for (String pkg : arch.boundedContextPackages()) {
            for (ExternalUpstream e : arch.packageAnnotations(pkg, ExternalUpstream.class)) {
              String id = normalizedExternalId(e.name());
              String known = idToName.getOrDefault(id, e.name());
              violations.require(
                  known.equals(e.name()),
                  "External system names '"
                      + known
                      + "' and '"
                      + e.name()
                      + "' normalize to the same mermaid node id '"
                      + id
                      + "' — use one canonical spelling");
              idToName.put(id, e.name());
            }
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every @ExternalUpstream declaration on the package-info of every package"
            + " carrying @BoundedContext, across all contexts, reading name(). PLANNED"
            + " declarations are included.")
    .checking(
        "Two declarations whose name() differs but normalizes to the same node id of"
            + " the generated context map (the renderer's own normalization) are reported"
            + " as a collision. Repeating one spelling of a name is not a collision.")
```

## Helpers

### `normalizedExternalId`

```java
/** The mermaid node id of an external system — the renderer's own normalisation. */
  private static String normalizedExternalId(String name) {
    return ContextMapRenderer.externalSystemNodeId(name);
  }
```

### `name`

```java
public String name() {
  return "contextmap";
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
