---
type: Rule
title: Domain Events must reside in domain package
rule: "Domain events are part of the domain layer (named in past tense)."
constraint: Domain Events must reside in domain package.
enforced_by: "DddAdvancedPatternsArchUnitTest#Domain Events must reside in domain package"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
classes()
  .that().implement(DomainEvent.class)
  .should().resideInAnyPackage(PRODUCT_DOMAIN_PACKAGE, CART_DOMAIN_PACKAGE, CHECKOUT_DOMAIN_PACKAGE, ACCOUNT_DOMAIN_PACKAGE, INVENTORY_DOMAIN_PACKAGE, PRICING_DOMAIN_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .because("Domain events are part of the domain layer (named in past tense)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
