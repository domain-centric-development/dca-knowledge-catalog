---
type: Rule
id: DCA-ADV-015
title: Factories must not carry container annotations
rule: Factories are framework-independent domain objects.
constraint: Factories must not carry container annotations.
selects: "Non-interface classes in <module>.domain.. of every module root that are assignable to Factory."
checks: "None carries one of the configured injectable stereotypes directly on the class. Only the configured annotations are checked - others, and meta-annotations, are not. An empty selection passes, and so does an empty role."
enforced_by: "AdvancedPatternRules#DCA-ADV-015"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface classes in <module>.domain.. of every module root that are assignable to Factory.

## Check

None carries one of the configured injectable stereotypes directly on the class. Only the configured annotations are checked - others, and meta-annotations, are not. An empty selection passes, and so does an empty role.

## .NET reading

**Selection.** Non-interface types in <module>.Domain of every module root that are assignable to IFactory.

**Check.** Every attribute on the type itself - not on members, not inherited - has a type whose namespace lies below an allowed prefix: the configured third-party namespaces the domain may use (by default System, Microsoft.Extensions.Logging.Abstractions and DomainCentric.BuildingBlocks), the building blocks, or a domain namespace of some module root. Any other attribute is a framework attribute and is reported; a type without a loadable runtime type is skipped. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-015",
        "Factories must not carry container annotations",
        "Factories are framework-independent domain objects",
        arch ->
            noClasses()
                .that()
                .implement(Factory.class)
                .and()
                .resideInAnyPackage(arch.allDomainPatterns())
                .should(AnnotationRoles.beAnnotatedWithAny(annotations.injectable()))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.domain.. of every module root that are assignable to"
            + " Factory.")
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

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Factory](/marker/tactical/factory.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
