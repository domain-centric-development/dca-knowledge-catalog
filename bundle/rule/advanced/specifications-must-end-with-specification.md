---
type: Rule
title: Specifications must end with 'Specification'
rule: Specification implementations are part of the domain layer.
constraint: Specifications must end with 'Specification'.
enforced_by: "DddAdvancedPatternsArchUnitTest#Specifications must end with 'Specification'"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
classes()
  .that().haveSimpleNameEndingWith("Specification")
  .and().areNotInterfaces()
  .and().doNotHaveSimpleName("Specification")
  .should().resideInAnyPackage(PRODUCT_DOMAIN_PACKAGE, CART_DOMAIN_PACKAGE, CHECKOUT_DOMAIN_PACKAGE, ACCOUNT_DOMAIN_PACKAGE, INVENTORY_DOMAIN_PACKAGE, PRICING_DOMAIN_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .because("Specification implementations are part of the domain layer")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Specification<T>](/marker/tactical/specification.md)
