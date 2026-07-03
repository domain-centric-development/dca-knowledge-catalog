---
type: Rule
title: "Use Case Queries should be immutable (final or records)"
rule: "Use case queries should be immutable (value objects)."
constraint: "Use Case Queries should be immutable (final or records)."
enforced_by: "UseCasePatternsArchUnitTest#Use Case Queries should be immutable (final or records)"
status: enforced
test_class: UseCasePatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/UseCasePatternsArchUnitTest.groovy
tags: [usecase, archunit]
---

```groovy
expect:
classes()
  .that().haveSimpleNameEndingWith("Query")
  .and().resideInAnyPackage(PRODUCT_APPLICATION_PACKAGE, CART_APPLICATION_PACKAGE, CHECKOUT_APPLICATION_PACKAGE, ACCOUNT_APPLICATION_PACKAGE, INVENTORY_APPLICATION_PACKAGE, PRICING_APPLICATION_PACKAGE, BACKOFFICE_APPLICATION_PACKAGE)
  .and().areNotInterfaces()
  .and().areNotRecords()
  .should().haveModifier(JavaModifier.FINAL)
  .because("Use case queries should be immutable (value objects)")
  .allowEmptyShould(true)
  .check(allClasses)
```
