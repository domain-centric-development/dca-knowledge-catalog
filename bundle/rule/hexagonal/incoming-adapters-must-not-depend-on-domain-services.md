---
type: Rule
id: DCA-HEX-012
title: Incoming Adapters must not depend on domain services
rule: "An incoming adapter translates external input, calls an input port and formats its result. Injecting or invoking a domain service bypasses the application boundary; the use case owns that collaboration and puts its outcome into the result. Outgoing adapters are outside this rule - repositories and other driven adapters may construct or reconstitute domain objects while implementing output ports."
constraint: Incoming Adapters must not depend on domain services.
enforced_by: "HexagonalRules#DCA-HEX-012"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

```java
DcaRule.of(
    "DCA-HEX-012",
    "Incoming Adapters must not depend on domain services",
    "An incoming adapter translates external input, calls an input port and formats its result."
        + " Injecting or invoking a domain service bypasses the application boundary; the use"
        + " case owns that collaboration and puts its outcome into the result. Outgoing adapters"
        + " are outside this rule - repositories and other driven adapters may construct or"
        + " reconstitute domain objects while implementing output ports",
    arch ->
        noClasses()
            .that()
            .resideInAnyPackage(arch.allIncomingAdapterPatterns())
            .should()
            .dependOnClassesThat()
            .areAssignableTo(DomainService.class)
            .allowEmptyShould(true))
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)
