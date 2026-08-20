---
type: Rule
title: "Aggregate Roots must implement AggregateRoot<T, ID>"
rule: "Classes named *AggregateRoot must implement AggregateRoot interface (DDD pattern)."
constraint: "Aggregate Roots must implement AggregateRoot<T, ID>."
enforced_by: "DddTacticalPatternsArchUnitTest#Aggregate Roots must implement AggregateRoot<T, ID>"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
classes()
  .that().resideInAnyPackage(DOMAIN_MODEL_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .and().haveSimpleNameEndingWith("AggregateRoot")
  .and().areNotInterfaces()
  .and().doNotHaveSimpleName("AggregateRoot") // Exclude the marker interface itself
  .should().implement(AggregateRoot.class)
  .because("Classes named *AggregateRoot must implement AggregateRoot interface (DDD pattern)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
