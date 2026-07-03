---
type: Section
title: Combining Best of Both
chapter: Domain-Centric Architecture vs Clean Architecture
source: guide
resource: implementing-domain-centric-architecture/clean-architecture-comparison.md
tags: [guide, section]
---

You can combine approaches:

**Hybrid Approach:**
```
✅ Use Clean Architecture layers (from Clean Architecture)
✅ Use DDD patterns in Domain layer (from Domain-Centric)
✅ Use Presenters OR DTOs (choose what fits)
✅ Add Bounded Contexts as needed (from Domain-Centric)
✅ Add Domain Events as needed (from Domain-Centric)
```

**Example:**
```
com.company.project
├── order/ (Bounded Context - from DCA)
│   ├── entities/ (Clean Architecture terminology)
│   │   ├── Order.java (but with DDD patterns - from DCA)
│   │   └── OrderLine.java
│   ├── usecases/ (Clean Architecture terminology)
│   │   └── CreateOrderUseCase.java
│   ├── controllers/ (Clean Architecture terminology)
│   │   └── OrderController.java
│   └── gateways/ (Clean Architecture terminology)
│       └── OrderGateway.java
```
