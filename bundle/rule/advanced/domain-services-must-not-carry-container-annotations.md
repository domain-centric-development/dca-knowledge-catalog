---
type: Rule
id: DCA-ADV-011
title: Domain Services must not carry container annotations
rule: "Domain services are framework-independent - the application layer instantiates or wires them, the domain does not know the container."
constraint: Domain Services must not carry container annotations.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to DomainService.
checks: "None carries one of the configured injectable stereotypes directly on the class. Only the configured annotations are checked - others, and meta-annotations, are not. An empty selection passes, and so does an empty role."
enforced_by: "AdvancedPatternRules#DCA-ADV-011"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to DomainService.

## Check

None carries one of the configured injectable stereotypes directly on the class. Only the configured annotations are checked - others, and meta-annotations, are not. An empty selection passes, and so does an empty role.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IDomainService.

**Check.** Every attribute on the type itself - not on members, not inherited - has a type whose namespace lies below an allowed prefix: the configured third-party namespaces the domain may use (by default System, Microsoft.Extensions.Logging.Abstractions and DomainCentric.BuildingBlocks), the building blocks, or a domain namespace of some module root. Any other attribute is a framework attribute and is reported; a type without a loadable runtime type is skipped. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-011",
        "Domain Services must not carry container annotations",
        "Domain services are framework-independent - the application layer instantiates or"
            + " wires them, the domain does not know the container",
        arch ->
            noClasses()
                .that()
                .implement(DomainService.class)
                .should(AnnotationRoles.beAnnotatedWithAny(annotations.injectable()))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to"
            + " DomainService.")
    .checking(
        "None carries one of the configured injectable stereotypes directly on the class. Only"
            + " the configured annotations are checked - others, and meta-annotations, are not."
            + " An empty selection passes, and so does an empty role.")
```

## Helpers

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

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
