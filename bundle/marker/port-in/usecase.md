---
type: Marker
title: "UseCase<INPUT, OUTPUT>"
category: port-in
kind: interface
signature: "public interface UseCase<INPUT, OUTPUT> extends InputPort"
extends: [InputPort]
methods: ["OUTPUT execute(INPUT input)"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/port/in/UseCase.java
tags: [port-in, marker]
---

Marker interface for Input Ports (Hexagonal Architecture) / Use Cases (Clean Architecture).

## Extends

- [InputPort](/marker/port-in/inputport.md)

## Governed by

- [Application layer InputPort implementations must end with 'UseCase'](/rule/naming/application-layer-inputport-implementations-must-end-with-usecase.md)
- [Use case classes must be annotated with @Service](/rule/naming/use-case-classes-must-be-annotated-with-service.md)
- [Use cases that save an aggregate must publish its domain events](/rule/usecase/use-cases-that-save-an-aggregate-must-publish-its-domain-events.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [DEPENDENCY STRUCTURE](/guide/readme/dependency-structure.md)
- [ELEMENTS](/guide/readme/elements.md)
- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
