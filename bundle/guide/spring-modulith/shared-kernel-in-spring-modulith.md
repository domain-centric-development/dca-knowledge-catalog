---
type: Section
title: Shared Kernel in Spring Modulith
chapter: Spring Modulith Implementation
source: guide
resource: implementing-domain-centric-architecture/spring-modulith.md
tags: [guide, section]
---

The Shared Kernel is a **small, carefully controlled** `shared/` module containing code used across multiple modules.

> **Important:** For general Shared Kernel concepts and when to use it, see [Domain-Centric Architecture](/guide/readme/rules.md).

### Spring Modulith Configuration

```java
// shared/package-info.java
@org.springframework.modulith.ApplicationModule(
    displayName = "Shared Kernel",
    type = org.springframework.modulith.ApplicationModule.Type.OPEN
)
package com.company.ecommerce.shared;
```

### Structure

```
com.company.ecommerce.shared/
├── package-info.java (@ApplicationModule with Type.OPEN)
├── marker/              ← Marker interfaces for DDD patterns
│   ├── AggregateRoot.java
│   ├── Entity.java
│   ├── ValueObject.java
│   ├── DomainEvent.java
│   ├── InputPort.java
│   └── OutputPort.java
├── types/               ← Common value objects
│   ├── Money.java
│   ├── Address.java
│   └── EmailAddress.java
└── exception/           ← Base exceptions
    ├── DomainException.java
    └── NotFoundException.java
```

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
package com.company.ecommerce.order;
```

**All modules can depend on `shared`:**
- Order → shared ✅
- Customer → shared ✅
- Inventory → shared ✅
- Shared → (no dependencies on other modules) ✅

## Related markers

- [InputPort](/marker/port-in/inputport.md)
- [OutputPort](/marker/port-out/outputport.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
