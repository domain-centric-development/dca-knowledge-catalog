---
type: Marker
title: "Repository<T, ID>"
category: port-out
kind: interface
signature: "public interface Repository<T extends AggregateRoot<T, ID>, ID extends Id> extends OutputPort"
package: dev.domaincentric.dca.buildingblocks.hexagonal.port.out
extends: [OutputPort]
methods: ["Optional<T> findById(ID id)", "T save(T aggregate)", "void deleteById(ID id)"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/hexagonal/port/out/Repository.java
tags: [port-out, marker]
---

Base interface for Repositories.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Governed by

- [Classes named *Repository must reside in the outgoing adapter package](/rule/hexagonal/classes-named-repository-must-reside-in-the-outgoing-adapter-package.md)
- [Controllers and Resources must never access repositories directly](/rule/hexagonal/controllers-and-resources-must-never-access-repositories-directly.md)
- [Output ports must not reside in the domain layer](/rule/hexagonal/output-ports-must-not-reside-in-the-domain-layer.md)
- [The shared kernel's output-port markers must all be interfaces](/rule/layered/the-shared-kernel-s-output-port-markers-must-all-be-interfaces.md)
- [Repository Interfaces must end with 'Repository'](/rule/naming/repository-interfaces-must-end-with-repository.md)
- [Aggregate Roots must not hold references to Repositories or other Output Ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md)
- [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/repository-implementations-must-reside-in-adapter-outgoing-package.md)
- [Repository interfaces must reside in the application layer's shared output-port package](/rule/tactical/repository-interfaces-must-reside-in-the-application-layer-s-shared-output-port-package.md)
- [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/repository-interfaces-should-extend-repository-marker-interface.md)
- [Repository methods must not return non-root Entities](/rule/tactical/repository-methods-must-not-return-non-root-entities.md)
- [Store interfaces must extend the Store marker, not Repository](/rule/tactical/store-interfaces-must-extend-the-store-marker-not-repository.md)
- [Store interfaces must not declare findById or save methods](/rule/tactical/store-interfaces-must-not-declare-findbyid-or-save-methods.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Framework Annotations Rules](/guide/architecture-reference-guide/framework-annotations-rules.md)
- [Interface vs Implementation Placement](/guide/architecture-reference-guide/interface-vs-implementation-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Ansatz 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/ansatz-1-domaingateway-pattern.md)
- [DEVIATIONS FROM THE LITERATURE](/guide/readme/deviations-from-the-literature.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
