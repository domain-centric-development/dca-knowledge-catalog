---
type: Rule
title: "Domain must not access Application Services (Onion Architecture - Domain is innermost layer)"
rule: Domain is the innermost layer in onion architecture and should not depend on application services.
constraint: "Domain must not access Application Services (Onion Architecture - Domain is innermost layer)."
enforced_by: "OnionArchitectureArchUnitTest#Domain must not access Application Services (Onion Architecture - Domain is innermost layer)"
status: enforced
test_class: OnionArchitectureArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/OnionArchitectureArchUnitTest.groovy
tags: [onion, archunit]
---

```groovy
expect:
noClasses()
.that().resideInAnyPackage(DOMAIN_PACKAGE)
.should().dependOnClassesThat().resideInAnyPackage(APPLICATION_PACKAGE)
.because("Domain is the innermost layer in onion architecture and should not depend on application services")
.check(allClasses)
```
