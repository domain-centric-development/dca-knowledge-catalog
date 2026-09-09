---
type: Rule
id: DCA-MAP-005
title: "Upstream declarations must be unique per context and channel, and via must not be empty"
rule: "The identity of an @Upstream declaration is (context, via); different translations per channel require separate annotations."
constraint: "Upstream declarations must be unique per context and channel, and via must not be empty."
selects: "Every @Upstream declaration on the package-info of every package carrying @BoundedContext, reading context() and via(). PLANNED declarations are included."
checks: "via() holds at least one channel, and the pair (context, channel) - the channel resolved to the layout's api or events sub-package name - occurs at most once among the declarations of one context. Two declarations towards the same context on different channels are allowed; the same context and channel declared twice, even with different translations, is reported."
enforced_by: "ContextMapRules#DCA-MAP-005"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ContextMapRules.cs
---

# Upstream declarations must be unique per context and channel, and via must not be empty

## Selection

Every @Upstream declaration on the package-info of every package carrying @BoundedContext, reading context() and via(). PLANNED declarations are included.

## Check

via() holds at least one channel, and the pair (context, channel) - the channel resolved to the layout's api or events sub-package name - occurs at most once among the declarations of one context. Two declarations towards the same context on different channels are allowed; the same context and channel declared twice, even with different translations, is reported.

## .NET reading

**Selection.** Every [Upstream] declaration on the marker class of every namespace carrying [BoundedContext], reading Context and Via. Planned declarations are included.

**Check.** Via holds at least one channel, and the pair (context, channel) - the channel resolved to the layout's Api or Events segment name - occurs at most once among the declarations of one context. Two declarations towards the same context on different channels are allowed; the same context and channel declared twice, even with different translations, is reported.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-005",
        "Upstream declarations must be unique per context and channel, and via must not be empty",
        "The identity of an @Upstream declaration is (context, via); different translations per"
            + " channel require separate annotations",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            List<String> edges = new ArrayList<>();
            for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
              violations.require(
                  u.via().length > 0,
                  "Context '"
                      + source
                      + "': @Upstream(context = \""
                      + u.context()
                      + "\") declares no channel — via must not be empty");
              for (Upstream.Consumes channel : u.via()) {
                String edge = u.context() + " :: " + channelName(arch, channel);
                violations.require(
                    !edges.contains(edge),
                    "Context '"
                        + source
                        + "' declares (context, channel) '"
                        + edge
                        + "' more than once — the identity of an @Upstream declaration is"
                        + " (context, via); different translations per channel require separate"
                        + " annotations");
                edges.add(edge);
              }
            }
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every @Upstream declaration on the package-info of every package carrying"
            + " @BoundedContext, reading context() and via(). PLANNED declarations are"
            + " included.")
    .checking(
        "via() holds at least one channel, and the pair (context, channel) - the"
            + " channel resolved to the layout's api or events sub-package name - occurs at"
            + " most once among the declarations of one context. Two declarations towards"
            + " the same context on different channels are allowed; the same context and"
            + " channel declared twice, even with different translations, is reported.")
```

## Helpers

### `channelName`

```java
private static String channelName(DcaArchitecture arch, Upstream.Consumes channel) {
  return arch.layout().channelSubpackage(channel);
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `contextName()`, `layout()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-MAP-005",
        "Upstream declarations must be unique per context and channel, and via must not be empty",
        "The identity of an [Upstream] declaration is (context, via); different translations per channel"
            + " require separate attributes",
        arch =>
        {
            var violations = new List<string>();
            foreach (var ns in arch.BoundedContextNamespaces)
            {
                var source = ShortName(arch, ns);
                var edges = new List<string>();
                foreach (var u in arch.NamespaceAttributes<UpstreamAttribute>(ns))
                {
                    if (u.Via.Count == 0)
                    {
                        violations.Add("Context '" + source + "': [Upstream(\"" + u.Context
                            + "\")] declares no channel — via must not be empty");
                    }
                    foreach (var channel in u.Via)
                    {
                        var edge = u.Context + " :: " + ChannelName(arch, channel);
                        if (edges.Contains(edge))
                        {
                            violations.Add("Context '" + source + "' declares (context, channel) '" + edge
                                + "' more than once — the identity of an [Upstream] declaration is (context, via);"
                                + " different translations per channel require separate attributes");
                        }
                        edges.Add(edge);
                    }
                }
            }
            DcaRule.Fail("Upstream declarations must be unique per context and channel", violations);
        })
    .Selecting(
        "Every [Upstream] declaration on the marker class of every namespace carrying"
            + " [BoundedContext], reading Context and Via. Planned declarations are"
            + " included.")
    .Checking(
        "Via holds at least one channel, and the pair (context, channel) - the"
            + " channel resolved to the layout's Api or Events segment name - occurs at"
            + " most once among the declarations of one context. Two declarations towards"
            + " the same context on different channels are allowed; the same context and"
            + " channel declared twice, even with different translations, is reported.")
```

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
