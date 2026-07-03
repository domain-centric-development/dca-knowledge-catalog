---
type: Rule
title: Repository Interfaces must reside in application output port package
rule: "Repository interfaces are output ports in the application layer (Hexagonal Architecture)."
constraint: Repository Interfaces must reside in application output port package.
enforced_by: "DddTacticalPatternsArchUnitTest#Repository Interfaces must reside in application output port package"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
classes()
  .that().implement(Repository.class)
  .and().areInterfaces()
  .should().resideInAnyPackage(PRODUCT_APPLICATION_PACKAGE, CART_APPLICATION_PACKAGE, CHECKOUT_APPLICATION_PACKAGE, ACCOUNT_APPLICATION_PACKAGE, INVENTORY_APPLICATION_PACKAGE, PRICING_APPLICATION_PACKAGE)
  .because("Repository interfaces are output ports in the application layer (Hexagonal Architecture)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
