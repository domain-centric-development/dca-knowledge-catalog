---
type: Rule
title: Domain Services must implement DomainService Marker Interface and reside in domain.service
rule: "Domain services implement DomainService marker and reside in domain.service packages (named descriptively, e.g., PricingService, CartTotalCalculator)."
constraint: Domain Services must implement DomainService Marker Interface and reside in domain.service.
enforced_by: "DddAdvancedPatternsArchUnitTest#Domain Services must implement DomainService Marker Interface and reside in domain.service"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
classes()
  .that().implement(DomainService.class)
  .and().areNotInterfaces()
  .should().resideInAPackage("..domain.service..")
  .because("Domain services implement DomainService marker and reside in domain.service packages (named descriptively, e.g., PricingService, CartTotalCalculator)")
  .check(allClasses)
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)
