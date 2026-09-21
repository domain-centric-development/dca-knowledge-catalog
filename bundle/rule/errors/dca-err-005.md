---
type: Rule
id: DCA-ERR-005
title: Domain and use-case exception names must stay in the language of their layer
rule: "A failure named after a transport concept is a decision about the answer, taken in a layer that does not know the protocol; the name should say what went wrong, not what the caller should be told."
constraint: Domain and use-case exception names must stay in the language of their layer.
selects: "Classes anywhere on the classpath under scan that are assignable to DomainException or to UseCaseException, the building-blocks package excluded."
checks: "The simple name ends with none of Error, Fault, Failure and contains none of Http, StatusCode, ResponseStatus, ResponseEntity. The bare words Status and Response are not matched: they are transport words and domain words, and the name alone does not tell them apart, so OrderStatusInvalidException passes. Whether the remaining name is a term of the Ubiquitous Language is not decidable here and stays with review. An empty selection passes."
enforced_by: "ErrorHandlingRules#DCA-ERR-005"
status: enforced
rule_set: errors
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Domain and use-case exception names must stay in the language of their layer

## Selection

Classes anywhere on the classpath under scan that are assignable to DomainException or to UseCaseException, the building-blocks package excluded.

## Check

The simple name ends with none of Error, Fault, Failure and contains none of Http, StatusCode, ResponseStatus, ResponseEntity. The bare words Status and Response are not matched: they are transport words and domain words, and the name alone does not tell them apart, so OrderStatusInvalidException passes. Whether the remaining name is a term of the Ubiquitous Language is not decidable here and stays with review. An empty selection passes.

## .NET reading

**Selection.** Types anywhere under the root namespace that are assignable to the domain-exception or the use-case-exception role, the vocabulary's own code excluded: the namespaces the configured role types live in are not selected, so a project's own base type is not reported as residing outside a layer it never claimed.

**Check.** The type name ends with none of Error, Fault, Failure and contains none of Http, StatusCode, ResponseStatus, ResponseEntity. The bare words Status and Response are not matched: they are transport words and domain words, and the name alone does not tell them apart, so OrderStatusInvalidException passes. Whether the remaining name is a term of the Ubiquitous Language is not decidable here and stays with review. An empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-ERR-005",
        "Domain and use-case exception names must stay in the language of their layer",
        "A failure named after a transport concept is a decision about the answer, taken in a"
            + " layer that does not know the protocol; the name should say what went wrong, not"
            + " what the caller should be told",
        arch -> {
          CollectedViolations collected =
              CollectedViolations.withHeader(
                  "A technical or transport word in an exception name");
          for (JavaClass type : arch.classes()) {
            if (!isProjectException(type, arch.layout().markers())) {
              continue;
            }
            String name = type.getSimpleName();
            for (String suffix : FORBIDDEN_SUFFIXES) {
              collected.require(
                  !name.endsWith(suffix),
                  type.getName() + " ends with the technical suffix " + suffix);
            }
            for (String word : FORBIDDEN_WORDS) {
              collected.require(
                  !name.contains(word),
                  type.getName() + " names the transport concept " + word);
            }
          }
          collected.throwIfAny();
        })
    .selecting(
        "Classes anywhere on the classpath under scan that are assignable to DomainException or"
            + " to UseCaseException, the building-blocks package excluded.")
    .checking(
        "The simple name ends with none of Error, Fault, Failure and contains none of Http,"
            + " StatusCode, ResponseStatus, ResponseEntity. The bare words Status and"
            + " Response are not matched: they are transport words and domain words, and"
            + " the name alone does not tell them apart, so OrderStatusInvalidException"
            + " passes. Whether the remaining name is a term of the Ubiquitous Language is"
            + " not decidable here and stays with review. An empty selection passes.")
```

## Helpers

### `isProjectException`

```java
/** A project's own exception type: assignable to a base type, outside the building blocks. */
  private static boolean isProjectException(JavaClass type, DcaMarkers markers) {
    return (type.isAssignableTo(markers.domainException())
            || type.isAssignableTo(markers.useCaseException()))
        && !markers.declaresTypesIn(type.getPackageName());
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

### `CollectedViolations.withHeader`

```java
/** A collector whose report starts with the given statement of what the rule demands. */
  static CollectedViolations withHeader(String header) {
    return new CollectedViolations(header);
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ERR-005",
    "Domain and use-case exception names must stay in the language of their layer",
    "A failure named after a transport concept is a decision about the answer, taken in a layer"
        + " that does not know the protocol; the name should say what went wrong, not what the"
        + " caller should be told",
    arch =>
    {
        var violations = new List<string>();
        foreach (var type in ExceptionsOfEitherLayer(arch))
        {
            foreach (var suffix in ForbiddenSuffixes.Where(s => type.Name.EndsWith(s, StringComparison.Ordinal)))
            {
                violations.Add($"{type.FullName} ends with the technical suffix {suffix}");
            }

            foreach (var word in ForbiddenWords.Where(w => type.Name.Contains(w, StringComparison.Ordinal)))
            {
                violations.Add($"{type.FullName} names the transport concept {word}");
            }
        }

        DcaRule.Fail("A technical or transport word in an exception name", violations);
    })
    .Selecting(
        "Types anywhere under the root namespace that are assignable to the domain-exception or the "
        + "use-case-exception role, the vocabulary's own code excluded: the namespaces the configured "
        + "role types live in are not selected, so a project's own base type is not reported as "
        + "residing outside a layer it never claimed.")
    .Checking(
        "The type name ends with none of Error, Fault, Failure and contains none of Http, "
        + "StatusCode, ResponseStatus, ResponseEntity. The bare words Status and Response are "
        + "not matched: they are transport words and domain words, and the name alone does not "
        + "tell them apart, so OrderStatusInvalidException passes. Whether the remaining name "
        + "is a term of the Ubiquitous Language is not decidable here and stays with review. "
        + "An empty selection passes.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
