---
type: Rule
id: DCA-ONI-003
title: Domain Models must not carry container or persistence annotations
rule: "Domain models are framework-independent: no injectable stereotype makes them a managed component, no mapping annotation ties them to a persistence framework - the outgoing adapter maps them."
constraint: Domain Models must not carry container or persistence annotations.
selects: "Classes in <module>.domain.model.. of every module root."
checks: "None carries one of the configured injectable stereotypes or persistence-entity annotations directly on the class. Only the configured annotations are checked; other framework annotations, meta-annotations, and classes elsewhere in the domain layer (domain.service, domain.event) are not. With both roles empty the rule has nothing to forbid and passes."
enforced_by: "OnionRules#DCA-ONI-003"
status: enforced
rule_set: onion
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/OnionRules.java
tags: [onion, archunit]
---

## Selection

Classes in <module>.domain.model.. of every module root.

## Check

None carries one of the configured injectable stereotypes or persistence-entity annotations directly on the class. Only the configured annotations are checked; other framework annotations, meta-annotations, and classes elsewhere in the domain layer (domain.service, domain.event) are not. With both roles empty the rule has nothing to forbid and passes.

## .NET reading

**Selection.** Types in <module>.Domain.Model of every module root, the shared kernel's included when it owns a domain layer.

**Check.** Every attribute on the type or on one of its own, non-inherited members has a namespace below a prefix of the layout's third-party allow-list - by default System, Microsoft.Extensions.Logging.Abstractions and DomainCentric.BuildingBlocks. Any other attribute is reported, whatever framework it comes from; types elsewhere in the domain layer (Domain.Service, Domain.Event) are not selected.

## Implementation

```java
DcaRule.of(
        "DCA-ONI-003",
        "Domain Models must not carry container or persistence annotations",
        "Domain models are framework-independent: no injectable stereotype makes them a managed"
            + " component, no mapping annotation ties them to a persistence framework - the"
            + " outgoing adapter maps them",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allDomainModelPatterns())
                .should(
                    AnnotationRoles.beAnnotatedWithAny(
                        annotations.injectable(), annotations.persistenceEntity()))
                .allowEmptyShould(true))
    .selecting("Classes in <module>.domain.model.. of every module root.")
    .checking(
        "None carries one of the configured injectable stereotypes or persistence-entity"
            + " annotations directly on the class. Only the configured annotations are checked;"
            + " other framework annotations, meta-annotations, and classes elsewhere in the"
            + " domain layer (domain.service, domain.event) are not. With both roles empty the"
            + " rule has nothing to forbid and passes.")
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainModelPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
