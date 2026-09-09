---
type: Rule
id: DCA-ADV-004
title: Domain Events must not carry container annotations
rule: Domain events are framework-independent plain objects - neither managed components nor listeners.
constraint: Domain Events must not carry container annotations.
selects: "Non-interface classes in <module>.domain.. of every module root that are assignable to DomainEvent."
checks: "None carries one of the configured injectable stereotypes or event-listener annotations directly on the class. Only the configured annotations are checked - others, and meta-annotations, are not. An empty selection passes, and so do empty roles."
enforced_by: "AdvancedPatternRules#DCA-ADV-004"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface classes in <module>.domain.. of every module root that are assignable to DomainEvent.

## Check

None carries one of the configured injectable stereotypes or event-listener annotations directly on the class. Only the configured annotations are checked - others, and meta-annotations, are not. An empty selection passes, and so do empty roles.

## .NET reading

**Selection.** Non-interface types in <module>.Domain of every module root that are assignable to IDomainEvent.

**Check.** Every attribute on the type itself - not on members, not inherited - has a type whose namespace lies below an allowed prefix: the configured third-party namespaces the domain may use (by default System, Microsoft.Extensions.Logging.Abstractions and DomainCentric.BuildingBlocks), the building blocks, or a domain namespace of some module root. Any other attribute is a framework attribute and is reported; a type without a loadable runtime type is skipped. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-004",
        "Domain Events must not carry container annotations",
        "Domain events are framework-independent plain objects - neither managed components nor"
            + " listeners",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allDomainPatterns())
                .and()
                .implement(DomainEvent.class)
                .should(
                    AnnotationRoles.beAnnotatedWithAny(
                        annotations.injectable(), annotations.eventListener()))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.domain.. of every module root that are assignable to"
            + " DomainEvent.")
    .checking(
        "None carries one of the configured injectable stereotypes or event-listener annotations"
            + " directly on the class. Only the configured annotations are checked - others, and"
            + " meta-annotations, are not. An empty selection passes, and so do empty roles.")
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

- [DomainEvent](/marker/tactical/domainevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
