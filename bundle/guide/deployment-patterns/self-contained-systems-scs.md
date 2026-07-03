---
type: Section
title: "Self-Contained Systems (SCS)"
chapter: Deployment Patterns
source: guide
resource: implementing-domain-centric-architecture/deployment-patterns.md
tags: [guide, section]
---

### What is SCS?

A **Self-Contained System** is an autonomous, independently deployable unit that includes:

- **UI** (if needed) - User interface components
- **Business Logic** - Domain and application layers
- **Data Storage** - Own database/schema
- **Integration** - Well-defined interfaces to other SCS

### SCS Characteristics

```
┌──────────────────────────────────────┐
│  Self-Contained System (SCS)         │
│                                      │
│  ┌──────────────────────────────┐    │
│  │ UI Layer (optional)          │    │
│  └──────────────────────────────┘    │
│  ┌──────────────────────────────┐    │
│  │ Business Logic               │    │
│  │ (Domain + Application)       │    │
│  └──────────────────────────────┘    │
│  ┌──────────────────────────────┐    │
│  │ Data Storage                 │    │
│  │ (own database)               │    │
│  └──────────────────────────────┘    │
│                                      │
│  Boundaries:                         │
│  - Autonomous deployment             │
│  - Isolated data                     │
│  - Independent release cycle         │
│  - Clear integration points          │
└──────────────────────────────────────┘
```

**SCS Principles:**
- **Autonomy** - Can be developed, deployed, and scaled independently
- **No shared data** - Each SCS owns its data
- **Integration via contracts** - Events or APIs
- **Technology heterogeneity** - Different tech stacks possible
- **Team ownership** - One team owns one SCS (typically)

### Bounded Context vs SCS

| Aspect | Bounded Context | Self-Contained System |
|--------|-----------------|------------------------|
| **Concept** | Logical boundary (DDD) | Physical boundary (deployment) |
| **Defines** | Model boundary | Deployment unit |
| **Granularity** | Language/model consistency | Autonomous service |
| **Relationship** | 1 BC can have 1+ SCS | 1 SCS contains ≤ 1 BC |
| **Goal** | Model clarity | Deployment autonomy |

**Typical Mapping:**
```
Bounded Context = Self-Contained System (common)
```

**Alternative Mapping:**
```
1 Bounded Context = Multiple Services (advanced)
```

> **When to use multiple services per BC:** See [Service Decomposition](#service-decomposition) below.
