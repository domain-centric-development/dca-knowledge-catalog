---
type: Rule
id: DCA-MAP-002
title: ExternalUpstream declarations must be well-formed and unique per name and interaction
rule: "The identity of an @ExternalUpstream declaration is (name, interaction); internal contexts are declared with @Upstream instead."
constraint: ExternalUpstream declarations must be well-formed and unique per name and interaction.
selects: "Every @ExternalUpstream declaration on the package-info of every package carrying @BoundedContext, reading name() and interaction(). PLANNED declarations are included."
checks: "name() is not blank and is not the name of an internal bounded context (a context's package name relative to the base package), and the pair (name, interaction) occurs at most once per declaring context. The same external system declared by two different contexts is not reported; translation() and contractPackages() are not checked here."
enforced_by: "ContextMapRules#DCA-MAP-002"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ContextMapRules.cs
---

# ExternalUpstream declarations must be well-formed and unique per name and interaction

## Selection

Every @ExternalUpstream declaration on the package-info of every package carrying @BoundedContext, reading name() and interaction(). PLANNED declarations are included.

## Check

name() is not blank and is not the name of an internal bounded context (a context's package name relative to the base package), and the pair (name, interaction) occurs at most once per declaring context. The same external system declared by two different contexts is not reported; translation() and contractPackages() are not checked here.

## .NET reading

**Selection.** Every [ExternalUpstream] declaration on the marker class of every namespace carrying [BoundedContext], reading Name and Interaction. Planned declarations are included.

**Check.** Name is not blank and is not the name of an internal bounded context (a context's namespace relative to the root namespace), and the pair (name, interaction) occurs at most once per declaring context. The same external system declared by two different contexts is not reported; Translation and ContractNamespaces are not checked here.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-002",
        "ExternalUpstream declarations must be well-formed and unique per name and interaction",
        "The identity of an @ExternalUpstream declaration is (name, interaction); internal"
            + " contexts are declared with @Upstream instead",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          Set<String> moduleNames = moduleNames(arch);
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            List<String> edges = new ArrayList<>();
            for (ExternalUpstream e : arch.packageAnnotations(pkg, ExternalUpstream.class)) {
              violations.require(
                  !e.name().isBlank(),
                  "Context '" + source + "' declares an @ExternalUpstream with a blank name");
              violations.require(
                  !moduleNames.contains(e.name()),
                  "Context '"
                      + source
                      + "' declares external system '"
                      + e.name()
                      + "', which is an internal bounded context module — use @Upstream for"
                      + " internal contexts");
              String edge = e.name() + " :: " + e.interaction();
              violations.require(
                  !edges.contains(edge),
                  "Context '"
                      + source
                      + "' declares external system edge '"
                      + edge
                      + "' more than once — the identity of an @ExternalUpstream declaration is"
                      + " (name, interaction)");
              edges.add(edge);
            }
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every @ExternalUpstream declaration on the package-info of every package"
            + " carrying @BoundedContext, reading name() and interaction(). PLANNED"
            + " declarations are included.")
    .checking(
        "name() is not blank and is not the name of an internal bounded context (a"
            + " context's package name relative to the base package), and the pair (name,"
            + " interaction) occurs at most once per declaring context. The same external"
            + " system declared by two different contexts is not reported; translation()"
            + " and contractPackages() are not checked here.")
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

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
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
        "DCA-MAP-002",
        "ExternalUpstream declarations must be well-formed and unique per name and interaction",
        "The identity of an [ExternalUpstream] declaration is (name, interaction); internal contexts are"
            + " declared with [Upstream] instead",
        arch =>
        {
            var violations = new List<string>();
            var moduleNames = ModuleNames(arch);
            foreach (var ns in arch.BoundedContextNamespaces)
            {
                var source = ShortName(arch, ns);
                var edges = new List<string>();
                foreach (var e in arch.NamespaceAttributes<ExternalUpstreamAttribute>(ns))
                {
                    if (string.IsNullOrWhiteSpace(e.Name))
                    {
                        violations.Add("Context '" + source + "' declares an [ExternalUpstream] with a blank name");
                    }
                    if (moduleNames.Contains(e.Name))
                    {
                        violations.Add("Context '" + source + "' declares external system '" + e.Name
                            + "', which is an internal bounded context module — use [Upstream] for internal contexts");
                    }
                    var edge = e.Name + " :: " + e.Interaction;
                    if (edges.Contains(edge))
                    {
                        violations.Add("Context '" + source + "' declares external system edge '" + edge
                            + "' more than once — the identity of an [ExternalUpstream] declaration is (name, interaction)");
                    }
                    edges.Add(edge);
                }
            }
            DcaRule.Fail("ExternalUpstream declarations must be well-formed and unique per name and interaction", violations);
        })
    .Selecting(
        "Every [ExternalUpstream] declaration on the marker class of every namespace"
            + " carrying [BoundedContext], reading Name and Interaction. Planned"
            + " declarations are included.")
    .Checking(
        "Name is not blank and is not the name of an internal bounded context (a"
            + " context's namespace relative to the root namespace), and the pair (name,"
            + " interaction) occurs at most once per declaring context. The same external"
            + " system declared by two different contexts is not reported; Translation"
            + " and ContractNamespaces are not checked here.")
```

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
