---
type: Rule
title: Converters must reside in the adapter layer
rule: Converters/Mappers translate between layers and should be in adapters.
constraint: Converters must reside in the adapter layer.
enforced_by: "NamingConventionsArchUnitTest#Converters must reside in the adapter layer"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
classes()
  .that().haveSimpleNameEndingWith("Converter")
  .and().resideInAnyPackage(BASE_PACKAGE + "..")
  .should().resideInAPackage(ADAPTER_PACKAGE)
  .because("Converters/Mappers translate between layers and should be in adapters")
  .allowEmptyShould(true)
  .check(allClasses)
```
