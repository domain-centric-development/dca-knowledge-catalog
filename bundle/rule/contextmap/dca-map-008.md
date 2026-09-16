---
type: Rule
id: DCA-MAP-008
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter"
rule: "The ACL sits where the dependency crosses the boundary — outgoing adapters for synchronous API calls, incoming adapters for consumed events — and translates the upstream contract into the context's own model there."
constraint: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter."
selects: "Every @Upstream declaration with translation() ANTI_CORRUPTION_LAYER and status() IMPLEMENTED on the package-info of every package carrying @BoundedContext whose context() names an existing bounded context, reading via(). PLANNED declarations and declarations towards an unknown context are skipped, as in DCA-MAP-007."
checks: "No class below the declaring context's package outside the matching adapter depends on a class in the target context's channel sub-package or below: the outgoing adapter (<context>.adapter.outgoing..) for the API channel, the incoming adapter (<context>.adapter.incoming..) for the EVENTS channel. Each declared interaction also needs a class in that adapter depending on both that upstream channel and its own domain/application. Multiple upstream translators may share the package. Structure establishes a translation site, not translation quality."
enforced_by: "ContextMapRules#DCA-MAP-008"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ContextMapRules.cs
---

# Anti-Corruption Layer: upstream contract types must stay inside the matching adapter

## Selection

Every @Upstream declaration with translation() ANTI_CORRUPTION_LAYER and status() IMPLEMENTED on the package-info of every package carrying @BoundedContext whose context() names an existing bounded context, reading via(). PLANNED declarations and declarations towards an unknown context are skipped, as in DCA-MAP-007.

## Check

No class below the declaring context's package outside the matching adapter depends on a class in the target context's channel sub-package or below: the outgoing adapter (<context>.adapter.outgoing..) for the API channel, the incoming adapter (<context>.adapter.incoming..) for the EVENTS channel. Each declared interaction also needs a class in that adapter depending on both that upstream channel and its own domain/application. Multiple upstream translators may share the package. Structure establishes a translation site, not translation quality.

## .NET reading

**Selection.** Every [Upstream] declaration with Translation AntiCorruptionLayer and Status Implemented on the marker class of every namespace carrying [BoundedContext] whose Context names an existing bounded context, reading Via. Planned declarations and declarations towards an unknown context are skipped, as in DCA-MAP-007.

**Check.** No type below the declaring context's namespace outside the matching adapter depends on a type in the target context's channel namespace or below: the outgoing adapter (<context>.Adapter.Outgoing) for the Api channel, the incoming adapter (<context>.Adapter.Incoming) for the Events channel. Each declared interaction needs its own adapter class depending on that upstream channel and its own domain/application. Multiple upstream translators may share a package. Structure establishes a translation site, not translation quality.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-008",
        "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter",
        "The ACL sits where the dependency crosses the boundary — outgoing adapters for synchronous"
            + " API calls, incoming adapters for consumed events — and translates the upstream"
            + " contract into the context's own model there",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          Map<String, String> packagesByName = packagesByName(arch);
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
              String targetPkg = packagesByName.get(u.context());
              if (u.translation() != Upstream.Translation.ANTI_CORRUPTION_LAYER
                  || u.status() != Upstream.Status.IMPLEMENTED
                  || targetPkg == null) {
                continue;
              }
              for (Upstream.Consumes channel : u.via()) {
                String allowedAdapter =
                    channel == Upstream.Consumes.API
                        ? layout.outgoingAdapterPattern(pkg)
                        : layout.incomingAdapterPattern(pkg);
                String contractPattern = targetPkg + "." + channelName(arch, channel) + "..";
                boolean translationSite =
                    arch.classes().stream()
                        .filter(
                            c ->
                                com.tngtech.archunit.core.domain.JavaClass.Predicates
                                    .resideInAPackage(allowedAdapter)
                                    .test(c))
                        .anyMatch(
                            c ->
                                c.getDirectDependenciesFromSelf().stream()
                                        .anyMatch(
                                            d ->
                                                com.tngtech.archunit.core.domain.JavaClass
                                                    .Predicates.resideInAPackage(
                                                        contractPattern)
                                                    .test(d.getTargetClass()))
                                    && c.getDirectDependenciesFromSelf().stream()
                                        .anyMatch(
                                            d ->
                                                com.tngtech.archunit.core.domain.JavaClass
                                                    .Predicates.resideInAnyPackage(
                                                        layout.domainPattern(pkg),
                                                        layout.applicationPattern(pkg))
                                                    .test(d.getTargetClass())));
                violations.require(
                    translationSite,
                    "Context '"
                        + source
                        + "' needs translation evidence towards '"
                        + u.context()
                        + "' ("
                        + channelName(arch, channel)
                        + ") in "
                        + allowedAdapter);
                violations.addAll(
                    noClasses()
                        .that()
                        .resideInAPackage(pkg + "..")
                        .and()
                        .resideOutsideOfPackage(allowedAdapter)
                        .should()
                        .dependOnClassesThat()
                        .resideInAPackage(targetPkg + "." + channelName(arch, channel) + "..")
                        .allowEmptyShould(true),
                    arch.classes(),
                    "Context '"
                        + source
                        + "' declares ANTI_CORRUPTION_LAYER towards '"
                        + u.context()
                        + "' ("
                        + channelName(arch, channel)
                        + ") — upstream contract types must not leave "
                        + allowedAdapter
                        + "; translate them there into the context's own model");
              }
            }
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every @Upstream declaration with translation() ANTI_CORRUPTION_LAYER and status()"
            + " IMPLEMENTED on the package-info of every package carrying @BoundedContext whose"
            + " context() names an existing bounded context, reading via(). PLANNED"
            + " declarations and declarations towards an unknown context are skipped, as in"
            + " DCA-MAP-007.")
    .checking(
        "No class below the declaring context's package outside the matching adapter"
            + " depends on a class in the target context's channel sub-package or below:"
            + " the outgoing adapter (<context>.adapter.outgoing..) for the API channel,"
            + " the incoming adapter (<context>.adapter.incoming..) for the EVENTS channel."
            + " Each declared interaction also needs a class in that adapter depending on both that upstream channel and its own domain/application. Multiple upstream translators may share the package. Structure establishes a translation site, not translation quality.")
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

### `CollectedViolations.require`

```java
/** Records the violation unless the condition holds. */
  void require(boolean condition, String violation) {
    if (!condition) {
      add(violation);
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
        "DCA-MAP-008",
        "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter",
        "The ACL sits where the dependency crosses the boundary — outgoing adapters for synchronous API calls,"
            + " incoming adapters for consumed events — and translates the upstream contract into the context's"
            + " own model there",
        arch =>
        {
            var violations = new List<string>();
            var namespacesByName = NamespacesByName(arch);
            foreach (var ns in arch.BoundedContextNamespaces)
            {
                var source = ShortName(arch, ns);
                foreach (var u in arch.NamespaceAttributes<UpstreamAttribute>(ns))
                {
                    if (u.Translation != Translation.AntiCorruptionLayer || u.Status != UpstreamStatus.Implemented
                        || !namespacesByName.TryGetValue(u.Context, out var targetNs))
                    {
                        continue;
                    }
                    foreach (var channel in u.Via)
                    {
                        var allowedAdapter = channel == Consumes.Api
                            ? OutgoingAdapterNamespace(ns)
                            : IncomingAdapterNamespace(ns);
                        var channelNs = targetNs + "." + ChannelName(arch, channel);
                        var translationSite = TypesBelow(arch, allowedAdapter).Any(t => DependsOnNamespace(t, channelNs)
                            && (DependsOnNamespace(t, ns + "." + Layout.DomainSegment) || DependsOnNamespace(t, ns + "." + Layout.ApplicationSegment)));
                        if (!translationSite) violations.Add("Context '" + source + "' needs translation evidence towards '" + u.Context + "' (" + ChannelName(arch, channel) + ") in " + allowedAdapter);
                        foreach (var type in TypesBelow(arch, ns).Where(t => !IsBelow(t, allowedAdapter)))
                        {
                            if (DependsOnNamespace(type, channelNs))
                            {
                                violations.Add("Context '" + source + "' declares AntiCorruptionLayer towards '" + u.Context
                                    + "' (" + ChannelName(arch, channel) + ") — " + type.FullName + " uses upstream contract types"
                                    + " outside " + allowedAdapter + "; translate them there into the context's own model");
                            }
                        }
                    }
                }
            }
            DcaRule.Fail("Anti-Corruption Layer: upstream contract types must stay inside the matching adapter", violations);
        })
    .Selecting(
        "Every [Upstream] declaration with Translation AntiCorruptionLayer and Status Implemented"
            + " on the marker class of every namespace carrying [BoundedContext] whose Context"
            + " names an existing bounded context, reading Via. Planned declarations and"
            + " declarations towards an unknown context are skipped, as in DCA-MAP-007.")
    .Checking(
        "No type below the declaring context's namespace outside the matching adapter"
            + " depends on a type in the target context's channel namespace or below:"
            + " the outgoing adapter (<context>.Adapter.Outgoing) for the Api channel,"
            + " the incoming adapter (<context>.Adapter.Incoming) for the Events channel."
            + " Each declared interaction needs its own adapter class depending on that upstream channel and its own domain/application. Multiple upstream translators may share a package. Structure establishes a translation site, not translation quality.")
```

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
