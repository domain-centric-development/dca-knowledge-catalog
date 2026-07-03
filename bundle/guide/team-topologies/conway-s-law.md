---
type: Section
title: Conway's Law
chapter: Team Topologies Integration
source: guide
resource: implementing-domain-centric-architecture/team-topologies.md
tags: [guide, section]
---

### The Law

> "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations."
> — Melvin Conway

**In Practice:**
- System boundaries tend to match team boundaries
- Communication patterns between teams reflect in system architecture
- Tightly coupled teams produce tightly coupled systems
- Independent teams produce independent systems

### Reverse Conway Maneuver

**Strategy:** Design team structure to achieve desired architecture

**Steps:**
1. Define desired architecture (bounded contexts)
2. Align team boundaries with bounded context boundaries
3. Minimize inter-team dependencies
4. Use appropriate interaction modes

**Example:**
```
Desired Architecture:
├── Order BC (independent)
├── Customer BC (independent)
└── Inventory BC (independent)

Team Structure:
├── Order Team (owns Order BC)
├── Customer Team (owns Customer BC)
└── Inventory Team (owns Inventory BC)

Result: Independent deployment, loose coupling
```

### Organizational Design Principles

**Align:**
- 1 Bounded Context = 1 Stream-Aligned Team
- Independent bounded contexts → Independent teams
- Clear bounded context boundaries → Clear team boundaries

**Minimize:**
- Inter-team dependencies
- Synchronous communication
- Shared code ownership

**Optimize:**
- Team autonomy
- Fast flow of value
- Independent deployment
