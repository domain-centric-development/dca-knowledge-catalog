---
type: Rule
id: DCA-HEX-010
title: Output ports must not reside in the domain layer
rule: "output ports (Repository, Store, OutputPort) are an application-layer concern and must live in application/shared/, not domain/."
constraint: Output ports must not reside in the domain layer.
selects: Interfaces anywhere on the classpath under scan that are assignable to OutputPort - the building-block port interfaces themselves included.
checks: "None resides in <module>.domain.. of any module root. Classes implementing an output port are not selected; where an interface outside the domain has to live is not checked here. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-010"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

## Selection

Interfaces anywhere on the classpath under scan that are assignable to OutputPort - the building-block port interfaces themselves included.

## Check

None resides in <module>.domain.. of any module root. Classes implementing an output port are not selected; where an interface outside the domain has to live is not checked here. An empty selection passes.

## .NET reading

**Selection.** Interfaces anywhere in the loaded assemblies that are assignable to IOutputPort - the building-block port interfaces themselves included.

**Check.** None resides in <module>.Domain of any module root. Classes implementing an output port are not selected; where an interface outside the domain has to live is not checked here. An empty selection passes.

## Implementation

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
    .selecting(
        "Interfaces anywhere on the classpath under scan that are assignable to"
            + " OutputPort - the building-block port interfaces themselves included.")
    .checking(
        "None resides in <module>.domain.. of any module root. Classes implementing an"
            + " output port are not selected; where an interface outside the domain has to live"
            + " is not checked here. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
