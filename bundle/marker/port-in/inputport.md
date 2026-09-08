---
type: Marker
title: InputPort
category: port-in
kind: interface
signature: public interface InputPort
package: dev.domaincentric.dca.buildingblocks.hexagonal.port.in
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/hexagonal/port/in/InputPort.java
tags: [port-in, marker]
---

Marker interface for Input Ports (Hexagonal Architecture).

Input ports are the entry points to the application layer. They define how the outside world
(driving/primary adapters) can interact with the application. In Hexagonal Architecture terms,
input ports sit on the "left side" of the hexagon.

**Driving Adapters that use Input Ports:**

- REST Controllers
- GraphQL Resolvers
- CLI Command Handlers
- Event Consumers (external events)
- Scheduled Tasks
- MCP Tool Providers

**Common Input Port Types:**

- `e` - Command/Query pattern with INPUT and OUTPUT types
- Event Handlers - Process incoming events from other systems

**Key Characteristics:**

- Technology-agnostic (no framework dependencies)
- Defined in terms of application/domain concepts
- Implemented by application layer classes (use cases)
- Called by adapters in the incoming adapter layer

**Example Hierarchy:**

```java
InputPort (marker)
  └── UseCase<INPUT, OUTPUT>
        └── CreateProductInputPort extends UseCase<CreateProductCommand, CreateProductResult>
```

## Governed by

- [Incoming Adapters must depend on input port interfaces, not on use case classes](/rule/hexagonal/incoming-adapters-must-depend-on-input-port-interfaces-not-on-use-case-classes.md)
- [Application layer InputPort implementations must end with 'UseCase'](/rule/naming/application-layer-inputport-implementations-must-end-with-usecase.md)
- [InputPort interfaces must end with 'InputPort'](/rule/naming/inputport-interfaces-must-end-with-inputport.md)
- [Base InputPort interface must be in the building-blocks port in package](/rule/usecase/base-inputport-interface-must-be-in-the-building-blocks-port-in-package.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
