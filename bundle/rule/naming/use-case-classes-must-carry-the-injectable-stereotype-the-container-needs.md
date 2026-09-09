---
type: Rule
id: DCA-NAM-002
title: Use case classes must carry the injectable stereotype the container needs
rule: "Use cases are container-managed components: the incoming adapters receive them by injection, and the container's transaction and event plumbing only applies to managed beans."
constraint: Use case classes must carry the injectable stereotype the container needs.
selects: "Non-interface classes in <module>.application.. of every module root whose simple name ends with the configured use-case suffix - provided the layout configures at least one injectable stereotype; with an empty role (a hand-wired application) nothing is selected."
checks: The class is directly annotated with one of the configured injectable stereotypes. Records are selected like any other class; the marker interfaces are not consulted - only the suffix selects. An empty selection passes.
enforced_by: "NamingRules#DCA-NAM-002"
status: enforced
rule_set: naming
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
not_applicable_dotnet: ".NET has no injectable stereotype attribute — use cases are registered in the DI container by code, there is no attribute to check"
---

## Selection

Non-interface classes in <module>.application.. of every module root whose simple name ends with the configured use-case suffix - provided the layout configures at least one injectable stereotype; with an empty role (a hand-wired application) nothing is selected.

## Check

The class is directly annotated with one of the configured injectable stereotypes. Records are selected like any other class; the marker interfaces are not consulted - only the suffix selects. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-002",
        "Use case classes must carry the injectable stereotype the container needs",
        "Use cases are container-managed components: the incoming adapters receive them by"
            + " injection, and the container's transaction and event plumbing only applies to"
            + " managed beans",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .haveSimpleNameEndingWith(layout.useCaseSuffix())
                .and()
                .areNotInterfaces()
                .and(AnnotationRoles.whenConfigured(injectable))
                .should(AnnotationRoles.beAnnotatedWithAny(injectable))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.application.. of every module root whose simple name"
            + " ends with the configured use-case suffix - provided the layout configures at"
            + " least one injectable stereotype; with an empty role (a hand-wired application)"
            + " nothing is selected.")
    .checking(
        "The class is directly annotated with one of the configured injectable stereotypes."
            + " Records are selected like any other class; the marker interfaces are not"
            + " consulted - only the suffix selects. An empty selection passes.")
```

## Helpers

### `AnnotationRoles.whenConfigured`

```java
/** {@code alwaysTrue} when the role is configured, {@code alwaysFalse} otherwise. */
  static DescribedPredicate<JavaClass> whenConfigured(List<String> role) {
    return role.isEmpty()
        ? DescribedPredicate.<JavaClass>alwaysFalse()
            .as("a configured annotation exists (none does)")
        : DescribedPredicate.<JavaClass>alwaysTrue().as("a configured annotation exists");
  }
```

### `AnnotationRoles.beAnnotatedWithAny`

```java
static ArchCondition<JavaClass> beAnnotatedWithAny(List<String>... roles) {
  List<String> all = new ArrayList<>();
  for (List<String> role : roles) {
    for (String fqn : role) {
      if (!all.contains(fqn)) {
        all.add(fqn);
      }
    }
  }
  if (all.isEmpty()) {
    return new ArchCondition<>("be annotated with a configured annotation (none configured)") {
      @Override
      public void check(JavaClass item, ConditionEvents events) {
        // nothing configured, nothing to record
      }
    };
  }
  ArchCondition<JavaClass> condition = ArchConditions.beAnnotatedWith(all.get(0));
  for (String fqn : all.subList(1, all.size())) {
    condition = condition.or(ArchConditions.beAnnotatedWith(fqn));
  }
  return condition;
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
