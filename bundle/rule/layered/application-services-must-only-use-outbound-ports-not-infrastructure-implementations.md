---
type: Rule
title: "Application Services must only use outbound ports (not infrastructure implementations)"
rule: "Application services should only use outbound ports from sharedkernel.application.port, not infrastructure implementation details."
constraint: "Application Services must only use outbound ports (not infrastructure implementations)."
enforced_by: "LayeredArchitectureArchUnitTest#Application Services must only use outbound ports (not infrastructure implementations)"
status: enforced
test_class: LayeredArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/LayeredArchitectureArchUnitTest.groovy
tags: [layered, archunit]
---

```groovy
expect:
noClasses()
  .that().resideInAnyPackage(PRODUCT_APPLICATION_PACKAGE, CART_APPLICATION_PACKAGE, CHECKOUT_APPLICATION_PACKAGE, ACCOUNT_APPLICATION_PACKAGE, INVENTORY_APPLICATION_PACKAGE, PRICING_APPLICATION_PACKAGE, BACKOFFICE_APPLICATION_PACKAGE)
  .should().dependOnClassesThat(INFRASTRUCTURE_IMPLEMENTATION)
  .because("Application services should only use outbound ports from sharedkernel.application.port, not infrastructure implementation details")
  .check(allClasses)
```
