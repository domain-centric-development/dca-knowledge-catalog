---
type: Rule
title: Factories must reside in domain package
rule: "Factories are part of the domain layer (complex aggregate creation logic)."
constraint: Factories must reside in domain package.
enforced_by: "DddAdvancedPatternsArchUnitTest#Factories must reside in domain package"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
classes()
  .that().implement(Factory.class)
  .should().resideInAnyPackage(PRODUCT_DOMAIN_PACKAGE, CART_DOMAIN_PACKAGE, CHECKOUT_DOMAIN_PACKAGE, ACCOUNT_DOMAIN_PACKAGE, INVENTORY_DOMAIN_PACKAGE, PRICING_DOMAIN_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .because("Factories are part of the domain layer (complex aggregate creation logic)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Factory](/marker/tactical/factory.md)
