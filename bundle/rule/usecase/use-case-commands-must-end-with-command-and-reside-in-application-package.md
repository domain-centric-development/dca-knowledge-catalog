---
type: Rule
title: Use Case Commands must end with 'Command' and reside in application package
rule: "Use case commands should be in application layer (CQRS pattern)."
constraint: Use Case Commands must end with 'Command' and reside in application package.
enforced_by: "UseCasePatternsArchUnitTest#Use Case Commands must end with 'Command' and reside in application package"
status: enforced
test_class: UseCasePatternsArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/UseCasePatternsArchUnitTest.groovy
tags: [usecase, archunit]
---

```groovy
expect:
classes()
  .that().haveSimpleNameEndingWith("Command")
  .and().resideInAnyPackage(BASE_PACKAGE + "..")
  .should().resideInAnyPackage(APPLICATION_PACKAGE)
  .because("Use case commands should be in application layer (CQRS pattern)")
  .allowEmptyShould(true)
  .check(allClasses)
```
