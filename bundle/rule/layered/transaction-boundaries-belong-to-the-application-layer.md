---
type: Rule
id: DCA-LAY-004
title: Transaction boundaries belong to the application layer
rule: Transactions are an application-layer concern - domain and incoming adapters must not manage them.
constraint: Transaction boundaries belong to the application layer.
selects: "Methods and classes under scan that carry the configured transactional annotation directly (meta-annotations do not count)."
checks: "Each annotated method is declared in, and each annotated class resides in, an application package of some module root (<module>.application..) or an outgoing adapter package (..adapter.outgoing..) anywhere. An annotation in a domain, incoming-adapter or infrastructure package is reported; all findings are collected into one violation. Programmatic boundaries (TransactionBoundary) are not checked."
enforced_by: "LayeredRules#DCA-LAY-004"
status: enforced
rule_set: layered
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
---

## Selection

Methods and classes under scan that carry the configured transactional annotation directly (meta-annotations do not count).

## Check

Each annotated method is declared in, and each annotated class resides in, an application package of some module root (<module>.application..) or an outgoing adapter package (..adapter.outgoing..) anywhere. An annotation in a domain, incoming-adapter or infrastructure package is reported; all findings are collected into one violation. Programmatic boundaries (TransactionBoundary) are not checked.

## .NET reading

**Selection.** Types under scan that have any dependency on the configured transaction type (by default System.Transactions.TransactionScope) - a field, a local, a method call or a using block all count.

**Check.** Each resides in an application namespace of some module root (<module>.Application or below) or in an outgoing adapter namespace of some module root (<module>.Adapter.Outgoing or below). A use in a domain, incoming-adapter or infrastructure namespace is reported; all findings are collected into one violation. The check is per type, not per method, and other transaction APIs (a DbContext transaction, TransactionScope subclasses) are not looked for.

## Implementation

```java
DcaRule.check(
        "DCA-LAY-004",
        "Transaction boundaries belong to the application layer",
        rationale,
        arch -> {
          String transactional = layout.frameworkAnnotations().transactional();
          List<String> allowedPatterns =
              new ArrayList<>(List.of(arch.allApplicationPatterns()));
          allowedPatterns.add(
              ".." + layout.adapterSubpackage() + "." + layout.outgoingSubpackage() + "..");
          String[] allowed = allowedPatterns.toArray(String[]::new);
          CollectedViolations violations = CollectedViolations.withoutHeader();
          violations.addAll(
              methods()
                  .that()
                  .areAnnotatedWith(transactional)
                  .should()
                  .beDeclaredInClassesThat()
                  .resideInAnyPackage(allowed)
                  .allowEmptyShould(true),
              arch.classes(),
              rationale);
          violations.addAll(
              classes()
                  .that()
                  .areAnnotatedWith(transactional)
                  .should()
                  .resideInAnyPackage(allowed)
                  .allowEmptyShould(true),
              arch.classes(),
              rationale);
          violations.throwIfAny();
        })
    .selecting(
        "Methods and classes under scan that carry the configured transactional annotation"
            + " directly (meta-annotations do not count).")
    .checking(
        "Each annotated method is declared in, and each annotated class resides in, an"
            + " application package of some module root (<module>.application..) or an outgoing"
            + " adapter package (..adapter.outgoing..) anywhere. An annotation in a domain,"
            + " incoming-adapter or infrastructure package is reported; all findings are"
            + " collected into one violation. Programmatic boundaries"
            + " (TransactionBoundary) are not checked.")
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [TransactionBoundary](/marker/application/transactionboundary.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
