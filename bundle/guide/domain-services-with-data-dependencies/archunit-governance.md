---
type: Section
title: ArchUnit Governance
chapter: Domain Services with Data Dependencies
source: guide
resource: dca-guide/domain-services-with-data-dependencies.md
tags: [guide, section]
---

### DomainGateway Rules

```java
@ArchTest
static final ArchRule domain_gateways_must_be_read_only =
    classes().that().implement(DomainGateway.class)
        .should().haveOnlyFinalFields()
        .andShould().notHaveModifier(JavaModifier.ABSTRACT)
        .because("DomainGateways are read-only lookup interfaces implemented by adapters");

@ArchTest
static final ArchRule domain_gateways_must_reside_in_domain_layer =
    classes().that().implement(DomainGateway.class)
        .and().areInterfaces()
        .should().resideInAnyPackage("..domain.gateway..")
        .because("DomainGateway interfaces belong to the domain layer");

@ArchTest
static final ArchRule domain_gateway_interfaces_must_not_extend_output_port =
    classes().that().implement(DomainGateway.class)
        .should().notImplement(OutputPort.class)
        .because("DomainGateways are tactical DDD patterns, not hexagonal OutputPorts");
```

### Strategy/Callback Rules

Since the Strategy/Callback Pattern defines no interface of its own in the Domain Layer, the existing ArchUnit rules are already sufficient:

```java
// Existing rule: the Domain Layer has no outward dependencies
@ArchTest
static final ArchRule domain_layer_has_no_outward_dependencies =
    classes().that().resideInAnyPackage("..domain..")
        .should().onlyDependOnClassesThat()
        .resideInAnyPackage("..domain..", "..sharedkernel..", "java..")
        .because("Domain layer must not depend on application, adapter, or infrastructure layers");
```

This rule automatically ensures that:
- No `Function` parameter refers to Adapter or Application classes
- The domain uses only `java.util.function.*` (allowed under `java..`)
- No hidden dependencies are smuggled in through lambdas

### Additional Governance for Dedicated Functional Interfaces

```java
@ArchTest
static final ArchRule functional_interfaces_in_domain_must_be_annotated =
    classes().that().resideInAnyPackage("..domain..")
        .and().areInterfaces()
        .and().haveSimpleNameNotEndingWith("DomainGateway")
        .and().areAnnotatedWith(FunctionalInterface.class)
        .should().resideInAnyPackage("..domain.service..", "..domain..")
        .because("Domain functional interfaces should be co-located with their Domain Services");
```

---

## Related mentions (heuristic)

- [OutputPort](/marker/port-out/outputport.md)
- [DomainGateway](/marker/tactical/domaingateway.md)
