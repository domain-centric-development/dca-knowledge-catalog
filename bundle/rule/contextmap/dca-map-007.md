---
type: Rule
id: DCA-MAP-007
title: Implemented Upstream declarations must be backed by an actual code dependency
rule: "A declared IMPLEMENTED edge without any real dependency is stale (or premature — then it is PLANNED) and would otherwise pass forever alongside an equally stale module boundary entry."
constraint: Implemented Upstream declarations must be backed by an actual code dependency.
selects: "Every @Upstream declaration with status() IMPLEMENTED on the package-info of every package carrying @BoundedContext whose context() names an existing bounded context, reading via(). PLANNED declarations and declarations towards an unknown context are skipped."
checks: "For every channel in via(), at least one class anywhere below the declaring context's package has a direct dependency on a class in the target context's channel sub-package (api or events per the layout) or below. Which layer holds the dependency is not checked here."
enforced_by: "ContextMapRules#DCA-MAP-007"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ContextMapRules.cs
---

# Implemented Upstream declarations must be backed by an actual code dependency

## Selection

Every @Upstream declaration with status() IMPLEMENTED on the package-info of every package carrying @BoundedContext whose context() names an existing bounded context, reading via(). PLANNED declarations and declarations towards an unknown context are skipped.

## Check

For every channel in via(), at least one class anywhere below the declaring context's package has a direct dependency on a class in the target context's channel sub-package (api or events per the layout) or below. Which layer holds the dependency is not checked here.

## .NET reading

**Selection.** Every [Upstream] declaration with Status Implemented on the marker class of every namespace carrying [BoundedContext] whose Context names an existing bounded context, reading Via. Planned declarations and declarations towards an unknown context are skipped.

**Check.** For every channel in Via, at least one type anywhere below the declaring context's namespace has a direct dependency on a type in the target context's channel namespace (Api or Events per the layout) or below. Which layer holds the dependency is not checked here.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-007",
        "Implemented Upstream declarations must be backed by an actual code dependency",
        "A declared IMPLEMENTED edge without any real dependency is stale (or premature — then it"
            + " is PLANNED) and would otherwise pass forever alongside an equally stale module"
            + " boundary entry",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          Map<String, String> packagesByName = packagesByName(arch);
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
              String targetPkg = packagesByName.get(u.context());
              if (u.status() != Upstream.Status.IMPLEMENTED || targetPkg == null) {
                continue;
              }
              for (Upstream.Consumes channel : u.via()) {
                String channelPkg = targetPkg + "." + channelName(arch, channel);
                boolean exists = false;
                for (JavaClass javaClass : arch.classes()) {
                  if (!inPackageTree(javaClass.getPackageName(), pkg)) {
                    continue;
                  }
                  for (Dependency dep : javaClass.getDirectDependenciesFromSelf()) {
                    if (inPackageTree(dep.getTargetClass().getPackageName(), channelPkg)) {
                      exists = true;
                      break;
                    }
                  }
                  if (exists) {
                    break;
                  }
                }
                violations.require(
                    exists,
                    "Context '"
                        + source
                        + "' declares @Upstream(context = \""
                        + u.context()
                        + "\", via = "
                        + channelName(arch, channel)
                        + ") as IMPLEMENTED, but no class in '"
                        + pkg
                        + "' depends on '"
                        + channelPkg
                        + "..' — implement the dependency, mark the declaration status = PLANNED,"
                        + " or remove it");
              }
            }
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every @Upstream declaration with status() IMPLEMENTED on the package-info"
            + " of every package carrying @BoundedContext whose context() names an existing"
            + " bounded context, reading via(). PLANNED declarations and declarations"
            + " towards an unknown context are skipped.")
    .checking(
        "For every channel in via(), at least one class anywhere below the declaring"
            + " context's package has a direct dependency on a class in the target"
            + " context's channel sub-package (api or events per the layout) or below."
            + " Which layer holds the dependency is not checked here.")
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

### `inPackageTree`

```java
private static boolean inPackageTree(String packageName, String root) {
  return DcaArchitecture.inPackageTree(packageName, root);
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `classes()`, `contextName()`, `layout()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-MAP-007",
        "Implemented Upstream declarations must be backed by an actual code dependency",
        "A declared Implemented edge without any real dependency is stale (or premature — then it is Planned) and"
            + " would otherwise pass forever alongside an equally stale module boundary entry",
        arch =>
        {
            var violations = new List<string>();
            var namespacesByName = NamespacesByName(arch);
            foreach (var ns in arch.BoundedContextNamespaces)
            {
                var source = ShortName(arch, ns);
                foreach (var u in arch.NamespaceAttributes<UpstreamAttribute>(ns))
                {
                    if (u.Status != UpstreamStatus.Implemented || !namespacesByName.TryGetValue(u.Context, out var targetNs))
                    {
                        continue;
                    }
                    foreach (var channel in u.Via)
                    {
                        var channelNs = targetNs + "." + ChannelName(arch, channel);
                        var exists = TypesBelow(arch, ns).Any(t => DependsOnNamespace(t, channelNs));
                        if (!exists)
                        {
                            violations.Add("Context '" + source + "' declares [Upstream(\"" + u.Context + "\", via = "
                                + ChannelName(arch, channel) + ")] as Implemented, but no type in '" + ns + "' depends on '"
                                + channelNs + "' — implement the dependency, mark the declaration Status = Planned, or remove it");
                        }
                    }
                }
            }
            DcaRule.Fail("Implemented Upstream declarations must be backed by an actual code dependency", violations);
        })
    .Selecting(
        "Every [Upstream] declaration with Status Implemented on the marker class"
            + " of every namespace carrying [BoundedContext] whose Context names an existing"
            + " bounded context, reading Via. Planned declarations and declarations"
            + " towards an unknown context are skipped.")
    .Checking(
        "For every channel in Via, at least one type anywhere below the declaring"
            + " context's namespace has a direct dependency on a type in the target"
            + " context's channel namespace (Api or Events per the layout) or below."
            + " Which layer holds the dependency is not checked here.")
```

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
