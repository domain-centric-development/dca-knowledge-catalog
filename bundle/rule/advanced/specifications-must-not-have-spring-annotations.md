---
type: Rule
title: Specifications must not have Spring annotations
rule: Specifications should be framework-independent value objects.
constraint: Specifications must not have Spring annotations.
enforced_by: "DddAdvancedPatternsArchUnitTest#Specifications must not have Spring annotations"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
noClasses()
  .that().haveSimpleNameEndingWith("Specification")
  .and().resideInAnyPackage(PRODUCT_DOMAIN_PACKAGE, CART_DOMAIN_PACKAGE, CHECKOUT_DOMAIN_PACKAGE, ACCOUNT_DOMAIN_PACKAGE, INVENTORY_DOMAIN_PACKAGE, PRICING_DOMAIN_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .should().beAnnotatedWith(Component.class)
  .orShould().beAnnotatedWith(Service.class)
  .because("Specifications should be framework-independent value objects")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Specification<T>](/marker/tactical/specification.md)
