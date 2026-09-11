---
type: Section
title: Module Structure
chapter: Spring Modulith Implementation
source: guide
resource: dca-guide/topics/spring-modulith.md
tags: [guide, section]
---

### Recommended Structure: Module per Bounded Context

```text
com.company.project
├── order/ (module = bounded context)
│   ├── api/ (published - public interface)
│   │   ├── OrderApi.java
│   │   ├── CreateOrderRequest.java
│   │   └── OrderResponse.java
│   ├── events/ (published - integration events)
│   │   ├── OrderCreatedEvent.java
│   │   └── OrderCancelledEvent.java
│   └── internal/ (hidden)
│       ├── domain/
│       │   ├── model/
│       │   │   ├── Order.java (Aggregate Root)
│       │   │   ├── OrderLine.java (Entity)
│       │   │   └── Money.java (Value Object)
│       │   ├── service/
│       │   │   └── PricingService.java
│       │   └── event/
│       │       └── OrderCreated.java (Domain Event)
│       ├── application/
│       │   ├── createorder/
│       │   │   ├── CreateOrderInputPort.java
│       │   │   ├── CreateOrderUseCase.java
│       │   │   ├── CreateOrderCommand.java
│       │   │   └── CreateOrderResult.java
│       │   ├── findorder/
│       │   ├── cancelorder/
│       │   └── shared/
│       │       ├── OrderRepository.java
│       │       └── DomainEventPublisher.java
│       ├── adapter/
│       │   ├── incoming/
│       │   │   ├── web/
│       │   │   │   └── OrderController.java
│       │   │   └── event/
│       │   │       └── OrderEventConsumer.java
│       │   └── outgoing/
│       │       ├── persistence/
│       │       │   └── OrderRepositoryAdapter.java
│       │       └── payment/
│       │           └── PaymentGatewayAdapter.java
│       └── config/
│           └── OrderModuleConfiguration.java
```

> **Note:** The `internal/` structure follows [Domain-Centric Architecture layers](/guide/package-structure.md). See main document for layer rules and responsibilities.

### Module Configuration

**Module Rules (package-info.java):**
```java
// order/package-info.java
@org.springframework.modulith.ApplicationModule(
    displayName = "Order Management",
    allowedDependencies = {"customer::api", "inventory::api", "shared"}
)
package com.company.project.order;
```

**API Package:**
```java
// order/api/package-info.java
@org.springframework.modulith.NamedInterface("api")
package com.company.project.order.api;
```

**Events Package:**
```java
// order/events/package-info.java
@org.springframework.modulith.NamedInterface("events")
package com.company.project.order.events;
```

## Related mentions (heuristic)

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
