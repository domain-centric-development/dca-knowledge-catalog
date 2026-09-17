---
type: Rule
id: DCA-MAP-009
title: "Conformist: upstream contract types must never reach the domain layer"
rule: Conformism does not suspend domain purity — the domain layer stays free of foreign contract types.
constraint: "Conformist: upstream contract types must never reach the domain layer."
selects: "Every @Upstream declaration with translation() CONFORMIST and status() IMPLEMENTED on the package-info of every package carrying @BoundedContext whose context() names an existing bounded context, reading via(). PLANNED declarations and declarations towards an unknown context are skipped, as in DCA-MAP-007."
checks: "No class in the declaring context's domain layer (<context>.domain..) depends on a class in the target context's channel sub-package (api or events per the layout) or below. Application and adapter classes may use the upstream's contract types."
enforced_by: "ContextMapRules#DCA-MAP-009"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ContextMapRules.cs
---

# Conformist: upstream contract types must never reach the domain layer

## Selection

Every @Upstream declaration with translation() CONFORMIST and status() IMPLEMENTED on the package-info of every package carrying @BoundedContext whose context() names an existing bounded context, reading via(). PLANNED declarations and declarations towards an unknown context are skipped, as in DCA-MAP-007.

## Check

No class in the declaring context's domain layer (<context>.domain..) depends on a class in the target context's channel sub-package (api or events per the layout) or below. Application and adapter classes may use the upstream's contract types.

## .NET reading

**Selection.** Every [Upstream] declaration with Translation Conformist and Status Implemented on the marker class of every namespace carrying [BoundedContext] whose Context names an existing bounded context, reading Via. Planned declarations and declarations towards an unknown context are skipped, as in DCA-MAP-007.

**Check.** No type in the declaring context's domain layer (<context>.Domain and below) depends on a type in the target context's channel namespace (Api or Events per the layout) or below. Application and adapter types may use the upstream's contract types.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-009",
        "Conformist: upstream contract types must never reach the domain layer",
        "Conformism does not suspend domain purity — the domain layer stays free of foreign"
            + " contract types",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          Map<String, String> packagesByName = packagesByName(arch);
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
              String targetPkg = packagesByName.get(u.context());
              if (u.translation() != Upstream.Translation.CONFORMIST || targetPkg == null) {
                continue;
              }
              for (Upstream.Consumes channel : u.via()) {
                violations.addAll(
                    noClasses()
                        .that()
                        .resideInAPackage(layout.domainPattern(pkg))
                        .should()
                        .dependOnClassesThat()
                        .resideInAPackage(targetPkg + "." + channelName(arch, channel) + "..")
                        .allowEmptyShould(true),
                    arch.classes(),
                    "Context '"
                        + source
                        + "' conforms to '"
                        + u.context()
                        + "' ("
                        + channelName(arch, channel)
                        + "), but conformism does not suspend domain purity — the domain"
                        + " layer stays free of foreign contract types");
              }
            }
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every @Upstream declaration with translation() CONFORMIST on the package-info of"
            + " every package carrying @BoundedContext whose context() names an existing"
            + " bounded context, reading via(). status() is not consulted: this is a placement"
            + " check on code that exists, so a PLANNED declaration is checked too - one"
            + " without any dependent code passes; declarations towards an unknown context are"
            + " skipped.")
    .checking(
        "No class in the declaring context's domain layer (<context>.domain..)"
            + " depends on a class in the target context's channel sub-package (api or"
            + " events per the layout) or below. Application and adapter classes may use"
            + " the upstream's contract types. Whether an implementation exists is"
            + " DCA-MAP-007's question, not this rule's.")
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `classes()`, `contextName()`, `layout()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-MAP-009",
        "Conformist: upstream contract types must never reach the domain layer",
        "Conformism does not suspend domain purity — the domain layer stays free of foreign contract types",
        arch =>
        {
            var violations = new List<string>();
            var namespacesByName = NamespacesByName(arch);
            foreach (var ns in arch.BoundedContextNamespaces)
            {
                var source = ShortName(arch, ns);
                foreach (var u in arch.NamespaceAttributes<UpstreamAttribute>(ns))
                {
                    if (u.Translation != Translation.Conformist || !namespacesByName.TryGetValue(u.Context, out var targetNs))
                    {
                        continue;
                    }
                    foreach (var channel in u.Via)
                    {
                        var channelNs = targetNs + "." + ChannelName(arch, channel);
                        foreach (var type in TypesBelow(arch, DomainNamespace(ns)))
                        {
                            if (DependsOnNamespace(type, channelNs))
                            {
                                violations.Add("Context '" + source + "' conforms to '" + u.Context + "' (" + ChannelName(arch, channel)
                                    + "), but conformism does not suspend domain purity — " + type.FullName
                                    + " in the domain layer uses foreign contract types");
                            }
                        }
                    }
                }
            }
            DcaRule.Fail("Conformist: upstream contract types must never reach the domain layer", violations);
        })
    .Selecting(
        "Every [Upstream] declaration with Translation Conformist on the marker class of"
            + " every namespace carrying [BoundedContext] whose Context names an existing"
            + " bounded context, reading Via. Status is not consulted: this is a placement"
            + " check on code that exists, so a Planned declaration is checked too - one"
            + " without any dependent code passes; declarations towards an unknown context are"
            + " skipped.")
    .Checking(
        "No type in the declaring context's domain layer (<context>.Domain and below)"
            + " depends on a type in the target context's channel namespace (Api or"
            + " Events per the layout) or below. Whether an implementation exists is DCA-MAP-007's"
            + " question, not this rule's. Application and adapter types may use"
            + " the upstream's contract types.")
```

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
