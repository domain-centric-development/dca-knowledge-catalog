---
type: Reference
title: Core Rule Categories — 2. Framework Independence Rules
tags: [reference]
evidence_for: "/guide/archunit-governance/core-rule-categories.md#2-framework-independence-rules"
---

[Full node and context](/guide/archunit-governance/core-rule-categories.md#2-framework-independence-rules). This is an evidence excerpt; retain the parent selection and caveats.

### 2. Framework Independence Rules

Use cases may be registered by configuration or carry an injectable stereotype. A
static reference does not prove registration, and runtime scanning need not leave one;
`DCA-NAM-002` therefore only lists unannotated Java operations as an informational
diagnostic. It never fails. .NET registration is code and has no stereotype counterpart.
Outgoing adapters may reuse global and own-module infrastructure; another module's
infrastructure remains private (`DCA-HEX-005`).

Domain metadata is classified by configured roles, including members and composed
metadata. Types prohibit injectable/container, persistence-entity and transactional
roles; fields (and .NET properties) prohibit injection-site and persistence-mapping
roles; methods prohibit transaction and event-listener roles, plus setter injection
except on events; constructors prohibit injection-site metadata. Java detects direct
and meta-annotations. .NET checks an attribute's namespace and every base attribute
type against persistence, injection, transaction and container namespace lists; no
event-listener attribute role is configured by default. Unclassified metadata is
allowed by this check, without claiming it harmless. Events, services, factories and
specifications have exclusive `ADV-004/011/015/018` ownership; `ONI-003` owns the
remaining domain-model types, so one type is never reported twice for metadata.

The following examples illustrate individual checks; the published rules apply the complete role policy above.

```java
@ArchTest
static final ArchRule domain_should_be_framework_agnostic =
    noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat()
            .resideInAnyPackage(
                "org.springframework..",
                "jakarta.persistence..",
                "javax.persistence..",
                "org.hibernate..",
                "jakarta.validation..",
                "javax.validation.."
            )
        .because("Domain must be framework-agnostic");

@ArchTest
static final ArchRule domain_should_not_use_jpa_annotations =
    noFields()
        .that().areDeclaredInClassesThat().resideInAPackage("..domain..")
        .should().beAnnotatedWith("jakarta.persistence.Id")
        .orShould().beAnnotatedWith("jakarta.persistence.Column")
        .orShould().beAnnotatedWith("jakarta.persistence.ManyToOne")
        .orShould().beAnnotatedWith("jakarta.persistence.OneToMany")
        .because("Domain should not use JPA annotations - use separate persistence model");

@ArchTest
static final ArchRule application_should_be_framework_agnostic =
    noClasses()
        .that().resideInAPackage("..application..")
        .should().dependOnClassesThat()
            .resideInAnyPackage(
                "org.springframework.web..",
                "jakarta.ws.rs..",
                "org.springframework.data.."
            )
        .because("Application layer should not depend on web or persistence frameworks");

@ArchTest
static final ArchRule application_layer_can_use_minimal_spring =
    classes()
        .that().resideInAPackage("..application..")
        .should().onlyDependOnClassesThat()
            .resideInAnyPackage(
                "..domain..",
                "..application..",
                "..sharedkernel..",
                "java..",
                "org.springframework.stereotype..",  // @Service is acceptable
                "org.springframework.transaction.."   // @Transactional is acceptable (pragmatic)
            )
        .because("Application can use minimal Spring annotations for pragmatism");
```
