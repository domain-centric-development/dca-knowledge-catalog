---
type: Reference
title: ELEMENTS — Repository vs. Store
tags: [reference]
evidence_for: "/guide/readme/elements.md#repository-vs-store"
---

[Full node and context](/guide/readme/elements.md#repository-vs-store). This is an evidence excerpt; retain the parent selection and caveats.

### Repository vs. Store

DCA distinguishes two kinds of persistence-shaped output ports. Both `extend OutputPort`, but their **business semantics differ**:

**Repository** — collection-like interface for Aggregate Roots (Evans, Vernon).

- Exists **only** for Aggregate Roots
- Identity + lifecycle semantics: `findById()`, `save()`, `delete()`
- Extends the `Repository<T, ID>` marker
- One Repository per Aggregate Root

```java
public interface CustomerAccountRepository extends Repository<CustomerAccount, CustomerAccountId> {
    Optional<CustomerAccount> findById(CustomerAccountId id);
    void save(CustomerAccount account);
}
```

**Store** — records or queries operational data without an own aggregate lifecycle.

- Exists for **Value Objects, Events, or technical state** without an aggregate lifecycle
- Append-/record-style semantics: `record()`, `count()`, `exists()`, `reset()` — lookup by key is allowed; no aggregate `save()` / `delete()` semantics
- Extends the `Store` marker (`Store extends OutputPort`) — never the `Repository` marker
- Implementation lives in `adapter.outgoing/`

```java
public interface LoginProtectionStore extends Store {
    void record(LoginAttempt attempt);
    int  countRecentFailures(BaseStore baseStore, Email email, Duration window);
    boolean isLoginBlocked(BaseStore baseStore, Email email);
}
```

**Decision matrix:**

| Criterion | Repository | Store |
|---|---|---|
| Stored object | Aggregate Root | Value Object / operational data |
| Aggregate lifecycle | yes — `save`, `delete` | no — `record`, `count`, `exists`; lookup by key allowed |
| Marker | `extends Repository<T, ID>` | `extends Store` |
| Examples | `CustomerAccountRepository`, `OrderRepository` | `LoginProtectionStore`, `AuditLogStore`, `EventStore` |

**Rules of thumb:**

1. Lookup by key (`findById`) is allowed on a Store too; aggregate lifecycle determines Repository semantics.
2. Need `record()` or `count()`? → Store (the object is recorded, not managed).
3. In doubt: if the stored object is a `Value` or a record, it's almost always a Store.

> **Note on EventStore (Event Sourcing):** The `EventStore` from Event Sourcing is a *specialization* of Store — one specifically for Domain Events that supports aggregate reconstruction. The general `Store` is the broader pattern for any operational data.

> **Note on cross-cutting `*Response` classes:** Generic Response/error classes (`ErrorResponse`, base `Response`, `SimpleResponse`) belong in the **shared kernel's adapter-incoming package**, not in any individual bounded context. ArchUnit rules that check `*Response` placement must include the shared kernel adapter — discover its package dynamically via `@SharedKernel` rather than hardcoding the name (`shared` / `common` / `core` / `sharedkernel`).

**Why the distinction matters:**
The naming is part of the Ubiquitous Language. A reader should know from the interface name alone whether they're dealing with a managed aggregate (Repository) or recorded data (Store) — without opening the implementation. Both are technically Output Ports in hexagonal architecture, but the business role is fundamentally different.

**What Belongs in Shared Kernel:**

✅ **Include:**
- **Universal value objects** used by multiple contexts (Money, Price, shared IDs)
- **Application-specific shared ports** with identical meaning in every context (an `IdentityProvider`)
- **Shared adapters** that implement a library port once for the whole application — on Spring these come from `dca-spring` (`SpringDomainEventPublisher`, `SpringTransactionBoundary`); other frameworks write them here
- **Specification pattern implementations** (CompositeSpecification, And/Or/Not specifications)
- **Cross-cutting domain concepts** that have identical meaning everywhere

📦 **Comes from the dependency, not written here:**
- **DDD marker interfaces** (Entity, AggregateRoot, Value, DomainEvent, …) and **strategic annotations**
- **Base port interfaces** (`UseCase<INPUT, OUTPUT>`, `Repository`, `Store`, `DomainEventPublisher`) and `TransactionBoundary`

❌ **Exclude:**
- **Aggregates** - These belong to specific bounded contexts
- **Business logic** - Should live in context-specific domain layers
- **Context-specific value objects** - Only truly universal ones belong here
- **Use case implementations** - Belong to specific contexts
- **Adapters** - Never shared between contexts

**Guidelines:**
- Keep the Shared Kernel **as small as possible**
- Changes to Shared Kernel affect all contexts - coordinate carefully
- Only include code that has **identical meaning** across all contexts
- When in doubt, duplicate rather than share
- Use versioning if Shared Kernel becomes a separate module

**Decision Tree: Should This Go in Shared Kernel?**
```
START: I have code that might be shared
   │
   ├─ Is it used by 2+ bounded contexts?
   │     NO → Keep in single context
   │     YES ↓
   │
   ├─ Does it have IDENTICAL meaning everywhere?
   │     NO → Duplicate instead (different models OK)
   │     YES ↓
   │
   ├─ Is it a generic marker or base port (a role, no business method)?
   │     YES → It is a building block: use the library's type, or propose it there
   │     NO ↓
   │
   ├─ Is it a universal value object (Money, Address)?
   │     YES → Add to sharedkernel/domain/model/
   │     NO ↓
   │
   └─ Is it a port with business methods that every context reads the same way?
         YES → Add to sharedkernel/application/shared/
         NO → Probably shouldn't be in Shared Kernel
```

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

**Example - Shared Value Object:**
```java
// sharedkernel/domain/model/Money.java
public record Money(BigDecimal amount, Currency currency) implements Value {

    public Money {
        Objects.requireNonNull(amount);
        Objects.requireNonNull(currency);
        if (amount.scale() > 2) {
            throw new IllegalArgumentException("Money cannot have more than 2 decimal places");
        }
    }

    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Cannot add money with different currencies");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
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
