---
type: Rule
title: Controller classes must end with 'Controller'
rule: "@Controller annotated classes should follow naming conventions."
constraint: Controller classes must end with 'Controller'.
enforced_by: "NamingConventionsArchUnitTest#Controller classes must end with 'Controller'"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
classes()
  .that().resideInAPackage(INCOMING_ADAPTER_PACKAGE)
  .and().areAnnotatedWith(Controller.class)
  .should().haveSimpleNameEndingWith("Controller")
  .because("@Controller annotated classes should follow naming conventions")
  .allowEmptyShould(true)
  .check(allClasses)
```
