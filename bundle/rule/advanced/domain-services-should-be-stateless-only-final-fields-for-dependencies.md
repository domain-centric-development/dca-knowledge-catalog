---
type: Rule
title: "Domain Services should be stateless (only final fields for dependencies)"
rule: "Domain services should be stateless (only final fields for dependencies)."
constraint: "Domain Services should be stateless (only final fields for dependencies)."
enforced_by: "DddAdvancedPatternsArchUnitTest#Domain Services should be stateless (only final fields for dependencies)"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
classes()
  .that().implement(DomainService.class)
  .and().resideInAnyPackage(DOMAIN_PACKAGE)
  .should().haveOnlyFinalFields()
  .because("Domain services should be stateless (only final fields for dependencies)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)
