---
type: Rule
title: "Domain Services should be stateless (only final fields for dependencies)"
rule: "Domain services should be stateless (only final fields for dependencies)."
constraint: "Domain Services should be stateless (only final fields for dependencies)."
enforced_by: "DddAdvancedPatternsArchUnitTest#Domain Services should be stateless (only final fields for dependencies)"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
classes()
  .that().implement(DomainService.class)
  .and().resideInAnyPackage(PRODUCT_DOMAIN_PACKAGE, CART_DOMAIN_PACKAGE, CHECKOUT_DOMAIN_PACKAGE, ACCOUNT_DOMAIN_PACKAGE, INVENTORY_DOMAIN_PACKAGE, PRICING_DOMAIN_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .should().haveOnlyFinalFields()
  .because("Domain services should be stateless (only final fields for dependencies)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)
