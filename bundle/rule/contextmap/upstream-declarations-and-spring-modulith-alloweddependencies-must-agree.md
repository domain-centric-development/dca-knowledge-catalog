---
type: Rule
id: DCA-MAP-006
title: Upstream declarations and Spring Modulith allowedDependencies must agree
rule: Neither the context map nor the module boundary may know more than the other — an edge that exists only on one side is stale.
constraint: Upstream declarations and Spring Modulith allowedDependencies must agree.
selects: "Every package carrying @BoundedContext, provided the layout names a module annotation (Spring Modulith's @ApplicationModule) that is on the class path; reads its @Upstream declarations (context(), via(); PLANNED included) and, reflectively, the module annotation's allowedDependencies attribute. Without a configured and loadable module annotation the rule selects nothing and passes."
checks: "The set of declared edges 'context :: channel' equals the set of allowedDependencies entries of the form 'module :: named-interface' whose module is a bounded context, whitespace around '::' normalized. Entries without '::' and entries naming a non-context module are ignored; a context whose package-info carries no module annotation contributes an empty set, so its @Upstream declarations are reported as unmatched."
enforced_by: "ContextMapRules#DCA-MAP-006"
status: enforced
rule_set: contextmap
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
not_applicable_dotnet: Upstream declarations and Spring Modulith allowedDependencies must agree — .NET has no module system annotation; project boundaries take that role
---

## Selection

Every package carrying @BoundedContext, provided the layout names a module annotation (Spring Modulith's @ApplicationModule) that is on the class path; reads its @Upstream declarations (context(), via(); PLANNED included) and, reflectively, the module annotation's allowedDependencies attribute. Without a configured and loadable module annotation the rule selects nothing and passes.

## Check

The set of declared edges 'context :: channel' equals the set of allowedDependencies entries of the form 'module :: named-interface' whose module is a bounded context, whitespace around '::' normalized. Entries without '::' and entries naming a non-context module are ignored; a context whose package-info carries no module annotation contributes an empty set, so its @Upstream declarations are reported as unmatched.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-006",
        "Upstream declarations and Spring Modulith allowedDependencies must agree",
        "Neither the context map nor the module boundary may know more than the other — an edge"
            + " that exists only on one side is stale",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          Optional<Class<? extends Annotation>> moduleAnnotation = moduleAnnotationType();
          if (moduleAnnotation.isEmpty()) {
            return;
          }
          Set<String> moduleNames = moduleNames(arch);
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            Set<String> declared = declaredEdges(arch, pkg);
            Set<String> allowed = new LinkedHashSet<>();
            for (String entry : allowedDependencies(arch, pkg, moduleAnnotation.get())) {
              String normalized = entry.replaceAll("\\s*::\\s*", " :: ").trim();
              if (normalized.contains(" :: ")
                  && moduleNames.contains(normalized.split(" :: ")[0])) {
                allowed.add(normalized);
              }
            }
            violations.require(
                declared.equals(allowed),
                "Context '"
                    + source
                    + "': @Upstream declarations "
                    + new TreeSet<>(declared)
                    + " and @ApplicationModule.allowedDependencies named-interface entries "
                    + new TreeSet<>(allowed)
                    + " must describe the same edges — neither side may know more than the other");
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every package carrying @BoundedContext, provided the layout names a module"
            + " annotation (Spring Modulith's @ApplicationModule) that is on the class"
            + " path; reads its @Upstream declarations (context(), via(); PLANNED included)"
            + " and, reflectively, the module annotation's allowedDependencies attribute."
            + " Without a configured and loadable module annotation the rule selects"
            + " nothing and passes.")
    .checking(
        "The set of declared edges 'context :: channel' equals the set of"
            + " allowedDependencies entries of the form 'module :: named-interface' whose"
            + " module is a bounded context, whitespace around '::' normalized. Entries"
            + " without '::' and entries naming a non-context module are ignored; a context"
            + " whose package-info carries no module annotation contributes an empty set,"
            + " so its @Upstream declarations are reported as unmatched.")
```

## Helpers

### `moduleAnnotationType`

```java
private Optional<Class<? extends Annotation>> moduleAnnotationType() {
  if (!layout.frameworkAnnotations().hasApplicationModule()) {
    return Optional.empty();
  }
  String name = layout.frameworkAnnotations().applicationModule();
  try {
    Class<?> type = Class.forName(name, false, Thread.currentThread().getContextClassLoader());
    return type.isAnnotation()
        ? Optional.of((Class<? extends Annotation>) type)
        : Optional.empty();
  } catch (ClassNotFoundException e) {
    return Optional.empty();
  }
}
```

### `moduleNames`

```java
private static Set<String> moduleNames(DcaArchitecture arch) {
  Set<String> names = new LinkedHashSet<>();
  arch.boundedContextPackages().forEach(p -> names.add(arch.contextName(p)));
  return names;
}
```

### `declaredEdges`

```java
/** All declared upstream edges of a context as "target :: channel" strings. */
  private static Set<String> declaredEdges(DcaArchitecture arch, String contextPackage) {
    Set<String> edges = new LinkedHashSet<>();
    for (Upstream u : arch.packageAnnotations(contextPackage, Upstream.class)) {
      for (Upstream.Consumes channel : u.via()) {
        edges.add(u.context() + " :: " + channelName(arch, channel));
      }
    }
    return edges;
  }
```

### `allowedDependencies`

```java
private static List<String> allowedDependencies(
    DcaArchitecture arch, String pkg, Class<? extends Annotation> moduleAnnotation) {
  Optional<? extends Annotation> module = arch.packageAnnotation(pkg, moduleAnnotation);
  if (module.isEmpty()) {
    return List.of();
  }
  try {
    Method attribute = moduleAnnotation.getMethod("allowedDependencies");
    Object value = attribute.invoke(module.get());
    return value instanceof String[] ? Arrays.asList((String[]) value) : List.of();
  } catch (ReflectiveOperationException e) {
    return List.of();
  }
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

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
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

### `channelName`

```java
private static String channelName(DcaArchitecture arch, Upstream.Consumes channel) {
  return arch.layout().channelSubpackage(channel);
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

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `contextName()`, `layout()`, `packageAnnotation()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
