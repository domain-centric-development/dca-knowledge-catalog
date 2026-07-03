---
type: Rule
title: "DTOs must reside in portadapter package (not in domain or application)"
rule: "DTOs are adapter concerns (presentation or external API) - not in domain or application."
constraint: "DTOs must reside in portadapter package (not in domain or application)."
enforced_by: "NamingConventionsArchUnitTest#DTOs must reside in portadapter package (not in domain or application)"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
classes()
  .that().haveSimpleNameEndingWith("Dto")
  .and().resideInAnyPackage(BASE_PACKAGE + "..")
  .should().resideInAPackage(ADAPTER_PACKAGE)
  .because("DTOs are adapter concerns (presentation or external API) - not in domain or application")
  .allowEmptyShould(true)
  .check(allClasses)
```
