---
type: Section
title: Team Structure Examples
chapter: Team Topologies Integration
source: guide
resource: implementing-domain-centric-architecture/team-topologies.md
tags: [guide, section]
---

### E-Commerce Organization

```
┌─────────────────────────────────────────────┐
│  Platform Team                              │
│  - Database as a Service                    │
│  - Message Broker as a Service              │
│  - CI/CD Pipelines                          │
│  - Monitoring/Observability                 │
└─────────────────────────────────────────────┘
     ↓ provides services (X-as-a-Service)
┌─────────────────────────────────────────────┐
│  Stream-Aligned Teams                       │
│                                             │
│  ┌─────────────┐  ┌─────────────┐         │
│  │ Order Team  │  │Customer Team│         │
│  │             │  │             │         │
│  │ Owns:       │  │ Owns:       │         │
│  │ - Order BC  │  │ - Customer  │         │
│  │ - Full stack│  │   BC        │         │
│  │ - Deployment│  │ - Full stack│         │
│  └─────────────┘  └─────────────┘         │
│         ↕                 ↕                 │
│         └── Events/APIs ──┘                 │
└─────────────────────────────────────────────┘
     ↑ receives help (Facilitating)
┌─────────────────────────────────────────────┐
│  Enabling Team                              │
│  - DDD/Architecture expertise               │
│  - Testing practices                        │
│  - Performance optimization                 │
└─────────────────────────────────────────────┘
```

### Team Interaction Patterns

**Stream-Aligned ↔ Stream-Aligned:**
- **Preferred:** X-as-a-Service via domain events (async)
- **Alternative:** X-as-a-Service via REST API (sync)
- **Initial:** Collaboration mode during integration discovery
- **Transition:** To X-as-a-Service when interfaces stabilize

**Stream-Aligned ↔ Platform:**
- **Always:** X-as-a-Service
- Platform provides self-service infrastructure
- Clear SLAs and documentation

**Stream-Aligned ↔ Enabling:**
- **Always:** Facilitating mode
- Time-boxed engagement
- Knowledge transfer, not delivery

**Stream-Aligned ↔ Complicated-Subsystem:**
- **Always:** X-as-a-Service
- Well-defined API
- Complicated subsystem hides complexity

> **For technical integration patterns:** See [Domain-Centric Architecture - Integration Patterns](/guide/readme/integration-patterns.md)
