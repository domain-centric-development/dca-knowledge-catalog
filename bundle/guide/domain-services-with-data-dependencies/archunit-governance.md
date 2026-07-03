---
type: Section
title: ArchUnit Governance
chapter: Domain Services mit Datenabhängigkeiten
source: guide
resource: implementing-domain-centric-architecture/domain-services-with-data-dependencies.md
tags: [guide, section]
---

### DomainGateway-Regeln

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

### Strategy/Callback-Regeln

Da das Strategy/Callback Pattern kein eigenes Interface im Domain Layer definiert, sind die bestehenden ArchUnit-Regeln bereits ausreichend:

```java
// Bestehende Regel: Domain Layer hat keine Abhängigkeiten nach außen
@ArchTest
static final ArchRule domain_layer_has_no_outward_dependencies =
    classes().that().resideInAnyPackage("..domain..")
        .should().onlyDependOnClassesThat()
        .resideInAnyPackage("..domain..", "..sharedkernel..", "java..")
        .because("Domain layer must not depend on application, adapter, or infrastructure layers");
```

Diese Regel stellt automatisch sicher, dass:
- Kein `Function`-Parameter auf Adapter- oder Application-Klassen verweist
- Die Domain nur `java.util.function.*` verwendet (erlaubt unter `java..`)
- Keine versteckten Abhängigkeiten über Lambdas eingeschleust werden

### Zusätzliche Governance für eigene Functional Interfaces

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

## Related markers

- [OutputPort](/marker/port-out/outputport.md)
- [DomainGateway](/marker/tactical/domaingateway.md)
