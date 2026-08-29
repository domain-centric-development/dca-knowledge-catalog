---
type: Rule
id: DCA-LAY-005
title: The shared kernel's output-port markers must all be interfaces
rule: "port.out contains outbound port interfaces (Repository, OutputPort, DomainEventPublisher) shared across all bounded contexts. These must be interfaces to ensure the application layer remains framework-independent and follows the Dependency Inversion Principle. Implementations belong in infrastructure or adapter packages."
constraint: The shared kernel's output-port markers must all be interfaces.
enforced_by: "LayeredRules#DCA-LAY-005"
status: enforced
rule_set: layered
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
---

```java
DcaRule.of(
    "DCA-LAY-005",
    "The shared kernel's output-port markers must all be interfaces",
    "port.out contains outbound port interfaces (Repository, OutputPort, DomainEventPublisher)"
        + " shared across all bounded contexts. These must be interfaces to ensure the"
        + " application layer remains framework-independent and follows the Dependency"
        + " Inversion Principle. Implementations belong in infrastructure or adapter packages.",
    arch ->
        classes()
            .that()
            .resideInAPackage(DcaLayout.BUILDING_BLOCKS_PORT_OUT_PACKAGE)
            .should()
            .beInterfaces()
            .allowEmptyShould(true))
```

## Applies to markers

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
