---
type: Rule
title: Application layer InputPort implementations must end with 'UseCase'
rule: "InputPort implementations (use cases) should follow consistent naming conventions (Hexagonal Architecture)."
constraint: Application layer InputPort implementations must end with 'UseCase'.
enforced_by: "NamingConventionsArchUnitTest#Application layer InputPort implementations must end with 'UseCase'"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
classes()
  .that().resideInAPackage(APPLICATION_PACKAGE)
  .and().areNotInterfaces()
  .and().areNotRecords()
  .and().implement(UseCase.class)
  .should().haveSimpleNameEndingWith("UseCase")
  .because("InputPort implementations (use cases) should follow consistent naming conventions (Hexagonal Architecture)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
