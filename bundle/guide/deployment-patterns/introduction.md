---
type: Section
title: Introduction
chapter: Deployment Patterns
source: guide
resource: implementing-domain-centric-architecture/deployment-patterns.md
tags: [guide, section]
---

While the main [Domain-Centric Architecture](./README.md) defines the logical structure of bounded contexts and layers, this document addresses **deployment strategies** and **physical boundaries**.

**Key Distinction:**
- **Logical Boundary** = Bounded Context (DDD concept)
- **Physical Boundary** = Service/Deployment Unit (infrastructure concept)

**Core Question:** When should one Bounded Context be deployed as multiple services?
