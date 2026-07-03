---
type: Rule
title: "Records for Value Objects are allowed (preferred pattern for simple Value Objects)"
rule: "Records are a valid pattern for immutable value objects (Java 14+)."
constraint: "Records for Value Objects are allowed (preferred pattern for simple Value Objects)."
enforced_by: "DddTacticalPatternsArchUnitTest#Records for Value Objects are allowed (preferred pattern for simple Value Objects)"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
classes()
  .that().resideInAnyPackage(PRODUCT_DOMAIN_MODEL_PACKAGE, CART_DOMAIN_MODEL_PACKAGE, CHECKOUT_DOMAIN_MODEL_PACKAGE, ACCOUNT_DOMAIN_MODEL_PACKAGE, INVENTORY_DOMAIN_MODEL_PACKAGE, PRICING_DOMAIN_MODEL_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .and().areRecords()
  .should().resideInAnyPackage(PRODUCT_DOMAIN_MODEL_PACKAGE, CART_DOMAIN_MODEL_PACKAGE, CHECKOUT_DOMAIN_MODEL_PACKAGE, ACCOUNT_DOMAIN_MODEL_PACKAGE, INVENTORY_DOMAIN_MODEL_PACKAGE, PRICING_DOMAIN_MODEL_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .because("Records are a valid pattern for immutable value objects (Java 14+)")
  .allowEmptyShould(true)
  .check(allClasses)
```
