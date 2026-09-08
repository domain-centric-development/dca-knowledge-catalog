---
type: Rule
id: DCA-MAP-011
title: Cross-context dependencies on published interfaces require an Upstream declaration
rule: Every real dependency on a foreign api/ or events/ package is a context-map edge and must be declared as such.
constraint: Cross-context dependencies on published interfaces require an Upstream declaration.
selects: "Every ordered pair of two distinct packages carrying @BoundedContext, combined with each published sub-package of the layout (api, events), for which the source context declares no @Upstream with context() naming the target and via() containing that channel. PLANNED declarations count as declared."
checks: "No class below the source context's package depends on a class in the target context's channel sub-package or below. Dependencies on a foreign context's other packages (domain, application, adapter) are not reported by this rule."
enforced_by: "ContextMapRules#DCA-MAP-011"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

## Selection

Every ordered pair of two distinct packages carrying @BoundedContext, combined with each published sub-package of the layout (api, events), for which the source context declares no @Upstream with context() naming the target and via() containing that channel. PLANNED declarations count as declared.

## Check

No class below the source context's package depends on a class in the target context's channel sub-package or below. Dependencies on a foreign context's other packages (domain, application, adapter) are not reported by this rule.

## .NET reading

**Selection.** Every ordered pair of two distinct namespaces carrying [BoundedContext], combined with each published segment of the layout (Api, Events), for which the source context declares no [Upstream] with Context naming the target and Via containing that channel. Planned declarations count as declared.

**Check.** No type below the source context's namespace depends on a type in the target context's channel namespace or below. Dependencies on a foreign context's other namespaces (Domain, Application, Adapter) are not reported by this rule.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-011",
        "Cross-context dependencies on published interfaces require an Upstream declaration",
        "Every real dependency on a foreign api/ or events/ package is a context-map edge and must"
            + " be declared as such",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          List<String> contexts = arch.boundedContextPackages();
          for (String srcPkg : contexts) {
            String source = arch.contextName(srcPkg);
            Set<String> declared = declaredEdges(arch, srcPkg);
            for (String tgtPkg : contexts) {
              if (tgtPkg.equals(srcPkg)) {
                continue;
              }
              String target = arch.contextName(tgtPkg);
              for (String channel : arch.layout().publishedSubpackages()) {
                if (declared.contains(target + " :: " + channel)) {
                  continue;
                }
                violations.addAll(
                    noClasses()
                        .that()
                        .resideInAPackage(srcPkg + "..")
                        .should()
                        .dependOnClassesThat()
                        .resideInAPackage(tgtPkg + "." + channel + "..")
                        .allowEmptyShould(true),
                    arch.classes(),
                    "Context '"
                        + source
                        + "' depends on '"
                        + target
                        + " :: "
                        + channel
                        + "' without declaring it — add @Upstream(context = \""
                        + target
                        + "\", translation = ..., via = ...) to its package-info");
              }
            }
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every ordered pair of two distinct packages carrying @BoundedContext,"
            + " combined with each published sub-package of the layout (api, events), for"
            + " which the source context declares no @Upstream with context() naming the"
            + " target and via() containing that channel. PLANNED declarations count as"
            + " declared.")
    .checking(
        "No class below the source context's package depends on a class in the"
            + " target context's channel sub-package or below. Dependencies on a foreign"
            + " context's other packages (domain, application, adapter) are not reported by"
            + " this rule.")
```

## Helpers

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

### `channelName`

```java
private static String channelName(DcaArchitecture arch, Upstream.Consumes channel) {
  return arch.layout().channelSubpackage(channel);
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

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
