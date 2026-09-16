---
type: Rule
id: DCA-MAP-006
title: Upstream declarations and the module declaration's allowed dependencies must agree
rule: Neither the context map nor the module boundary may know more than the other — an edge that exists only on one side is stale.
constraint: Upstream declarations and the module declaration's allowed dependencies must agree.
selects: "Every package carrying @BoundedContext, provided the layout configures at least one module declaration annotation (a module system's per-package declaration, for example Spring Modulith's) that is on the class path; reads its @Upstream declarations (context(), via(); PLANNED included) and, reflectively, the allowedDependencies attribute of every configured and loadable module declaration the package carries. Without a configured and loadable module declaration the rule selects nothing and passes."
checks: "The set of declared edges 'context :: channel' equals the set of allowedDependencies entries of the form 'module :: named-interface' whose module is a bounded context, whitespace around '::' normalized. Entries without '::' and entries naming a non-context module are ignored. A context that declares @Upstream edges but whose package-info carries none of the configured module declaration annotations is reported once, as a missing module declaration with unknown allowed dependencies - its edges are not compared; a context without @Upstream declarations and without a module declaration has nothing to compare and passes."
enforced_by: "ContextMapRules#DCA-MAP-006"
status: enforced
rule_set: contextmap
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
not_applicable_dotnet: Upstream declarations and the module declaration's allowed dependencies must agree — .NET has no module-declaration attribute; project boundaries take that role
---

# Upstream declarations and the module declaration's allowed dependencies must agree

## Selection

Every package carrying @BoundedContext, provided the layout configures at least one module declaration annotation (a module system's per-package declaration, for example Spring Modulith's) that is on the class path; reads its @Upstream declarations (context(), via(); PLANNED included) and, reflectively, the allowedDependencies attribute of every configured and loadable module declaration the package carries. Without a configured and loadable module declaration the rule selects nothing and passes.

## Check

The set of declared edges 'context :: channel' equals the set of allowedDependencies entries of the form 'module :: named-interface' whose module is a bounded context, whitespace around '::' normalized. Entries without '::' and entries naming a non-context module are ignored. A context that declares @Upstream edges but whose package-info carries none of the configured module declaration annotations is reported once, as a missing module declaration with unknown allowed dependencies - its edges are not compared; a context without @Upstream declarations and without a module declaration has nothing to compare and passes.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-006",
        "Upstream declarations and the module declaration's allowed dependencies must agree",
        "Neither the context map nor the module boundary may know more than the other — an edge"
            + " that exists only on one side is stale",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          List<Class<? extends Annotation>> moduleAnnotations = moduleAnnotationTypes();
          if (moduleAnnotations.isEmpty()) {
            return;
          }
          Set<String> moduleNames = moduleNames(arch);
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            Set<String> declared = declaredEdges(arch, pkg);
            if (!declared.isEmpty()
                && !carriesModuleDeclaration(arch, pkg, moduleAnnotations)) {
              violations.add(
                  "Context '"
                      + source
                      + "': module declaration missing on '"
                      + source
                      + "', allowed dependencies unknown - it declares @Upstream edges "
                      + new TreeSet<>(declared)
                      + " but its package-info carries none of the configured module"
                      + " declaration annotations; declare the module there so both sides can"
                      + " be compared");
              continue;
            }
            Set<String> allowed = new LinkedHashSet<>();
            for (String entry : allowedDependencies(arch, pkg, moduleAnnotations)) {
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
                    + " and the module declaration's allowedDependencies named-interface entries "
                    + new TreeSet<>(allowed)
                    + " must describe the same edges — neither side may know more than the other");
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every package carrying @BoundedContext, provided the layout configures at least one"
            + " module declaration annotation (a module system's per-package declaration, for"
            + " example Spring Modulith's) that is on the class path; reads its @Upstream"
            + " declarations (context(), via(); PLANNED included) and, reflectively, the"
            + " allowedDependencies attribute of every configured and loadable module"
            + " declaration the package carries. Without a configured and loadable module"
            + " declaration the rule selects nothing and passes.")
    .checking(
        "The set of declared edges 'context :: channel' equals the set of"
            + " allowedDependencies entries of the form 'module :: named-interface' whose"
            + " module is a bounded context, whitespace around '::' normalized. Entries"
            + " without '::' and entries naming a non-context module are ignored. A context"
            + " that declares @Upstream edges but whose package-info carries none of the"
            + " configured module declaration annotations is reported once, as a missing"
            + " module declaration with unknown allowed dependencies - its edges are not"
            + " compared; a context without @Upstream declarations and without a module"
            + " declaration has nothing to compare and passes.")
```

## Helpers

### `moduleAnnotationTypes`

```java
private List<Class<? extends Annotation>> moduleAnnotationTypes() {
  List<Class<? extends Annotation>> types = new ArrayList<>();
  for (String name : layout.frameworkAnnotations().moduleDeclaration()) {
    try {
      Class<?> type = Class.forName(name, false, Thread.currentThread().getContextClassLoader());
      if (type.isAnnotation()) {
        types.add((Class<? extends Annotation>) type);
      }
    } catch (ClassNotFoundException e) {
      // not on the class path - a declaration the project does not use
    }
  }
  return types;
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

### `carriesModuleDeclaration`

```java
/** Whether the package carries at least one of the configured module declarations. */
  private static boolean carriesModuleDeclaration(
      DcaArchitecture arch, String pkg, List<Class<? extends Annotation>> moduleAnnotations) {
    return moduleAnnotations.stream()
        .anyMatch(annotation -> arch.packageAnnotation(pkg, annotation).isPresent());
  }
```

### `allowedDependencies`

```java
/**
   * The {@code allowedDependencies} of every module declaration the package actually carries - a
   * package may use any of the configured declarations, and a package carrying none contributes
   * nothing.
   */
  private static List<String> allowedDependencies(
      DcaArchitecture arch, String pkg, List<Class<? extends Annotation>> moduleAnnotations) {
    List<String> allowed = new ArrayList<>();
    for (Class<? extends Annotation> moduleAnnotation : moduleAnnotations) {
      Optional<? extends Annotation> module = arch.packageAnnotation(pkg, moduleAnnotation);
      if (module.isEmpty()) {
        continue;
      }
      try {
        Method attribute = moduleAnnotation.getMethod("allowedDependencies");
        Object value = attribute.invoke(module.get());
        if (value instanceof String[]) {
          allowed.addAll(Arrays.asList((String[]) value));
        }
      } catch (ReflectiveOperationException e) {
        // a declaration without that attribute contributes nothing
      }
    }
    return allowed;
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

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
