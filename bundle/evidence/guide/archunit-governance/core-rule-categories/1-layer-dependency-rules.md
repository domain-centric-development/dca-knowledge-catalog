---
type: Reference
title: Core Rule Categories — 1. Layer Dependency Rules
tags: [reference]
evidence_for: "/guide/archunit-governance/core-rule-categories.md#1-layer-dependency-rules"
---

[Full node and context](/guide/archunit-governance/core-rule-categories.md#1-layer-dependency-rules). This is an evidence excerpt; retain the parent selection and caveats.

### 1. Layer Dependency Rules

Enforce that dependencies only point inward toward the domain.

```java
@ArchTest
static final ArchRule domain_should_not_depend_on_outer_layers =
    noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat()
            .resideInAnyPackage(
                "..application..",
                "..adapter..",
                "..infrastructure.."
            )
        .because("Domain must be independent of outer layers");

@ArchTest
static final ArchRule application_should_not_depend_on_adapters =
    noClasses()
        .that().resideInAPackage("..application..")
        .should().dependOnClassesThat()
            .resideInAnyPackage("..adapter..", "..infrastructure..")
        .because("Application should only depend on domain");

@ArchTest
static final ArchRule adapters_should_not_depend_on_infrastructure =
    noClasses()
        .that().resideInAPackage("..adapter..")
        .should().dependOnClassesThat()
            .resideInPackage("..infrastructure..")
        .because("Adapters should not depend on infrastructure layer");

@ArchTest
static final ArchRule layered_architecture_is_respected =
    layeredArchitecture()
        .consideringAllDependencies()

        .layer("Domain").definedBy("..domain..")
        .layer("Application").definedBy("..application..")
        .layer("Adapter").definedBy("..adapter..")
        .layer("Infrastructure").definedBy("..infrastructure..")

        .whereLayer("Domain").mayNotAccessAnyLayer()
        .whereLayer("Application").mayOnlyAccessLayers("Domain")
        .whereLayer("Adapter").mayOnlyAccessLayers("Application", "Domain")
        .whereLayer("Infrastructure").mayAccessAnyLayer()

        .because("Dependencies must point inward toward domain");
```
