---
type: Rule
title: Domain Services must not have Spring annotations
rule: Domain services should be framework-independent.
constraint: Domain Services must not have Spring annotations.
enforced_by: "DddAdvancedPatternsArchUnitTest#Domain Services must not have Spring annotations"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
noClasses()
  .that().implement(DomainService.class)
  .should().beAnnotatedWith(Service.class)
  .orShould().beAnnotatedWith(Component.class)
  .because("Domain services should be framework-independent")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)
