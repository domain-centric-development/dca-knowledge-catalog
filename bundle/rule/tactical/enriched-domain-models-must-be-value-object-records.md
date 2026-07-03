---
type: Rule
title: Enriched Domain Models must be Value Object records
rule: Enriched domain models are immutable read projections and must be records implementing Value.
constraint: Enriched Domain Models must be Value Object records.
enforced_by: "DddTacticalPatternsArchUnitTest#Enriched Domain Models must be Value Object records"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
classes()
  .that().haveSimpleNameStartingWith("Enriched")
  .and().resideInAPackage(DOMAIN_MODEL_PACKAGE)
  .and().doNotImplement(Factory.class)
  .should().beRecords()
  .because("Enriched domain models are immutable read projections and must be records implementing Value")
  .check(allClasses)
```

## Applies to markers

- [Factory](/marker/tactical/factory.md)
