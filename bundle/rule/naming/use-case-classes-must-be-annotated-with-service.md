---
type: Rule
title: "Use case classes must be annotated with @Service"
rule: Use case classes must be Spring-managed beans.
constraint: "Use case classes must be annotated with @Service."
enforced_by: "NamingConventionsArchUnitTest#Use case classes must be annotated with @Service"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
classes()
  .that().resideInAPackage(APPLICATION_PACKAGE)
  .and().haveSimpleNameEndingWith("UseCase")
  .and().areNotInterfaces()  // Exclude the UseCase interface itself
  .should().beAnnotatedWith(Service.class)
  .because("Use case classes must be Spring-managed beans")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
