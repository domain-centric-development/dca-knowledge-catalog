---
type: Rule
title: Use Case Result Models must end with 'Result' and reside in application package
rule: "Use case result models should be in application layer (ADR-020: Application layer uses *Result). Domain Value Objects with 'Result' in name are allowed in domain layer."
constraint: Use Case Result Models must end with 'Result' and reside in application package.
enforced_by: "UseCasePatternsArchUnitTest#Use Case Result Models must end with 'Result' and reside in application package"
status: enforced
test_class: UseCasePatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/UseCasePatternsArchUnitTest.groovy
tags: [usecase, archunit]
---

```groovy
expect:
classes()
  .that().haveSimpleNameEndingWith("Result")
  .and().resideInAnyPackage(BASE_PACKAGE + "..")
  .and().doNotImplement(de.sample.aiarchitecture.sharedkernel.marker.tactical.Value.class)
  .should().resideInAnyPackage(APPLICATION_PACKAGE)
  .because("Use case result models should be in application layer (ADR-020: Application layer uses *Result). Domain Value Objects with 'Result' in name are allowed in domain layer.")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Value](/marker/tactical/value.md)
