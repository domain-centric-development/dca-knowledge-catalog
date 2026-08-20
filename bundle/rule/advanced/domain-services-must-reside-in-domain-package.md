---
type: Rule
title: Domain Services must reside in domain package
rule: "Domain services are part of the domain layer, not application layer."
constraint: Domain Services must reside in domain package.
enforced_by: "DddAdvancedPatternsArchUnitTest#Domain Services must reside in domain package"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
classes()
  .that().implement(DomainService.class)
  .should().resideInAnyPackage(DOMAIN_PACKAGE)
  .because("Domain services are part of the domain layer, not application layer")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)
