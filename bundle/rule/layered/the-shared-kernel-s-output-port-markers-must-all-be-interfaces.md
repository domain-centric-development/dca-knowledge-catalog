---
type: Rule
title: The shared kernel's output-port markers must all be interfaces
rule: "sharedkernel.marker.port.out contains outbound port interfaces (Repository, OutputPort, DomainEventPublisher) ."
constraint: The shared kernel's output-port markers must all be interfaces.
enforced_by: "LayeredArchitectureArchUnitTest#The shared kernel's output-port markers must all be interfaces"
status: enforced
test_class: LayeredArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/LayeredArchitectureArchUnitTest.groovy
tags: [layered, archunit]
---

```groovy
expect:
classes()
  .that().resideInAPackage(SHAREDKERNEL_MARKER_PORT_OUT_PACKAGE)
  .should().beInterfaces()
  .because("sharedkernel.marker.port.out contains outbound port interfaces (Repository, OutputPort, DomainEventPublisher) " +
  "shared across all bounded contexts. These must be interfaces to ensure the application layer remains framework-independent " +
  "and follows the Dependency Inversion Principle. Implementations belong in infrastructure or adapter packages.")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
