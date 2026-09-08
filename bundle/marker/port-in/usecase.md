---
type: Marker
title: "UseCase<INPUT, OUTPUT>"
category: port-in
kind: interface
signature: "public interface UseCase<INPUT, OUTPUT> extends InputPort"
package: dev.domaincentric.dca.buildingblocks.hexagonal.port.in
generics: "INPUT, OUTPUT"
extends: [InputPort]
methods: ["OUTPUT execute(INPUT input)"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/hexagonal/port/in/UseCase.java
tags: [port-in, marker]
---

Marker interface for Input Ports (Hexagonal Architecture) / Use Cases (Clean Architecture).

An input port represents an entry point to the application layer, defining a single use case
or application feature. In Hexagonal Architecture, input ports are called by primary/driving
adapters (e.g., REST controllers, event consumers, CLI handlers).

**Characteristics of Input Ports:**

- Represent a single user action or system operation
- Define the interface that use cases implement
- Accept Input models (Commands or Queries) as parameters
- Return Output models, not domain entities
- Technology-agnostic (no framework dependencies)

**Input/Output Pattern:** Input ports accept Input models and return Output models to
decouple the application layer from presentation and infrastructure concerns.

**Example:**

```java
public interface CreateProductInputPort extends UseCase<CreateProductCommand, CreateProductResult> {}

public class CreateProductUseCase implements CreateProductInputPort {
    @Override
    public CreateProductResult execute(CreateProductCommand input) {
        // Use case implementation
    }
}
```

**Naming Convention:** the input port interface is `{Action`{Entity}InputPort}
(`CreateProductInputPort`, `UpdateProductPriceInputPort`); the class implementing it
is `{Action`{Entity}UseCase}. The interface inherits `execute` from `UseCase`
and needs no method of its own.

**References:**

- Alistair Cockburn - Hexagonal Architecture (Ports & Adapters)
- Robert C. Martin - Clean Architecture (Chapter 19-20: Use Cases)
- Tom Hombergs - Get Your Hands Dirty on Clean Architecture

## Extends

- [InputPort](/marker/port-in/inputport.md)

## Governed by

- [Application layer InputPort implementations must end with 'UseCase'](/rule/naming/application-layer-inputport-implementations-must-end-with-usecase.md)
- [InputPort interfaces must end with 'InputPort'](/rule/naming/inputport-interfaces-must-end-with-inputport.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [Ports and Use Cases](/guide/language-mappings/ports-and-use-cases.md)
- [ELEMENTS](/guide/readme/elements.md)
- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
