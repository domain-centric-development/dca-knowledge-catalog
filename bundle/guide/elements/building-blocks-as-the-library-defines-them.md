---
type: Section
title: "Building blocks, as the library defines them"
chapter: Elements
source: guide
resource: dca-guide/architecture/elements.md
tags: [guide, section]
---

**The tactical markers, as the library defines them:**
```java
// dev.domaincentric.dca.buildingblocks.ddd.tactical — from dca-building-blocks, not written per project
public interface Id {
    // Marker interface - typed identifiers, no type parameter of their own
}

public interface Entity<T extends Entity<T, ID>, ID extends Id> {
    ID id();
    default boolean sameIdentityAs(T other) {
        return other != null && id().equals(other.id());
    }
}

public interface AggregateRoot<T extends AggregateRoot<T, ID>, ID extends Id>
        extends Entity<T, ID> {
    // Marker interface - identifies aggregate roots for all contexts
}
```

```csharp
// DomainCentric.BuildingBlocks.Ddd.Tactical — the same contracts in C#
public interface IId { }
public interface IEntity<TSelf, TId> : IEntity where TSelf : IEntity<TSelf, TId> where TId : IId { TId Id { get; } }
public interface IAggregateRoot<TSelf, TId> : IEntity<TSelf, TId>, IAggregateRoot
    where TSelf : IAggregateRoot<TSelf, TId> where TId : IId { }
```

**The port hierarchy, as the library defines it — and how a context uses it:**
```java
// dev.domaincentric.dca.buildingblocks.hexagonal.port.in
public interface InputPort {
    // Marker interface for all input ports (hexagonal architecture concept)
}

public interface UseCase<INPUT, OUTPUT> extends InputPort {
    OUTPUT execute(INPUT input);
}

// dev.domaincentric.dca.buildingblocks.hexagonal.port.out
public interface OutputPort {
    // Marker interface for all output ports (hexagonal architecture concept)
}

public interface Repository<T extends AggregateRoot<T, ID>, ID extends Id> extends OutputPort {
    Optional<T> findById(ID id);
    T save(T aggregate);
    void deleteById(ID id);
}

// Usage in a bounded context:
// order/application/createorder/CreateOrderInputPort.java
public interface CreateOrderInputPort extends UseCase<CreateOrderCommand, CreateOrderResult> {
    // Inherits execute() method with specific types
}

// order/application/shared/OrderRepository.java
public interface OrderRepository extends Repository<Order, OrderId> {
    // Inherits base methods, add domain-specific queries
    Optional<Order> findByCustomerId(CustomerId customerId);
}
```

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Id](/marker/tactical/id.md)
