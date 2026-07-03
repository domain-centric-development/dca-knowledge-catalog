---
type: Rule
title: "Domain must not access Application Services (Onion Architecture - Domain is innermost layer)"
rule: Domain is the innermost layer in onion architecture and should not depend on application services.
constraint: "Domain must not access Application Services (Onion Architecture - Domain is innermost layer)."
enforced_by: "OnionArchitectureArchUnitTest#Domain must not access Application Services (Onion Architecture - Domain is innermost layer)"
status: enforced
test_class: OnionArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/OnionArchitectureArchUnitTest.groovy
tags: [onion, archunit]
---

```groovy
expect:
noClasses()
.that().resideInAnyPackage(PRODUCT_DOMAIN_PACKAGE, CART_DOMAIN_PACKAGE, CHECKOUT_DOMAIN_PACKAGE, ACCOUNT_DOMAIN_PACKAGE, INVENTORY_DOMAIN_PACKAGE, PRICING_DOMAIN_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
.should().dependOnClassesThat().resideInAnyPackage(PRODUCT_APPLICATION_PACKAGE, CART_APPLICATION_PACKAGE, CHECKOUT_APPLICATION_PACKAGE, ACCOUNT_APPLICATION_PACKAGE, INVENTORY_APPLICATION_PACKAGE, PRICING_APPLICATION_PACKAGE)
.because("Domain is the innermost layer in onion architecture and should not depend on application services")
.check(allClasses)
```
