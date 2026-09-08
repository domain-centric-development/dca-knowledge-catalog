---
type: Rule
id: DCA-HEX-012
title: Incoming Adapters must not depend on domain services
rule: "An incoming adapter translates external input, calls an input port and formats its result. Injecting or invoking a domain service bypasses the application boundary; the use case owns that collaboration and puts its outcome into the result. Outgoing adapters are outside this rule - repositories and other driven adapters may construct or reconstitute domain objects while implementing output ports."
constraint: Incoming Adapters must not depend on domain services.
selects: "Classes in <module>.adapter.incoming.. of every module root, event consumers included. Outgoing adapters are not selected."
checks: "No dependency on a class assignable to DomainService - the building-block marker interface, any sub-interface of it and every class implementing one. A domain class without the marker is not a domain service by this rule. Injecting it, calling it or naming it in a signature all count as a dependency. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-012"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

## Selection

Classes in <module>.adapter.incoming.. of every module root, event consumers included. Outgoing adapters are not selected.

## Check

No dependency on a class assignable to DomainService - the building-block marker interface, any sub-interface of it and every class implementing one. A domain class without the marker is not a domain service by this rule. Injecting it, calling it or naming it in a signature all count as a dependency. An empty selection passes.

## .NET reading

**Selection.** Classes in <module>.Adapter.Incoming of every module root, event consumers included. Outgoing adapters are not selected.

**Check.** No dependency on a type assignable to IDomainService - the building-block marker interface, any sub-interface of it and every class implementing one. A domain class without the marker is not a domain service by this rule. Injecting it, calling it or naming it in a signature all count as a dependency; constructor parameters are read from the runtime type as well, so a service injected into an adapter whose members are all async is still found. An empty selection passes.

## Implementation

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
    .selecting(
        "Classes in <module>.adapter.incoming.. of every module root, event consumers"
            + " included. Outgoing adapters are not selected.")
    .checking(
        "No dependency on a class assignable to DomainService - the building-block marker"
            + " interface, any sub-interface of it and every class implementing one. A domain"
            + " class without the marker is not a domain service by this rule. Injecting it,"
            + " calling it or naming it in a signature all count as a dependency. An empty"
            + " selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
