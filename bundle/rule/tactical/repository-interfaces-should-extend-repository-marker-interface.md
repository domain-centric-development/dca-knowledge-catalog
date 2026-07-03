---
type: Rule
title: Repository Interfaces should extend Repository Marker Interface
rule: Repository interfaces should extend Repository marker interface.
constraint: Repository Interfaces should extend Repository Marker Interface.
enforced_by: "DddTacticalPatternsArchUnitTest#Repository Interfaces should extend Repository Marker Interface"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
classes()
  .that().resideInAnyPackage(PRODUCT_APPLICATION_PACKAGE, CART_APPLICATION_PACKAGE, CHECKOUT_APPLICATION_PACKAGE, ACCOUNT_APPLICATION_PACKAGE, INVENTORY_APPLICATION_PACKAGE, PRICING_APPLICATION_PACKAGE)
  .and().areInterfaces()
  .and().haveSimpleNameEndingWith("Repository")
  .and().doNotHaveSimpleName("Repository")
  .should().beAssignableTo(Repository.class)
  .because("Repository interfaces should extend Repository marker interface")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
