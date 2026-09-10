---
type: Rule
id: DCA-NAM-002
title: "Diagnostic: use cases without injectable stereotypes"
rule: Use cases may be registered by configuration or annotated; static references cannot prove wiring.
constraint: "Diagnostic: use cases without injectable stereotypes."
selects: Concrete non-nested application operations selected by InputPort marker or use-case suffix when the injectable role is configured.
checks: "Informational diagnostic only: lists operations without a direct or composed injectable stereotype and never fails. Configuration registration is equally valid; this does not prove wiring."
enforced_by: "NamingRules#DCA-NAM-002"
status: informational
rule_set: naming
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
not_applicable_dotnet: ".NET has no injectable stereotype attribute — use cases are registered in the DI container by code, there is no attribute to check"
---

# Diagnostic: use cases without injectable stereotypes

## Selection

Concrete non-nested application operations selected by InputPort marker or use-case suffix when the injectable role is configured.

## Check

Informational diagnostic only: lists operations without a direct or composed injectable stereotype and never fails. Configuration registration is equally valid; this does not prove wiring.

## Implementation

```java
DcaRule.informational(
        "DCA-NAM-002",
        "Diagnostic: use cases without injectable stereotypes",
        "Use cases may be registered by configuration or annotated; static references cannot prove wiring",
        arch -> {
          List<String> injectable = layout.frameworkAnnotations().injectable();
          if (injectable.isEmpty()) return;
          for (var type : arch.classes()) {
            if (!type.isInterface()
                && !type.isNestedClass()
                && com.tngtech.archunit.core.domain.JavaClass.Predicates.resideInAnyPackage(
                        arch.allApplicationPatterns())
                    .test(type)
                && (type.isAssignableTo(InputPort.class)
                    || type.getSimpleName().endsWith(layout.useCaseSuffix()))
                && !AnnotationRoles.annotatedWithAny(injectable).test(type)
                && !AnnotationRoles.isMetaAnnotatedWithAny(type, injectable)) {
              System.out.println(
                  "[DCA-NAM-002] "
                      + type.getName()
                      + ": register by configuration or annotate");
            }
          }
        })
    .selecting(
        "Concrete non-nested application operations selected by InputPort marker or use-case suffix when the injectable role is configured.")
    .checking(
        "Informational diagnostic only: lists operations without a direct or composed injectable stereotype and never fails. Configuration registration is equally valid; this does not prove wiring.")
```

## Helpers

### `AnnotationRoles.annotatedWithAny`

```java
/** Directly annotated with any annotation of the role; never true for an empty role. */
  static DescribedPredicate<CanBeAnnotated> annotatedWithAny(List<String> role) {
    if (role.isEmpty()) {
      return DescribedPredicate.<CanBeAnnotated>alwaysFalse()
          .as("annotated with a configured annotation (none configured)");
    }
    DescribedPredicate<CanBeAnnotated> predicate =
        CanBeAnnotated.Predicates.annotatedWith(role.get(0));
    for (String fqn : role.subList(1, role.size())) {
      predicate = predicate.or(CanBeAnnotated.Predicates.annotatedWith(fqn));
    }
    return predicate.as("annotated with any of " + role);
  }

static DescribedPredicate<CanBeAnnotated> annotatedWithAny(List<String>... roles) {
  DescribedPredicate<CanBeAnnotated> predicate = null;
  for (List<String> role : roles) {
    if (role.isEmpty()) {
      continue;
    }
    predicate = predicate == null ? annotatedWithAny(role) : predicate.or(annotatedWithAny(role));
  }
  return predicate == null
      ? DescribedPredicate.<CanBeAnnotated>alwaysFalse()
          .as("annotated with a configured annotation (none configured)")
      : predicate;
}
```

### `AnnotationRoles.isMetaAnnotatedWithAny`

```java
/** Meta-annotated with any annotation of the role; false for an empty role. */
  static boolean isMetaAnnotatedWithAny(CanBeAnnotated item, List<String> role) {
    for (String fqn : role) {
      if (item.isMetaAnnotatedWith(fqn)) {
        return true;
      }
    }
    return false;
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
