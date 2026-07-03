---
type: Section
title: Deployment Pattern Comparison
chapter: Deployment Patterns
source: guide
resource: implementing-domain-centric-architecture/deployment-patterns.md
tags: [guide, section]
---

### Pattern 1: Modular Monolith (Single Deployment Unit)

**Structure:**
```
Single Deployment Unit
┌──────────────────────────────────────┐
│  Spring Boot Application             │
│                                      │
│  ┌────────┐ ┌────────┐ ┌──────────┐  │
│  │ Order  │ │Customer│ │Inventory │  │
│  │ Module │ │ Module │ │ Module   │  │
│  └────────┘ └────────┘ └──────────┘  │
│                                      │
│  Shared Database                     │
└──────────────────────────────────────┘
```

**Characteristics:**
- ✅ Simple deployment
- ✅ Simple transactions (ACID)
- ✅ Simple development
- ✅ Fast inter-module calls
- ❌ Single technology stack
- ❌ Coupled deployment
- ❌ Difficult to scale parts independently

**When to Use:**
- Starting new projects
- Small to medium complexity
- Single team or co-located teams
- Clear module boundaries exist

**Implementation:** See [Spring Modulith Implementation](./spring-modulith.md)

### Pattern 2: Self-Contained Systems (Multiple SCS)

**Structure:**
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Order SCS   │     │ Customer SCS │     │Inventory SCS │
│              │     │              │     │              │
│ ┌──────────┐ │     │ ┌──────────┐ │     │ ┌──────────┐ │
│ │ Domain   │ │     │ │ Domain   │ │     │ │ Domain   │ │
│ └──────────┘ │     │ └──────────┘ │     │ └──────────┘ │
│ ┌──────────┐ │     │ ┌──────────┐ │     │ ┌──────────┐ │
│ │ Own DB   │ │     │ │ Own DB   │ │     │ │ Own DB   │ │
│ └──────────┘ │     │ └──────────┘ │     │ └──────────┘ │
└──────────────┘     └──────────────┘     └──────────────┘
       ↕                     ↕                     ↕
       └─────────── Events / APIs ─────────────────┘
```

**Characteristics:**
- ✅ Independent deployment
- ✅ Independent scaling
- ✅ Technology diversity possible
- ✅ Clear boundaries
- ✅ Team autonomy
- ❌ Distributed system complexity
- ❌ Eventual consistency
- ❌ More operational overhead

**When to Use:**
- Clear bounded contexts
- Different scaling needs
- Multiple autonomous teams
- Mature DevOps capability

**Mapping:** Typically 1 Bounded Context = 1 SCS

### Pattern 3: Multi-Service Bounded Context (Advanced)

**Structure:**
```
Order Bounded Context
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Management   │  │ Pricing      │  │ Notification │   │
│  │ Service      │  │ Service      │  │ Service      │   │
│  │              │  │              │  │              │   │
│  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │   │
│  │ │ Domain   │ │  │ │ Domain   │ │  │ │ Domain   │ │   │
│  │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │   │
│  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │   │
│  │ │ Own DB   │ │  │ │ Own DB   │ │  │ │ Own DB   │ │   │
│  │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│         ↕                  ↕                  ↕         │
│         └──── Internal Events (within BC) ────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
         │
         ↓ Integration Events
         │
    Other Bounded Contexts
```

**Characteristics:**
- ✅ Independent scaling within BC
- ✅ Independent deployment within BC
- ✅ Technology diversity within BC
- ✅ Shared ubiquitous language
- ❌ High complexity
- ❌ Distributed transactions within BC
- ❌ Internal events + integration events

**When to Use:**
- Very large bounded context
- Clear subdomains within BC
- Different scaling/tech needs within BC
- Very mature teams

**Caution:** This is the most complex pattern. Only use when benefits are clear and substantial.
