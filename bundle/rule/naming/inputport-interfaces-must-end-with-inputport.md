---
type: Rule
title: InputPort interfaces must end with 'InputPort'
rule: "Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)."
constraint: InputPort interfaces must end with 'InputPort'.
enforced_by: "NamingConventionsArchUnitTest#InputPort interfaces must end with 'InputPort'"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
// Matched by marker, not by package: DCA places each input port in its own use-case folder,
// so there is no single ..application.port.in.. package to point at.
classes()
  .that().resideInAPackage(APPLICATION_PACKAGE)
  .and().areInterfaces()
  .and().areAssignableTo(InputPort.class)
  .and().doNotHaveSimpleName("InputPort")
  .and().doNotHaveSimpleName("UseCase")
  .should().haveSimpleNameEndingWith("InputPort")
  .because("Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
