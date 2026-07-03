---
type: Rule
title: "Value Object classes should be final (immutability)"
rule: "Value objects should be immutable (final classes) - Vernon's DDD recommendation."
constraint: "Value Object classes should be final (immutability)."
enforced_by: "DddTacticalPatternsArchUnitTest#Value Object classes should be final (immutability)"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
classes()
  .that().resideInAnyPackage(PRODUCT_DOMAIN_MODEL_PACKAGE, CART_DOMAIN_MODEL_PACKAGE, CHECKOUT_DOMAIN_MODEL_PACKAGE, ACCOUNT_DOMAIN_MODEL_PACKAGE, INVENTORY_DOMAIN_MODEL_PACKAGE, PRICING_DOMAIN_MODEL_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .and().implement(Value.class)
  .and().areNotInterfaces()
  .and().areNotRecords()
  .should().haveModifier(JavaModifier.FINAL)
  .because("Value objects should be immutable (final classes) - Vernon's DDD recommendation")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Value](/marker/tactical/value.md)
