---
type: Rule
title: Domain must not have dependencies on Infrastructure
rule: "Domain should not depend on infrastructure concerns (Dependency Inversion Principle)."
constraint: Domain must not have dependencies on Infrastructure.
enforced_by: "LayeredArchitectureArchUnitTest#Domain must not have dependencies on Infrastructure"
status: enforced
test_class: LayeredArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/LayeredArchitectureArchUnitTest.groovy
tags: [layered, archunit]
---

```groovy
expect:
noClasses()
  .that().resideInAnyPackage(PRODUCT_DOMAIN_PACKAGE, CART_DOMAIN_PACKAGE, CHECKOUT_DOMAIN_PACKAGE, ACCOUNT_DOMAIN_PACKAGE, INVENTORY_DOMAIN_PACKAGE, PRICING_DOMAIN_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .should().dependOnClassesThat().resideInAPackage(INFRASTRUCTURE_PACKAGE)
  .because("Domain should not depend on infrastructure concerns (Dependency Inversion Principle)")
  .check(allClasses)
```
