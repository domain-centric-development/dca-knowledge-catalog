---
type: Rule
id: DCA-STR-009
title: Anti-Corruption Layer components must be in acl packages
rule: "Anti-Corruption Layer components must be in 'acl' packages for clear architectural intent (DDD Strategic Pattern)."
constraint: Anti-Corruption Layer components must be in acl packages.
enforced_by: "StrategicPatternRules#DCA-STR-009"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

```java
DcaRule.of(
    "DCA-STR-009",
    "Anti-Corruption Layer components must be in acl packages",
    "Anti-Corruption Layer components must be in 'acl' packages for clear architectural intent"
        + " (DDD Strategic Pattern)",
    arch ->
        classes()
            .that()
            .haveSimpleNameEndingWith("EventTranslator")
            .or()
            .haveSimpleNameEndingWith("ACL")
            .or()
            .haveSimpleNameEndingWith("AntiCorruptionLayer")
            .should()
            .resideInAPackage("..acl..")
            .allowEmptyShould(true))
```
