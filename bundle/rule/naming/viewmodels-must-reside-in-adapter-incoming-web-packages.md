---
type: Rule
title: ViewModels must reside in adapter.incoming.web packages
rule: ViewModels are presentation concerns and must reside in incoming web adapter packages.
constraint: ViewModels must reside in adapter.incoming.web packages.
enforced_by: "NamingConventionsArchUnitTest#ViewModels must reside in adapter.incoming.web packages"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
classes()
  .that().haveSimpleNameEndingWith("ViewModel")
  .and().resideInAnyPackage(BASE_PACKAGE + "..")
  .should().resideInAPackage("..adapter.incoming.web..")
  .because("ViewModels are presentation concerns and must reside in incoming web adapter packages")
  .check(allClasses)
```
