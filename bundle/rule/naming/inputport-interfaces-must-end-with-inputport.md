---
type: Rule
title: InputPort interfaces must end with 'InputPort'
rule: "Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)."
constraint: InputPort interfaces must end with 'InputPort'.
enforced_by: "NamingConventionsArchUnitTest#InputPort interfaces must end with 'InputPort'"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
classes()
  .that().resideInAPackage("..application.port.in..")
  .and().areInterfaces()
  .should().haveSimpleNameEndingWith("InputPort")
  .because("Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
