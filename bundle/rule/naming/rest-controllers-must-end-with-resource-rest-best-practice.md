---
type: Rule
title: "REST Controllers must end with 'Resource' (REST best practice)"
rule: "@RestController annotated classes should end with 'Resource' following RESTful naming conventions."
constraint: "REST Controllers must end with 'Resource' (REST best practice)."
enforced_by: "NamingConventionsArchUnitTest#REST Controllers must end with 'Resource' (REST best practice)"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
classes()
  .that().resideInAPackage(INCOMING_ADAPTER_PACKAGE)
  .and().areAnnotatedWith(RestController.class)
  .should().haveSimpleNameEndingWith("Resource")
  .because("@RestController annotated classes should end with 'Resource' following RESTful naming conventions")
  .check(allClasses)
```
