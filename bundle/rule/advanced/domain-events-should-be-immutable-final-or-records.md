---
type: Rule
title: "Domain Events should be immutable (final or records)"
rule: "Domain events should be immutable (final classes or records)."
constraint: "Domain Events should be immutable (final or records)."
enforced_by: "DddAdvancedPatternsArchUnitTest#Domain Events should be immutable (final or records)"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
classes()
  .that().resideInAnyPackage(PRODUCT_DOMAIN_PACKAGE, CART_DOMAIN_PACKAGE, CHECKOUT_DOMAIN_PACKAGE, ACCOUNT_DOMAIN_PACKAGE, SHAREDKERNEL_DOMAIN_PACKAGE)
  .and().implement(DomainEvent.class)
  .and().areNotInterfaces()
  .and().areNotEnums()
  .and().areNotRecords()
  .should().haveModifier(JavaModifier.FINAL)
  .because("Domain events should be immutable (final classes or records)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
