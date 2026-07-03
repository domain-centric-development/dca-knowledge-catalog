---
type: Rule
title: Domain Models must not have Spring/JPA annotations
rule: "Domain models must be framework-independent (no Spring or JPA annotations)."
constraint: Domain Models must not have Spring/JPA annotations.
enforced_by: "OnionArchitectureArchUnitTest#Domain Models must not have Spring/JPA annotations"
status: enforced
test_class: OnionArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/OnionArchitectureArchUnitTest.groovy
tags: [onion, archunit]
---

```groovy
expect:
noClasses()
.that().resideInAnyPackage(PRODUCT_DOMAIN_MODEL_PACKAGE, CART_DOMAIN_MODEL_PACKAGE, CHECKOUT_DOMAIN_MODEL_PACKAGE, ACCOUNT_DOMAIN_MODEL_PACKAGE, INVENTORY_DOMAIN_MODEL_PACKAGE, PRICING_DOMAIN_MODEL_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
.should().beAnnotatedWith(Component.class)
.orShould().beAnnotatedWith(Service.class)
.orShould().beAnnotatedWith("jakarta.persistence.Entity")
.orShould().beAnnotatedWith("jakarta.persistence.Table")
.because("Domain models must be framework-independent (no Spring or JPA annotations)")
.check(allClasses)
```
