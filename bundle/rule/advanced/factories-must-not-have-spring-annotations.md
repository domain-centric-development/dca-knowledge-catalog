---
type: Rule
title: Factories must not have Spring annotations
rule: Factories should be framework-independent.
constraint: Factories must not have Spring annotations.
enforced_by: "DddAdvancedPatternsArchUnitTest#Factories must not have Spring annotations"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
noClasses()
  .that().implement(Factory.class)
  .and().resideInAnyPackage(PRODUCT_DOMAIN_PACKAGE, CART_DOMAIN_PACKAGE, CHECKOUT_DOMAIN_PACKAGE, ACCOUNT_DOMAIN_PACKAGE, INVENTORY_DOMAIN_PACKAGE, PRICING_DOMAIN_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .should().beAnnotatedWith(Component.class)
  .orShould().beAnnotatedWith(Service.class)
  .because("Factories should be framework-independent")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Factory](/marker/tactical/factory.md)
