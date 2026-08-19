---
type: Rule
title: "Use Case Result Models should be immutable (final or records)"
rule: "Use case result models should be immutable (value objects)."
constraint: "Use Case Result Models should be immutable (final or records)."
enforced_by: "UseCasePatternsArchUnitTest#Use Case Result Models should be immutable (final or records)"
status: enforced
test_class: UseCasePatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/UseCasePatternsArchUnitTest.groovy
tags: [usecase, archunit]
---

```groovy
expect:
classes()
  .that().haveSimpleNameEndingWith("Result")
  .and().resideInAnyPackage(APPLICATION_PACKAGE)
  .and().areNotInterfaces()
  .and().areNotRecords()
  .should().haveModifier(JavaModifier.FINAL)
  .because("Use case result models should be immutable (value objects)")
  .allowEmptyShould(true)
  .check(allClasses)
```
