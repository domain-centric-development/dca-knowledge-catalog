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
- Carries no framework annotations - the interface is plain Java
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

## Related mentions in guides (heuristic)

- [Adoption Path (Tiers)](/guide/archunit-governance/adoption-path-tiers.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Approach 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md)
- [Application Layer (Use Cases / Application Business Rules)](/guide/elements/application-layer-use-cases-application-business-rules.md)
- [Deviations from the literature](/guide/readme/deviations-from-the-literature.md)
- [Repository](/guide/repository-vs-store/repository.md)
- [APPLICATION LAYER RULES](/guide/rules/application-layer-rules.md)
- [TRANSACTION RULES](/guide/rules/transaction-rules.md)
- [Shared Kernel Pattern (Strategic DDD)](/guide/strategic-design/shared-kernel-pattern-strategic-ddd.md)
