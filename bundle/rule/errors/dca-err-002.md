---
type: Rule
id: DCA-ERR-002
title: Domain and use-case exceptions reside in the layer whose failure they name
rule: The base type states which layer owns the failure; declaring it elsewhere puts the vocabulary of that layer outside it and lets an adapter invent failures the application never reports.
constraint: Domain and use-case exceptions reside in the layer whose failure they name.
selects: "Classes anywhere on the classpath under scan that are assignable to DomainException or to UseCaseException, except the two base types themselves and anything else in the building-blocks package."
checks: "A subtype of DomainException resides in <module>.domain.. of some module root, a subtype of UseCaseException in <module>.application... Both findings are collected into one violation. Which of the two a given failure should have been is not checked here. An empty selection passes."
enforced_by: "ErrorHandlingRules#DCA-ERR-002"
status: enforced
rule_set: errors
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Domain and use-case exceptions reside in the layer whose failure they name

## Selection

Classes anywhere on the classpath under scan that are assignable to DomainException or to UseCaseException, except the two base types themselves and anything else in the building-blocks package.

## Check

A subtype of DomainException resides in <module>.domain.. of some module root, a subtype of UseCaseException in <module>.application... Both findings are collected into one violation. Which of the two a given failure should have been is not checked here. An empty selection passes.

## .NET reading

**Selection.** Types anywhere under the root namespace that are assignable to DomainException or to UseCaseException, except the two base types themselves and anything else in the building-blocks namespace.

**Check.** A subtype of DomainException resides under <Module>.Domain of some module root, a subtype of UseCaseException under <Module>.Application. Both findings are collected into one violation. Which of the two a given failure should have been is not checked here. An empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-ERR-002",
        "Domain and use-case exceptions reside in the layer whose failure they name",
        "The base type states which layer owns the failure; declaring it elsewhere puts the"
            + " vocabulary of that layer outside it and lets an adapter invent failures the"
            + " application never reports",
        arch -> {
          CollectedViolations collected =
              CollectedViolations.withHeader(
                  "DCA-ERR-002: an exception resides outside the layer its base type names");
          collected.addAll(
              classes()
                  .that()
                  .areAssignableTo(DomainException.class)
                  .and()
                  .resideOutsideOfPackage(DcaLayout.BUILDING_BLOCKS_PACKAGE)
                  .should()
                  .resideInAnyPackage(arch.allDomainPatterns())
                  .allowEmptyShould(true),
              arch.classes(),
              "a domain exception belongs to the domain layer");
          collected.addAll(
              classes()
                  .that()
                  .areAssignableTo(UseCaseException.class)
                  .and()
                  .resideOutsideOfPackage(DcaLayout.BUILDING_BLOCKS_PACKAGE)
                  .should()
                  .resideInAnyPackage(arch.allApplicationPatterns())
                  .allowEmptyShould(true),
              arch.classes(),
              "a use-case exception belongs to the application layer");
          collected.throwIfAny();
        })
    .selecting(
        "Classes anywhere on the classpath under scan that are assignable to DomainException or"
            + " to UseCaseException, except the two base types themselves and anything else in"
            + " the building-blocks package.")
    .checking(
        "A subtype of DomainException resides in <module>.domain.. of some module root, a"
            + " subtype of UseCaseException in <module>.application... Both findings are"
            + " collected into one violation. Which of the two a given failure should have been"
            + " is not checked here. An empty selection passes.")
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

### `CollectedViolations.withoutHeader`

```java
/** A collector whose report is the bare list of violations. */
  static CollectedViolations withoutHeader() {
    return new CollectedViolations("");
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `allDomainPatterns()`, `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ERR-002",
    "Domain and use-case exceptions reside in the layer whose failure they name",
    "The base type states which layer owns the failure; declaring it elsewhere puts the vocabulary"
        + " of that layer outside it and lets an adapter invent failures the application never"
        + " reports",
    arch =>
    {
        var domain = new Regex(DcaLayout.AnyOf(arch.AllDomainPatterns()));
        var application = new Regex(DcaLayout.AnyOf(arch.AllApplicationPatterns()));
        var violations = new List<string>();
        foreach (var type in ProjectExceptions(arch))
        {
            var ns = type.Namespace?.FullName ?? "";
            if (IsAssignableTo(type, typeof(DomainException)) && !domain.IsMatch(ns))
            {
                violations.Add($"{type.FullName} is a domain exception outside the domain layer");
            }

            if (IsAssignableTo(type, typeof(UseCaseException)) && !application.IsMatch(ns))
            {
                violations.Add($"{type.FullName} is a use-case exception outside the application layer");
            }
        }

        DcaRule.Fail("DCA-ERR-002: an exception resides outside the layer its base type names", violations);
    })
    .Selecting(
        "Types anywhere under the root namespace that are assignable to DomainException or to "
        + "UseCaseException, except the two base types themselves and anything else in the "
        + "building-blocks namespace.")
    .Checking(
        "A subtype of DomainException resides under <Module>.Domain of some module root, a subtype "
        + "of UseCaseException under <Module>.Application. Both findings are collected into one "
        + "violation. Which of the two a given failure should have been is not checked here. An "
        + "empty selection passes.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
