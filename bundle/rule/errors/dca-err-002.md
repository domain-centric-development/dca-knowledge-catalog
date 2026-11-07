---
type: Rule
id: DCA-ERR-002
title: Domain and port exceptions reside in the layer whose failure they name
rule: The base type states which layer owns the failure; declaring it elsewhere puts the vocabulary of that layer outside it and lets an adapter invent failures the application never reports.
constraint: Domain and port exceptions reside in the layer whose failure they name.
selects: "Classes anywhere on the classpath under scan that are assignable to the domain-exception or the port-exception role, except the vocabulary's own code: the packages the configured role types live in are excluded, so a project's own base class is not reported as residing outside a layer it never claimed."
checks: "A subtype of DomainException resides in <module>.domain.. of some module root, a subtype of PortException - UseCaseException, OutputPortException and any other port failure - in <module>.application... An output port's failure is declared beside the port, even though the adapter that implements the port raises it. Both findings are collected into one violation. Which of the two a given failure should have been is not checked here. An empty selection passes."
enforced_by: "ErrorHandlingRules#DCA-ERR-002"
status: enforced
maturity: released
rule_set: errors
implementations: [java, dotnet, rust]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Domain and port exceptions reside in the layer whose failure they name

## Selection

Classes anywhere on the classpath under scan that are assignable to the domain-exception or the port-exception role, except the vocabulary's own code: the packages the configured role types live in are excluded, so a project's own base class is not reported as residing outside a layer it never claimed.

## Check

A subtype of DomainException resides in <module>.domain.. of some module root, a subtype of PortException - UseCaseException, OutputPortException and any other port failure - in <module>.application... An output port's failure is declared beside the port, even though the adapter that implements the port raises it. Both findings are collected into one violation. Which of the two a given failure should have been is not checked here. An empty selection passes.

## .NET reading

**Selection.** Types anywhere under the root namespace that are assignable to DomainException or to PortException, except the base types themselves and anything else in the building-blocks namespace.

**Check.** A subtype of DomainException resides under <Module>.Domain of some module root, a subtype of PortException - UseCaseException, OutputPortException and any other port failure - under <Module>.Application. An output port's failure is declared beside the port, even though the adapter that implements the port raises it. Both findings are collected into one violation. Which of the two a given failure should have been is not checked here. An empty selection passes.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a lint or a test (source-test).

**Selection.** Types that implement DomainFailure or a port failure (UseCaseFailure, OutputPortFailure, or the classification traits PortFailure and InputPortFailure).

**Check.** A DomainFailure sits in a domain crate, a port failure in an application crate - an output port's failure beside the port, although the adapter that implements the port returns it.

## Implementation

```java
DcaRule.check(
        "DCA-ERR-002",
        "Domain and port exceptions reside in the layer whose failure they name",
        "The base type states which layer owns the failure; declaring it elsewhere puts the"
            + " vocabulary of that layer outside it and lets an adapter invent failures the"
            + " application never reports",
        arch -> {
          CollectedViolations collected =
              CollectedViolations.withHeader(
                  "An exception resides outside the layer its base type names");
          collected.addAll(
              classes()
                  .that(arch.layout().markers().is("domainException"))
                  .and()
                  .resideOutsideOfPackages(
                      arch.layout().markers().declaringPackagePatterns().toArray(String[]::new))
                  .should(LayerConditions.be(arch.inDomain()))
                  .allowEmptyShould(true),
              arch.classes(),
              "a domain exception belongs to the domain layer");
          collected.addAll(
              classes()
                  .that(arch.layout().markers().is("portException"))
                  .and()
                  .resideOutsideOfPackages(
                      arch.layout().markers().declaringPackagePatterns().toArray(String[]::new))
                  .should(LayerConditions.be(arch.inApplication()))
                  .allowEmptyShould(true),
              arch.classes(),
              "a port exception - use-case or output-port - belongs to the application layer");
          collected.throwIfAny();
        })
    .selecting(
        "Classes anywhere on the classpath under scan that are assignable to the domain-exception"
            + " or the port-exception role, except the vocabulary's own code: the packages the"
            + " configured role types live in are excluded, so a project's own base class is not"
            + " reported as residing outside a layer it never claimed.")
    .checking(
        "A subtype of DomainException resides in <module>.domain.. of some module root, a"
            + " subtype of PortException - UseCaseException, OutputPortException and any other"
            + " port failure - in <module>.application... An output port's failure is declared"
            + " beside the port, even though the adapter that implements the port raises it."
            + " Both findings are"
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `inApplication()`, `inDomain()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ERR-002",
    "Domain and port exceptions reside in the layer whose failure they name",
    "The base type states which layer owns the failure; declaring it elsewhere puts the vocabulary"
        + " of that layer outside it and lets an adapter invent failures the application never"
        + " reports",
    arch =>
    {
        var violations = new List<string>();
        foreach (var type in ProjectExceptions(arch))
        {
            if (arch.Layout.Markers.Is(nameof(DcaMarkers.DomainException), type) && !arch.InDomain(type))
            {
                violations.Add($"{type.FullName} is a domain exception outside the domain layer");
            }

            if (arch.Layout.Markers.Is(nameof(DcaMarkers.PortException), type) && !arch.InApplication(type))
            {
                violations.Add($"{type.FullName} is a port exception - use-case or output-port - outside the application layer");
            }
        }

        DcaRule.Fail("An exception resides outside the layer its base type names", violations);
    })
    .Selecting(
        "Types anywhere under the root namespace that are assignable to DomainException or to "
        + "PortException, except the base types themselves and anything else in the "
        + "building-blocks namespace.")
    .Checking(
        "A subtype of DomainException resides under <Module>.Domain of some module root, a subtype "
        + "of PortException - UseCaseException, OutputPortException and any other port failure - under "
        + "<Module>.Application. An output port's failure is declared beside the port, even though the "
        + "adapter that implements the port raises it. Both findings are collected into one "
        + "violation. Which of the two a given failure should have been is not checked here. An "
        + "empty selection passes.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [OutputPortException](/marker/application/outputportexception.md)
- [PortException](/marker/application/portexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
