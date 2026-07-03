---
type: Rule
title: Anti-Corruption Layer components must be in acl packages
rule: "Anti-Corruption Layer components must be in 'acl' packages for clear architectural intent (DDD Strategic Pattern)."
constraint: Anti-Corruption Layer components must be in acl packages.
enforced_by: "DddStrategicPatternsArchUnitTest#Anti-Corruption Layer components must be in acl packages"
status: enforced
test_class: DddStrategicPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddStrategicPatternsArchUnitTest.groovy
tags: [strategic, archunit]
---

```groovy
expect:
// ACL components translate between bounded contexts' ubiquitous languages
// They should be clearly marked in 'acl' packages for visibility
classes()
  .that().haveSimpleNameEndingWith("EventTranslator")
  .or().haveSimpleNameEndingWith("ACL")
  .or().haveSimpleNameEndingWith("AntiCorruptionLayer")
  .should().resideInAPackage("..acl..")
  .allowEmptyShould(true)
  .because("Anti-Corruption Layer components must be in 'acl' packages for clear architectural intent (DDD Strategic Pattern)")
  .check(allClasses)
```
