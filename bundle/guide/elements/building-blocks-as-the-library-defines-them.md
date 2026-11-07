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

public interface Owned<OWNER extends Id> {
    // Marker for an aggregate root that belongs to someone; OWNER is the owner's id type.
    // Its repository declares a lookup by the aggregate's id and the owner's id (DCA-TAC-026).
}

public abstract class DomainException extends RuntimeException {
    // Base of every business-rule violation the model raises; carries no code and no status
}
```

```java
// dev.domaincentric.dca.buildingblocks.application — the failures a port's contract declares
public abstract class PortException extends RuntimeException { }

public abstract class InputPortException extends PortException {
    // Declared by an input port, caught by its caller; never extended directly
}

public abstract class UseCaseException extends InputPortException {
    // Thrown only by a use case: an expected refusal where the context throws its refusals.
    // Concrete use-case failures extend this.
}

public abstract class OutputPortException extends PortException {
    // Declared by an output port's contract, thrown by its adapter, caught by the use case:
    // an expected conflict the store sees, or a foreign system that refused or did not answer.
    // A failure of the system's own infrastructure is not one.
}

public interface Refusal {
    // Marker for a refusal case of a sealed use-case result; the transaction boundary rolls back on it.
    // A success case never carries it, and a sealed result of successes alone has none.
}
```

```csharp
// DomainCentric.BuildingBlocks.Ddd.Tactical — the same contracts in C#
public interface IId { }
public interface IEntity<TSelf, TId> : IEntity where TSelf : IEntity<TSelf, TId> where TId : IId { TId Id { get; } }
public interface IAggregateRoot<TSelf, TId> : IEntity<TSelf, TId>, IAggregateRoot
    where TSelf : IAggregateRoot<TSelf, TId> where TId : IId { }
public interface IOwned<TOwnerId> : IOwned where TOwnerId : IId { }   // IOwned: the non-generic base the rules select on
public abstract class DomainException : Exception { }

// DomainCentric.BuildingBlocks.Application
public abstract class PortException : Exception { }
public abstract class InputPortException : PortException { }
public abstract class UseCaseException : InputPortException { }
public abstract class OutputPortException : PortException { }
public interface IRefusal { }
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

- [InputPortException](/marker/application/inputportexception.md)
- [OutputPortException](/marker/application/outputportexception.md)
- [PortException](/marker/application/portexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)
- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainException](/marker/tactical/domainexception.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Id](/marker/tactical/id.md)
