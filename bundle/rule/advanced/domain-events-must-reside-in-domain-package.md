---
type: Rule
id: DCA-ADV-002
title: Domain Events must reside in domain package
rule: "Domain events are part of the domain layer (named in past tense)."
constraint: Domain Events must reside in domain package.
enforced_by: "AdvancedPatternRules#DCA-ADV-002"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.of(
    "DCA-ADV-002",
    "Domain Events must reside in domain package",
    "Domain events are part of the domain layer (named in past tense)",
    arch ->
        classes()
            .that()
            .implement(DomainEvent.class)
            .should()
            .resideInAnyPackage(arch.allDomainPatterns())
            .allowEmptyShould(true))
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
