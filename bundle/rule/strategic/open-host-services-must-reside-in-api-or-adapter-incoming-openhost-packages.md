---
type: Rule
title: Open Host Services must reside in api or adapter.incoming.openhost packages
rule: "Open Host Services expose context capabilities via api/ packages (Spring Modulith @NamedInterface) or adapter.incoming.openhost/ packages."
constraint: Open Host Services must reside in api or adapter.incoming.openhost packages.
enforced_by: "DddStrategicPatternsArchUnitTest#Open Host Services must reside in api or adapter.incoming.openhost packages"
status: enforced
test_class: DddStrategicPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddStrategicPatternsArchUnitTest.groovy
tags: [strategic, archunit]
---

```groovy
expect:
classes()
  .that().areAnnotatedWith(OpenHostService)
  .should().resideInAnyPackage("..api..", "..adapter.incoming.openhost..")
  .allowEmptyShould(true)
  .because("Open Host Services expose context capabilities via api/ packages (Spring Modulith @NamedInterface) or adapter.incoming.openhost/ packages")
  .check(allClasses)
```

## Applies to markers

- [@OpenHostService](/marker/strategic/openhostservice.md)
