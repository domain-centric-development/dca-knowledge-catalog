---
type: Rule
title: DTOs must not be used in the Domain Layer
rule: "Domain layer should not depend on DTOs (presentation concerns) - Dependency Inversion Principle."
constraint: DTOs must not be used in the Domain Layer.
enforced_by: "UseCasePatternsArchUnitTest#DTOs must not be used in the Domain Layer"
status: enforced
test_class: UseCasePatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/UseCasePatternsArchUnitTest.groovy
tags: [usecase, archunit]
---

```groovy
expect:
noClasses()
  .that().resideInAnyPackage(PRODUCT_DOMAIN_PACKAGE, CART_DOMAIN_PACKAGE, CHECKOUT_DOMAIN_PACKAGE, ACCOUNT_DOMAIN_PACKAGE, INVENTORY_DOMAIN_PACKAGE, PRICING_DOMAIN_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .should().dependOnClassesThat().haveSimpleNameEndingWith("Dto")
  .because("Domain layer should not depend on DTOs (presentation concerns) - Dependency Inversion Principle")
  .check(allClasses)
```
