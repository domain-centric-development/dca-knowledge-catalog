---
type: Rule
id: DCA-HEX-010
title: Output ports must not reside in the domain layer
rule: "output ports (Repository, Store, OutputPort) are an application-layer concern and must live in application/shared/, not domain/."
constraint: Output ports must not reside in the domain layer.
enforced_by: "HexagonalRules#DCA-HEX-010"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

```java
DcaRule.of(
    "DCA-HEX-010",
    "Output ports must not reside in the domain layer",
    "output ports (Repository, Store, OutputPort) are an application-layer concern and must live"
        + " in application/shared/, not domain/",
    arch ->
        noClasses()
            .that()
            .areAssignableTo(OutputPort.class)
            .and()
            .areInterfaces()
            .should()
            .resideInAnyPackage(arch.allDomainPatterns())
            .allowEmptyShould(true))
```

## Applies to markers

- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
