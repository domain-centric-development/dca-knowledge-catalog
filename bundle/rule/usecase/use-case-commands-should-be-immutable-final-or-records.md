---
type: Rule
title: "Use Case Commands should be immutable (final or records)"
rule: "Use case commands should be immutable (value objects)."
constraint: "Use Case Commands should be immutable (final or records)."
enforced_by: "UseCasePatternsArchUnitTest#Use Case Commands should be immutable (final or records)"
status: enforced
test_class: UseCasePatternsArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/UseCasePatternsArchUnitTest.groovy
tags: [usecase, archunit]
---

```groovy
expect:
classes()
  .that().haveSimpleNameEndingWith("Command")
  .and().resideInAnyPackage(APPLICATION_PACKAGE)
  .and().areNotInterfaces()
  .and().areNotRecords()
  .should().haveModifier(JavaModifier.FINAL)
  .because("Use case commands should be immutable (value objects)")
  .allowEmptyShould(true)
  .check(allClasses)
```
