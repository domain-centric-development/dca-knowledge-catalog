---
type: Section
title: Implementation Patterns
chapter: Team Topologies Integration
source: guide
resource: implementing-domain-centric-architecture/team-topologies.md
tags: [guide, section]
---

### With Modular Monolith (Spring Modulith)

**Team Structure:**
```
Single Deployment, Multiple Teams
┌─────────────────────────────────────────┐
│  E-Commerce Application                 │
│                                         │
│  ┌────────────┐  Order Team (owns)     │
│  │Order Module│                         │
│  └────────────┘                         │
│                                         │
│  ┌──────────────┐  Customer Team (owns)│
│  │Customer      │                       │
│  │Module        │                       │
│  └──────────────┘                       │
│                                         │
│  ┌────────────┐  Inventory Team (owns) │
│  │Inventory   │                         │
│  │Module      │                         │
│  └────────────┘                         │
└─────────────────────────────────────────┘
        ↓ deployed by
┌─────────────────────────────────────────┐
│  Platform Team                          │
│  - Deployment pipeline                  │
│  - Database                             │
│  - Monitoring                           │
└─────────────────────────────────────────┘
```

> **For Spring Modulith details:** See [Spring Modulith Implementation](/guide/spring-modulith.md)

### With Microservices

**Team Structure:**
```
┌────────┐     ┌──────────────────────┐     ┌────────┐
│ Order  │     │ Spring Boot App      │     │Inventory│
│Service │     │ ┌────────┐          │     │Service │
│        │────→│ │Customer│          │←────│        │
│(Order  │     │ │ Module │          │     │(Inven- │
│Team)   │     │ └────────┘          │     │tory    │
└────────┘     │ (Customer Team)     │     │Team)   │
               └──────────────────────┘     └────────┘
```

> **For service decomposition:** See [Deployment Patterns](/guide/deployment-patterns.md)
