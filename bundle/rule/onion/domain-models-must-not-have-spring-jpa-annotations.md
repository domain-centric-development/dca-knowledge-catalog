---
type: Rule
title: Domain Models must not have Spring/JPA annotations
rule: "Domain models must be framework-independent (no Spring or JPA annotations)."
constraint: Domain Models must not have Spring/JPA annotations.
enforced_by: "OnionArchitectureArchUnitTest#Domain Models must not have Spring/JPA annotations"
status: enforced
test_class: OnionArchitectureArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/OnionArchitectureArchUnitTest.groovy
tags: [onion, archunit]
---

```groovy
expect:
noClasses()
.that().resideInAnyPackage(DOMAIN_MODEL_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
.should().beAnnotatedWith(Component.class)
.orShould().beAnnotatedWith(Service.class)
.orShould().beAnnotatedWith("jakarta.persistence.Entity")
.orShould().beAnnotatedWith("jakarta.persistence.Table")
.because("Domain models must be framework-independent (no Spring or JPA annotations)")
.check(allClasses)
```
