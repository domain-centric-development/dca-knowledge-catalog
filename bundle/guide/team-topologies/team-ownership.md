---
type: Section
title: Team Ownership
chapter: Team Topologies Integration
source: guide
resource: implementing-domain-centric-architecture/team-topologies.md
tags: [guide, section]
---

### Bounded Context Ownership

**Rule:** One stream-aligned team owns one bounded context

**Ownership Includes:**
- All layers: domain, application, adapters, infrastructure (see [Domain-Centric Architecture Layers](/guide/readme/dependency-structure.md))
- Code, tests, deployment, monitoring, support
- Autonomy over internal implementation
- Responsibility for published interfaces/APIs

**Example:**
```
Order Team owns Order Bounded Context
├── domain/ (Order, OrderLine, Money)
├── application/ (CreateOrderUseCase, CancelOrderUseCase)
├── adapter/ (OrderController, OrderRepositoryAdapter)
├── infrastructure/ (Spring configuration)
├── Tests (unit, integration, E2E within context)
├── CI/CD pipeline
├── Monitoring dashboards
└── On-call rotation
```

> **For bounded context technical structure:** See [Domain-Centric Architecture](/guide/readme/java-package-structure.md)

### Code Ownership

**Strong Code Ownership:**
- Team controls all changes to their context
- Cross-team code changes via API/interface only
- No shared code ownership across teams
- Pull requests reviewed by team members

**Shared Kernel Exception:**
- Requires explicit team agreement
- Coordinate changes via architecture guild
- Use sparingly (see [Domain-Centric Architecture - Shared Kernel](/guide/readme/rules.md))

### API/Interface Ownership

**Team API Responsibilities:**
- **Synchronous APIs:** REST endpoints (in `adapter/incoming/web/`)
- **Asynchronous APIs:** Integration Events (in `adapter/outgoing/messaging/event/`)
- **Domain APIs:** Input Ports (in `application/{usecasename}/`)

**API Management:**
- Team owns and versions their public APIs
- Breaking changes require coordination
- Semantic versioning for APIs
- Backward compatibility preferred
- Anti-Corruption Layer for consuming external APIs

**Example:**
```
Order Team's APIs:
├── REST API: POST /orders, GET /orders/{id}
├── Integration Events: OrderCreatedEvent, OrderCancelledEvent
└── Versioning: Semantic versioning (v1, v2, v3)
    └── v2 maintains backward compatibility with v1
```

> **For adapter and API technical patterns:** See [Domain-Centric Architecture - Adapter Layer](/guide/readme/rules.md)
