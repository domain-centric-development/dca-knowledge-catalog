---
type: Rule
id: DCA-MAP-012
title: "Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric"
rule: A partnership is a mutual commitment — it exists only when both contexts declare it.
constraint: "Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric."
selects: "Every @Partnership declaration on the package-info of every package carrying @BoundedContext, reading context()."
checks: "context() names an existing bounded context and is not the declaring context itself, and the target context's package-info carries a @Partnership whose context() names the declaring context in turn. A partnership grants no dependency permission - whether any code dependency exists between the two contexts is not checked."
enforced_by: "ContextMapRules#DCA-MAP-012"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ContextMapRules.cs
---

# Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric

## Selection

Every @Partnership declaration on the package-info of every package carrying @BoundedContext, reading context().

## Check

context() names an existing bounded context and is not the declaring context itself, and the target context's package-info carries a @Partnership whose context() names the declaring context in turn. A partnership grants no dependency permission - whether any code dependency exists between the two contexts is not checked.

## .NET reading

**Selection.** Every [Partnership] declaration on the marker class of every namespace carrying [BoundedContext], reading Context.

**Check.** Context names an existing bounded context and is not the declaring context itself, and the target context's marker class carries a [Partnership] whose Context names the declaring context in turn. A partnership grants no dependency permission - whether any code dependency exists between the two contexts is not checked.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-012",
        "Partnership declarations must reference an existing bounded context, never themselves,"
            + " and must be symmetric",
        "A partnership is a mutual commitment — it exists only when both contexts declare it",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          Map<String, String> packagesByName = packagesByName(arch);
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            for (Partnership p : arch.packageAnnotations(pkg, Partnership.class)) {
              if (!packagesByName.containsKey(p.context())) {
                violations.add(
                    "Context '"
                        + source
                        + "' declares @Partnership(context = \""
                        + p.context()
                        + "\") but no bounded context module with that name exists");
                continue;
              }
              if (p.context().equals(source)) {
                violations.add("Context '" + source + "' declares a partnership with itself");
                continue;
              }
              boolean reverse =
                  arch
                      .packageAnnotations(packagesByName.get(p.context()), Partnership.class)
                      .stream()
                      .anyMatch(r -> r.context().equals(source));
              violations.require(
                  reverse,
                  "Partnership between '"
                      + source
                      + "' and '"
                      + p.context()
                      + "' is only declared on '"
                      + source
                      + "' — partnerships are symmetric, add @Partnership(context = \""
                      + source
                      + "\") to '"
                      + p.context()
                      + "'");
            }
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every @Partnership declaration on the package-info of every package"
            + " carrying @BoundedContext, reading context().")
    .checking(
        "context() names an existing bounded context and is not the declaring"
            + " context itself, and the target context's package-info carries a"
            + " @Partnership whose context() names the declaring context in turn. A"
            + " partnership grants no dependency permission - whether any code dependency"
            + " exists between the two contexts is not checked.")
```

## Helpers

### `packagesByName`

```java
private static Map<String, String> packagesByName(DcaArchitecture arch) {
  Map<String, String> byName = new LinkedHashMap<>();
  arch.boundedContextPackages().forEach(p -> byName.put(arch.contextName(p), p));
  return byName;
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

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
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

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `contextName()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-MAP-012",
        "Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric",
        "A partnership is a mutual commitment — it exists only when both contexts declare it",
        arch =>
        {
            var violations = new List<string>();
            var namespacesByName = NamespacesByName(arch);
            foreach (var ns in arch.BoundedContextNamespaces)
            {
                var source = ShortName(arch, ns);
                foreach (var p in arch.NamespaceAttributes<PartnershipAttribute>(ns))
                {
                    if (!namespacesByName.TryGetValue(p.Context, out var partnerNs))
                    {
                        violations.Add("Context '" + source + "' declares [Partnership(\"" + p.Context
                            + "\")] but no bounded context module with that name exists");
                        continue;
                    }
                    if (p.Context == source)
                    {
                        violations.Add("Context '" + source + "' declares a partnership with itself");
                        continue;
                    }
                    var reverse = arch.NamespaceAttributes<PartnershipAttribute>(partnerNs).Any(r => r.Context == source);
                    if (!reverse)
                    {
                        violations.Add("Partnership between '" + source + "' and '" + p.Context + "' is only declared on '"
                            + source + "' — partnerships are symmetric, add [Partnership(\"" + source + "\")] to '"
                            + p.Context + "'");
                    }
                }
            }
            DcaRule.Fail("Partnership declarations must be symmetric and reference existing contexts", violations);
        })
    .Selecting(
        "Every [Partnership] declaration on the marker class of every namespace"
            + " carrying [BoundedContext], reading Context.")
    .Checking(
        "Context names an existing bounded context and is not the declaring"
            + " context itself, and the target context's marker class carries a"
            + " [Partnership] whose Context names the declaring context in turn. A"
            + " partnership grants no dependency permission - whether any code dependency"
            + " exists between the two contexts is not checked.")
```

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Partnership](/marker/strategic/partnership.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
