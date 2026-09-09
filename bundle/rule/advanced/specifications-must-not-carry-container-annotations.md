---
type: Rule
id: DCA-ADV-018
title: Specifications must not carry container annotations
rule: Specifications are framework-independent value objects.
constraint: Specifications must not carry container annotations.
selects: "Classes in <module>.domain.. of every module root whose simple name ends with Specification - interfaces included."
checks: "None carries one of the configured injectable stereotypes directly on the class. Only the configured annotations are checked - others, and meta-annotations, are not. An empty selection passes, and so does an empty role."
enforced_by: "AdvancedPatternRules#DCA-ADV-018"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Classes in <module>.domain.. of every module root whose simple name ends with Specification - interfaces included.

## Check

None carries one of the configured injectable stereotypes directly on the class. Only the configured annotations are checked - others, and meta-annotations, are not. An empty selection passes, and so does an empty role.

## .NET reading

**Selection.** Types in <module>.Domain of every module root whose simple name ends with Specification - interfaces included.

**Check.** Every attribute on the type itself - not on members, not inherited - has a type whose namespace lies below an allowed prefix: the configured third-party namespaces the domain may use (by default System, Microsoft.Extensions.Logging.Abstractions and DomainCentric.BuildingBlocks), the building blocks, or a domain namespace of some module root. Any other attribute is a framework attribute and is reported; a type without a loadable runtime type is skipped. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-018",
        "Specifications must not carry container annotations",
        "Specifications are framework-independent value objects",
        arch ->
            noClasses()
                .that()
                .haveSimpleNameEndingWith("Specification")
                .and()
                .resideInAnyPackage(arch.allDomainPatterns())
                .should(AnnotationRoles.beAnnotatedWithAny(annotations.injectable()))
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.domain.. of every module root whose simple name ends with Specification -"
            + " interfaces included.")
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

- [Specification<T>](/marker/tactical/specification.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
