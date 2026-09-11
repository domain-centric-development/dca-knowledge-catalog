---
type: Marker
title: OutputPort
category: port-out
kind: interface
signature: public interface OutputPort
package: dev.domaincentric.dca.buildingblocks.hexagonal.port.out
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/hexagonal/port/out/OutputPort.java
tags: [port-out, marker]
---

Marker interface for Output Ports (Hexagonal Architecture).

Output ports define what the application needs from the outside world. They represent
dependencies that the application layer requires but does not implement itself. In Hexagonal
Architecture terms, output ports sit on the "right side" of the hexagon.

**Driven Adapters that implement Output Ports:**

- Repository implementations (database access)
- External API clients (REST, gRPC, SOAP)
- Message publishers (Kafka, RabbitMQ, SQS)
- Email/SMS services
- File storage services
- Cache implementations

**Common Output Port Types:**

- `y` - Aggregate persistence
- `r` - Event publication
- External service ports - Integration with external systems

**Key Characteristics:**

- Technology-agnostic interface (no framework dependencies)
- Defined in terms of application/domain concepts
- Implemented by adapters in the outgoing adapter layer
- Used (depended upon) by application layer classes

**Example Hierarchy:**

```java
OutputPort (marker)
  ├── Repository<T, ID>
  │     └── ProductRepository extends Repository<Product, ProductId>
  └── DomainEventPublisher
```

**Dependency Inversion Principle:** Output ports enable the application layer to depend on
abstractions rather than concrete implementations. The application defines what it needs (the
interface), and the infrastructure provides concrete implementations.

## Related mentions in guides (heuristic)

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [Approach 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md)
- [Application Layer (Use Cases / Application Business Rules)](/guide/elements/application-layer-use-cases-application-business-rules.md)
- [14. Architecture Placement (DCA Pattern)](/guide/jwt-implementation-guide/14-architecture-placement-dca-pattern.md)
- [Detailed Structure with All Subdivisions](/guide/package-structure/detailed-structure-with-all-subdivisions.md)
- [Structure Evolution Example: From Startup to Maturity](/guide/package-structure/structure-evolution-example-from-startup-to-maturity.md)
- [Deviations from the literature](/guide/readme/deviations-from-the-literature.md)
- [APPLICATION LAYER RULES](/guide/rules/application-layer-rules.md)
- [Shared Kernel Pattern (Strategic DDD)](/guide/strategic-design/shared-kernel-pattern-strategic-ddd.md)
