---
type: Section
title: What belongs in the shared kernel
chapter: Strategic Architecture
source: guide
resource: dca-guide/architecture/strategic-design.md
tags: [guide, section]
---

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
- **Context-specific adapters** - An adapter one context owns stays in that context

**Guidelines:**
- Keep the Shared Kernel **as small as possible**
- Changes to Shared Kernel affect all contexts - coordinate carefully
- Only include code that has **identical meaning** across all contexts
- When in doubt, duplicate rather than share
- Use versioning if Shared Kernel becomes a separate module

**Every shared type has an owner.** One team, or one named person, owns each type in the shared kernel and decides
its changes; the contexts that use it are told before a change lands, not after. Without an owner, every context
changes `Money` for its own need, and the shared meaning is gone. The owner keeps changes compatible: a new field
gets a default, a new method leaves the old one in place until every context has moved, and a change of meaning — an
amount in cents instead of units — is a new type, not an edit of the old one. A type that cannot be kept compatible
this way is no longer shared; each context takes its own copy.

**Several teams: a module of its own.** In one application with one team, the shared kernel is a package next to the
contexts and changes with them in one commit. When several teams own the contexts, the shared kernel moves into a
module or artifact of its own with a version: each context names the version it uses and moves to the next one on its
own schedule, and a breaking change is a new major version. The package layout inside stays the same.

**Its words are written once, like a context's.** The shared kernel has a glossary of its own beside the contexts'
(`spec/shared-kernel/glossary.md` where the description keeps its spec), in the same form — each term with its type,
its definition and, for an id, whose identity it is. It is not a context: it has no subdomain, no features and no
scenarios of its own. A context's glossary names a shared term where the context uses it — an aggregate's
`**Identity:**` line names its shared id — and does not define it again.

**Decision Tree: Should This Go in Shared Kernel?**
```mermaid
flowchart TD
    START(["I have code that might be shared"]) --> Q1{"Used by two or more<br>bounded contexts?"}
    Q1 -- no --> KEEP["Keep it in the one context"]
    Q1 -- yes --> Q2{"Identical meaning<br>in every one of them?"}
    Q2 -- no --> DUP["Duplicate it —<br>different models are fine"]
    Q2 -- yes --> Q3{"A generic marker or base port —<br>a role, no business method?"}
    Q3 -- yes --> BB["It is a building block:<br>use the library's type,<br>or propose it there"]
    Q3 -- no --> Q4{"A universal value object?<br>Money, Address"}
    Q4 -- yes --> VO["sharedkernel/domain/model/"]
    Q4 -- no --> Q5{"A port with business methods<br>every context reads the same way?"}
    Q5 -- yes --> PORT["sharedkernel/application/shared/"]
    Q5 -- no --> OUT["Probably does not belong<br>in the shared kernel"]
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

## Related mentions (heuristic)

- [TransactionBoundary](/marker/application/transactionboundary.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [Specification<T>](/marker/tactical/specification.md)
