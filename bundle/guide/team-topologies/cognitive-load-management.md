---
type: Section
title: Cognitive Load Management
chapter: Team Topologies Integration
source: guide
resource: implementing-domain-centric-architecture/team-topologies.md
tags: [guide, section]
---

### What is Cognitive Load?

**Definition:** Mental capacity required to work with a system

**Three Types:**
1. **Intrinsic:** Inherent complexity of domain
2. **Extraneous:** Complexity from poor design/tools
3. **Germane:** Learning and skill development

**Goal:** Keep total cognitive load within team capacity

### Managing Team Cognitive Load

**For Stream-Aligned Teams:**
- Limit to **one bounded context** per team
- Limit to **one core domain** per team
- Offload generic subdomains to platform or external services
- Use platform team to reduce infrastructure cognitive load
- Use enabling team to reduce learning cognitive load

**For Platform Team:**
- Provides self-service infrastructure
- Reduces cognitive load of stream-aligned teams
- Makes complex infrastructure simple to consume

**For Enabling Team:**
- Reduces learning curve for new patterns/technologies
- Transfers knowledge to reduce future cognitive load

**Example - Reducing Load:**
```
Before:
Order Team manages:
├── Order domain (intrinsic load)
├── Kubernetes infrastructure (extraneous load)
├── Database setup (extraneous load)
├── Monitoring setup (extraneous load)
└── Total: OVERLOADED

After:
Order Team manages:
├── Order domain (intrinsic load)
└── Total: MANAGEABLE

Platform Team provides:
├── Kubernetes platform (X-as-a-Service)
├── Database service (X-as-a-Service)
└── Monitoring service (X-as-a-Service)
```
