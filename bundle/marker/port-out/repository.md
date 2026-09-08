---
type: Marker
title: "Repository<T, ID>"
category: port-out
kind: interface
signature: "public interface Repository<T extends AggregateRoot<T, ID>, ID extends Id> extends OutputPort"
package: dev.domaincentric.dca.buildingblocks.hexagonal.port.out
generics: "T extends AggregateRoot<T, ID>, ID extends Id"
extends: [OutputPort]
methods: ["Optional<T> findById(ID id)", "T save(T aggregate)", "void deleteById(ID id)"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/hexagonal/port/out/Repository.java
tags: [port-out, marker]
---

Base interface for Repositories.

Repositories provide a collection-like interface for accessing Aggregate Roots. They
encapsulate the logic for retrieving and persisting aggregates, presenting the illusion of an
in-memory collection.

**Key Principles:**

- One Repository per Aggregate Root (not per Entity)
- Repository implementations belong in secondary adapters (infrastructure layer)
- Use domain language in method names (not generic CRUD)
- Return domain objects, never infrastructure objects

**Characteristics:**

- Interface resides in the application layer as an output port (e.g., `product.application.shared.ProductRepository`)
- Implementation resides in an outgoing adapter (e.g., `product.adapter.outgoing.persistence.InMemoryProductRepository`)
- Methods use ubiquitous language (e.g., `findBySku()`, `findByCategory()`)
- Should NOT have Spring annotations in the interface
- Collections should be immutable when returned

**Common Methods:**

- `findById(ID)` - Retrieve aggregate by its unique identifier
- `save(T)` - Add or update an aggregate (collection metaphor)
- `deleteById(ID)` - Remove an aggregate from the collection

These three are the deliberate minimum: what every aggregate's life cycle needs and nothing a
concrete port would have to override. The port extends them freely with the questions its use
cases ask - `findBySku(SKU)`, `existsBySku(SKU)`, `count()`, `deleteAll()`; the marker adds no generic `existsById` or `findAll`, because whether
such a question is asked at all is a decision of the owning context, not of the building block.

**Example:**

```java
// Output port in the application layer
public interface ProductRepository extends Repository<Product, ProductId> {
  Optional<Product> findBySku(SKU sku);
  List<Product> findByCategory(Category category);
  boolean existsBySku(SKU sku);
}

// Secondary adapter implementation
@Repository
public class InMemoryProductRepository implements ProductRepository {
  // Implementation using in-memory storage
}
```

**Pattern:** Repositories mediate between the domain and data mapping layers using a
collection-like interface for accessing domain objects.

**References:**

- Eric Evans' Domain-Driven Design (2003), Chapter 6: "The Life Cycle of a Domain Object"
- Vaughn Vernon's Implementing Domain-Driven Design (2013), Chapter 12: "Repositories"
- Martin Fowler's Repository
Pattern

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Governed by

- [Classes named *Repository must reside in the outgoing adapter package](/rule/hexagonal/classes-named-repository-must-reside-in-the-outgoing-adapter-package.md)
- [Controllers and Resources must never access repositories directly](/rule/hexagonal/controllers-and-resources-must-never-access-repositories-directly.md)
- [Output Ports in application.shared must extend OutputPort](/rule/hexagonal/output-ports-in-application-shared-must-extend-outputport.md)
- [Output ports must not reside in the domain layer](/rule/hexagonal/output-ports-must-not-reside-in-the-domain-layer.md)
- [The shared kernel's output-port markers must all be interfaces](/rule/layered/the-shared-kernel-s-output-port-markers-must-all-be-interfaces.md)
- [Repository Interfaces must end with 'Repository'](/rule/naming/repository-interfaces-must-end-with-repository.md)
- [Aggregate Roots must not hold references to Repositories or other Output Ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md)
- [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md)
- [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/repository-implementations-must-reside-in-adapter-outgoing-package.md)
- [Repository interfaces must reside in the application layer's shared output-port package](/rule/tactical/repository-interfaces-must-reside-in-the-application-layer-s-shared-output-port-package.md)
- [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/repository-interfaces-should-extend-repository-marker-interface.md)
- [Repository methods must not return non-root Entities](/rule/tactical/repository-methods-must-not-return-non-root-entities.md)
- [Store interfaces must extend the Store marker, not Repository](/rule/tactical/store-interfaces-must-extend-the-store-marker-not-repository.md)
- [Store interfaces must not declare findById or save methods](/rule/tactical/store-interfaces-must-not-declare-findbyid-or-save-methods.md)
- [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md)
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
