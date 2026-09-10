---
type: Rule
id: DCA-MAP-001
title: "Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages"
rule: "Context map declarations are reserved for bounded contexts — only a context can be downstream of, or partner with, another."
constraint: "Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages."
selects: "Every package at or below the base package that an imported class lives in, its ancestors included, whose package-info does not carry @BoundedContext. The resolved context roots themselves are skipped."
checks: "The package declares no @Upstream, @ExternalUpstream or @Partnership. A declaration on a nested package (a use-case, feature or grouping package) is reported; whether a declaration is well-formed is left to the other rules."
enforced_by: "ContextMapRules#DCA-MAP-001"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ContextMapRules.cs
---

# Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages

## Selection

Every package at or below the base package that an imported class lives in, its ancestors included, whose package-info does not carry @BoundedContext. The resolved context roots themselves are skipped.

## Check

The package declares no @Upstream, @ExternalUpstream or @Partnership. A declaration on a nested package (a use-case, feature or grouping package) is reported; whether a declaration is well-formed is left to the other rules.

## .NET reading

**Selection.** Every namespace at or below the root namespace that a loaded type lives in, its ancestors included, that carries no marker class with [BoundedContext]. The resolved context roots themselves are skipped.

**Check.** No class residing exactly in the namespace declares [Upstream], [ExternalUpstream] or [Partnership]. A declaration on a nested namespace (a use-case, feature or grouping namespace) is reported; whether a declaration is well-formed is left to the other rules.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-001",
        "Upstream, ExternalUpstream, and Partnership may only be declared on bounded context"
            + " packages",
        "Context map declarations are reserved for bounded contexts — only a context can be"
            + " downstream of, or partner with, another",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          for (String pkg : arch.packagesBelowBase()) {
            if (arch.packageAnnotation(pkg, BoundedContext.class).isPresent()) {
              continue;
            }
            requireNoDeclaration(violations, arch, pkg, Upstream.class, "@Upstream");
            requireNoDeclaration(
                violations, arch, pkg, ExternalUpstream.class, "@ExternalUpstream");
            requireNoDeclaration(violations, arch, pkg, Partnership.class, "@Partnership");
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every package at or below the base package that an imported class lives in,"
            + " its ancestors included, whose package-info does not carry @BoundedContext."
            + " The resolved context roots themselves are skipped.")
    .checking(
        "The package declares no @Upstream, @ExternalUpstream or @Partnership. A"
            + " declaration on a nested package (a use-case, feature or grouping package)"
            + " is reported; whether a declaration is well-formed is left to the other"
            + " rules.")
```

## Helpers

### `requireNoDeclaration`

```java
private static void requireNoDeclaration(
    CollectedViolations violations,
    DcaArchitecture arch,
    String pkg,
    Class<? extends Annotation> type,
    String label) {
  violations.require(
      arch.packageAnnotations(pkg, type).isEmpty(),
      "Package '"
          + pkg
          + "' declares "
          + label
          + " but is not a @BoundedContext — context map declarations are reserved for bounded"
          + " contexts; declare the relationship on the context's root package");
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

### `CollectedViolations.require`

```java
/** Records the violation unless the condition holds. */
  void require(boolean condition, String violation) {
    if (!condition) {
      add(violation);
    }
  }
```

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
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

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `packageAnnotation()`, `packageAnnotations()`, `packagesBelowBase()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-MAP-001",
        "Upstream, ExternalUpstream, and Partnership may only be declared on bounded context namespaces",
        "Context map declarations are reserved for bounded contexts — only a context can be downstream of,"
            + " or partner with, another",
        arch =>
        {
            var violations = new List<string>();
            foreach (var ns in arch.NamespacesBelowRoot())
            {
                if (arch.NamespaceAttribute<BoundedContextAttribute>(ns) is not null)
                {
                    continue;
                }
                RequireNoDeclaration<UpstreamAttribute>(arch, ns, "[Upstream]", violations);
                RequireNoDeclaration<ExternalUpstreamAttribute>(arch, ns, "[ExternalUpstream]", violations);
                RequireNoDeclaration<PartnershipAttribute>(arch, ns, "[Partnership]", violations);
            }
            DcaRule.Fail("Context map declarations are reserved for bounded contexts", violations);
        })
    .Selecting(
        "Every namespace at or below the root namespace that a loaded type lives in,"
            + " its ancestors included, that carries no marker class with [BoundedContext]."
            + " The resolved context roots themselves are skipped.")
    .Checking(
        "No class residing exactly in the namespace declares [Upstream], [ExternalUpstream] or"
            + " [Partnership]. A declaration on a nested namespace (a use-case, feature or grouping"
            + " namespace) is reported; whether a declaration is well-formed is left to the other"
            + " rules.")
```

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
