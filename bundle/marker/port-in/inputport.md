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

- [The base InputPort contract is not redeclared in the project](/rule/usecase/dca-use-001.md)

## Related mentions in guides (heuristic)

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Application Layer (Use Cases / Application Business Rules)](/guide/elements/application-layer-use-cases-application-business-rules.md)
- [Structure Evolution Example: From Startup to Maturity](/guide/package-structure/structure-evolution-example-from-startup-to-maturity.md)
- [APPLICATION LAYER RULES](/guide/rules/application-layer-rules.md)
- [Operation boundaries and declared contracts](/guide/rules/operation-boundaries-and-declared-contracts.md)
- [Shared Kernel Pattern (Strategic DDD)](/guide/strategic-design/shared-kernel-pattern-strategic-ddd.md)
