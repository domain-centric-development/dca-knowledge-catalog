---
type: Rule
title: Domain Events must not have Spring annotations
rule: Domain events must be framework-independent POJOs.
constraint: Domain Events must not have Spring annotations.
enforced_by: "DddAdvancedPatternsArchUnitTest#Domain Events must not have Spring annotations"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
noClasses()
  .that().resideInAnyPackage(DOMAIN_PACKAGE)
  .and().implement(DomainEvent.class)
  .should().beAnnotatedWith(Component.class)
  .orShould().beAnnotatedWith(Service.class)
  .orShould().beAnnotatedWith(EventListener.class)
  .because("Domain events must be framework-independent POJOs")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
