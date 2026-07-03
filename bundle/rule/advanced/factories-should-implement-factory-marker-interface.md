---
type: Rule
title: Factories should implement Factory Marker Interface
rule: Classes implementing Factory marker should have 'Factory' in their name.
constraint: Factories should implement Factory Marker Interface.
enforced_by: "DddAdvancedPatternsArchUnitTest#Factories should implement Factory Marker Interface"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
classes()
  .that().implement(Factory.class)
  .should().haveSimpleNameEndingWith("Factory")
  .because("Classes implementing Factory marker should have 'Factory' in their name")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Factory](/marker/tactical/factory.md)
