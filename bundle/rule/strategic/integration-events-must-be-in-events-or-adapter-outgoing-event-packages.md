---
type: Rule
title: Integration Events must be in events or adapter outgoing event packages
rule: "Integration Events must be in events/ packages (Spring Modulith @NamedInterface) or adapter.outgoing.event/ packages."
constraint: Integration Events must be in events or adapter outgoing event packages.
enforced_by: "DddStrategicPatternsArchUnitTest#Integration Events must be in events or adapter outgoing event packages"
status: enforced
test_class: DddStrategicPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddStrategicPatternsArchUnitTest.groovy
tags: [strategic, archunit]
---

```groovy
expect:
// Integration Events are published for cross-module consumption.
// With Spring Modulith, they reside in events/ packages (@NamedInterface("events"))
// or in adapter.outgoing.event/ packages (legacy location)
classes()
  .that().implement(IntegrationEvent)
  .should().resideInAnyPackage("..events..", "..adapter.outgoing.event..")
  .allowEmptyShould(true)
  .because("Integration Events must be in events/ packages (Spring Modulith @NamedInterface) or adapter.outgoing.event/ packages")
  .check(allClasses)
```

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)
