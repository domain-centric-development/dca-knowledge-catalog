---
type: Section
title: Building Blocks
chapter: "Language Mappings: Java/Spring ↔ C#/.NET"
source: guide
resource: dca-guide/topics/language-mappings.md
tags: [guide, section]
---

The tactical markers, one to one. Java package `ddd.tactical`, .NET namespace `Ddd.Tactical`.

| Concept | Java | C# |
|---|---|---|
| Identifier | `Id` | `IId` — implemented by a `readonly record struct` |
| Value object | `Value` | `IValue` — implemented by a `record` |
| Entity | `Entity<T extends Entity<T, ID>, ID extends Id>` | `IEntity<TSelf, TId>` (+ non-generic `IEntity` for reflection) |
| Aggregate root | `AggregateRoot<T, ID>` | `IAggregateRoot<TSelf, TId>` (+ non-generic `IAggregateRoot`) |
| Event-collecting base class | `BaseAggregateRoot<T, ID>` | `AggregateRootBase<TSelf, TId>` |
| Domain event | `DomainEvent` (`eventId()`, `occurredOn()`) | `IDomainEvent` (`EventId`, `OccurredOn`) — a `record` |
| Integration event | `IntegrationEvent` + `@IntegrationEventType(name, version)` | `IIntegrationEvent` + `[IntegrationEventType(name, Version = …)]` |
| Domain service | `DomainService` | `IDomainService` |
| Domain gateway | `DomainGateway` | `IDomainGateway` |
| Factory | `Factory` | `IFactory` |
| Specification | `Specification<T>` (`isSatisfiedBy`) | `ISpecification<T>` (`IsSatisfiedBy`) |
| Timestamps, ids | `java.time.Instant`, `java.util.UUID` | `DateTimeOffset`, `Guid` |
| Absence | `Optional<T>` | nullable reference `T?` |

The self-referencing generics (`TSelf`) are kept in C# for parity with the Java signatures, so the
templates and rules read the same in both languages; idiomatic C# would often write `IAggregateRoot<TId>`.

```java
public record OrderId(UUID value) implements Id {}
public class Order extends BaseAggregateRoot<Order, OrderId> { … }
```

```csharp
public readonly record struct OrderId(Guid Value) : IId;
public sealed class Order : AggregateRootBase<Order, OrderId> { … }
```

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainGateway](/marker/tactical/domaingateway.md)
- [DomainService](/marker/tactical/domainservice.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Factory](/marker/tactical/factory.md)
- [Id](/marker/tactical/id.md)
- [IntegrationEvent](/marker/tactical/integrationevent.md)
- [@IntegrationEventType](/marker/tactical/integrationeventtype.md)
- [Specification<T>](/marker/tactical/specification.md)
