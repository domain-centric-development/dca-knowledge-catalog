---
type: Marker
title: "Repository<T, ID>"
category: port-out
kind: interface
signature: "public interface Repository<T extends AggregateRoot<T, ID>, ID extends Id> extends OutputPort"
extends: [OutputPort]
methods: ["Optional<T> findById(ID id)", "T save(T aggregate)", "void deleteById(ID id)"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/port/out/Repository.java
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
- [The Domain Model should be framework independent and should not use 3rd party libraries when possible](/rule/onion/the-domain-model-should-be-framework-independent-and-should-not-use-3rd-party-libraries-when-possible.md)
- [Aggregate Roots must not hold references to Repositories or other Output Ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md)
- [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md)
- [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/repository-implementations-must-reside-in-adapter-outgoing-package.md)
- [Repository interfaces must reside in the application layer's shared output-port package](/rule/tactical/repository-interfaces-must-reside-in-the-application-layer-s-shared-output-port-package.md)
- [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/repository-interfaces-should-extend-repository-marker-interface.md)
- [Repository methods must return Aggregate Roots](/rule/tactical/repository-methods-must-return-aggregate-roots.md)
- [Use cases that save an aggregate must publish its domain events](/rule/usecase/use-cases-that-save-an-aggregate-must-publish-its-domain-events.md)

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
