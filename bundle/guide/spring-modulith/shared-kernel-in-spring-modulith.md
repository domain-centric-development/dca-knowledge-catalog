---
type: Section
title: Shared Kernel in Spring Modulith
chapter: Spring Modulith Implementation
source: guide
resource: dca-guide/topics/spring-modulith.md
tags: [guide, section]
---

The Shared Kernel is a **small, carefully controlled** `shared/` module containing code used across multiple modules.

> **Important:** For general Shared Kernel concepts and when to use it, see [Domain-Centric Architecture](/guide/rules/packaging-rules.md).

### Spring Modulith Configuration

```java
// shared/package-info.java
@org.springframework.modulith.ApplicationModule(
    displayName = "Shared Kernel",
    type = org.springframework.modulith.ApplicationModule.Type.OPEN
)
package com.company.project.shared;
```

### Structure

```text
com.company.project.shared/
├── package-info.java (@ApplicationModule with Type.OPEN)
├── domain/model/        # Universal value objects
│   ├── Money.java
│   ├── Address.java
│   └── EmailAddress.java
└── application/shared/  # Application ports every context reads the same way
    └── IdentityProvider.java
```

> **The architectural markers are not in here.** `AggregateRoot`, `Entity`, `Value`, `DomainEvent`,
> `InputPort`, `OutputPort`, `DomainException`, `UseCaseException` come from the `dca-building-blocks`
> dependency — writing them into a shared module duplicates a library the project already has on its
> class path, under names the rule suite does not recognise. The shared module holds what is *yours*
> and universal: value objects and shared application ports. A named failure belongs to the context
> that raises it, so it is not in here either.

### Module Dependencies on Shared

```java
// order/package-info.java
@org.springframework.modulith.ApplicationModule(
    allowedDependencies = {
        "shared",              // Can depend on entire shared module
        "customer::api",
        "inventory::api"
    }
)
package com.company.project.order;
```

**All modules can depend on `shared`:**
- Order → shared ✅
- Customer → shared ✅
- Inventory → shared ✅
- Shared → (no dependencies on other modules) ✅

## Related mentions (heuristic)

- [UseCaseException](/marker/application/usecaseexception.md)
- [InputPort](/marker/port-in/inputport.md)
- [OutputPort](/marker/port-out/outputport.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainException](/marker/tactical/domainexception.md)
