---
type: Section
title: Progressive Complexity for Spring Modulith Modules
chapter: Spring Modulith Implementation
source: guide
resource: implementing-domain-centric-architecture/spring-modulith.md
tags: [guide, section]
---

When creating a Spring Modulith module (bounded context), **start with minimal structure** and add complexity only when needed.

> **Core Principle:** The full package structure shown in this document is for **mature modules**. Don't start there!

For general progressive complexity guidelines, see [Domain-Centric Architecture](./README.md#progressive-complexity-principle).

### Phase 1: Minimal Module Structure (Starting Out)

**When:**
- New module creation
- <10 domain classes
- <5 use cases
- MVP or proof-of-concept phase

**Timeline:** Weeks 1-2

**Structure:**
```
com.company.ecommerce.order/ (module)
├── package-info.java (@ApplicationModule)
├── api/ (published)
│   ├── package-info.java (@NamedInterface("api"))
│   ├── OrderApi.java
│   └── CreateOrderRequest.java
├── events/ (published)
│   ├── package-info.java (@NamedInterface("events"))
│   └── OrderCreatedEvent.java (implements Externalized)
└── internal/ (hidden)
    ├── Order.java (Aggregate Root - domain)
    ├── OrderLine.java (Entity - domain)
    ├── Money.java (Value Object - domain)
    ├── CreateOrderUseCase.java (application)
    ├── OrderRepository.java (port - interface)
    ├── OrderController.java (adapter - web)
    └── OrderRepositoryAdapter.java (adapter - persistence)
```

**Characteristics:**
- **Flat internal structure** - all implementation files directly in `internal/`
- **Essential packages only** - `api/`, `events/`, `internal/`
- **~10-15 files total**
- Fast to navigate, easy to understand

### Phase 2: Growing Module Structure (Adding Features)

**When:**
- 10-30 domain classes
- 5-10 use cases
- Multiple external integrations

**Timeline:** Months 2-3

**Triggers for Refactoring:**
- **>10 files in internal/** suggests subdivision
- **>3 domain events** suggests `internal/domain/event/` package
- **>2 adapter types** suggests `internal/adapter/incoming/` and `/outgoing/` packages

**Structure:**
```
com.company.ecommerce.order/
├── api/
├── events/
└── internal/
    ├── domain/
    │   ├── model/
    │   │   ├── Order.java
    │   │   ├── OrderLine.java
    │   │   └── Money.java
    │   ├── event/
    │   │   ├── OrderCreated.java (Domain Event - internal)
    │   │   └── OrderCancelled.java
    │   └── service/
    │       └── PricingService.java
    ├── application/
    │   ├── createorder/
    │   ├── findorder/
    │   ├── cancelorder/
    │   └── shared/
    ├── adapter/
    │   ├── incoming/
    │   │   ├── web/
    │   │   └── event/
    │   └── outgoing/
    │       ├── persistence/
    │       └── payment/
    └── config/
```

> **Refactoring Note:** Refactoring from Phase 1 → Phase 2 takes **<30 minutes** with IDE. Use IDE "Move" refactoring, and Spring Modulith verification tests catch any issues.

### Phase 3: Mature Module Structure (Production-Ready)

**When:**
- >30 domain classes
- >10 use cases
- Complex domain logic
- Multiple bounded contexts to integrate with

**Timeline:** Months 6+

**Full structure:** See [Module Structure](#module-structure) above for complete example.

**Characteristics:**
- **Full subdirectory structure**
- **Use case folders** with Command/Query/Result
- **60+ files**, well-organized
- **Event mappers** - Domain Events → Integration Events
- **Anti-Corruption Layers** - protect domain from external events
