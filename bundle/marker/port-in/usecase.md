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

## Referenced by ADRs

- [ADR-020: Use Case Output Naming Convention (*Result instead of *Response)](/adr/adr-020-use-case-result-naming.md)

## Discussed in

- [Step 4: Application Layer - Use Case](/book/03-getting-started/step-4-application-layer-use-case.md)
- [Application Layer](/book/04-the-four-layers/application-layer.md)
- [Use Case Implementation](/book/06-application-layer/use-case-implementation.md)
- [Use Case Pattern](/book/06-application-layer/use-case-pattern.md)
- [Use Case Organization](/book/09-package-structure/use-case-organization.md)
- [Application Layer Testing](/book/12-testing-strategy/application-layer-testing.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
